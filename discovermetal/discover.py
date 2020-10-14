from .modules import discovery_modules
from datetime import datetime
import traceback as traceback_pkg
import logging
import requests

log = logging.getLogger()


def now():
    return datetime.utcnow().isoformat() + "Z"


class DiscoverMetal(object):
    def __init__(self):
        self.modules = []
        self._data = DiscoveryData()
        self.load_modules()

    def load_modules(self):
        for module in discovery_modules():
            self.modules.append(module())

    def run(self):
        self.data.start()
        for module in self.modules:
            self.run_module(module)
        self.data.stop()

    def run_module(self, module):
        try:
            self.data.log("DEBUG", "[{}]: Started".format(module.__class__.__name__))
            return module.run(self.data)
        except:
            self.data.log(
                "ERROR",
                "Exception occured while running module: %s"
                % module.__class__.__name__,
                traceback=True,
            )
        finally:
            self.data.log("DEBUG", "[{}]: Completed".format(module.__class__.__name__))

    @property
    def data(self):
        return self._data

    def flatten(self):
        return self.data.flatten()

    def send(self, to, **request_args):
        self.data.log("DEBUG", "Sending to '{}'".format(to))
        return requests.post(to, json=self.flatten(), **request_args)


class DiscoveryData(dict):
    def __init__(self):
        self["stats"] = {"start": None, "stop": None, "logs": []}

    @property
    def stats(self):
        return self["stats"]

    def start(self):
        self.stats["start"] = now()
        self.log("INFO", "Discovery Started")

    def stop(self):
        self.stats["stop"] = now()
        self.log("INFO", "Discovery Finished")

    def log(self, level, message, traceback=False, **data):
        level = str(level).upper()
        if level not in ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]:
            raise LookupError(
                "Invalid log level {level}".format(level), (level, message, data)
            )
        l = {
            "time": now(),
            "level": level.upper(),
            "message": str(message),
            "data": data,
        }
        log_msg = str(message)

        if data:
            log_msg += " " + " ".join(["{}={}".format(k, v) for k, v in data.items()])

        if traceback:
            l["traceback"] = traceback_pkg.format_exc()
            log_msg += "\n" + l["traceback"]
        self.stats["logs"].append(l)

        log_level = getattr(logging, level)
        log.log(log_level, log_msg)

    def flatten(self):
        flat = {}
        for k, v in self.items():
            try:
                flat[k] = v.flatten()
            except AttributeError:
                flat[k] = v
        return flat
