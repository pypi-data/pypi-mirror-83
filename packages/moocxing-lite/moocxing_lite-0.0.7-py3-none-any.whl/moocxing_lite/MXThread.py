from threading import Thread
print("*** 初始化Thread模块")


class MXThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

    def _start(self, target=None, name=None, args=(), kwargs={}):
        self.__init__()
        self._target = target
        self._name = str(name)
        self._args = args
        self._kwargs = kwargs

        self.start()
        self.join(1)



