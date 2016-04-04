import sys
from unittest.mock import MagicMock, patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal


# Mock spidev so tests run even when it's not installed
spidev = MagicMock()
sys.modules["spidev"] = spidev
from ..max6675_block import MAX6675


class TestMAX6675(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        spidev.reset_mock()

    def test_spi_connection(self):
        """Assert that SPI connection is created and destroyed."""
        blk = MAX6675()
        self.assertTrue(blk._spi is None)
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        spidev.SpiDev.assert_called_once_with(0, 0)
        self.assertTrue(blk._spi is not None)
        blk._spi.close.assert_called_once_with()

    def test_spi_configuration_properties(self):
        """Assert that SPI connection is configured by block properties."""
        blk = MAX6675()
        self.assertTrue(blk._spi is None)
        self.configure_block(blk, {"bus": 1, "client": 1})
        blk.start()
        blk.stop()
        spidev.SpiDev.assert_called_once_with(1, 1)
        self.assertTrue(blk._spi is not None)
        blk._spi.close.assert_called_once_with()

    def test_thermocouple_read(self):
        """Assert that 'temperature' is appended on to notified signal."""
        blk = MAX6675()
        self.configure_block(blk, {})
        blk._spi = MagicMock()
        blk._spi.readbytes.return_value = b"\x01\x01"
        blk.start()
        blk.process_signals([Signal({"i'm a": "signal"})])
        blk.stop()
        blk._spi.readbytes.assert_called_once_with(2)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].__dict__,
            {"i'm a": "signal", "temperature": 8.0}
        )

    def test_failed_thermocouple_read(self):
        """Failed spi read should log an error and not notify a signal."""
        blk = MAX6675()
        self.configure_block(blk, {})
        blk._spi = MagicMock()
        blk._spi.readbytes.side_effect = Exception
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(0)
        self.assertEqual(len(self.last_notified[DEFAULT_TERMINAL]), 0)
