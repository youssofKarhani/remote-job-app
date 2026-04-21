# remotejobs-cli

## Live Application

You can access the live web application here: [https://jobs-surfer.up.railway.app/](https://jobs-surfer.up.railway.app/)

## Project Overview

The `remotejobs-cli` project is a versatile tool for finding the latest remote job listings from the Arbeitnow API. It provides two ways to access job data: a powerful command-line interface (CLI) and an interactive web application.

The CLI is designed to be lightweight and quick to launch, making it perfect for developers who want to check for new jobs directly in their terminal. It supports advanced filtering by location, keywords, and job types.

The web application offers a more visual and user-friendly experience. It allows you to browse and explore job listings through a graphical interface, featuring real-time insights, interactive charts, and maps to help you visualize job trends.

This dual-interface approach gives you the flexibility to choose the method that best fits your workflow. The project is built with **Python** and uses **requests** for fetching data, **rich** to create beautiful CLI output, and **Streamlit** to power the feature-rich web UI.

## Technical Structure

The project is structured to separate the core logic from the user interfaces:

- **`jobs.py`**: This module is the heart of the application's data handling. It contains the logic for fetching and processing job data from the Arbeitnow API, ensuring consistency between both the CLI and web interfaces.
- **`main.py`**: The entry point for the command-line interface. It uses `jobs.py` to fetch job listings and supports several filtering options to narrow down your search.
- **`app.py`**: The entry point for the interactive web application. It uses the Streamlit framework to provide a modern, interactive interface with advanced search capabilities and data visualizations.
- **`inspect_job.py`**: A small utility script for developers to inspect the raw API response for debugging.

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

You can refine your search with the following arguments:
- `--country`: Filter jobs by country (e.g., `--country Germany`).
- `--keywords`: Comma-separated keywords to search in titles and descriptions (e.g., `--keywords "Python, React"`).
- `--job-type`: Filter jobs by type (e.g., `--job-type "internship"`).

Example:
```bash
uv run python main.py --country "United States" --keywords "Python"
```

**3. Running the Web Application:**

To run the Streamlit web application, use the following command:

```bash
uv run streamlit run app.py
```

**Web App Features:**
- **Advanced Filtering:** Filter by remote-only status, location, keywords, and job types.
- **Data Insights:** View interactive bar charts for top job categories and locations.
- **Interactive Map:** Visualize job distributions in Germany on a map.
- **Theme Support:** Choose between Light and Dark themes for your comfort.
- **Pagination:** Easily navigate through multiple pages of job listings.

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
