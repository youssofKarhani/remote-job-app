# GEMINI.md

## Project Overview

This project is a Python command-line interface (CLI) application named `remotejobs-cli`. Its purpose is to fetch the latest remote job listings from the Arbeitnow API and display them in a well-formatted table in the console.

The core technologies used are:
- **Python:** The application is written in Python.
- **requests:** To make HTTP requests to the Arbeitnow API.
- **rich:** To create a visually appealing table for displaying the job data in the terminal.

The application's entry point is `main.py`, which fetches the jobs and prints them to the console.

## Development



This project uses `uv` for dependency management and running tasks.



**1. Install Dependencies:**



To install the project and its development dependencies, run the following command from the root of the project:



```bash

uv pip install .[dev]

```



**2. Running the Application:**



To run the application and see the latest remote jobs, execute the following command:



```bash

uv run python main.py

```



**3. Running Tests:**



To run the test suite, use the following command:



```bash

uv run pytest

```



**4. Linting and Formatting:**



This project uses `ruff` for linting and formatting.



To check for linting errors, run:



```bash

uv run ruff check .

```



To automatically fix linting errors, run:



```bash

uv run ruff check --fix .

```



To format the code, run:



```bash

uv run ruff format .

```



## Development Conventions



*   **Dependency Management:** Dependencies are listed in the `pyproject.toml` file and managed with `uv`.

*   **Code Style:** The code is formatted using `ruff` and follows standard Python conventions.

*   **API Interaction:** The application interacts with the Arbeitnow API at `https://arbeitnow.com/api/job-board-api`.
