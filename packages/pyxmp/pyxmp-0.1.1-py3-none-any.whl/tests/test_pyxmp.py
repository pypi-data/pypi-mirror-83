import unittest
from io import BytesIO
from PIL import Image

from pyxmp import pyxmp


class TestXmpReadWrite(unittest.TestCase):
    def setUp(self):
        file = BytesIO()
        image = Image.new('RGB', size=(50, 50), color=(0, 0, 0))
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        self.image = file.read()
        self.metadata = [
            {
                "provider": "InfoSnapshot",
                "name": "Brand",
                "value": "My Service"
            },
            {
                "provider": "InfoSnapshot",
                "name": "Current GPS Accuracy",
                "value": "14.589"
            },
            {
                "provider": "InfoSnapshot",
                "name": "Current GPS Latitude",
                "value": "25.045234"
            },
            {
                "provider": "InfoSnapshot",
                "name": "Current GPS Longitude",
                "value": "121.530795"
            },
            {
                "provider": "InfoSnapshot",
                "name": "Current GPS Timestamp",
                "value": "2020-09-15T13:50:25.143Z"
            },
            {
                "provider":"InfoSnapshot",
                "name":"Timestamp",
                "value":"2020-09-15T13:50:30.203Z"
            }
        ]


    def test_read_empty(self):
        xmp_metadata = pyxmp.read(self.image)
        self.assertEqual(xmp_metadata, {})

    def test_inject_read(self):
        image = pyxmp.inject(self.image, self.metadata, 'http://numbersprotocol.io/xmp/', 'examplePrefix')
        xmp_metadata = pyxmp.read(image)
        xmp_metadata_assert_target = {
            'Xmp.examplePrefix.infoSnapshot.brand': 'My Service',
            'Xmp.examplePrefix.infoSnapshot.currentGPSAccuracy': '14.589',
            'Xmp.examplePrefix.infoSnapshot.currentGPSLatitude': '25.045234',
            'Xmp.examplePrefix.infoSnapshot.currentGPSLongitude': '121.530795',
            'Xmp.examplePrefix.infoSnapshot.currentGPSTimestamp': '2020-09-15T13:50:25.143Z',
            'Xmp.examplePrefix.infoSnapshot.timestamp': '2020-09-15T13:50:30.203Z'
        }
        self.assertEqual(xmp_metadata, xmp_metadata_assert_target)


if __name__ == '__main__':
    unittest.main()