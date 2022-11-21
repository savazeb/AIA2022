def q_receiver(function):
    return function.queue.receive()[0].decode()


# non blocking method
def q_cmsg_receiver(function):
    try:
        if function.queue.current_messages:
            return function.queue.receive()[0].decode()
    except:
        pass
    return None
