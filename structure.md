my-agent-site/
├─ data/                  # 원시 데이터 또는 결과물
│
├─ scripts/               # ⬅︎ 주요 코드
│   ├─ py/                #   └─ Python
│   │    └─ make_report.py
│   └─ js/                #   └─ Node/TS (선택)
│        └─ build_chart.mjs
│
├─ site_src/              # MkDocs · Astro · Next.js 등 정적 사이트 소스
│    └─ index.md
│
├─ requirements.txt       # Python 잠금 파일
├─ package.json           # Node 의존성(선택)
├─ .github/
│   └─ workflows/
│        build.yml        # GitHub Pages CI/CD
└─ AGENTS.md              # Codex에게 주는 “작업 가이드”
