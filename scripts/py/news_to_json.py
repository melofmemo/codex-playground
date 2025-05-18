import json
import re
from pathlib import Path

NEWS_MD = Path('data/news.md')
OUTPUT_JSON = Path('data/news_parsed.json')


def parse_news(lines):
    items = []
    current_date = None
    i = 0
    year = 2025
    # attempt to detect year from reference links
    for line in reversed(lines):
        m_year = re.search(r'(20\d{2})-\d{2}-\d{2}', line)
        if m_year:
            year = int(m_year.group(1))
            break
    while i < len(lines):
        line = lines[i].rstrip('\n')
        stripped = line.strip()
        m_date = re.match(r'^##\s*(\d+)\s*월\s*(\d+)\s*일', stripped)
        if m_date:
            month = int(m_date.group(1))
            day = int(m_date.group(2))
            current_date = f"{year}-{month:02d}-{day:02d}"
            i += 1
            continue
        if stripped.startswith('###'):
            headline = stripped.lstrip('#').strip()
            i += 1
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            bullet_lines = []
            while i < len(lines):
                next_line = lines[i].rstrip('\n')
                if next_line.strip() == '':
                    if bullet_lines:
                        i += 1
                        break
                    i += 1
                    continue
                if next_line.startswith('##') or next_line.startswith('###') or next_line.startswith('---'):
                    break
                if next_line.lstrip().startswith('*'):
                    bullet_lines.append(next_line.strip())
                    i += 1
                    while i < len(lines):
                        cont = lines[i].rstrip('\n')
                        if cont.startswith('##') or cont.startswith('###') or cont.startswith('---'):
                            break
                        if cont.lstrip().startswith('*'):
                            break
                        bullet_lines.append(cont.strip())
                        i += 1
                    break
                else:
                    i += 1
            bullet_text = ' '.join(bullet_lines)
            m_src = re.search(r'\(\[([^\]]+)\]\[[0-9]+\]\)', bullet_text)
            if m_src and current_date:
                src = m_src.group(1).strip()
                items.append({'date': current_date, 'src': src, 'headline': headline})
            continue
        i += 1
    return items


def main():
    lines = NEWS_MD.read_text(encoding='utf-8').splitlines()
    items = parse_news(lines)
    items_sorted = sorted(items, key=lambda x: x['date'], reverse=True)[:10]
    OUTPUT_JSON.write_text(json.dumps(items_sorted, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
