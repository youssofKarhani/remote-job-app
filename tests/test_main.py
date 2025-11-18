from unittest.mock import patch
from main import fetch_jobs


def test_fetch_jobs():
    with patch("main.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"data": []}
        jobs = fetch_jobs()
        assert isinstance(jobs, list)
