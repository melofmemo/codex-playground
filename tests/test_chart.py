import os


def test_price_chart_exists_and_large():
    path = os.path.join('site_src', 'assets', 'price_sma.png')
    assert os.path.exists(path), 'Chart image not found'
    size_kb = os.path.getsize(path) / 1024
    assert size_kb >= 10, f'Chart image too small: {size_kb:.2f} KB'
