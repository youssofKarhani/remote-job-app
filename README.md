# remotejobs-cli

## Project Overview

The `remotejobs-cli` project is a versatile tool for finding the latest remote job listings from the Arbeitnow API. It provides two ways to access job data: a fast and simple command-line interface (CLI) and an interactive web application.

The CLI is designed to be lightweight and quick to launch, making it perfect for developers who want to check for new jobs directly in their terminal. It's also ideal for automation—for example, you could run a script to see the latest job updates every time you open your computer.

The web application offers a more visual and user-friendly experience. It allows you to browse and explore job listings through a graphical interface in your web browser, making it easy to interact with the data.

This dual-interface approach gives you the flexibility to choose the method that best fits your workflow. The project is built with **Python** and uses **requests** for fetching data, **rich** to create beautiful CLI output, and **Streamlit** to power the web UI.

## Technical Structure

The project is structured to separate the core logic from the user interfaces:

- **`jobs.py`**: This module is the heart of the application's data handling. It contains the logic for fetching job data from the Arbeitnow API, ensuring that data retrieval is consistent and can be shared between both the CLI and web interfaces.
- **`main.py`**: This is the entry point for the command-line interface. It uses the functions from `jobs.py` to get job listings and presents them in a clean, readable table in the terminal.
- **`app.py`**: This is the entry point for the web application. It uses the Streamlit framework and the data from `jobs.py` to create the interactive web interface.

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
