# Meshtastic Firmware Builder
## Seeed XIAO ESP32S3 + Wio SX1262 (Header / Edge Pins)

This repo auto-builds a custom Meshtastic firmware for the **Seeed Wio-SX1262-for-XIAO**
standalone board connected to a **Seeed XIAO ESP32S3** via the physical edge header pins —
**not** the B2B (board-to-board) surface connector used in the official kit.

---

## The Problem

The official Meshtastic `seeed-xiao-s3` firmware target ships with pin definitions
for the **kit version** of the Wio SX1262, which uses a 30-pin B2B connector
(internal traces, not accessible on the header). If you bought the standalone
Wio SX1262 board and wired it yourself, those pins are wrong and LoRa will not work.

## The Fix

This repo patches the `variant.h` pin definitions at build time to use the correct
**header-accessible GPIO pins**:

| SX1262 Pin      |SEEED ESP32s3|
|-----------------|------|
| LORA_MOSI       | 10   |
| LORA_MISO       | 9    |
| LORA_SCK        | 8    |
| LORA_CS         | 4    |
| LORA_RESET      | 2    |
| LORA_DIO1       | 1    |
| SX126X_BUSY     | 3    |
| SX126X_RXEN     | 5    |
| TCXO voltage    | 1.8V |

---

## How to Build (GitHub Actions — no software needed on your PC)

### 1. Create a GitHub account (free)
Go to [github.com](https://github.com) and sign up if you haven't already.

### 2. Create a new repository
- Click **+** → **New repository**
- Name it anything, e.g. `meshtastic-xiao-builder`
- Set it to **Public** (required for free Actions minutes)
- Click **Create repository**

### 3. Upload this folder's contents
Drag and drop all files from this folder into your new repo, or use:
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/meshtastic-xiao-builder.git
git add .
git commit -m "Initial build config"
git push -u origin main
```

### 4. Trigger the build
- Go to your repo on GitHub
- Click the **Actions** tab
- Click **Build Meshtastic – Seeed XIAO ESP32S3 + Wio SX1262 (Header Pins)**
- Click **Run workflow** → **Run workflow**
- Wait ~15–25 minutes for the build to finish

### 5. Download your firmware
- Once the workflow shows a green ✅, click into the run
- Scroll down to **Artifacts**
- Click **meshtastic-xiao-esp32s3-wio-sx1262-header-pins** to download a `.zip`

---

## How to Flash

### Option A — Meshtastic Web Flasher (haven't gotten this to work successful)
1. Go to [flasher.meshtastic.org](https://flasher.meshtastic.org)
2. Connect your XIAO ESP32S3 via USB
3. Click **Custom firmware** (or drag-and-drop the `.zip` from the artifact)
4. Follow the on-screen steps

### Option B — esptool (manual, mac)
```bash
python3 -m pip install esptool

cd ~/Downloads/[EXTRACTED ARTIFACTS FOLDER]

python3 -m esptool --chip esp32s3 --port /dev/tty.usbmodem1101 --baud 921600 erase_flash

python3 -m esptool --chip esp32s3 --port /dev/tty.usbmodem101 --baud 921600 write_flash 0x0000 bootloader.bin 0x8000 partitions.bin 0x10000 firmware.bin

```
Replace `/dev/tty.usbmodem101` with your actual port (`COM3`, `/dev/tty.usbserial-...`, etc.).
Check with `ls /dev/tty.*`
---

## Wiring Reference

Wire the standalone Wio SX1262 to your XIAO ESP32S3 header:

```

```

---

## Rebuilding / Updating

To rebuild against a newer Meshtastic release, just re-trigger the workflow from
the **Actions** tab. The workflow always pulls the latest `master` branch of the
official Meshtastic firmware repo.

---

## Credits
- [Meshtastic firmware](https://github.com/meshtastic/firmware)
- Pin mapping sourced from community research on
  [Meshtastic issue #6478](https://github.com/meshtastic/firmware/issues/6478)
