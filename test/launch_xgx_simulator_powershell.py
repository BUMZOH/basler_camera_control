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
    creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB,
)

time.sleep(3)

subprocess.run(
    [
        "powershell",
        "-Command",
        (
            "$wshell = New-Object -ComObject WScript.Shell; "
            "$wshell.AppActivate('Baslerテスト'); "
            "$wshell.SendKeys('T')"
        ),
    ]
)