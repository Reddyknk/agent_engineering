import unittest
from app import app, TALKS, SPEAKERS, CONFERENCE_INFO

class GCPConferenceWebsiteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_talk_count(self):
        """Requirement 2: The 1-day event is a list of 10 talks in total."""
        self.assertEqual(len(TALKS), 10, "Conference must have exactly 10 talks.")

    def test_talk_speakers_limit(self):
        """Requirement 3: Each talk has 1 or 2 max speakers."""
        for talk in TALKS:
            num_speakers = len(talk["speaker_ids"])
            self.assertGreaterEqual(num_speakers, 1, f"Talk ID {talk['id']} must have at least 1 speaker.")
            self.assertLessEqual(num_speakers, 2, f"Talk ID {talk['id']} has {num_speakers} speakers, exceeding max of 2.")

    def test_talk_fields(self):
        """Requirement 4: Talk has ID, Title, Speakers, Category (1 or 2), Description and time."""
        required_fields = ["id", "title", "categories", "description", "time", "speaker_ids"]
        for talk in TALKS:
            for field in required_fields:
                self.assertIn(field, talk, f"Talk ID {talk.get('id')} missing required field '{field}'")
            
            # Check categories count (1 or 2 max)
            self.assertGreaterEqual(len(talk["categories"]), 1, f"Talk ID {talk['id']} must have at least 1 category.")
            self.assertLessEqual(len(talk["categories"]), 2, f"Talk ID {talk['id']} has more than 2 categories.")

    def test_speaker_fields(self):
        """Requirement 5: Each speaker has First Name, Last Name and LinkedIn url."""
        required_fields = ["first_name", "last_name", "linkedin"]
        for spk_id, speaker in SPEAKERS.items():
            for field in required_fields:
                self.assertIn(field, speaker, f"Speaker '{spk_id}' missing field '{field}'")
                self.assertTrue(speaker[field], f"Speaker '{spk_id}' field '{field}' should not be empty")
            self.assertTrue(speaker["linkedin"].startswith("https://www.linkedin.com/in/"), 
                            f"Speaker '{spk_id}' LinkedIn URL must be valid format.")

    def test_lunch_break_60_minutes(self):
        """Requirement 7: Give a lunch break of 60 minutes."""
        lunch = CONFERENCE_INFO.get("lunch_break")
        self.assertIsNotNone(lunch, "Lunch break must be defined.")
        self.assertEqual(lunch.get("duration_minutes"), 60, "Lunch break must be exactly 60 minutes.")

    def test_index_route(self):
        """Requirement 1: Home page loads successfully."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GCP Tech Summit", response.data)
        self.assertIn(b"Google Cloud Technical Conference", response.data)

    def test_api_talks_all(self):
        """Requirement 6: API returns all 10 talks and lunch break info."""
        response = self.client.get("/api/talks")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 10)
        self.assertEqual(len(data["talks"]), 10)
        self.assertIn("lunch_break", data)
        self.assertEqual(data["lunch_break"]["duration_minutes"], 60)

    def test_api_talks_search_by_category(self):
        """Requirement 6: Allow users to search by category."""
        response = self.client.get("/api/talks?category=AI+%26+Machine+Learning")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["total"], 0)
        for talk in data["talks"]:
            self.assertTrue(any("AI & Machine Learning" in cat for cat in talk["categories"]))

    def test_api_talks_search_by_speaker(self):
        """Requirement 6: Allow users to search by speaker."""
        response = self.client.get("/api/talks?speaker=Sundar")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["total"], 0)
        for talk in data["talks"]:
            self.assertTrue(any("Sundar" in spk["first_name"] for spk in talk["speakers"]))

    def test_api_talks_search_by_title(self):
        """Requirement 6: Allow users to search by title."""
        response = self.client.get("/api/talks?q=Kubernetes")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 1)
        self.assertIn("Kubernetes", data["talks"][0]["title"])

if __name__ == "__main__":
    unittest.main()
