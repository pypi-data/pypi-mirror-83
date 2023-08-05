import ctypes
import os

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)
MAX_PATH = 1024

def is_python(pid):
    """Determine whether the process `pid` is a Python interpreter"""
    h = kernel32.OpenProcess(0x1000, False, pid)
    buf = ctypes.create_unicode_buffer(MAX_PATH)
    r = psapi.GetProcessImageFileNameW(h, buf, MAX_PATH)
    kernel32.CloseHandle(h)
    return os.path.split(buf.value)[-1].lower().startswith("py")

def maybe_pause():
    """Pause if there's a non-Python program in charge of this console"""
    N = 10
    processes = (ctypes.c_uint * N)()
    num_processes = kernel32.GetConsoleProcessList(processes, N)
    if all(is_python(proc) for proc in processes[:num_processes]):
        input("Press ENTER to quit the program...")
