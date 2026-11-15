# Shared Docs

`agy` CLI에서 생성한 단독 HTML 리포트·분석 문서를 Google Drive(`dashboard_incoming/shared-docs`)에 업로드하고, GitHub Pages로 즉시 공유·열람할 수 있는 온디맨드(On-Demand) 문서 허브입니다.

- **GitHub Pages**: [https://dh419.github.io/shared-docs/](https://dh419.github.io/shared-docs/)

## 동작 흐름 (지시 시 실행)
1. **HTML 생성**: `agy` CLI에서 단독 HTML 리포트 생성
2. **Drive 업로드**: Google Drive `dashboard_incoming/shared-docs` (`1IW8ytiDhiZknLmrkffisi1uZ8i1S6xed`) 폴더에 `YYYY-MM-DD-<slug>.html` 업로드
3. **GitHub 동기화**: `sync_shared_docs.yml` (`workflow_dispatch`)이 `scripts/sync_from_gdrive.py`로 HTML을 `docs/YYYY-MM/`에 수집하고, `scripts/update_index.py`로 `hub-data.json` 인덱스 갱신 후 Pages 배포

## 디렉터리 구조
- `scripts/sync_from_gdrive.py`: `dashboard_incoming/shared-docs` 내 HTML 파일 수집
- `scripts/update_index.py`: `docs/` 하위 HTML 제목·날짜 파싱 및 `hub-data.json` 생성
- `index.html`: 공유 문서 검색·열람용 허브 페이지
- `docs/YYYY-MM/`: 게시된 단독 HTML 문서들
