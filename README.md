# remotejobs-cli

## Project Overview

This project is a Python command-line interface (CLI) and a web application for fetching the latest remote job listings from the Arbeitnow API.

The core technologies used are:
- **Python:** The application is written in Python.
- **requests:** To make HTTP requests to the Arbeitnow API.
- **rich:** To create a visually appealing table for displaying the job data in the terminal.
- **streamlit:** To create a simple web interface for displaying jobs.

The application has two entry points:
- `main.py`: The CLI for fetching and displaying jobs in the console.
- `app.py`: The Streamlit web application.

## Development

This project uses `uv` for dependency management and running tasks.

**1. Install Dependencies:**

To install the project and its development dependencies, run the following command from the root of the project:

```bash
uv pip install .[dev]
```

**2. Running the CLI Application:**

To run the CLI and see the latest remote jobs, execute the following command:

```bash
uv run python main.py
```

**3. Running the Web Application:**

To run the Streamlit web application, use the following command:

```bash
uv run streamlit run app.py
```

**4. Running Tests:**

To run the test suite, use the following command:

```bash
uv run pytest
```

**5. Linting and Formatting:**

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
