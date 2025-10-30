# GitHub Summarizer (CLI) - DevOps Project

This is a simple Python command-line tool that uses an NLP model to summarize a GitHub issue or pull request thread.

This project was built to demonstrate a full end-to-end DevOps pipeline, including:
* **Version Control** (Git)
* **Containerization** (Docker)
* **Continuous Integration** (GitHub Actions)

## How to Run

1.  **Build the Docker image:**
    ```bash
    docker build -t summarizer .
    ```

2.  **Run the container** (pass the GitHub URL as an argument):
    ```bash
    docker run summarizer "[https://github.com/owner/repo/issues/123](https://github.com/owner/repo/issues/123)"
    ```
