# dj-services

[![Build Status](https://travis-ci.com/artemowkin/dj-services.svg?branch=main)](https://travis-ci.com/artemowkin/dj-services)
[![Coverage Status](https://coveralls.io/repos/github/artemowkin/dj-services/badge.svg?branch=main)](https://coveralls.io/github/artemowkin/dj-services?branch=main)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Documentation Status](https://readthedocs.org/projects/numpydoc/badge/?version=latest)](https://numpydoc.readthedocs.io/en/latest/?badge=latest)

Thanks to this library, you can build your business logic in beautiful
services, not in huge views and fat models.

## Summary

  - [Getting Started](#getting-started)
  - [Runing the tests](#running-the-tests)
  - [Contributing](#contributing)
  - [Versioning](#versioning)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Getting Started

Install this library using `pip`

```
$ pip install dj-services
```

Create `services.py` module in your Django app and create your first service

```python
# services.py
from djservices import CRUDService

from .models import MyModel
from .forms import MyForm


class MyService(CRUDService):
    model = MyModel
    form = MyForm
```

After that you can use this service in `views.py`

```python
# views.py
from django.shortcuts import render

from .services import MyService


def list_entries(request):
    service = MyService()
    entries = service.get_all()
    return render(request, 'some_template.html', {'entries': entries})
```

That's all. Now you can add business logic in your service. Let's go!

## Running the tests

If you want to run the tests you need to run the following command:

```
$ ./manage.py test tests.base
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/PurpleBooth/a-good-readme-template/tags).

## Authors

  - **Artyom Loskan** - [artemowkin](https://github.com/artemowkin)

See also the list of
[contributors](https://github.com/artemowkin/dj-services/contributors)
who participated in this project.

## License

This project is licensed under the
[GNU General Public License v3.0](LICENSE)

