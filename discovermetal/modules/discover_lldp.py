from collections import namedtuple
from .modules import DiscoverModule
from . import utils
import json
import time


class DiscoverLLDP(DiscoverModule):
    LLDPD_PATH = "/usr/sbin/lldpd"
    LLDPD_ARGS = ["-d"]
    LLDPCTL_PATH = "/usr/sbin/lldpctl"
    LLDPCTL_ARGS = ["-f", "json"]
    TIMEOUT = 1  # minutes
    AUTORESTART = 5  # Number of times to restart if exited

    def run(self, data):
        lldpd_cmd = (self.LLDPD_PATH, *self.LLDPD_ARGS)
        with utils.Run(*lldpd_cmd, autorestart=self.AUTORESTART) as service:
            lldpctl = utils.Run(self.LLDPCTL_PATH, *self.LLDPCTL_ARGS)

            lldp_data = None
            found_data = False
            started = time.time()
            while True:
                # Run lldpctl
                if not lldpctl.run():
                    # If lldpctl returns bad status, log it
                    data.log(
                        "ERROR",
                        "{} return exit code: {}".format(
                            lldpctl.args[0], lldpctl.return_code
                        ),
                        lldpctl=lldpctl,
                    )

                # If lldpctl prints to stderr, log it
                if lldpctl.stderr and lldpctl.stderr.strip():
                    data.log("ERROR", lldpctl.stderr, lldpctl=lldpctl)

                lldp_data = self.get_lldp_response(lldpctl)
                if lldp_data is not False:
                    if not found_data:
                        data.log(
                            "DEBUG",
                            "LLDP data received, waiting 5 seconds to do a final check",
                        )
                        # It's possible we got the lldp for only some of the interfaces.
                        # waiting an additional amount of time allows us to be sure we've
                        # received lldp for all interfaces
                        found_data = True
                        time.sleep(5)
                        continue
                    # If we found data two times in a row, then lets continue
                    # with the rest of the script
                    break

                if time.time() - started > self.TIMEOUT * 60:
                    raise TimeoutError("Timedout waiting for lldp")
                data.log(
                    "DEBUG",
                    "No lldp data returned, trying again in 5 seconds",
                    started=started,
                    current=time.time(),
                )
                time.sleep(5)

            data["lldp"] = self.format_lldp_response(lldp_data)

    @staticmethod
    def get_lldp_response(lldpctl):
        try:
            ret_obj = json.loads(lldpctl.stdout.decode("utf-8"))["lldp"]
            if len(ret_obj):
                return ret_obj
        except:
            pass
        return False

    @staticmethod
    def format_lldp_response(data):
        if not data:
            return
        response = []
        interfaces = data.get("interface")
        if type(interfaces) is dict:
            # If only one interface data is found, data.interface is a dict
            # If more than one interface is found, data.interface is a list
            interfaces = [interfaces]
        for entry in interfaces:
            for iface_name, iface_lldp in entry.items():
                switches = iface_lldp.get("chassis", {})
                port = iface_lldp.get("port", {})
                print(iface_name, port)
                for sw_name, sw_data in switches.items():
                    iface_record = {
                        "interface": iface_name,
                        "switch": {
                            "hostname": sw_name,
                            "id": sw_data.get("id"),
                            "description": sw_data.get("descr"),
                        },
                        "port": {
                            "id": port.get("id"),
                            "agg": port.get("aggregation"),
                            "description": port.get("descr"),
                        },
                    }
                    response.append(iface_record)
        return response
