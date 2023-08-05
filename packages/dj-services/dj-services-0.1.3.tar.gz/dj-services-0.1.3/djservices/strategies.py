"""This module includes base services strategies

Notes
-----
Each strategy must be a subclass of `BaseStrategy` class. Each strategy
has a `model` attribute to work with database. Strategies using in
services in `strategy` attribute

"""

from __future__ import annotations
from typing import Any

from django.db.models import Model, QuerySet
from django.forms import Form
from django.shortcuts import get_object_or_404


class BaseStrategy:

    """Base class for strategies

    Attributes
    ----------
    model : |Model|
        Model strategy works with. It's for working with DB

    Examples
    --------
    Strategies must be used in services. All you need is to create
    your strategy subclassing `BaseStrategy` and add it in `strategy_class`
    service attribute:

    >>> class MyStrategy(BaseStrategy):
    ...
    ...     def get_all(self):
    ...         return self.model.objects.all()
    ...
    ...
    ... class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...
    ...     def get_all(self):
    ...         return self.strategy.get_all()

    """

    def __init__(self, model: Model) -> None:
        self.model = model


class SimpleCRUDStrategy(BaseStrategy):

    """Simple strategy with CRUD functionality

    Attributes
    ----------
    form : |Form|
        Form strategy works with

    """

    def __init__(self, model: Model, form: Form) -> None:
        super().__init__(model)
        self.form = form

    def get_all(self) -> QuerySet:
        """Returns all model entries"""
        return self.model.objects.all()

    def get_concrete(self, pk: Any) -> Model:
        """Returns a concrete model entry

        Parameters
        ----------
        pk : |Any|
            Primary key of the entry

        """
        return get_object_or_404(self.model, pk=pk)

    def create(self, data: dict) -> Any[Form, Model]:
        """Creates a new model entry from `data`

        Parameters
        ----------
        data : |dict|
            Data from request.POST validating in form

        Returns
        -------
        If data is correct, creates an entry and returns it.
        Else returns invalid form

        """
        form = self.form(data)
        if form.is_valid():
            entry = self.model.objects.create(**form.cleaned_data)
            return entry

        return form

    def _change_entry_fields(self, data: dict, entry: Model) -> None:
        """Changes `entry` fields using `data`"""
        for field in data:
            setattr(entry, field, data[field])

    def change(self, data: dict, pk: Any) -> Any[Form, Model]:
        """Change a model entry with `pk` from `data`

        Parameters
        ----------
        data : |dict|
            Data from request.POST validating in form
        pk : |Any|
            Primary key of the model entry

        Returns
        -------
        Returns changed entry if data is valid, else form with errors

        """
        form = self.form(data)
        if form.is_valid():
            changing_entry = self.get_concrete(pk)
            self._change_entry_fields(form.cleaned_data, changing_entry)
            changing_entry.save()
            return changing_entry

        return form

    def delete(self, pk: Any) -> None:
        """Deletes a concrete model entry with `pk`

        Parameters
        ----------
        pk : |Any|
            Primary key of the model entry

        """
        entry = self.get_concrete(pk)
        entry.delete()

    def get_create_form(self) -> Form:
        """Returns a form to create a new model entry"""
        return self.form()

    def _get_form_data_from_entry(self, entry: Model) -> dict:
        """Returns dict with model entry fields and values for form"""
        fields = self.form.base_fields.keys()
        fields_values = [getattr(entry, field) for field in fields]
        return dict(zip(fields, fields_values))

    def get_change_form(self, pk: Any) -> Form:
        """Returns a form with data from model entry with `pk`

        Parameters
        ----------
        pk : |Any|
            Primary key of the model entry

        """
        changing_entry = self.get_concrete(pk)
        form_data = self._get_form_data_from_entry(changing_entry)
        return self.form(form_data)
