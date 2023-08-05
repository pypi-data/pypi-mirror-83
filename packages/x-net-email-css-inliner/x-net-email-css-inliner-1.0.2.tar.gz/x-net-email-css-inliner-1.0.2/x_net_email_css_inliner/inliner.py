from collections import OrderedDict
from typing import Optional
import re
import requests
import tinycss2
from bs4 import (
    BeautifulSoup,
    Tag,
)

from tinycss2.ast import (
    AtRule,
    CurlyBracketsBlock,
    DimensionToken,
    HashToken,
    NumberToken,
    ParenthesesBlock,
    PercentageToken,
    QualifiedRule,
    URLToken,
)


class EmailCSSInliner:
    """Inline a external CSS to html.

    Inlining is the process of prepping an HTML email for delivery to email clients
    Some email clients strip out your email's styles unless they are written inline
    with style tags. Here's what the inliner does:

    * Inlining CSS: All of your CSS is embedded directly into the HTML as style attributes on each tag.
    * CSS inside a @media block can't be inlined, so it's put in a <style> tag.
    """

    def __init__(self, html: str, css: Optional[str] = None):
        """Prepare HTML for delivery to email clients.

        Keyword arguments:
        html -- HTML as a string
        """
        self._css = css
        self.soup = BeautifulSoup(html, "html.parser")
        self._stylesheets = self.soup.head.find_all("link", rel="stylesheet")

        for rule in self._rules:
            if isinstance(rule, AtRule) and rule.at_keyword == "media":
                selectors_list = ["@media", ]

                for token in rule.prelude:
                    if isinstance(token, ParenthesesBlock):
                        selectors_list.append(f"({self._get_declarations(token.content)})")
                    else:
                        selectors_list.append(getattr(token, "value", ""))

                selectors = "".join(selectors_list).strip()

                media_style: Tag = self.soup.new_tag("style")
                media_style.append('%s {%s}' % (selectors, self._get_declarations(rule.content, )))
                self._stylesheets[-1].insert_after(media_style)
            elif isinstance(rule, QualifiedRule):
                selectors = "".join([getattr(token, "value", "") for token in rule.prelude]).strip()

                for selectors in selectors.split(","):
                    selectors = selectors.strip().split(" ")
                    self._inline_css(selectors, self._get_declarations(rule.content))

    def __str__(self):
        """Return the minified email HTML code as string."""
        return str(self.soup)

    @property
    def _rules(self) -> list:
        """Return all styles from <link> tags as list."""
        rules: list = []

        tinycss2_options: dict = {
            "skip_comments": True,
            "skip_whitespace": True,
        }

        if self._css:
            for rule in tinycss2.parse_stylesheet(self._css, **tinycss2_options):
                rules.append(rule)
        else:
            for stylesheet in self._stylesheets:
                response: requests.Response = requests.get(stylesheet["href"], verify=False)

                if response is not None:
                    for rule in tinycss2.parse_stylesheet(response.text, **tinycss2_options):
                        rules.append(rule)

        return rules

    def _get_declarations(self, tokens: list) -> set:
        """Return processed rule declarations as string."""
        declarations: str = ""

        for token in tokens:
            if isinstance(token, HashToken):
                value = f"#{token.value}"
            elif isinstance(token, DimensionToken):
                value = f"{token.representation}{token.unit}"
            elif isinstance(token, NumberToken):
                value = f"{token.representation}"
            elif isinstance(token, PercentageToken):
                value = f"{token.value}%"
            elif isinstance(token, CurlyBracketsBlock):
                value = self._get_declarations(token.content)
            elif isinstance(token, URLToken):
                value = f"url(\"{token.value}\")"
            else:
                value = token.value

            declarations += str(value)

        return re.sub(r"\s+", " ", declarations.replace("\n", "").strip())

    def _inline_css(self, selectors: list, declarations: str, soup=None) -> None:
        """Inlining CSS to HTML tags."""
        if soup is None:
            soup = self.soup

        if not selectors:
            if soup.has_attr("style"):
                declarations = "%s%s" % (soup["style"], declarations)
                declarations = ";".join(list(OrderedDict.fromkeys(declarations.split(";"))))

            if declarations:
                if not declarations.endswith(";"):
                    declarations = f"{declarations};"

                soup["style"] = declarations

            return

        selector = selectors.pop(0)

        for tag in soup.select(selector):
            self._inline_css(selectors.copy(), declarations, tag)
