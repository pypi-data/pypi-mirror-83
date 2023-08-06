from multiprocessing import Process

def process_wrapper(func):
    def wrapper(*args,**kwargs):
        p = Process(target=func,args=args,kwargs=kwargs)
        p.start()
        return p
    return wrapper