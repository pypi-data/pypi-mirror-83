def empty_queue(queue):
    while True:
        try:
            queue.get(block=False)
        except:
            return queue