from pathlib import Path


def test_price_chart_exists():
    img_path = Path('site_src/assets/price_sma.png')
    assert img_path.exists(), 'price_sma.png should exist'
    assert img_path.stat().st_size >= 10 * 1024, 'image should be at least 10 KB'
