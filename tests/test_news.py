import json
from pathlib import Path


def test_news_json_top_10():
    path = Path('data/news_parsed.json')
    assert path.exists(), 'data/news_parsed.json should exist'

    data = json.loads(path.read_text(encoding='utf-8'))
    assert isinstance(data, list)
    assert len(data) == 10, 'Expected exactly 10 news items'

    for idx, item in enumerate(data):
        assert 'date' in item, f'Missing date in item {idx}'
        assert 'src' in item, f'Missing src in item {idx}'
        assert 'headline' in item, f'Missing headline in item {idx}'
