
import board
import busio
import time

from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

class ShowReadings:

    def read_nfc(self, parent):

        pn532.SAM_configuration()  # Configure PN532 to communicate with MiFare cards
        while True:
            uid = pn532.read_passive_target(timeout=0.5)

            parent.return_read_nfc.value = None
            if uid:
                parent.return_read_nfc.value = "Jose de Almeida Lobinho"
                time.sleep(0.5)




