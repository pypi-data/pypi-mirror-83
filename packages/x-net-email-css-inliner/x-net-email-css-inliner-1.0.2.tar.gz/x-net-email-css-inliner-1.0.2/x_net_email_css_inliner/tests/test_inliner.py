from typing import TextIO

from bs4 import BeautifulSoup

from x_net_email_css_inliner import EmailCSSInliner


raw_html_file: TextIO = open("x_net_email_css_inliner/tests/html/example.html", "r")
raw_html: str = raw_html_file.read()

css_file: TextIO = open("x_net_email_css_inliner/tests/html/example.css", "r")
css: str = css_file.read()

raw_html_file.close()
css_file.close()

html = str(EmailCSSInliner(html=raw_html, css=css))
soup = BeautifulSoup(html, "html.parser")


def test_existing_inline_css():
    """Test if inline css exists on HTML tags."""
    assert soup.find("body").has_attr("style") is True, "<body> has no inline style"
    assert soup.find("table").has_attr("style") is True, "<table> has no inline style"
    assert soup.find("tr").has_attr("style") is True, "<tr> has no inline style"
    assert soup.find("td").has_attr("style") is True, "<td> has no inline style"
    assert soup.find("h1").has_attr("style") is True, "<h1> has no inline style"
    assert soup.find("p").has_attr("style") is True, "<p> has no inline style"
    assert soup.select("table.body")[0].has_attr("style") is True, "<table class=\"body\"> has no inline style"
    assert soup.select("table.container")[0].has_attr("style") is True, "<table class=\"container\"> has no inline style"
    assert soup.select(".content")[0].has_attr("style") is True, "<table class=\"content\"> has no inline style"


def test_existing_media_query():
    """Test if <style> and media query exists."""
    assert str(soup.find("style")).startswith("<style>@media") is True, "No <style> with a media_query found"
