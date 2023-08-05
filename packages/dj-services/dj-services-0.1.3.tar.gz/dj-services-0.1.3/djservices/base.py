"""This module includes base services classes

Notes
-----
To use services you need to create `services.py` module in your app and
create `BaseService` subclasses in it. Services must have `model` attribute
and `strategy_class` if it's not setted in service class

"""

from __future__ import annotations
from typing import Any

from django.db.models import QuerySet, Model
from django.forms import Form

from .strategies import SimpleCRUDStrategy


class BaseService:

    """Base services class

    Attributes
    ----------
    strategy_class : |BaseStrategy subclass|
        A BaseStrategy subclass with service functionality
    model : |Model|
        A model using in service logic
    strategy : |BaseStrategy instance|
        A BaseStrategy instance created in constructor using
        `strategy_class`

    Examples
    --------
    To use this service you need to subclass it and set `model`
    and `strategy_class` attributes, and add some methods:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...
    ...     def do_something(self):
    ...         return self.strategy.do_something()
    ...

    If arguments other than `model` must be passed to the constructor
    of your strategy you can add them to the `_get_strategy_args()` method:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...     another_attribute = Something
    ...
    ...     def _get_strategy_args(self):
    ...         args = (self.another_attribute,)
    ...         return super()._get_strategy_args() + args
    ...

    """

    strategy_class = None
    model = None

    def __init__(self) -> None:
        if not all((self.strategy_class, self.model)):
            raise AttributeError(
                "You need to set `strategy_class` and `model` attributes"
            )

        self.strategy = self.strategy_class(*self._get_strategy_args())

    def _get_strategy_args(self) -> tuple:
        """Returns tuple with arguments for strategy constructor

        Returns
        -------
        Tuple with `model` attribute value. It's default behavior

        """
        return (self.model,)


class CRUDService(BaseService):

    """Service with CRUD functionality

    Attributes
    ----------
    form : |Form|
        A form using in service logic basically for validating data
    strategy_class : |SimpleCRUDStrategy|
        Default strategy with CRUD functionality

    Methods
    -------
    get_all(*args, **kwargs)
        This method returns all model entries
    get_concrete(*args, **kwargs)
        This method returns a concrete model entry
    create(*args, **kwargs)
        This method creates a new model entry
    change(*args, **kwargs)
        This method changes a model entry
    delete(*args, **kwargs)
        This method deletes a model entry
    get_create_form(*args, **kwargs)
        This method returns form for creating a new model entry
    get_change_form(*args, **kwargs)
        This method returns form with entry data for changing that entry

    Examples
    --------
    To use this services you need to subclass it and set `model` and `form`
    attributes:

    >>> class MyService(CRUDService):
    ...     model = MyModel
    ...     form = MyModelForm
    ...

    After that you can use this service in Django views. For example,
    you can make Django's ListView analog:

    >>> def list_view(request):
    ...     service = MyService()
    ...     entries = service.get_all()
    ...     return render(request, 'entries.html', {'entries': entries})
    ...

    """

    strategy_class = SimpleCRUDStrategy
    form = None

    def __init__(self) -> None:
        if not self.form:
            raise AttributeError("You need to set `form` attribute")

        super().__init__()

    def _get_strategy_args(self) -> tuple:
        """Returns tuple with default attributes and `form` because `form`
        attribute is necessary for CRUD strategies
        """
        args = (self.form,)
        return super()._get_strategy_args() + args

    def get_all(self, *args, **kwargs) -> QuerySet:
        """Returns all model entries calling `get_all` strategy method"""
        return self.strategy.get_all(*args, **kwargs)

    def get_concrete(self, *args, **kwargs) -> Model:
        """Returns a concrete model entry calling `get_concrete`
        strategy method
        """
        return self.strategy.get_concrete(*args, **kwargs)

    def create(self, *args, **kwargs) -> Any[Model, Form]:
        """Creates a new model entry calling `create` strategy method"""
        return self.strategy.create(*args, **kwargs)

    def change(self, *args, **kwargs) -> Any[Model, Form]:
        """Changes a concrete model entry calling `change`
        strategy method
        """
        return self.strategy.change(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """Deletes a concrete model entry calling `delete`
        strategy method
        """
        return self.strategy.delete(*args, **kwargs)

    def get_create_form(self, *args, **kwargs) -> Form:
        """Returns form for creating a new model entry calling
        `get_create_form` strategy method
        """
        return self.strategy.get_create_form(*args, **kwargs)

    def get_change_form(self, *args, **kwargs) -> Form:
        """Returns form with entry data for changing that entry
        calling `get_change_form` strategy method
        """
        return self.strategy.get_change_form(*args, **kwargs)
