import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 7629

# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb, lsb])

# Repeatedly switch a MCP4151 digital pot off then on
while True:
    # write_pot(0x1FF)
    # time.sleep(0.5)
    # write_pot(0x00)
    # print(spi.readbytes(2))
    time.sleep(0.5)
    received_data = spi.xfer([0x01])
    print(received_data)
    received_data = spi.xfer([0x02])
    print(received_data)
    received_data = spi.xfer([0x03])
    print(received_data)
    received_data = spi.xfer([0x04])
    print(received_data)

    