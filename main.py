import argparse

from rich.console import Console

from jobs import fetch_jobs, show_jobs

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Fetch remote jobs from Arbeitnow API."
    )
    parser.add_argument(
        "--country",
        type=str,
        help="Filter jobs by country.",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Comma-separated keywords to filter job titles and descriptions.",
    )
    parser.add_argument(
        "--job-type",
        type=str,
        help="Filter jobs by type (e.g., 'student', 'internship').",
    )
    args = parser.parse_args()

    console.print("[bold blue]Fetching latest remote jobs...[/bold blue]")
    jobs = fetch_jobs()

    if args.country:
        jobs = [
            job
            for job in jobs
            if args.country.lower() in job.get("location", "").lower()
        ]

    if args.keywords:
        keywords_list = [k.strip().lower() for k in args.keywords.split(",")]
        jobs = [
            job
            for job in jobs
            if any(
                k in job.get("title", "").lower()
                or k in job.get("description", "").lower()
                for k in keywords_list
            )
        ]

    if args.job_type:
        job_type_lower = args.job_type.lower()
        jobs = [
            job
            for job in jobs
            if job_type_lower in job.get("title", "").lower()
            or job_type_lower in job.get("description", "").lower()
        ]

    show_jobs(
        jobs,
        country=args.country,
        keywords=args.keywords.split(",") if args.keywords else None,
        job_type=args.job_type,
    )


if __name__ == "__main__":
    main()
