from jobs import fetch_jobs

jobs = fetch_jobs()
if jobs:
    print(f"URL: {jobs[0].get('url')}")
    print(f"Data: {jobs[0]}")
else:
    print("No jobs found")
