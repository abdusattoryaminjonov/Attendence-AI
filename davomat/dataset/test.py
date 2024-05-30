import json

def model():
    filename = r'C:\Users\Pbl4\pbl4\davomat\dataset\model.ipynb'
    
    try:
        with open(filename, encoding='utf-8') as fp:
            nb = json.load(fp)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the notebook file.")
        return
    except UnicodeDecodeError as e:
        print(f"Error: Unicode decode error: {e}")
        return
    
    try:
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = ''.join(line for line in cell.get('source', []) if not line.startswith('%'))
                exec(source, globals(), locals())
    except Exception as e:
        print(f"Error while executing code from notebook: {e}")

if __name__ == "__main__":
    model()
