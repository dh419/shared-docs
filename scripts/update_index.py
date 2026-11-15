import os
import re
import json
import glob
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, 'docs')
HUB_DATA_PATH = os.path.join(REPO_ROOT, 'hub-data.json')


def extract_meta(html_path):
    filename = os.path.basename(html_path)
    rel_path = os.path.relpath(html_path, REPO_ROOT).replace('\\', '/')

    m_date = re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)\.html$', filename, re.IGNORECASE)
    if m_date:
        date_str = m_date.group(1)
        doc_id = f"{date_str}-{m_date.group(2)}"
        month_str = date_str[:7]
    else:
        date_str = datetime.fromtimestamp(os.path.getmtime(html_path)).strftime('%Y-%m-%d')
        doc_id = os.path.splitext(filename)[0]
        month_str = date_str[:7]

    title = doc_id
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            head = f.read(6000)
            t_m = re.search(r'<title>(.*?)</title>', head, re.IGNORECASE | re.DOTALL)
            if t_m and t_m.group(1).strip():
                title = t_m.group(1).strip()
    except Exception as e:
        print(f"Error reading {html_path}: {e}")

    return {
        "id": doc_id,
        "month": month_str,
        "date": date_str,
        "title": title,
        "path": rel_path,
    }


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    files = glob.glob(os.path.join(DOCS_DIR, '**', '*.html'), recursive=True)
    docs = [extract_meta(f) for f in files]
    docs.sort(key=lambda x: (x['date'], x['id']), reverse=True)

    with open(HUB_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    print(f"Indexed {len(docs)} documents into hub-data.json")


if __name__ == '__main__':
    main()
