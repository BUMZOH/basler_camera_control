import subprocess
import time
from pathlib import Path

import pyautogui
import pygetwindow as gw

# =========================================================
# Settings
# =========================================================
SIMULATOR = r"C:\Program Files (x86)\KEYENCE\XG-X VisionEditor H1X\sim\XG-X Simulator.exe"
BOOT_FILE = Path(__file__).resolve().parent / "XG_SimBoot.dat"

WINDOW_X = 0
WINDOW_Y = 0
WINDOW_WIDTH = 1060
WINDOW_HEIGHT = 875

WINDOW_TIMEOUT = 10


# Check the boot file
if not BOOT_FILE.exists():
    print('"XG_SimBoot.dat"が見つかりません。')
    print('"XG_SimBoot.dat"は以下のフォルダにあります。')
    print(r'"C:\ProgramData\KEYENCE\XG-H7N\Vision Editor"')
    raise SystemExit


# Start the XG-X Simulator
subprocess.Popen(
    [
        SIMULATOR,
        BOOT_FILE,
    ],
    # Allow the simulator to run correctly from the VS Code debugger
    creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB,
)

# Wait for the XG-X Simulator window
start_time = time.time()

while True:
    windows = gw.getWindowsWithTitle("Baslerテスト")

    if windows:
        break

    if time.time() - start_time >= WINDOW_TIMEOUT:
        raise TimeoutError("XG-X Simulator window not found.")

    time.sleep(0.1)

window = windows[0]

# Set window position and size
window.moveTo(WINDOW_X, WINDOW_Y)
window.resizeTo(WINDOW_WIDTH, WINDOW_HEIGHT)

# Activate the XG-X Simulator window
window.activate()

time.sleep(0.5)

# Press the T key
pyautogui.press("t")