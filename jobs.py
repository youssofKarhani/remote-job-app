import requests
from rich.console import Console
from rich.table import Table

API_URL = "https://arbeitnow.com/api/job-board-api"
console = Console()


def fetch_jobs(page=1):
    """Fetch jobs from the Arbeitnow API for a specific page."""
    response = requests.get(API_URL, params={"page": page})
    response.raise_for_status()
    return response.json().get("data", [])


def show_jobs(jobs, limit=10, country=None, keywords=None, job_type=None):
    title = f"Top {limit} Remote Jobs"
    if country:
        title += f" in {country.title()}"
    if keywords:
        title += f" with keywords: {', '.join(keywords)}"
    if job_type:
        title += f" for {job_type.title()}"
    table = Table(title=title, show_lines=True)
    table.add_column("Company", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Location", style="magenta")
    table.add_column("URL", style="yellow", overflow="fold")

    for job in jobs[:limit]:
        table.add_row(
            job.get("company_name", "N/A"),
            job.get("title", "N/A"),
            job.get("location", "N/A"),
            job.get("url", ""),
        )
    console.print(table)
