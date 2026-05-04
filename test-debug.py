import subprocess, os

def get_file_info(filepath):
    result = subprocess.run(
        ['git', 'log', '-1', '--pretty=format:%s|%ad', '--date=short', '--', filepath],
        capture_output=True, text=True
    )
    if result.stdout:
        parts = result.stdout.split('|')
        return parts[0].strip(), parts[1].strip()
    return 'nessun commit', 'N/A'

EXCLUDE = {'.git', 'node_modules', '__pycache__', '.github', '.scripts', '.env'}

def build_tree(base_path, prefix=''):
    lines = []
    try:
        entries = sorted(os.scandir(base_path), key=lambda e: (not e.is_dir(), e.name))
    except PermissionError:
        return lines
    entries = [e for e in entries if e.name not in EXCLUDE and not e.name.startswith('.')]
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = '└── ' if is_last else '├── '
        if entry.is_dir():
            lines.append(f'{prefix}{connector}📁 {entry.name}/')
            new_prefix = prefix + ('    ' if is_last else '│   ')
            lines.extend(build_tree(entry.path, new_prefix))
        else:
            rel_path = os.path.relpath(entry.path)
            message, date = get_file_info(rel_path)
            lines.append(f'{prefix}{connector}📄 {entry.name}: "{message}" (last update: {date})')
    return lines

tree = build_tree('.')
print(f'TREE LINES: {len(tree)}')
for l in tree:
    print(l)