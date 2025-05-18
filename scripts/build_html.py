from pathlib import Path
import json

SITE_SRC = Path('site_src')
ASSETS_DIR = SITE_SRC / 'assets'

NEWS_JSON = Path('data/news_parsed.json')
OUTPUT_HTML = SITE_SRC / 'index.html'


def load_news(max_items=10):
    if not NEWS_JSON.exists():
        return []
    try:
        data = json.loads(NEWS_JSON.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []

    if isinstance(data, dict):
        # try known keys
        items = data.get('articles') or data.get('news') or []
    else:
        items = data

    news_list = []
    for item in items[:max_items]:
        if isinstance(item, dict):
            title = item.get('title') or item.get('headline') or str(item)
        else:
            title = str(item)
        news_list.append(title)
    return news_list


def build_html():
    news_items = load_news()

    html_parts = [
        '<html>',
        '  <head>',
        '    <meta charset="utf-8">',
        '    <title>Tesla Stock Report</title>',
        '  </head>',
        '  <body>',
        '    <h1>Tesla Stock Price</h1>',
        '    <img src="assets/price_sma.png" alt="Stock chart">',
        '    <h2>Latest News</h2>',
        '    <ul>',
    ]

    for item in news_items:
        html_parts.append(f'      <li>{item}</li>')

    html_parts.extend([
        '    </ul>',
        '  </body>',
        '</html>',
    ])

    OUTPUT_HTML.write_text('\n'.join(html_parts), encoding='utf-8')


if __name__ == '__main__':
    build_html()
