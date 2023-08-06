from imutils.video import VideoStream
from robot_core.executor.executor import Executor


class WebCamExecutor(Executor):

    vs = None

    def execute(self, **kwargs):
        if kwargs["command"] == "capture":
            return self.capture()
        elif kwargs["command"] == "start":
            return self.start()
        elif kwargs["command"] == "stop":
            return self.stop()

    def start(self):
        self.vs = VideoStream(src=1).start()

    def stop(self):
        self.vs.stop()

    def capture(self):
        return self.vs.read()
