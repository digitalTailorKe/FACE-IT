import unittest
from io import BytesIO
from app import create_app

class FaceRecognitionTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = create_app()
        self.client = self.app.test_client()

        # Set up paths for test images
        self.known_image_path = 'known_images/austin.jpeg'
        self.compared_image_path = 'compared_images/obama.jpg'

    def test_compare_faces(self):
        # Open the images in binary mode
        with open(self.known_image_path, 'rb') as known_image, open(self.compared_image_path, 'rb') as compared_image:
            known_image_data = BytesIO(known_image.read())
            compared_image_data = BytesIO(compared_image.read())

            # Make a POST request to the /compare endpoint
            response = self.client.post('/compare', data={
                'known_image': (known_image_data, 'austin.jpeg'),
                'compared_image': (compared_image_data, 'obama.jpg')
            })

            # Assert the response status code and data
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('match', data)
            self.assertIn('distance', data)
            self.assertIsInstance(data['match'], bool)
            self.assertIsInstance(data['distance'], float)

    def test_missing_files(self):
        # Make a POST request without images
        response = self.client.post('/compare')
        
        # Assert the response status code and error message
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Missing image files')

if __name__ == '__main__':
    unittest.main()
