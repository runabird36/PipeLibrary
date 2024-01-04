
from PySide2.QtCore import QObject, Signal, QThread, QThreadPool, QRunnable
import traceback, sys

class Worker(QThread, QObject):

    try:
        _job_thread_finished = Signal()
    except:
        _job_thread_finished = Signal()

    def __init__(self):
        QObject.__init__(self)

    def set_job(self, job_instance):
        self._job = job_instance

    def run(self):
        print('Query task start!!')
        self._job.run()
        self._job_thread_finished.emit()




class WorkerSTR(QThread, QObject):


    try:
        _job_thread_finished = Signal(str)
    except:
        _job_thread_finished = Signal(str)

    def __init__(self):
        QObject.__init__(self)

    def set_job(self, job_instance, *args, **kwargs):
        self._job = job_instance
        self.param_list = args
        self.param_dict = kwargs

    def run(self):
        try:
            result = self._job(*self.param_list, **self.param_dict)
            self._job_thread_finished.emit(result)
        except:
            import traceback
            traceback.print_exc()

        

class WorkerLIST(QThread, QObject):

    try:
        _job_thread_finished = Signal(list)
    except:
        _job_thread_finished = Signal(list)

    def __init__(self):
        QObject.__init__(self)

    def set_job(self, job_instance, *args, **kwargs):
        self._job = job_instance
        self.param_list = args
        self.param_dict = kwargs

    def run(self):
        try:
            result = self._job(*self.param_list, **self.param_dict)
            self._job_thread_finished.emit(result)
        except:
            import traceback
            traceback.print_exc()







class WorkerDict(QThread, QObject):

    try:
        _job_thread_finished = Signal(dict)
    except:
        _job_thread_finished = Signal(dict)

    def __init__(self):
        QObject.__init__(self)

    def set_job(self, job_instance, *args, **kwargs):
        self._job = job_instance
        self.param_list = args
        self.param_dict = kwargs

    def run(self):
        try:
            result = self._job(*self.param_list, **self.param_dict)
            self._job_thread_finished.emit(result)
        except:
            import traceback
            traceback.print_exc()










class WorkerSignals(QObject):
    error       = Signal(tuple)
    result      = Signal(list)
    progress    = Signal(int)
    finished    = Signal(int)
    
class PoolWorker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''
    def __init__(self, _idx, fn, *args, **kwargs):
        super(PoolWorker, self).__init__()
        self._work_idx = _idx
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


    def run(self):
        try:

            result = self.fn(*self.args, **self.kwargs)


        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit([self._work_idx, result])  # Return the result of the processing
        finally:
            self.signals.finished.emit(self._work_idx)  # Done




class Pool(QObject):
    try:
        finished = Signal(str)
    except:
        finished = Signal(str)
    def __init__(self):
        super(Pool, self).__init__()

        self.pool = QThreadPool()

        self.job_list = []
        self.param_list = []
        self.job_status_list = []
        self.job_result_list = []

        self.pool.setMaxThreadCount(5)


    def add_job(self, _fn, *args, **kwargs):

        self.job_list.append(_fn)
        self.param_list.append([args, kwargs])
        self.job_status_list.append(False)
        self.job_result_list.append(None)

        

    def check_pool_finished(self, _job_idx):
        self.job_status_list[_job_idx] = True

        if False in self.job_status_list:
            pass
            # self.finished.emit("Yet")
        else:
            self.finished.emit("Clear")


    def update_job_result_list(self, res_list):

        job_idx = res_list[0]
        job_res = res_list[1]
        self.job_result_list[job_idx] = job_res


    def start_pool(self):
        for _idx, _job in enumerate(self.job_list):
            args = self.param_list[_idx][0]
            kwargs = self.param_list[_idx][1]
            worker = PoolWorker(_idx, _job, *args, **kwargs)
            worker.signals.finished.connect(self.check_pool_finished)
            worker.signals.result.connect(self.update_job_result_list)

            self.pool.start(worker)





    def get_res_list(self):
        return self.job_result_list


    def reset_all(self):
        self.pool.clear()
        self.job_list = []
        self.job_status_list = []
        self.job_result_list = []

