# BugHunter

BugHunter is a Python script that analyzes Python code files in the current directory, detects errors using the xAI Grok API, and optionally fixes them while respecting the project's intended functionality as described in the `README.md` file. It generates a `bugs.md` file listing all detected issues and overwrites the original files with corrected versions upon user confirmation.

## Features

- **Error Detection**: Scans all `.py` files in the current directory (excluding `bughunter_en.py`) and identifies errors using the xAI Grok API.
- **Documentation-Aware Fixes**: Reads the `README.md` file (if available) to ensure fixes align with the project's intended functionality.
- **Error Reporting**: Saves detailed error descriptions in a structured `bugs.md` file in English.
- **Code Correction**: Automatically overwrites original files with fixed code, preserving the functionality outlined in the `README.md`.
- **Interactive Interface**: Prompts the user for an xAI API key and provides options to fix errors, skip fixes, or exit the program.

## Prerequisites

- Python 3.6 or higher
- An active [xAI API key](https://x.ai/api)
- Required Python package: `requests`

Install the required package using:
```bash
pip install requests
```

## Usage

1. Place `bughunter_en.py` in the directory containing the Python files you want to analyze.
2. Ensure a `README.md` file is present in the same directory if you want fixes to respect project documentation.
3. Run the script in a terminal:
   ```bash
   python bughunter_en.py
   ```
4. Enter your xAI API key when prompted.
5. The script will:
   - Analyze all `.py` files in the current directory.
   - Generate a `bugs.md` file with a detailed list of errors.
   - Prompt you to choose an action:
     - **1. Yes, fix**: Overwrites original files with corrected code, considering `README.md` for context.
     - **2. No, do not fix**: Exits without modifying files.
     - **3. Exit program**: Terminates the script.
6. Review the `bugs.md` file for error details and check the modified files if fixes were applied.

## Notes

- The script assumes the xAI API is compatible with an OpenAI-style endpoint (`https://api.x.ai/v1/chat/completions`) and uses Bearer authentication. Refer to the [xAI API documentation](https://x.ai/api) for details.
- Only `.py` files in the current directory are analyzed (no recursive directory scanning).
- The script reads the `README.md` file to ensure fixes align with the project's intended functionality. If no `README.md` is found, it proceeds with fixes based solely on the code and detected errors.
- Original files are overwritten when fixing errors, so back up your code before running the fix option.
- For xAI API details, visit [xAI API](https://x.ai/api).

## Contributing

Feel free to fork this repository, submit issues, or create pull requests to improve BugHunter. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [xAI's Grok](https://x.ai/grok), which excels in code analysis and correction.
- Designed for developers seeking to automate code quality checks while respecting project documentation.
