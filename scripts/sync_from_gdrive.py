import os
import io
import re
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, 'docs')
FOLDER_ID = '1IW8ytiDhiZknLmrkffisi1uZ8i1S6xed'  # dashboard_incoming/shared-docs
KST = timezone(timedelta(hours=9))
ROBOTS_META_TAG = '<meta name="robots" content="noindex, nofollow" />'


def ensure_noindex_meta(html_bytes: bytes) -> bytes:
    """Inject noindex, nofollow meta tag into HTML <head> if not already present."""
    try:
        text = html_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return html_bytes

    if re.search(r'<meta\s+name=["\']robots["\']', text, re.IGNORECASE):
        return html_bytes

    if re.search(r'<head[^>]*>', text, re.IGNORECASE):
        updated = re.sub(
            r'(<head[^>]*>)',
            rf'\1\n  {ROBOTS_META_TAG}',
            text,
            count=1,
            flags=re.IGNORECASE,
        )
        return updated.encode('utf-8')

    return html_bytes


def resolve_month_dir(filename, modified_time_str):
    m = re.match(r'^(\d{4}-\d{2})-\d{2}-', filename)
    if m:
        return m.group(1)
    if modified_time_str:
        try:
            dt = datetime.fromisoformat(modified_time_str.replace('Z', '+00:00')).astimezone(KST)
            return dt.strftime('%Y-%m')
        except Exception:
            pass
    return datetime.now(KST).strftime('%Y-%m')


def main():
    sa_json = os.environ.get('GDRIVE_SA_KEY')
    if not sa_json:
        raise ValueError("GDRIVE_SA_KEY environment variable is missing.")

    creds = service_account.Credentials.from_service_account_info(
        json.loads(sa_json),
        scopes=['https://www.googleapis.com/auth/drive.readonly'],
    )
    service = build('drive', 'v3', credentials=creds)

    res = service.files().list(
        q=f"'{FOLDER_ID}' in parents and (mimeType = 'text/html' or name contains '.html') and trashed = false",
        orderBy='modifiedTime desc',
        pageSize=50,
        fields='files(id, name, modifiedTime)',
    ).execute()
    files = res.get('files', [])
    if not files:
        print("No HTML files found in dashboard_incoming/shared-docs.")
        return

    for f in files:
        name = f['name']
        if not name.lower().endswith('.html'):
            continue
        month_part = resolve_month_dir(name, f.get('modifiedTime', ''))
        out_dir = os.path.join(DOCS_DIR, month_part)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, name)

        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, service.files().get_media(fileId=f['id']))
        done = False
        while not done:
            _, done = downloader.next_chunk()

        with open(out_path, 'wb') as out_f:
            out_f.write(ensure_noindex_meta(buf.getvalue()))
        print(f"Synced: {out_path}")


if __name__ == '__main__':
    main()
