import unittest
from indalsig.utils import get_address_from_coords, get_address_from_text


class TestMainFunctions(unittest.TestCase):

    def test_get_address_from_coords(self):

        address = get_address_from_coords("37.423021", "-122.083739")

        self.assertEqual(address.formatted_address, "1500 Amphitheatre Pkwy, Mountain View, CA 94043, USA")

    def test_get_address_from_text(self):

        address = get_address_from_text("1500 Amphitheatre Pkwy, Mountain View, CA 94043, USA")

        self.assertEqual(address.formatted_address, "1500 Amphitheatre Pkwy, Mountain View, CA 94043, USA")

