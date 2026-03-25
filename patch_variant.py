import re, pathlib, sys

variant_path = pathlib.Path(sys.argv[1])
variant_dir = variant_path.parent

print("Variant dir:", variant_dir)
print("Files:", list(variant_dir.iterdir()))

# XIAO ESP32S3 GPIO mapping (from official pinout diagram):
# D1=GPIO2, D2=GPIO3, D3=GPIO4, D4=GPIO5
# D8=GPIO7, D9=GPIO8, D10=GPIO9
PIN_BLOCK = """
#undef USE_SX1262
#undef LORA_MOSI
#undef LORA_MISO
#undef LORA_SCK
#undef LORA_CS
#undef LORA_RESET
#undef LORA_DIO1
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

#define USE_SX1262
#define LORA_MOSI        9
#define LORA_MISO        8
#define LORA_SCK         7
#define LORA_DIO1        2
#define LORA_RESET       3
#define LORA_CS          5
#define SX126X_CS        LORA_CS
#define SX126X_DIO1      LORA_DIO1
#define SX126X_BUSY      4
#define SX126X_RESET     LORA_RESET
#define SX126X_DIO2_AS_RF_SWITCH
#define SX126X_RXEN      RADIOLIB_NC
#define SX126X_TXEN      RADIOLIB_NC
#define SX126X_DIO3_TCXO_VOLTAGE 1.8
#define PIN_SPI_MOSI     9
#define PIN_SPI_MISO     8
#define PIN_SPI_SCK      7
"""

def patch_file(path):
    if not path.exists():
        print("Not found, skipping:", path)
        return
    text = path.read_text()
    if re.search(r'#endif', text):
        text = re.sub(r'(#endif\b[^\n]*$)', PIN_BLOCK + r'\1', text, count=1, flags=re.MULTILINE)
    else:
        text += "\n" + PIN_BLOCK + "\n"
    path.write_text(text)
    print("Patched:", path)

patch_file(variant_path)
patch_file(variant_dir / "pins_arduino.h")
