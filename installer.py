import ctypes
import os
import shutil
import sys

INSTALL_DIR = os.path.join(
    os.environ.get("ProgramFiles", r"C:\Program Files"), "DisableEfficiencyMode"
)
EXE_NAME = "DisableEfficiencyMode.exe"
INSTALL_PATH = os.path.join(INSTALL_DIR, EXE_NAME)


def current_exe() -> str:
    return sys.executable if getattr(sys, "frozen", False) else os.path.abspath(sys.argv[0])


def is_installed() -> bool:
    return os.path.normcase(current_exe()) == os.path.normcase(INSTALL_PATH)


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def install():
    """Copy exe to Program Files. Must be called from an elevated process."""
    os.makedirs(INSTALL_DIR, exist_ok=True)
    shutil.copy2(current_exe(), INSTALL_PATH)


def elevate_and_install() -> bool:
    """
    Re-launch self elevated with --install flag to copy to Program Files.
    Returns True if UAC was accepted, False if denied/cancelled.
    """
    result = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", current_exe(), "--install", None, 1
    )
    return int(result) > 32
