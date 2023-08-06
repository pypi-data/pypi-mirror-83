from threading import Thread
import inspect
import ctypes


def stop_thread(thread):
    try:
        exctype = SystemExit
        tid = ctypes.c_long(thread.ident)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 1: return True
        else: return False
    except:
        return None

def thread_wrapper(func):
    def wrapper(*args, **kwargs):
        thread_target = Thread(target=func,args=args,kwargs=kwargs)
        thread_target.start()
        return thread_target
    return wrapper


