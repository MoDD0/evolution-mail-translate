# Moddo Evolution Translator

**Offline email translation for GNOME Evolution using ArgosTranslate**

[![Latest release](https://img.shields.io/github/v/release/MoDD0/moddo-evolution-translator?label=latest%20release&color=blue)](https://github.com/MoDD0/moddo-evolution-translator/releases/latest)
[![Release date](https://img.shields.io/github/release-date/MoDD0/moddo-evolution-translator?color=blue)](https://github.com/MoDD0/moddo-evolution-translator/releases/latest)
[![Last commit](https://img.shields.io/github/last-commit/MoDD0/moddo-evolution-translator?color=informational)](https://github.com/MoDD0/moddo-evolution-translator/commits/main)
[![License](https://img.shields.io/badge/license-LGPL--2.1%2B-green.svg)](#license)
[![Documentation](https://img.shields.io/badge/docs-complete-brightgreen.svg)](docs/USER_GUIDE.md)

> 🆕 **Latest: v1.2.1** — Verified on **GNOME Evolution 3.60.1**, plus optional CPU quantization (`ARGOS_COMPUTE_TYPE=int8`) for 2–4× faster translation.
> See the [release notes](https://github.com/MoDD0/moddo-evolution-translator/releases/latest) or the full [CHANGELOG](docs/CHANGELOG.md).

> **Tested on Manjaro Linux with GNOME Evolution 3.58.3 and 3.60.1.**
> Originally forked from [costantinoai/evolution-mail-translate](https://github.com/costantinoai/evolution-mail-translate),
> extended and maintained independently. Compatibility with Evolution ≥ 3.56's new EUIManager API
> was the original motivation — see [Changes from upstream](#changes-from-upstream).

## Overview

This Evolution extension adds instant, privacy-preserving email translation directly within GNOME Evolution. Translate foreign language emails to your preferred language with a single click—all processing happens locally on your machine with no data ever leaving your computer.

## Key Features

- **One-Click Translation**: Translate emails directly from the toolbar, menu, or keyboard shortcut
- **Toggle back instantly**: Press the shortcut (or click the toolbar button) again to restore the original
- **100% Offline & Private**: Uses local translation models (ArgosTranslate), no internet required, no data transmitted
- **Toolbar button**: Translate icon appears next to Reply/Forward in the mail toolbar
- **Custom keyboard shortcut**: Default `Alt+Shift+T`, fully configurable in Translate Settings
- **Install-on-Demand**: Automatically downloads missing translation models as needed
- **HTML Email Support**: Preserves formatting, styles, and structure in translated emails
- **Auto Language Detection**: Automatically detects source language
- **50+ Languages**: Supports translation between 50+ language pairs
- **GPU Acceleration**: Automatically uses CUDA when available for faster translation

## Quick Start

### Installation

> **No prebuilt packages yet.** All distros currently install via build-from-source.
> Prebuilt `.deb` and an AUR package are on the roadmap (alongside our v1.5 release).
> If you want a `.deb` locally, run `cd build && cpack -G DEB` after the build step
> below — it'll produce `moddo-evolution-translator_1.2.1-1_<arch>.deb` you can
> `apt install ./...`.

#### Ubuntu / Debian

```bash
# 1. Install build dependencies
sudo apt install cmake pkg-config evolution-dev evolution-data-server-dev \
  python3 python3-venv python3-pip

# 2. Clone and build
git clone https://github.com/MoDD0/moddo-evolution-translator.git
cd moddo-evolution-translator
./scripts/install-from-source.sh

# 3. Restart Evolution
killall evolution 2>/dev/null || true
evolution &
```

#### Manjaro / Arch Linux

> Tested on Manjaro with GNOME Evolution 3.58.3 and 3.60.1.
> On Arch-based distros the `evolution` package already includes development headers,
> so no separate `-dev` package is needed.

```bash
# 1. Install build dependencies
sudo pacman -S --needed cmake pkgconf python python-pip

# 2. Clone and build
git clone https://github.com/MoDD0/moddo-evolution-translator.git
cd moddo-evolution-translator
./scripts/install-from-source.sh

# 3. Restart Evolution
killall evolution 2>/dev/null || true
evolution &
```

**Notes:**
- Evolution only loads modules from `/usr/lib*/evolution/modules/`, so installation requires sudo
- The module is installed to `/usr/lib*/evolution/modules/libtranslate-module.so`
- Python helper scripts are installed to `/usr/share/evolution-translate/translate/`
- Python environment and models are per-user: run `evolution-translate-setup` to create a venv under `~/.local/lib/evolution-translate/venv` and install models under `~/.local/share/argos-translate/packages/`

**Uninstall:**

```bash
# From the repository directory
./scripts/uninstall.sh
```

See **[USER_GUIDE.md](docs/USER_GUIDE.md)** for detailed installation instructions and all available methods.

### Usage

1. Select an email and press `Alt+Shift+T` — or click the **Translate button** in the toolbar
2. Press the same shortcut (or click the toolbar button) again to toggle back to the original
3. Configure settings in `Edit` → `Translate Settings`
   - Change the target language, translation provider, or keyboard shortcut

See **[USER_GUIDE.md](docs/USER_GUIDE.md)** for complete usage documentation.

## Documentation

- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Installation, usage, configuration, and troubleshooting
- **[DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** - Architecture, development, and contribution guidelines
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Notable changes

## Settings

Open “Translate Settings” via **Edit → Translate Settings**.

- **Target language**: Choose your default translation target
- **Provider**: Argos Translate (offline) or Google Translate (online)
- **Translate shortcut**: Customize the keyboard shortcut (default: `Alt+Shift+T`). Takes effect after restarting Evolution.
- **Install models on demand**: If enabled, missing Argos models are downloaded automatically the first time a pair is needed
- **Python venv**: Create and manage your per-user venv with `evolution-translate-setup` (installs Python deps and optionally models)

Tip: You can also set environment variables for development overrides:
- `TRANSLATE_HELPER_PATH` to point to a local translate_runner.py
- `TRANSLATE_PYTHON_BIN` to point to a specific Python interpreter
- `ARGOS_COMPUTE_TYPE` to opt into ctranslate2 quantization for faster CPU
  translation. Recommended: `int8` (or `int8_float32` for slightly higher
  quality). Default is argos's `auto`. Invalid values fall back to default.

## Security & Privacy

- **No Data Transmission**: All translation happens locally; message content never leaves your machine
- **Body Only**: Only email body is processed; headers, addresses, and attachments are never touched
- **Open Source Models**: Uses transparent, auditable open-source translation models
- **No API Keys**: No accounts, no tracking, no telemetry

## Requirements

- **GNOME Evolution** ≥ 3.36
- **Python** 3.8+
- **CMake** 3.10+ (for building from source)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

This project follows the same LGPL-2.1+ licensing model as the Evolution example module files.

## Changes from upstream

This fork fixes two issues that prevent the plugin from building and running on
**Evolution ≥ 3.56** (which ships with Manjaro, Fedora, and other rolling-release distros):

### 1. `e_ui_manager_add_actions_with_eui_data` API change

Evolution 3.56 reduced the function from 10 arguments to 7. The `name` string,
`-1` length, and `&error` parameters were removed, and `user_data` moved before `eui`:

```c
/* Old (Evolution < 3.56) */
e_ui_manager_add_actions_with_eui_data(ui_manager, group, domain,
    entries, n_entries, "ui-name", eui_def, -1, user_data, &error);

/* New (Evolution ≥ 3.56) */
e_ui_manager_add_actions_with_eui_data(ui_manager, group, domain,
    entries, n_entries, user_data, eui_def);
```

### 2. EUI XML format for custom submenus

The new EUI parser requires `<submenu action='...'>` referencing a registered action.
The old `<submenu id='...'>` with `<attribute name='label'>` and `after=` attributes
are no longer valid. Custom plugin menus must use the `custom-menus` placeholder:

```xml
<eui>
  <menu id='main-menu'>
    <placeholder id='custom-menus'>
      <submenu action='translate-menu'>
        <item action='translate-message-action'/>
        ...
      </submenu>
    </placeholder>
  </menu>
</eui>
```

The submenu header (`translate-menu`) must be registered as an `EUIActionEntry`
with a `NULL` activate callback.

## Why a separate project?

This started as a fork of [costantinoai/evolution-mail-translate](https://github.com/costantinoai/evolution-mail-translate).
While extending it, we noticed the upstream project independently tagged their own `v1.2.0` release
with different content — making it clear that the two projects had diverged enough to warrant
a distinct identity rather than risk confusing users about which `v1.2.0` is which.

The rename to **Moddo Evolution Translator** reflects that this is now an independently maintained
project, not just a patch on top of the original.

## Credits

- Originally forked from [costantinoai/evolution-mail-translate](https://github.com/costantinoai/evolution-mail-translate)
- Built on [ArgosTranslate](https://github.com/argosopentech/argos-translate)
- Integrates with [GNOME Evolution](https://wiki.gnome.org/Apps/Evolution)
- Translation models from [OpenNMT](https://opennmt.net/)
