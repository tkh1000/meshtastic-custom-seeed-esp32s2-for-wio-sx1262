import re, pathlib, sys

variant_path = pathlib.Path(sys.argv[1])
variant_dir = variant_path.parent
firmware_dir = variant_path.parent.parent.parent  # up from variants/seeed_xiao_s3/

print("Variant dir:", variant_dir)
print("Firmware dir:", firmware_dir)
print("Files in variant dir:", list(variant_dir.iterdir()))

# ── 1. Patch variant.h and pins_arduino.h with #undef + #define ───────────
PIN_BLOCK = """
#undef LORA_MOSI
#undef LORA_MISO
#undef LORA_SCK
#undef LORA_CS
#undef LORA_RESET
#undef LORA_DIO1
#undef LORA_DIO2
#undef SX126X_CS
#undef SX126X_DIO1
#undef SX126X_BUSY
#undef SX126X_RESET
#undef SX126X_DIO2_AS_RF_SWITCH
#undef SX126X_RXEN
#undef SX126X_TXEN
#undef SX126X_DIO3_TCXO_VOLTAGE
#undef PIN_SPI_MOSI
#undef PIN_SPI_MISO
#undef PIN_SPI_SCK
#undef PIN_SPI_SS

#define USE_SX1262
#define LORA_MOSI        9
#define LORA_MISO        8
#define LORA_SCK         7
#define LORA_DIO1        2
#define LORA_RESET       3
#define LORA_CS          5
#define SX126X_CS        5
#define SX126X_DIO1      2
#define SX126X_BUSY      4
#define SX126X_RESET     3
#define SX126X_DIO2_AS_RF_SWITCH
#define SX126X_RXEN      6
#define SX126X_TXEN      RADIOLIB_NC
#define SX126X_DIO3_TCXO_VOLTAGE 1.8
#define PIN_SPI_MOSI     9
#define PIN_SPI_MISO     8
#define PIN_SPI_SCK      7
#define PIN_SPI_SS       5
"""

def patch_header(path):
    if not path.exists():
        print("Not found, skipping:", path)
        return
    text = path.read_text()
    # Append at very end — after all other definitions so our #undefs win
    text = text.rstrip() + "\n" + PIN_BLOCK + "\n"
    path.write_text(text)
    print("Patched:", path)

patch_header(variant_path)
patch_header(variant_dir / "pins_arduino.h")

# ── 2. Patch platformio.ini — remove any -D flags for these pins ──────────
pio_ini = firmware_dir / "platformio.ini"
if pio_ini.exists():
    text = pio_ini.read_text()
    # Remove any build_flags lines that hardcode the B2B kit pins
    for pin in ["LORA_CS", "LORA_DIO1", "LORA_RESET", "LORA_BUSY",
                "SX126X_CS", "SX126X_DIO1", "SX126X_BUSY", "SX126X_RESET"]:
        text = re.sub(r'\s*-D' + pin + r'=\d+', '', text)
    pio_ini.write_text(text)
    print("Patched platformio.ini")
else:
    print("platformio.ini not found at", pio_ini)

# ── 3. Also search for any board-specific ini that might hardcode pins ─────
for ini_file in firmware_dir.rglob("*.ini"):
    text = ini_file.read_text()
    if "seeed" in text.lower() and "xiao" in text.lower():
        print("Found board ini:", ini_file)
        # Show the relevant section
        for line in text.splitlines():
            if any(x in line for x in ["LORA_", "SX126X_", "seeed", "xiao"]):
                print("  >>", line)
