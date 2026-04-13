import sys
import winreg

APP_NAME = "DisableEfficiencyMode"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _exe_path() -> str:
    # Works both when run as a script and as a PyInstaller exe
    return sys.executable if getattr(sys, "frozen", False) else sys.argv[0]


def is_enabled() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False


def enable(path: str = None):
    target = path or _exe_path()
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, RUN_KEY, access=winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, target)


def disable():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, RUN_KEY, access=winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, APP_NAME)
    except FileNotFoundError:
        pass
