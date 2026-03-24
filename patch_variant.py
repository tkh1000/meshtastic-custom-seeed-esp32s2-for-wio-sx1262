import re, pathlib, sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()

# Remove any existing LoRa/SX126x pin definitions
for p in [
    r'#define\s+USE_SX1262[^\n]*\n',
    r'#define\s+LORA_MISO[^\n]*\n',
    r'#define\s+LORA_SCK[^\n]*\n',
    r'#define\s+LORA_MOSI[^\n]*\n',
    r'#define\s+LORA_CS[^\n]*\n',
    r'#define\s+LORA_RESET[^\n]*\n',
    r'#define\s+LORA_DIO1[^\n]*\n',
    r'#define\s+SX126X_CS[^\n]*\n',
    r'#define\s+SX126X_DIO1[^\n]*\n',
    r'#define\s+SX126X_BUSY[^\n]*\n',
    r'#define\s+SX126X_RESET[^\n]*\n',
    r'#define\s+SX126X_DIO2_AS_RF_SWITCH[^\n]*\n',
    r'#define\s+SX126X_RXEN[^\n]*\n',
    r'#define\s+SX126X_TXEN[^\n]*\n',
    r'#define\s+SX126X_DIO3_TCXO_VOLTAGE[^\n]*\n',
]:
    text = re.sub(p, '', text)

# New pin block for standalone Wio-SX1262 board (header pins, not B2B kit)
new_block = (
    "\n"
    "#define USE_SX1262\n"
    "#define LORA_MISO        8\n"
    "#define LORA_SCK         7\n"
    "#define LORA_MOSI        9\n"
    "#define LORA_CS          5\n"
    "#define LORA_RESET       3\n"
    "#define LORA_DIO1        2\n"
    "#define SX126X_CS        LORA_CS\n"
    "#define SX126X_DIO1      LORA_DIO1\n"
    "#define SX126X_BUSY      4\n"
    "#define SX126X_RESET     LORA_RESET\n"
    "#define SX126X_DIO2_AS_RF_SWITCH\n"
    "#define SX126X_RXEN      6\n"
    "#define SX126X_TXEN      RADIOLIB_NC\n"
    "#define SX126X_DIO3_TCXO_VOLTAGE  1.8\n"
    "\n"
)

text = re.sub(r'(#endif\s*//[^\n]*$)', new_block + r'\1', text, flags=re.MULTILINE)
path.write_text(text)
print("Patched: " + str(path))
