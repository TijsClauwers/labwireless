
# bmp280_test.py — quick sanity check for BMP280 over I2C
import time, board, busio
import adafruit_bmp280

i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp.sea_level_pressure = 1013.25

print("Reading BMP280 (Ctrl+C to stop)")
while True:
    print(f"Temp: {bmp.temperature:.2f} °C | Pressure: {bmp.pressure:.2f} hPa")
    time.sleep(1.0)
