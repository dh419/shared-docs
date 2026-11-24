# Shared Docs

단독 HTML 리포트를 Google Drive에서 동기화해 GitHub Pages 허브로 게시하는 문서 허브입니다.

- **Pages**: https://dh419.github.io/shared-docs/

## 동작 흐름
1. **HTML 동기화**: `sync_shared_docs.yml`(`workflow_dispatch`) 실행 시 `scripts/sync_from_gdrive.py`가 Google Drive의 HTML 파일을 `docs/YYYY-MM/`으로 수집하며 `<meta name="robots" content="noindex, nofollow" />`를 자동 삽입합니다.
2. **인덱스 및 배포**: `scripts/update_index.py`가 `hub-data.json`과 검색 차단(`robots.txt`, `noindex`)을 갱신해 Pages로 배포합니다.

## 구성
- `.github/workflows/sync_shared_docs.yml`: 수동 동기화 및 배포 워크플로
- `scripts/sync_from_gdrive.py`: Drive HTML 수집 및 `noindex` 자동 주입
- `scripts/update_index.py`: `hub-data.json` 인덱스 및 검색 차단 자동 보정
- `docs/YYYY-MM/`: 게시된 HTML 문서
- `index.html`, `hub-data.json`, `robots.txt`: 허브 UI 및 정적 리소스
