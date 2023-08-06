import time


def retry_wrapper(max_retry_num=3, retry_delay=1, exception=True):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            this_for_num = max_retry_num - 1 if exception else max_retry_num
            for i in range(this_for_num):
                try:
                    return func(*args, **kwargs)
                except:
                    time.sleep(retry_delay)
            if exception:
                return func(*args, **kwargs)
            else:
                return None

        return wrapper2

    return wrapper1