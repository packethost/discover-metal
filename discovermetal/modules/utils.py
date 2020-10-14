import time
import shlex
import threading
import subprocess


class Run(object):
    def __init__(self, *args, autorestart=None, timeout=None, watch_sleep=None):
        if len(args) == 1:
            args = shlex.split(args[0])
        self._args = list(args)
        self._return_code = None
        self._stdout = None
        self._stderr = None
        self._process = None
        self._started = None
        self._finished = None
        self._thread = None
        self._terminate = False
        self._autorestart = None
        self._timeout = None
        self._watch_sleep = None

    @property
    def args(self):
        return self._args

    @property
    def process(self):
        return self._process

    @property
    def thread(self):
        return self._thread

    @property
    def return_code(self):
        return self._return_code

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr

    @property
    def started(self):
        return self._started

    @property
    def finished(self):
        return self._finished

    def run(
        self, *args, background=False, autorestart=None, timeout=None, watch_sleep=None
    ):
        if len(args) == 1:
            args = shlex.split(args[0])
        args = self.args + list(args)

        self._return_code = None
        self._stdout = None
        self._stderr = None
        self._started = time.time()
        self._finished = False
        self._process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        autorestart = autorestart or self._autorestart
        watch_sleep = watch_sleep or self._watch_sleep
        timeout = timeout or self._timeout

        if background:
            self._thread = threading.Thread(
                target=self.wait,
                kwargs=dict(
                    sleep=watch_sleep, autorestart=autorestart, timeout=timeout
                ),
            )
            self._thread.start()
            return self
        else:
            return self.collect()[0] == 0

    def collect(self):
        self._stdout, self._stderr = self.process.communicate()
        self._return_code = self.process.returncode
        self._finished = time.time()
        return (self.return_code, self.stdout, self.stderr)

    def wait(self, sleep=None, autorestart=None, timeout=None, __restarts=0):
        if self._terminate:
            return self.collect()[0] == 0
        start = time.time()
        sleep = sleep if sleep and sleep > 0 else 0.5
        timeout = timeout if timeout and timeout > 0 else None
        while self.process.poll() is None:
            time.sleep(sleep)
            if timeout and time.time() > start + timeout:
                self.process.terminate()
                raise TimeoutError(
                    "Process '{}' didn't complete within {} seconds".format(
                        " ".join(self.args), timeout
                    )
                )

        if autorestart is True:
            return self.wait(sleep, autorestart, timeout, __restarts + 1)
        elif autorestart and __restarts < autorestart:
            return self.wait(sleep, autorestart, timeout, __restarts + 1)

        return self.collect()[0] == 0

    def terminate(self):
        self._terminate = True
        self.process.terminate()

    def __enter__(self):
        return self.run(background=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.terminate()

    def __str__(self):
        return "{args} return_code={return_code} stdout.length={stdout_len} stderr.length={stderr.length}".format(
            args=self.args,
            return_code=self.return_code,
            stdout_len=len(self.stdout or ""),
            stderr_len=len(self.stderr or ""),
        )

    def __repr__(self):
        return "<{}>".format(str(self))
