import posix_ipc as ipc

class Queue:

    def __init__(self, qname, block=True):
        self.queue = ipc.MessageQueue(qname, ipc.O_CREAT)
        self.queue.block = block

    def cleanup(self):
        self.queue.close()
        self.queue.unlink()