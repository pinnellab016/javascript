import subprocess
import os
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime, timezone, timedelta

def get_file_info(filepath):
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%s|%ad", "--date=format:%d-%m-%Y", "--", filepath],
        capture_output=True, text=True
    )
    if result.stdout:
        parts = result.stdout.split("|")
        message = parts[0].strip()
        date = parts[1].strip() if len(parts) > 1 else "N/A"
        return message, date
    return "nessun commit", "N/A"

EXCLUDE = {'.git', 'node_modules', '__pycache__', '.github', 'scripts', '.env'}
EXCLUDE_EXT = {'.pyc', '.lock', '.log'}

def build_tree(base_path, prefix=""):
    lines = []
    try:
        entries = sorted(os.scandir(base_path), key=lambda e: (not e.is_dir(), e.name))
    except PermissionError:
        return lines

    entries = [e for e in entries if e.name not in EXCLUDE and not e.name.startswith('.')]
    
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        extension = connector = connector

        if entry.is_dir():
            lines.append(f"{prefix}{connector}📁 {entry.name}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(build_tree(entry.path, new_prefix))
        else:
            ext = os.path.splitext(entry.name)[1]
            if ext in EXCLUDE_EXT:
                continue
            rel_path = os.path.relpath(entry.path)
            message, date = get_file_info(rel_path)
            lines.append(f"{prefix}{connector}📄 {entry.name}: \"{message}\" (last update: {date})")
    
    return lines

def update_readme():
    tree_lines = build_tree(".")
    tree_content = "\n".join(tree_lines)
    
    marker_start = "<!-- FILE_TREE_START -->"
    marker_end = "<!-- FILE_TREE_END -->"
    
    readme_path = "README.md"
    
    # Legge il README esistente
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# Repository\n\n"
    
    new_section = f"{marker_start}\n```\n{tree_content}\n```\n\n*Aggiornato il: {datetime.now().strftime('%d-%m-%Y')}*\n{marker_end}"
    # Sostituisce la sezione se esiste, altrimenti la appende
    if marker_start in content:
        import re
        content = re.sub(f"{marker_start}.*?{marker_end}", new_section, content, flags=re.DOTALL)
    else:
        content += f"\n\n{new_section}"
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("README.md aggiornato con successo.")

if __name__ == "__main__":
    update_readme()