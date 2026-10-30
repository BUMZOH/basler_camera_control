import ctypes
import subprocess
import time


SIMULATOR = (
    r"C:\Program Files (x86)\KEYENCE"
    r"\XG-X VisionEditor H1X\sim\XG-X Simulator.exe"
)

BOOT_FILE = (
    r"C:\Users\fumih\Desktop"
    r"\basler_camera_test\XG_SimBoot.dat"
)


subprocess.Popen(
    [
        SIMULATOR,
        BOOT_FILE,
    ],
    # Allow the simulator to run correctly from the VS Code debugger
    creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB,
)

time.sleep(3)


# Find the XG-X Simulator window
simulator_hwnd = None

def enum_windows_callback(hwnd, _):
    global simulator_hwnd

    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)

    if length > 0:
        title = ctypes.create_unicode_buffer(length + 1)

        ctypes.windll.user32.GetWindowTextW(
            hwnd,
            title,
            length + 1,
        )

        if "Baslerテスト" in title.value:
            simulator_hwnd = hwnd
            return False

    return True


enum_windows_proc = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    ctypes.c_void_p,
    ctypes.c_void_p,
)

ctypes.windll.user32.EnumWindows(
    enum_windows_proc(enum_windows_callback),
    0,
)

print("Window handle:", simulator_hwnd)

# Activate the XG-X Simulator window
ctypes.windll.user32.SetForegroundWindow(simulator_hwnd)

time.sleep(0.5)

# Press the T key
ctypes.windll.user32.keybd_event(
    ord("T"),
    0,
    0,
    0,
)

# Release the T key
ctypes.windll.user32.keybd_event(
    ord("T"),
    0,
    2,
    0,
)