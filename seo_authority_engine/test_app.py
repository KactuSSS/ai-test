import unittest
import json
from app import app

class AuthorityStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_generate_endpoint_success(self):
        payload = {
            "topic": "Sustainable Energy",
            "data_points": "solar efficiency, battery storage, grid integration"
        }
        response = self.app.post('/generate',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('title', data)
        self.assertIn('sections', data)
        self.assertTrue(len(data['sections']) > 0)

    def test_generate_endpoint_missing_data(self):
        payload = {"topic": "Sustainable Energy"}
        response = self.app.post('/generate',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
