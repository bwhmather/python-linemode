from concurrent.futures import Future
from threading import Thread, Lock
import queue

import logging
log = logging.getLogger('linemode')


class PrintJob(Future):
    def __init__(self, program):
        super(PrintJob, self).__init__()
        self.program = program


class PrintSpooler(object):
    """ Manages access to a printer from multiple threads
    """
    def __init__(self, printer):
        self._printer = printer

        self._job_queue = queue.Queue()
        self._shutdown = False
        self._shutdown_lock = Lock()

        self._print_thread = Thread(target=self._print_loop, daemon=True)
        self._print_thread.start()

    def _print_loop(self):
        try:
            while not self._shutdown:
                job = self._job_queue.get()
                if job is None:
                    # shutdown will push None onto the send queue to stop send
                    # loop from blocking on get forever
                    break
                if job.set_running_or_notify_cancel():
                    try:
                        self._printer.execute(job.program)
                    except Exception as e:
                        job.set_exception(e)
                        raise
                    job.set_result(None)
        except Exception:
            if not self._shutdown:
                log.exception("error in print loop")
        finally:
            self._shutdown_async()

    def submit(self, commands):
        # TODO clean up old results
        if self._shutdown:
            raise RuntimeError("spooler has been shut down")

        program = self._printer.compile(commands)
        job = PrintJob(program)

        self._job_queue.put(job)

        return job

    def shutdown(self):
        with self._shutdown_lock:
            if not self._shutdown:
                log.debug("shutting down")
                self._shutdown = True
                # send loop will block trying to fetch items from it's queue
                # forever unless we push something onto it
                self._job_queue.put(None)

                self._printer.shutdown()

                self._print_thread.join()

                while not self._job_queue.empty():
                    job = self._job_queue.get()
                    if job is not None:
                        job.cancel()

                log.debug("successfully shut down")

    def _shutdown_async(self):
        """ Shutdown without blocking.
        """
        Thread(target=self.shutdown)
