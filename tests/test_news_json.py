import json
from pathlib import Path


def test_news_json_structure():
    path = Path('data/news_parsed.json')
    assert path.exists(), 'data/news_parsed.json should exist'

    data = json.loads(path.read_text(encoding='utf-8'))
    assert isinstance(data, list), 'JSON should contain a list'
    assert len(data) >= 10, 'Expected at least 10 news items'

    for idx, item in enumerate(data):
        assert isinstance(item, dict), f'Item {idx} should be a dict'
        for key in ('date', 'src', 'headline'):
            assert key in item, f'Item {idx} missing key: {key}'
