# User Guide

## Overview

Translate email bodies in GNOME Evolution offline using ArgosTranslate. HTML formatting is preserved.

## Install

> **No prebuilt packages yet** — install via build-from-source on all distros.
> Prebuilt `.deb` (Ubuntu/Debian) and AUR (Manjaro/Arch) are planned for the v1.5
> release. To produce a local `.deb` from the source tree, run `cd build && cpack -G DEB`
> after building.

### From source — Ubuntu / Debian

```bash
sudo apt install cmake pkg-config evolution-dev evolution-data-server-dev \
  python3 python3-venv python3-pip
git clone https://github.com/MoDD0/moddo-evolution-translator.git
cd moddo-evolution-translator
./scripts/install-from-source.sh
evolution-translate-setup
killall evolution 2>/dev/null || true
evolution &
```

### From source — Manjaro / Arch

```bash
sudo pacman -S --needed cmake pkgconf python python-pip
git clone https://github.com/MoDD0/moddo-evolution-translator.git
cd moddo-evolution-translator
./scripts/install-from-source.sh
evolution-translate-setup
killall evolution 2>/dev/null || true
evolution &
```

## Usage

- **Translate**: press `Alt+Shift+T` or click the **Translate button** in the toolbar
- **Toggle back to original**: press the same shortcut or click the toolbar button again
- **Settings**: Edit → Translate Settings

### Settings Explained

- **Target language**: default output language for translations
- **Provider**: Argos Translate (offline, privacy-focused) or Google Translate (online)
- **Translate shortcut**: keyboard shortcut for the Translate action (default: `Alt+Shift+T`). Takes effect after restarting Evolution.
- **Install models on demand**: automatically download missing Argos Translate models the first time they are needed
- **Python setup**: run `evolution-translate-setup` once per user to create a virtualenv and install Python dependencies and (optionally) default models

Advanced (optional):
- `TRANSLATE_HELPER_PATH` can point to a local translate_runner.py for development
- `TRANSLATE_PYTHON_BIN` can point to a custom Python interpreter (e.g., inside your venv)

## Notes

- Module path: `/usr/lib*/evolution/modules/libtranslate-module.so`
- Helper scripts: `/usr/share/evolution-translate/translate/`
- Per‑user Python env: `~/.local/lib/evolution-translate/venv`
- Models: `~/.local/share/argos-translate/packages/`
