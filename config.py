
# config.py — LoRa ABP + BMP280 (I2C) configuration

COUNTRY = "EU"

DEVADDR_HEX  = "26 0B A2 AF"
NWKSKEY_HEX  = "66 0F 8B F3 53 22 3C A0 80 02 C6 5A 1D D5 53 8B"
APPSKEY_HEX  = "AB AA 90 D7 87 AC 36 31 38 06 D6 65 0E BD 0E 44"

PIN_CS_RADIO  = "D5"  # GPIO5
PIN_IRQ_RADIO = "D6"  # GPIO6 (DIO0)
PIN_RST_RADIO = "D4"  # GPIO4

UPLINK_INTERVAL = 300
FCNT_FILE = "counter.json"

def _hex_to_bytearray(s: str) -> bytearray:
    s = s.replace(" ", "").replace("-", "")
    return bytearray.fromhex(s)

DEVADDR = _hex_to_bytearray(DEVADDR_HEX)
NWKSKEY = _hex_to_bytearray(NWKSKEY_HEX)
APPSKEY = _hex_to_bytearray(APPSKEY_HEX)
