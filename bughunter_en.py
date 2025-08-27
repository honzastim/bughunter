import os
import sys
import requests
import json

def get_api_key():
    return input("Enter your Grok API key: ")

def analyze_code_with_grok(api_key, code, filename):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"Find bugs in this Python code from the file '{filename}':\n```python\n{code}\n```\nRespond in English and in a structured way, e.g. - Bug: description\n"
    data = {
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": "You are an expert in finding bugs in Python code."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1024
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error calling API for file {filename}: {e}")
        return "Error during analysis."

def fix_code_with_grok(api_key, code, bugs, filename):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"Fix the bugs in this Python code from file '{filename}' based on these found bugs:\n{bugs}\nOriginal code:\n```python\n{code}\n```\nReturn the fixed code in a ```python block."
    data = {
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": "You are an expert in fixing bugs in Python code."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 2048
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        fixed_code = result['choices'][0]['message']['content']
        if "```python" in fixed_code:
            fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
        return fixed_code
    except requests.exceptions.RequestException as e:
        print(f"Error calling API for fixing file {filename}: {e}")
        return None

def main():
    api_key = get_api_key()
    print("Initialization successful. Starting bug analysis in Python files in the current directory.")

    current_dir = os.getcwd()
    bugs_content = "# Found bugs\n\n"

    python_files = [f for f in os.listdir(current_dir) if f.endswith('.py') and f != 'bughunter_en.py']

    if not python_files:
        print("No Python files found in the current directory.")
        sys.exit(0)

    for filename in python_files:
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        bugs = analyze_code_with_grok(api_key, code, filename)
        bugs_content += f"## File: {filename}\n\n{bugs}\n\n---\n\n"

    with open('bugs.md', 'w', encoding='utf-8') as bugs_file:
        bugs_file.write(bugs_content)

    print("Bugs have been found and saved to bugs.md.")

    while True:
        choice = input("Do you want to fix the bugs? Choose:\n1. Yes, fix them.\n2. No, don't fix.\n3. Exit program.\nYour choice: ")
        if choice == '3':
            print("Exiting program.")
            sys.exit(0)
        elif choice == '2':
            print("Not fixing bugs. Program ends.")
            sys.exit(0)
        elif choice == '1':
            print("Starting to fix bugs.")
            for filename in python_files:
                with open(filename, 'r', encoding='utf-8') as file:
                    code = file.read()
                with open('bugs.md', 'r', encoding='utf-8') as bugs_file:
                    bugs_data = bugs_file.read()
                    start = bugs_data.find(f"## File: {filename}")
                    if start != -1:
                        end = bugs_data.find("---", start)
                        bugs = bugs_data[start:end].strip()
                    else:
                        bugs = ""
                fixed_code = fix_code_with_grok(api_key, code, bugs, filename)
                if fixed_code:
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(fixed_code)
                    print(f"File {filename} has been fixed.")
                else:
                    print(f"Failed to fix file: {filename}")
            print("Fixing completed.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
