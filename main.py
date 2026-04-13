import os
import sys
import pystray
from PIL import Image, ImageDraw
from monitor import Monitor
import startup
import installer


def create_icon_image():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 4, size - 4], fill=(34, 197, 94, 255))
    draw.line([20, 20, 44, 20], fill="white", width=5)
    draw.line([20, 32, 40, 32], fill="white", width=5)
    draw.line([20, 44, 44, 44], fill="white", width=5)
    draw.line([20, 20, 20, 44], fill="white", width=5)
    return img


def main():
    # Running elevated to perform install (launched by elevate_and_install)
    if "--install" in sys.argv:
        installer.install()
        startup.enable(installer.INSTALL_PATH)
        # Launch the installed copy and exit
        os.startfile(installer.INSTALL_PATH)
        sys.exit(0)

    # Not yet in Program Files — request one-time UAC to install
    if not installer.is_installed():
        accepted = installer.elevate_and_install()
        if accepted:
            # Elevated copy will launch the installed exe; we're done here
            sys.exit(0)
        else:
            # User denied UAC — run from current location and register startup here
            startup.enable()

    else:
        # Already installed — ensure startup key stays pointing here
        startup.enable()

    mon = Monitor(interval=5.0)
    mon.start()

    def on_exit(icon, item):
        mon.stop()
        icon.stop()

    def status_title(item):
        return f"Protected: {mon.protected} | Skipped: {mon.failed}"

    menu = pystray.Menu(
        pystray.MenuItem(status_title, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", on_exit),
    )

    icon = pystray.Icon(
        "DisableEfficiencyMode",
        create_icon_image(),
        "Disable Efficiency Mode",
        menu,
    )
    icon.run()


if __name__ == "__main__":
    main()
