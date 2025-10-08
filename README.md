
# LoRa Lab — BMP280 (I2C) + RFM95W (EU868) → TTN → ThingSpeak

## Wiring
**BMP280 (I2C)**
- VIN → 3.3V
- GND → GND
- SCL → GPIO3 (Pin 5)
- SDA → GPIO2 (Pin 3)

**RFM95W**
- VCC → 3.3V
- GND → GND
- SCK → GPIO11
- MOSI → GPIO10
- MISO → GPIO9
- NSS/CS → GPIO5
- DIO0/IRQ → GPIO6
- RST → GPIO4
- ANT → antenna attached

## Setup (once)
sudo apt-get update
sudo apt-get install -y python3-venv i2c-tools libgpiod-dev python3-libgpiod
sudo raspi-config   # enable I2C & SPI
# If needed: add 'dtoverlay=spi0-0cs' to /boot/firmware/config.txt (or /boot/config.txt) and reboot

## Python env
cd ~/lora-lab
python3 -m venv blinka-env --system-site-packages
source blinka-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

## Test sensor
python bmp280_test.py

## Run transmitter
python transmitter.py

## TTN Uplink Decoder
function Decoder(bytes, port) {
  if (bytes.length < 4) return { error: "payload too short" };
  var tempInt = (bytes[0] << 8) | (bytes[1] & 0xFF);
  if (tempInt & 0x8000) tempInt = tempInt - 0x10000; // two's complement
  var presInt = (bytes[2] << 8) | (bytes[3] & 0xFF);
  var temperature = tempInt / 100.0; // °C
  var pressure = presInt;            // hPa
  return { field1: temperature, field2: pressure };
}
