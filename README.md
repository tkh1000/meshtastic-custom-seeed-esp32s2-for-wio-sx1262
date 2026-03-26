# Meshtastic Firmware Builder
## Seeed XIAO ESP32S3 + Wio SX1262 NON-KIT (Header / Edge Pins)

This repo auto-builds a custom Meshtastic firmware for the **Seeed Wio-SX1262-for-XIAO**
standalone board connected to a **Seeed XIAO ESP32S3** via the physical edge header pins —
**not** the B2B (board-to-board) surface connector used in the official kit. You can also just download the latest .zip I have and flash it using esptools. Still working on how get this working on the webflasher anyone want to help lmk ok thx byeeee. 

---

## The Problem

The official Meshtastic `seeed-xiao-s3` firmware target ships with pin definitions
for the **kit version** of the Wio SX1262, which uses a 30-pin B2B connector
(internal traces, not accessible on the header). If you bought the standalone Seeed esp32s3 and
Wio SX1262 board and wired it yourself (like my dumbarse did) those pins are wrong and LoRa will not work (might even wreck the board if you leave it wired and powered long enough).

## The Fix

Custom firmware reprogrammed to use the pins available on the seeed board, directly stacked too so you don't need to use jumper cables. 

**header-accessible pins**: *big disclaimer that the pin numbers on dev board are actually different that the gpio pins of the actually chip* Astric means connection is required, all other pins can stack normally as such for ease or disconnected. 
 
| SX1262 Pin      |SEEED ESP32s3 Pin (NOT GPIO) |
|-----------------|-------------|
| VIN      | VIN         |
| GND*      | GND         |
| 3v3*       | 3v3           |
| LORA_MOSI*       | D10          |
| LORA_MISO*       | D9           |
| LORA_SCK*        | D8           |
| D7        | D7           |


| D0        | D0           |
| LORA_DIO1*       | D1           |
| LORA_RESET*      | D2           |
| LORA_BUSY*      | D3           |
| LORA_CS*         | D4           |
| RF_SW        | D5           | <- re-programmed so init doesnt hang for a minute 
| D6        | D6           |


---

## INSTRUCTIONS: 

How to Build (GitHub Actions — no software needed on your PC)

### STEP 1 (You can skip this if you want): Build it with GitHub Actions
- Download this repo, and upload it into a new repo on github
- Click Actions > Build Meshtastic Firmware > Run Workflow drop down > Run Workflow
- Download the Artifacts and proceed to Step 2
  
### STEP 2 (Easy, you should do this): Download firmware and flash using linux or mac
- Download this the .zip firmware release v5 (or the artifact from step 1)
- Extract, Change directory to the extracted folder
    `cd ~/Downloads/[EXTRACTED ARTIFACTS FOLDER]`
- Download and install esptools if you haven't already
    `python3 -m pip install esptool`
- Erase the flash (Optional if you want a clean slate)
    `python3 -m esptool --chip esp32s3 --port /dev/[YOUR PORT] --baud 921600 erase_flash`
    Replace `[YOUR PORT]` with your actual port (`COM3`, `/dev/tty.usbserial-, /dev/tty.usbmodem1101...`, etc.).
    Check with `ls /dev/tty.*`
- Flash firmware
    `python3 -m esptool --chip esp32s3 --port [YOUR PORT] --baud 921600 write_flash 0x0000 bootloader.bin 0x8000 partitions.bin 0x10000 firmware.bin`

- Enjoy!
  
  
  


## Credits
- Claude.ai
- [Meshtastic firmware](https://github.com/meshtastic/firmware)
- Pin mapping sourced from community research on
  [Meshtastic issue #6478](https://github.com/meshtastic/firmware/issues/6478)
