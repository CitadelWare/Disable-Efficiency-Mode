# Disable Efficiency Mode

**Stop Windows from throttling your apps.**

Windows 11 quietly puts processes into "Efficiency Mode" — deprioritising CPU time and memory to save power. This is fine for background apps, but it can silently degrade performance for games, creative tools, and anything that needs consistent responsiveness.

**Disable Efficiency Mode** runs silently in your system tray and continuously prevents Windows from applying this throttle to any running process.

---

## Download

<p align="center">
  <a href="https://github.com/CitadelWare/Disable-Efficiency-Mode/raw/refs/heads/main/DisableEfficiencyMode.exe">
    <img src="https://img.shields.io/badge/Download-DisableEfficiencyMode.exe-brightgreen?style=for-the-badge&logo=windows" alt="Download">
  </a>
</p>

> **Requirements:** Windows 10/11 (64-bit)  
> **Size:** ~12 MB &nbsp;|&nbsp; **No installer needed**

---

## How it works

1. **Run the exe** — a one-time UAC prompt copies it to `C:\Program Files\DisableEfficiencyMode\` and registers it to launch on startup automatically.
2. **It runs silently** — a small green icon appears in your system tray. No windows, no configuration needed.
3. **Every 5 seconds** it scans all running processes and calls the Windows `SetProcessInformation` API to disable CPU throttling on each one.
4. **Right-click the tray icon → Exit** to stop it at any time.

---

## What it actually does (technically)

The app calls a single Windows API per process:

```
SetProcessInformation(
    hProcess,
    ProcessPowerThrottling,
    { ControlMask: EXECUTION_SPEED, StateMask: 0 }  ← 0 = disabled
)
```

Setting `StateMask` to `0` instructs the Windows kernel scheduler to treat the process with normal CPU priority — the same as disabling Efficiency Mode manually via Task Manager. No kernel drivers, no system file modifications, no third-party services.

Startup persistence is handled via a standard registry entry:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

---

## Security & transparency

This tool is closed-source but designed to be fully auditable through standard Windows tooling:

| Concern | Answer |
|---|---|
| **Network activity** | None. The app makes zero network connections. Verify with [Wireshark](https://www.wireshark.org/) or Windows Firewall logs. |
| **What APIs does it call?** | `SetProcessInformation` (kernel32), `OpenProcess` (kernel32), `RegSetValueEx` (advapi32). Verify with [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) from Sysinternals. |
| **What does it write to disk?** | Only copies itself to `C:\Program Files\DisableEfficiencyMode\` on first run. Nothing else. |
| **Registry changes** | One key: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\DisableEfficiencyMode`. Inspect it in `regedit` at any time. |
| **Does it need admin?** | A one-time UAC prompt is required to write to Program Files. After that, no elevation is needed. |
| **Can I remove it?** | Yes — delete `C:\Program Files\DisableEfficiencyMode\` and remove the registry key, or simply uninstall via Windows Settings → Apps. |

You can inspect all API calls live using [Process Hacker](https://processhacker.sourceforge.io/) or [System Informer](https://systeminformer.sourceforge.io/) while the app is running.

---

## Why not just use Task Manager?

Task Manager lets you disable Efficiency Mode on individual processes manually — but the setting doesn't persist. The next time that process restarts, Windows reapplies it. This tool handles it automatically for every process, every time.

---

*Built by [CitadelWare](https://github.com/CitadelWare)*
