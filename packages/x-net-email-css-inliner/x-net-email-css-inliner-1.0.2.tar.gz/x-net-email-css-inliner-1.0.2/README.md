# X-Net Email CSS Inliner

The *X-Net Email CSS Inliner* is a HTML email inliner inspired by the
[ZURB CSS inliner](https://get.foundation/emails/inliner.html).

Inlining is the process of prepping an HTML email for delivery to email clients
Some email clients strip out your email's styles unless they are written inline
with style tags. Here's what the inliner does:

* *Inlining CSS:* All of your CSS is embedded directly into the HTML as style attributes on each tag.
* CSS inside a *@media* block can't be inlined, so it's put in a `<style>` tag.

You can use our great [X-Net Django Email Template](https://github.com/x-net-services/x-net-django-email-template)
with the *X-Net Email CSS Inliner*

## Installation

```
pip install x_net_email_css_inliner
```

## Example

```
from x_net_email_css_inliner import EmailCSSInliner

raw_html = "<html>...</html>"  # HTML email template
html_with_inline_css = str(EmailCSSInliner(raw_html))
```
