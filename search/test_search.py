from django.test import TestCase
from django.urls import reverse


class SearchAndExportTestCase(TestCase):
    def setUp(self):
        # Setting up both the search and export URLs for use in the test
        self.search_url = reverse('search')
        self.export_url = reverse('export_csv')

    def test_search_and_export_csv(self):
        # Defining a test search query for both searching and exporting
        query = 'Test Search'

        # Simulating a POST request to search with the given query
        response = self.client.post(self.search_url, {'query': query})

        # Verifying that the response status code is 200 OK, indicating successful request
        self.assertEqual(response.status_code, 200)

        # Verifying that the search results have been stored in the session
        session_results = self.client.session.get('search_results', [])
        # Ensuring that the session contains at least one search result
        self.assertGreater(len(session_results), 0)

        # Performing a POST request to export the results to CSV
        response = self.client.post(self.export_url, {'query': query})

        # Verifying that the CSV export request returns a successful response (200 OK)
        self.assertEqual(response.status_code, 200)

        # Decoding the response content to read the CSV data (assuming UTF-8 encoding)
        csv_content = response.content.decode('utf-8')

        # Verifying that the CSV contains the appropriate headers
        self.assertIn('Title', csv_content)
        self.assertIn('Link', csv_content)
        self.assertIn('Description', csv_content)

        # Verifying that the data in the CSV matches the results stored in the session
        for result in session_results:
            self.assertIn(result['title'], csv_content)