import unittest
import numpy as np
import cv2
import sys
sys.path.append('../')
from video_transformer import VidoeTransformer

class TestVideoTransformer(unittest.TestCase):
    def setUp(self):
        self.video_transformer = VidoeTransformer()

if __name__ == '__main__':
    unittest.main()
def test_transform_point_outside_polygon(self):
    # Create a point that is outside the polygon
    outside_point = [-100, -100]
    
    # Call the transform_point method
    result = self.video_transformer.transform_point(outside_point)
    
    # Assert that the result is None
    self.assertIsNone(result)