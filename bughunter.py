import os
import sys
import requests
import json

def get_api_key():
    return input("Zadejte API klíč od Grok: ")

def analyze_code_with_grok(api_key, code, filename):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"Najdi chyby v tomto Python kódu ze souboru '{filename}':\n```python\n{code}\n```\nOdpovídej v češtině a strukturovaně, např. - Chyba: popis\n"
    data = {
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": "Jsi expert na hledání chyb v Python kódu."},
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
        print(f"Chyba při volání API pro soubor {filename}: {e}")
        return "Chyba při analýze."

def fix_code_with_grok(api_key, code, bugs, filename):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"Oprav chyby v tomto Python kódu ze souboru '{filename}' na základě těchto nalezených chyb:\n{bugs}\nPůvodní kód:\n```python\n{code}\n```\nVrát opravený kód v bloku ```python\nopravný kód\n```"
    data = {
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": "Jsi expert na opravu chyb v Python kódu."},
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
        print(f"Chyba při volání API pro opravu souboru {filename}: {e}")
        return None

def main():
    api_key = get_api_key()
    print("Inicializace úspěšná. Začínám analýzu chyb v Python souborech v aktuální složce.")

    current_dir = os.getcwd()
    bugs_content = "# Nalezené chyby\n\n"

    python_files = [f for f in os.listdir(current_dir) if f.endswith('.py') and f != 'bughunter.py']

    if not python_files:
        print("Žádné Python soubory nalezeny v aktuální složce.")
        sys.exit(0)

    for filename in python_files:
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        bugs = analyze_code_with_grok(api_key, code, filename)
        bugs_content += f"## Soubor: {filename}\n\n{bugs}\n\n---\n\n"

    with open('bugs.md', 'w', encoding='utf-8') as bugs_file:
        bugs_file.write(bugs_content)

    print("Chyby byly nalezeny a uloženy do souboru bugs.md.")

    while True:
        choice = input("Chcete chyby opravit? Vyberte:\n1. Ano, opravit.\n2. Ne, neopravovat.\n3. Vypnout program.\nVaše volba: ")
        if choice == '3':
            print("Vypínám program.")
            sys.exit(0)
        elif choice == '2':
            print("Neopravuji chyby. Program končí.")
            sys.exit(0)
        elif choice == '1':
            print("Začínám opravu chyb.")
            for filename in python_files:
                with open(filename, 'r', encoding='utf-8') as file:
                    code = file.read()
                with open('bugs.md', 'r', encoding='utf-8') as bugs_file:
                    bugs_data = bugs_file.read()
                    start = bugs_data.find(f"## Soubor: {filename}")
                    if start != -1:
                        end = bugs_data.find("---", start)
                        bugs = bugs_data[start:end].strip()
                    else:
                        bugs = ""
                fixed_code = fix_code_with_grok(api_key, code, bugs, filename)
                if fixed_code:
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(fixed_code)
                    print(f"Soubor {filename} byl opraven.")
                else:
                    print(f"Nepodařilo se opravit soubor: {filename}")
            print("Oprava dokončena.")
            break
        else:
            print("Neplatná volba. Zkuste znovu.")

if __name__ == "__main__":
    main()
