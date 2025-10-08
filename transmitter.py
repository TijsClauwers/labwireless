
# transmitter.py — LoRa uplink: BMP280 (I2C) temperature + pressure
import time, struct, json, os
import board, busio, digitalio
import adafruit_bmp280
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import config

def load_counter(path):
    try:
        with open(path, "r") as f: return int(json.load(f))
    except Exception:
        return 0

def save_counter(path, value):
    with open(path, "w") as f: json.dump(int(value), f)

i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp.sea_level_pressure = 1013.25

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs_radio  = digitalio.DigitalInOut(getattr(board, config.PIN_CS_RADIO))
irq_radio = digitalio.DigitalInOut(getattr(board, config.PIN_IRQ_RADIO))
rst_radio = digitalio.DigitalInOut(getattr(board, config.PIN_RST_RADIO))

ttn = TTN(config.DEVADDR, config.NWKSKEY, config.APPSKEY, country=config.COUNTRY)
lora = TinyLoRa(spi, cs_radio, irq_radio, rst_radio, ttn)

lora.frame_counter = load_counter(config.FCNT_FILE)

print("LoRa transmitter (BMP280) ready. Interval:", config.UPLINK_INTERVAL, "s")

while True:
    try:
        temperature_c = bmp.temperature
        pressure_hpa  = bmp.pressure

        temp_int = int(temperature_c * 100)     # signed int16
        pres_int = int(round(pressure_hpa))     # uint16

        payload = struct.pack(">hH", temp_int, pres_int)

        print(f"Uplink #{lora.frame_counter} | Temp={temperature_c:.2f} °C  Press={pressure_hpa:.2f} hPa | payload={payload.hex()}")

        lora.send_data(payload, len(payload), lora.frame_counter)
        lora.frame_counter += 1
        save_counter(config.FCNT_FILE, lora.frame_counter)

    except Exception as e:
        print("Send error:", e)

    time.sleep(config.UPLINK_INTERVAL)
