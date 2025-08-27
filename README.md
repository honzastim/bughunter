# BugHunter

BugHunter is a Python script designed to analyze Python code files in a specified directory, detect errors using the xAI Grok API, and optionally fix them. It generates a `bugs.md` file listing all detected issues and allows users to overwrite the original files with corrected versions.

## Features

- **Error Detection**: Scans all `.py` files in the current directory (excluding `bughunter.py`) and identifies errors using the xAI Grok API.
- **Error Reporting**: Saves detailed error descriptions in a structured `bugs.md` file.
- **Code Correction**: Offers to automatically fix detected errors and overwrite the original files with corrected code.
- **Interactive Interface**: Prompts the user for an xAI API key and provides options to fix errors, skip fixes, or exit the program.

## Prerequisites

- Python 3.6 or higher
- An active [xAI API key](https://x.ai/api)
- Required Python packages: `requests`

Install the required package using:
```bash
pip install requests
```

## Usage

1. Place `bughunter.py` in the directory containing the Python files you want to analyze.
2. Run the script in a terminal:
   ```bash
   python bughunter.py
   ```
3. Enter your xAI API key when prompted.
4. The script will:
   - Analyze all `.py` files in the current directory.
   - Generate a `bugs.md` file with a detailed list of errors.
   - Prompt you to choose an action:
     - **1. Yes, fix**: Overwrites the original files with corrected code.
     - **2. No, do not fix**: Exits without modifying files.
     - **3. Exit program**: Terminates the script.
5. Review the `bugs.md` file for error details and check the modified files if fixes were applied.

## Notes

- The script assumes the xAI API is compatible with an OpenAI-style endpoint (`https://api.x.ai/v1/chat/completions`) and uses Bearer authentication. Refer to the [xAI API documentation](https://x.ai/api) for details.
- Only `.py` files in the current directory are analyzed (no recursive directory scanning).
- Ensure you have a valid xAI API key. For more information, visit [xAI API](https://x.ai/api).
- The script overwrites original files when fixing errors, so back up your code before running the fix option.

## Contributing

Feel free to fork this repository, submit issues, or create pull requests to improve BugHunter. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [xAI's Grok](https://x.ai/grok), which outperformed other models in creating this tool.
- Built with simplicity and usability in mind for developers looking to automate code quality checks.
