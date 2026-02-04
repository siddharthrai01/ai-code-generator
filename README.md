# AI-Assisted Python Code Generation (Codex Web UI)

This repository demonstrates how to use Codex Web UI to generate, refine, and structure
production-ready Python code for common data engineering and automation tasks.

All code is generated or iteratively improved using Codex prompts, with a focus on:
- Code quality
- Reusability
- Readability

## What’s Inside

- Python scripts for data cleaning, transformation, and file format conversion
- Prompt examples used in Codex Web UI
- Example input/output files
- Refactored versions of AI-generated code

## How Codex Is Used

Codex Web UI is used as an AI coding assistant to:
- Generate initial Python implementations
- Refactor code for performance and readability
- Remove hardcoded values
- Add docstrings and structure

All prompts used are documented in the `prompts/` directory.

## Example Codex Prompt

You are a senior Python developer.

Write clean, production-ready Python code to:
- Read a CSV file
- Remove duplicates based on a key
- Handle missing values
- Save the output as a Parquet file

Output only Python code.

## Project Structure

ai-data-assistant/
├── src/
├── prompts/
├── examples/
└── README.md

## License

This project is licensed under the MIT License.
