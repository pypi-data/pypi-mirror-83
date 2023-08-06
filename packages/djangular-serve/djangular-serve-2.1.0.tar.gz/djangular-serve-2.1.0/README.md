<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

![PyPI](https://img.shields.io/pypi/v/djangular-serve)
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/forafekt/djangular-serve">
    <img src="https://github.com/forafekt/quick-assets/blob/master/images/djangular_serve.jpg?raw=true" 
    alt="Logo" width="90" height="100">
  </a>

  <h3 align="center">DJANGULAR SERVE</h3>
  <p align="center">
    Djangular-Serve is a tool to fluidly connect Django and Angular.  
    It will serve the entire Angular project through one base template and url of your Django project as a single 
    progressive web application. It will also take care of Angular RouterLinks & Django urls/paths as well as serving 
    all the static files directly to your template. It includes built-in meta, service worker & more. All fully 
    customizable as you will see in the example.
    <br />
    <a href="https://github.com/forafekt/djangular-serve/tree/master/djangular_serve/docs">
    <strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/forafekt/djangular-serve/tree/master/example">View Demo</a>
    ·
    <a href="https://github.com/forafekt/djangular-serve/issues">Report Bugs</a>
    ·
    <a href="https://github.com/forafekt/djangular-serve/issues">Request Feature</a>
  </p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Commands](#commands)
* [PWA Usage](#pwa-usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/forafekt/djangular-serve)


### Built With

* [Python 3]()
* [Django]()
* [Angular 2]()



<!-- GETTING STARTED -->
## Getting Started

To start using Djangular-Serve, continue with the following instructions...

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm & Angular
```sh
See https://nodejs.org for installing NODEJS/NPM on your machine correctly
```
Once installed run:
```sh
npm install -g @angular/cli
```

### Installation

1 . Install djangular-serve

```sh
pip install djangular-serve or pip3 install djangular-serve
```
2 . Add to Django INSTALLED_APPS

```sh
'djangular_serve'
```
3 . Add urls

```sh
urlpatterns = [
    ...
    path('', include('djangular_serve.urls'),
    or
    url(r'^', include('djangular_serve.urls'),
]
```

4 . In your settings.py file add and edit the following settings:
#### Set your relevant paths to allow djangular-serve to find templates and static
#### This is one way.  Do it in whatever way it works for you.
#### Build paths inside the project like this: APP_DIR / 'subdir'.
```sh
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent  # Absolute root path
APP_DIR = Path(__file__).resolve(strict=True).parent  # 'example' project
URL = os.path.relpath(APP_DIR / "static")  # example/static
ANGULAR_DIR = os.path.join(BASE_DIR / ".")  # root/ngservetest <- Your Angular project
```

#
#### Tell Django to look for Static files and templates.
#### In debug it is possible to have a different static location for local dev if preferred.
#### Again, set this to whatever way works best for your project.

```sh
if DEBUG:
    DJANGO_TEMPLATE_DIRS = (
        os.path.join(APP_DIR, 'templates'),
    )

    STATICFILES_DIRS = (
        os.path.join(APP_DIR, 'static_files'),
    )
else:  # Change later for production if needed.
    DJANGO_TEMPLATE_DIRS = (
        os.path.join(APP_DIR, 'templates'),
    )

    STATICFILES_DIRS = (
        os.path.join(APP_DIR, 'static_files'),
    )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': DJANGO_TEMPLATE_DIRS,
        ...
        ...
    },
]
```

<!-- COMMAND EXAMPLES -->
## Commands
```sh
# Build Angular application to Django static
serve -s ng

# Move relevant static files to respective directories
serve -mv js, css, img or all

# Make a new directory in your static root
serve -mk <any-dir>
```

<!-- PWA USAGE EXAMPLES -->
## PWA Usage

#### The settings below are what will automatically distribute your app to your chosen path
# 
```sh
""" 
Serve CDN or static css files to your template. 
"""
STYLESHEETS = [
    {
        'src': 'example/static/ng_css/styles.css'
    },
    # OR
    #    {
    #        'src': '{}/styles.css'.format(URL)
    #    },
]

""" 
Serve CDN or static js files to your template. 
"""
JAVASCRIPT = [
    {
        'src': 'example/static/ng_js/main.js'
    },
    {
        'src': 'example/static/ng_js/polyfills.js'
    },
    {
        'src': 'example/static/ng_js/runtime.js'
    },
]

""" 
Serve CDN or static fonts files to your template. 
"""
FONTS = [
    {
        'src': 'https://fonts.googleapis.com/icon?family=Material+Icons'
    },
]
# Path to get service-worker
SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'example/templates', 'sw.js')

# Gets name of service worker to automatically register .e.g 'sw.js'
# This will tell manifest and url to get this specific file and serve.
SERVICE_WORKER_NAME = os.path.basename(SERVICE_WORKER_PATH)

APP_NAME = 'Djangular Serve'
APP_DESCRIPTION = "Build Angular into Django static"
APP_THEME_COLOR = '#000000'
APP_BACKGROUND_COLOR = '#ffffff'
APP_DISPLAY = 'standalone'
APP_SCOPE = '/'
APP_ORIENTATION = 'any'
APP_START_URL = '/'
APP_STATUS_BAR_COLOR = 'default'
APP_DIR = '.'
APP_LANG = LANGUAGE_CODE
APP_ICONS = [
    {
        'src': '/static/images/logo_icons.png',
        'sizes': '160x160'
    }
]
APP_ICONS_APPLE = [
    {
        'src': '/static/images/apple_icons.png',
        'sizes': '160x160'
    }
]
APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
```
### Here is an example on setting up your `_index.html` template.
```
<!doctype html>
{% load static %}
{% load serve_tags %}
{% load i18n %}
{% get_current_language as LANGUAGE_CODE %}
{% get_current_language_bidi as LANGUAGE_BIDI %}
<html lang="{{ LANGUAGE_CODE|default:'en' }}" {% if LANGUAGE_BIDI %}dir="rtl"{% endif %}>
<head>
  <meta charset="utf-8">
  <title>{% block title %}{% endblock title %}</title>
  <base href="/">

  {% block head %}{% manifest_meta %}{% endblock head %}
  <!-- [if lt IE 9]>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.min.js"
          type="text/javascript"></script>
  <![endif] -->

  {% serve_fonts %}
  {% serve_css %}
</head>

<body class="mat-typography">
{% block body %}


<app-root>{% block content%}{% endblock content %}</app-root>


  <!-- JS -->
  {% serve_js %}
  {% block js %}{% endblock js %}

<!-- [if lte IE 9]>
<script src="https://cdnjs.cloudflare.com/ajax/libs/placeholders/3.0.2/placeholders.min.js"></script>
<![endif] -->
{% endblock body %}
</body>
</html>
```

_For more examples, please refer to the 
[Documentation](https://github.com/forafekt/djangular-serve/tree/master/djangular_serve/docs)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/forafekt/djangular-serve/issues) 
for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` in djangular_serve/docs for more information.



<!-- CONTACT -->
## Contact
LinkedIn:  https://linkedin.com/in/jonnydoyle 
<br>
Project Link: [https://github.com/forafekt/djangular-serve](https://github.com/forafekt/djangular-serve)



<!-- ACKNOWLEDGEMENTS 
## Acknowledgements

* []()
* []()
* []()
-->




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/forafekt/djangular-serve.svg?style=flat-square
[contributors-url]: https://github.com/forafekt/djangular-serve/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/forafekt/djangular-serve.svg?style=flat-square
[forks-url]: https://github.com/forafekt/djangular-serve/network/members
[stars-shield]: https://img.shields.io/github/stars/forafekt/djangular-serve.svg?style=flat-square
[stars-url]: https://github.com/forafekt/djangular-serve/stargazers
[issues-shield]: https://img.shields.io/github/issues/forafekt/djangular-serve.svg?style=flat-square
[issues-url]: https://github.com/forafekt/djangular-serve/issues
[license-shield]: https://img.shields.io/github/license/forafekt/djangular-serve.svg?style=flat-square
[license-url]: https://github.com/forafekt/djangular-serve/blob/master/djangular_serve/docs/license/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/jonnydoyle
[product-screenshot]: https://github.com/forafekt/quick-assets/blob/master/images/djangular_serve.jpg?raw=true