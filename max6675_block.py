from threading import Lock
from nio.block.base import Block
from nio.properties import IntProperty, VersionProperty


try:
    import spidev
except:
    # Let the block code load anyway so that som unit tests can run.
    pass


class MAX6675(Block):

    bus = IntProperty(default=0, title="Bus")
    client = IntProperty(default=0, title="Client")
    version = VersionProperty('0.0.1')

    def __init__(self):
        super().__init__()
        self._spi = None
        self._spi_lock = Lock()

    def configure(self, context):
        super().configure(context)
        with self._spi_lock:
            self._spi = spidev.SpiDev(self.bus(), self.client())

    def stop(self):
        try:
            with self._spi_lock:
                self._spi.close()
        except:
            self.logger.warning("Error when closing SPI connection")
        super().stop()

    def process_signals(self, signals):
        try:
            with self._spi_lock:
                bytes_read = self._spi.readbytes(2)
                self.logger.debug("Read bytes over SPI: {}".format(bytes_read))
            temperature = ((bytes_read[0] << 8 | bytes_read[1]) >> 3) * 0.25
        except:
            self.logger.exception(
                "Error reading MAX6675 from (bus, client): ({}, {})".format(
                    self.bus(), self.client()))
            return

        for signal in signals:
            setattr(signal, 'temperature', temperature)

        self.notify_signals(signals)
