import numpy as np
import os
import time
from multiprocessing import shared_memory
from multiprocessing import resource_tracker
import signal

def shared_memory_manager(name):
    #remove_shm_from_resource_tracker()
    a = np.array([name.encode(), str(os.getpid()).encode()], dtype="S30")
    nb_process = 4
    shm_name = "crossroad"
    first = False
    try:
        shm = shared_memory.SharedMemory(name=shm_name)

        b = np.ndarray((nb_process, *a.shape), dtype=a.dtype, buffer=shm.buf)

    except FileNotFoundError:
        first = True
            
        shm = shared_memory.SharedMemory(create=True, size=nb_process * a.nbytes, name=shm_name)
        b = np.ndarray((nb_process, *a.shape), dtype=a.dtype, buffer=shm.buf)
        b[:] = b''
    for i in range(nb_process):
        if b[i][0] == b'':
            b[i] = a
            print(f'Process {os.getpid()} a écrit à l’index {i}')
            break
    signal.signal(signal.SIGINT, lambda a, b: keyboardInteruptHandler(shm))
    while b[-1][0]==b'':
        time.sleep(0.5)

    print("Tous les processus sont OK")

    list_process = [tuple(row.astype(str)) for row in b]  
    shm.close()
    if first:

        time.sleep(1)
        shm.unlink()
    return list_process
def keyboardInteruptHandler(shm):
    shm.unlink()
    raise KeyboardInterrupt()






#code de stackoverflow pour régler un bug dans les shared memory https://stackoverflow.com/questions/77285558/why-does-python-shared-memory-implicitly-unlinked-on-exit
def remove_shm_from_resource_tracker():
    """Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked

    More details at: https://bugs.python.org/issue38119
    """

    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.register(name, rtype)
    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.unregister(name, rtype)
    resource_tracker.unregister = fix_unregister

    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]

