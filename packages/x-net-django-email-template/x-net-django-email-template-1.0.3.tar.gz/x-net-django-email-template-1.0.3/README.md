# X-Net Django Email Template

This is the default email template that we use in our [company](https://www.x-net.at) for sending emails with django (registration, password forgot, eg.)

## Installation

1. pip install `x_net_django_email_template`
2. Add `x_net_django_email_template` to INSTALLED_APPS

## Usage

When extends the default.html you can overwrite the blocks:

```html
{% extends "email/default.html" %}

{% load html_email i18n %}

{% block title %}Title{% endblock %}
{% block header_title %}Header title{% endblock %}

{% block main %}
  <p>This is an example of text.</p>

  <table role="presentation">
      <tr>
      <td class="button-wrapper">
        <table class="button" role="presentation">
          <tr>
            <td>
              <a href="#">Click me</a>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
{% endblock %}

{% block footer %}
  <p><small>{% trans "This is an automatically generated email, please do not reply to this message." %}</small></p>
{% endblock %}
````

### Templatetags

With the `full_static` template tag you can insert absolute urls in the email template.

```html
{% load html_email %}
<link rel="stylesheet" href="{% full_static "css/email/html-email.min.css" %}" />
```

## Compatibility

You can inline css to this HTML template with the [X-Net Email Inliner](https://github.com/x-net-services/x-net-email-css-inliner).
We have test this HTML template with the following email client:

* Apple Mail 13
* Outlook 2007
* Outlook 2010
* Outlook 2013
* Outlook 2013 with 120 DPI
* Outlook 2016 (macOS)
* Outlook 2016
* Outlook 2016 with 120 DPI
* Outlook 2019
* Outlook 2019 with 120 DPI
* Outlook Office 365
* Thunderbird
* Gmail App
* Samsung Mail
* Mail/iOS
* Outlook Android
* Outlook iOS
* Office 365 (Browser)
* Gmail (Browser)
* GMX.de (Browser)
