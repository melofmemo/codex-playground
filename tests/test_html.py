from pathlib import Path


def test_index_html_exists_and_has_text():
    html_file = Path('site_src/index.html')
    assert html_file.exists(), 'index.html should exist'
    content = html_file.read_text(encoding='utf-8')
    assert 'Tesla Stock Price' in content
