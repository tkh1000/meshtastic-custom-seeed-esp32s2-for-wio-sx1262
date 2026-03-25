import re, pathlib, sys

variant_path = pathlib.Path(sys.argv[1])
variant_dir = variant_path.parent

print("Variant dir:", variant_dir)
print("Files:", list(variant_dir.iterdir()))

# GPIO mapping for XIAO ESP32S3:
# D1=3, D2=4, D3=5, D4=6, D8=8, D9=9, D10=10
PIN_BLOCK = """
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
#define SX126X_DIO3_TCXO_VOLTAGE 0
"""

STRIP_PATTERNS = [
    r'#define\s+USE_SX1262[^\n]*\n',
    r'#define\s+LORA_MISO[^\n]*\n',
    r'#define\s+LORA_SCK[^\n]*\n',
    r'#define\s+LORA_MOSI[^\n]*\n',
    r'#define\s+LORA_CS[^\n]*\n',
    r'#define\s+LORA_RESET[^\n]*\n',
    r'#define\s+LORA_DIO1[^\n]*\n',
    r'#define\s+LORA_DIO2[^\n]*\n',
    r'#define\s+SX126X_CS[^\n]*\n',
    r'#define\s+SX126X_DIO1[^\n]*\n',
    r'#define\s+SX126X_BUSY[^\n]*\n',
    r'#define\s+SX126X_RESET[^\n]*\n',
    r'#define\s+SX126X_DIO2_AS_RF_SWITCH[^\n]*\n',
    r'#define\s+SX126X_RXEN[^\n]*\n',
    r'#define\s+SX126X_TXEN[^\n]*\n',
    r'#define\s+SX126X_DIO3_TCXO_VOLTAGE[^\n]*\n',
]

def patch_file(path):
    if not path.exists():
        print("Not found, skipping:", path)
        return
    text = path.read_text()
    for p in STRIP_PATTERNS:
        text = re.sub(p, '', text)
    if re.search(r'#endif', text):
        text = re.sub(r'(#endif\b[^\n]*$)', PIN_BLOCK + r'\1', text, count=1, flags=re.MULTILINE)
    else:
        text += PIN_BLOCK
    path.write_text(text)
    print("Patched:", path)

patch_file(variant_path)
patch_file(variant_dir / "pins_arduino.h")
