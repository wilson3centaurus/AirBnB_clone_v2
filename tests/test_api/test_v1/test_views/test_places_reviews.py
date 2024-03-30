import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


class TestReviewAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)
        self.client = self.app.test_client()
        self.place = Place(name="Mos Eisley Cantina", description="A wretched hive of scum and villainy")
        self.review = Review(text="Great spot!", place_id=self.place.id)

    def tearDown(self):
        storage.delete(self.place)
        storage.save()

    def test_get_all_reviews(self):
        """ Create place and reviews """
        storage.new(self.place)
        for _ in range(3):
            review = Review(text="Nice place!", place_id=self.place.id)
            storage.new(review)
        storage.save()

        # Test GET request
        response = self.client.get(f'/api/v1/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 3)

    def test_get_review(self):
        """ Create place and review """
        storage.new(self.place)
        storage.new(self.review)
        storage.save()

        # Test GET request
        response = self.client.get(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['text'], "Great spot!")

    def test_delete_review(self):
        """ Create place and review """
        storage.new(self.place)
        storage.new(self.review)
        storage.save()

        # Test DELETE request
        response = self.client.delete(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        # Make sure the review is deleted
        review = storage.get(Review, self.review.id)
        self.assertIsNone(review)

    def test_create_review(self):
        """ Create place """
        storage.new(self.place)
        storage.save()

        # Test POST request
        new_review_data = {'text': 'Amazing place!'}
        response = self.client.post(f'/api/v1/places/{self.place.id}/reviews', json=new_review_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['text'], 'Amazing place!')

        # Make sure the review is created
        review = storage.get(Review, data['id'])
        self.assertIsNotNone(review)

    def test_update_review(self):
        """ Create place and review """
        storage.new(self.place)
        storage.new(self.review)
        storage.save()

        # Test PUT request
        updated_review_data = {'text': 'Decent spot!'}
        response = self.client.put(f'/api/v1/reviews/{self.review.id}', json=updated_review_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['text'], 'Decent spot!')

        # Make sure the review is updated
        review = storage.get(Review, self.review.id)
        self.assertEqual(review.text, 'Decent spot!')


if __name__ == '__main__':
    unittest.main()
