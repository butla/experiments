import tests.common
from txodds_code_test import url_extractor


def test_scrape_urls():
    urls_to_find = ['http://example.com/1', 'https://other-site-example.com/',
                    'http://example.com/2']
    html = tests.common.HTML_WITH_EMPTY_BODY.format("""
    <p>This is just some text</p>
    <a href="http://example.com/1">Here's a link</a>
    <a href="https://other-site-example.com/">Here's a link</a>
    <div>
      <a href="/2">Here's different a link</a>
    </div>""")
    base_url = 'http://example.com'
    assert url_extractor._scrape_urls(html, base_url) == urls_to_find


def test_scrape_malformed_url():
    html = tests.common.HTML_WITH_EMPTY_BODY.format(
        "<a>I don't have a href even though I should.</a>")
    dummy_base_url = ''
    assert url_extractor._scrape_urls(html, dummy_base_url) == []
