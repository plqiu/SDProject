# encoding: utf-8
import threading


class TASK:

    def __init__(self, queue):
        self._task_buffer = []
        self._queue = queue

    def addhandler(self, handler):
        t = threading.Thread(target=handler.start)
        self._task_buffer.append(t)

    def start(self):
        for task in self._task_buffer:
            task.setDaemon(True)
            task.start()
        # for task in self._task_buffer:
        #     task.join()