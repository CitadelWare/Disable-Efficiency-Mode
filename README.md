<div align="center">

<h1>Disable Efficiency Mode</h1>

<p><strong>Stop Windows from silently throttling your apps.</strong></p>

<p>
  <a href="https://github.com/CitadelWare/Disable-Efficiency-Mode/raw/refs/heads/main/DisableEfficiencyMode.exe">
    <img src="https://img.shields.io/badge/Download-DisableEfficiencyMode.exe-22c55e?style=for-the-badge&logo=windows&logoColor=white" alt="Download">
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Windows-10%2F11-0078d4?style=flat-square&logo=windows&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3.12-3776ab?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square">
  <img src="https://img.shields.io/badge/Network_calls-0-22c55e?style=flat-square">
</p>

</div>

---

Windows 11 quietly places processes into **Efficiency Mode** (EcoQoS) — deprioritising CPU scheduling and lowering memory priority to save power. This is fine for true background tasks, but Windows applies it aggressively and without distinction, silently degrading performance for games, creative tools, and anything that needs consistent responsiveness.

**Disable Efficiency Mode** runs silently in your system tray and uses the Windows `SetProcessInformation` API to continuously prevent this throttle from being applied to any running process.

---

## Download

<p align="center">
  <a href="https://github.com/CitadelWare/Disable-Efficiency-Mode/raw/refs/heads/main/DisableEfficiencyMode.exe">
    <img src="https://img.shields.io/badge/Download-DisableEfficiencyMode.exe-22c55e?style=for-the-badge&logo=windows&logoColor=white" alt="Download">
  </a>
</p>

> **Requirements:** Windows 10 or 11 (64-bit) &nbsp;|&nbsp; **Size:** ~12 MB &nbsp;|&nbsp; **No installer needed**

---

## How it works

1. **Run the exe** — a one-time UAC prompt copies it to `C:\Program Files\DisableEfficiencyMode\` and registers it to launch on every startup automatically.
2. **Runs silently** — a small green icon in your system tray confirms it's active. No windows, no configuration.
3. **Every 5 seconds**, all running processes are scanned and CPU throttling is disabled on each one via a Windows API call.
4. **Right-click the tray icon → Exit** to stop it any time.

---

## Technical details

The core of the app is a single Windows API call per process:

```c
PROCESS_POWER_THROTTLING_STATE state = {
    .Version     = PROCESS_POWER_THROTTLING_CURRENT_VERSION,
    .ControlMask = PROCESS_POWER_THROTTLING_EXECUTION_SPEED,
    .StateMask   = 0  // 0 = disabled
};

SetProcessInformation(hProcess, ProcessPowerThrottling, &state, sizeof(state));
```

Setting `StateMask` to `0` instructs the Windows kernel scheduler to treat the process with normal CPU priority — identical to disabling Efficiency Mode manually in Task Manager, but persistent and automatic across all processes.

Startup persistence uses a standard per-user registry entry (no elevated access required after install):
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\DisableEfficiencyMode
```

---

## Security

The source code is fully open — read it yourself. In summary:

| What | Detail |
|---|---|
| **Network activity** | None. Zero connections, ever. |
| **APIs used** | `SetProcessInformation`, `OpenProcess` (kernel32) · `RegSetValueEx` (advapi32) |
| **Files written** | Copies itself to `C:\Program Files\DisableEfficiencyMode\` on first run only |
| **Registry** | One key: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\DisableEfficiencyMode` |
| **Admin rights** | One-time UAC prompt to write to Program Files. Not required again after. |
| **Kernel drivers** | None. Entirely user-space. |

To verify live: use [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) or [System Informer](https://systeminformer.sourceforge.io/) while the app is running.

---

## Building from source

```bash
git clone https://github.com/CitadelWare/Disable-Efficiency-Mode.git
cd Disable-Efficiency-Mode
pip install -r requirements.txt
python main.py
```

To build the exe:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name DisableEfficiencyMode main.py
# Output: dist/DisableEfficiencyMode.exe
```

---

## Uninstalling

1. Right-click the tray icon → **Exit**
2. Delete `C:\Program Files\DisableEfficiencyMode\`
3. Open `regedit` and remove `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\DisableEfficiencyMode`

Or uninstall via **Windows Settings → Apps**.

---

## Why not just use Task Manager?

Task Manager lets you disable Efficiency Mode per-process manually — but the setting resets every time that process restarts. This tool handles it automatically, for every process, every time.

---

<div align="center">
  <sub>Built by <a href="https://github.com/CitadelWare">CitadelWare</a> · MIT License</sub>
</div>
