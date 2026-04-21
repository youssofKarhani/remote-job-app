# GEMINI.md

## Project Overview

This project is a Python-based job fetcher named `remotejobs-cli`. Its purpose is to fetch the latest remote job listings from the Arbeitnow API and display them through two interfaces:
- **CLI (`main.py`)**: A fast and simple terminal-based interface with advanced filtering options.
- **Web App (`app.py`)**: An interactive Streamlit-based web application with data visualizations and interactive maps.

The core technologies used are:
- **Python:** The application is written in Python.
- **requests:** To make HTTP requests to the Arbeitnow API.
- **rich:** To create a visually appealing table for the CLI.
- **Streamlit:** To power the web application and its interactive features.
- **Altair & Pandas:** For data analysis and visualization.

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

**CLI Filter Options:**
- `--country`: Filter jobs by country.
- `--keywords`: Comma-separated keywords.
- `--job-type`: Filter jobs by type.

Example:
```bash
uv run python main.py --country Germany --keywords "Python"
```

**3. Running the Web Application:**

To run the Streamlit web application, execute:

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

To format the code, run:
```bash
uv run ruff format .
```

## Development Conventions

*   **Dependency Management:** Dependencies are listed in `pyproject.toml` and managed with `uv`.
*   **Code Style:** The code is formatted using `ruff` and follows standard Python conventions.
*   **API Interaction:** The application interacts with the Arbeitnow API at `https://arbeitnow.com/api/job-board-api`.
