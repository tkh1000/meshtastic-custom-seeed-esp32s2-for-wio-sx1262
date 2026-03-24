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

| Signal          | GPIO |
|-----------------|------|
| LORA_MOSI       | 9    |
| LORA_MISO       | 8    |
| LORA_SCK        | 7    |
| LORA_CS         | 5    |
| LORA_RESET      | 3    |
| LORA_DIO1       | 2    |
| SX126X_BUSY     | 4    |
| SX126X_RXEN     | 6    |
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

### Option A — Meshtastic Web Flasher (easiest)
1. Go to [flasher.meshtastic.org](https://flasher.meshtastic.org)
2. Connect your XIAO ESP32S3 via USB
3. Click **Custom firmware** (or drag-and-drop the `.zip` from the artifact)
4. Follow the on-screen steps

### Option B — esptool (manual)
```bash
pip install esptool

esptool.py --chip esp32s3 --port /dev/ttyUSB0 \
  --baud 921600 write_flash \
  0x0000  bootloader.bin \
  0x8000  partitions.bin \
  0x10000 firmware.bin
```
Replace `/dev/ttyUSB0` with your actual port (`COM3`, `/dev/tty.usbserial-...`, etc.).

---

## Wiring Reference

Wire the standalone Wio SX1262 to your XIAO ESP32S3 header:

```
XIAO ESP32S3 Pin   →   Wio SX1262 Pin
──────────────────────────────────────
D0  (GPIO 1)           (not used)
D1  (GPIO 2)       →   DIO1
D2  (GPIO 3)       →   RESET
D3  (GPIO 4)       →   BUSY
D4  (GPIO 5)       →   NSS / CS
D5  (GPIO 6)       →   DIO2 / RXEN
D7  (GPIO 7)       →   SCK
D8  (GPIO 8)       →   MISO
D9  (GPIO 9)       →   MOSI
3V3                →   VCC
GND                →   GND
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
