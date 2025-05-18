자동 리포트 생성 파이프라인

## 사용 방법
1. 가상 환경을 활성화합니다.
   ```bash
   source .venv/bin/activate
   ```
2. 뉴스 데이터를 JSON 형식으로 변환합니다.
   ```bash
   python scripts/news_to_json.py
   ```
3. 이후 다른 빌드 스텝(`python scripts/make_charts.py`, `python scripts/build_html.py` 등)을 실행합니다.
