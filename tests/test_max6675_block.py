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

    def test_thermocouple_read(self):
        """Assert that 'temperature' is appended on to notified signal."""
        blk = MAX6675()
        self.configure_block(blk, {'com_select': 1})
        blk.start()
        blk.process_signals([Signal({"i'm a": "signal"})])
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].__dict__,
            {"i'm a": "signal", "temperature": 0.0}
        )
