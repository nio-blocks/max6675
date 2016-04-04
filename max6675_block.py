from nio.block.base import Block
from nio.properties.int import IntProperty
from nio.util.discovery import discoverable


try:
    import spidev
except:
    # Let the block code load anyway so that som unit tests can run.
    pass


@discoverable
class MAX6675(Block):

    bus = IntProperty(default=0, title="Bus")
    client = IntProperty(default=0, title="Client")

    def configure(self, context):
        super().configure(context)
        self._spi = spidev.SpiDev(self.bus(), self.client())

    def process_signals(self, signals):
        try:
            value = 0.0
        except:
            self.logger.error(
                "Error reading MAX6675 from (bus, client}: ({}, {})".format(
                    self.bus(), self.client()))
            return

        for signal in signals:
            setattr(signal, 'temperature', value)

        self.notify_signals(signals)
