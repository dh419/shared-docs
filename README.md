# Shared Docs

`agy` CLI에서 생성한 단독 HTML 리포트·분석 문서를 Google Drive(`dashboard_incoming/shared-docs`)에 업로드하고, GitHub Pages로 즉시 공유·열람할 수 있는 온디맨드(On-Demand) 문서 허브입니다.

- **GitHub Pages**: [https://dh419.github.io/shared-docs/](https://dh419.github.io/shared-docs/)

## 주요 기능
- **단독 HTML 문서 허브**: `hub-data.json` 기반 사이드바 탐색, 검색, 모바일 반응형 탑바 및 라이트/다크 테마 지원
- **검색엔진 색인 차단**: `robots.txt` (`Disallow: /`) 및 `index.html`·`docs/` 하위 전체 HTML에 `<meta name="robots" content="noindex, nofollow" />` 적용
- **자동 `noindex` 주입**: `scripts/sync_from_gdrive.py`가 Google Drive에서 HTML을 수집할 때 `<meta name="robots">` 태그가 없으면 `<head>`에 자동 삽입

## 동작 흐름 (지시 시 실행)
1. **HTML 생성**: `agy` CLI에서 단독 HTML 리포트 생성
2. **Drive 업로드**: Google Drive `dashboard_incoming/shared-docs` (`1IW8ytiDhiZknLmrkffisi1uZ8i1S6xed`) 폴더에 `YYYY-MM-DD-<slug>.html` 업로드
3. **GitHub 동기화**: `sync_shared_docs.yml` (`workflow_dispatch`)이 `scripts/sync_from_gdrive.py`로 HTML을 `docs/YYYY-MM/`에 수집(`noindex` 자동 보강)하고, `scripts/update_index.py`로 `hub-data.json` 인덱스 갱신 후 Pages 배포

## 디렉터리 구조
- `.github/workflows/sync_shared_docs.yml`: 수동(`workflow_dispatch`) Drive 동기화 및 Pages 배포 워크플로
- `scripts/sync_from_gdrive.py`: `dashboard_incoming/shared-docs` 내 HTML 파일 수집 및 `noindex` 메타 태그 자동 주입
- `scripts/update_index.py`: `docs/` 하위 HTML 제목·날짜 파싱 및 `hub-data.json` 생성
- `index.html`, `hub-data.json`: 공유 문서 검색·열람용 허브 페이지 및 인덱스 데이터
- `docs/YYYY-MM/`: 게시된 단독 HTML 문서들
- `robots.txt`: 검색엔진 크롤링 차단 설정
