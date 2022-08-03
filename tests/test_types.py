from strawberry import auto

import strawberry_django
from strawberry_django.fields.field import StrawberryDjangoField

from .models import User


def test_type_instance():
    @strawberry_django.type(User)
    class UserType:
        id: auto
        name: auto

    user = UserType(1, "user")
    assert user.id == 1
    assert user.name == "user"


def test_type_instance_auto_as_str():
    @strawberry_django.type(User)
    class UserType:
        id: "auto"
        name: "auto"

    user = UserType(1, "user")
    assert user.id == 1
    assert user.name == "user"


def test_input_instance():
    @strawberry_django.input(User)
    class InputType:
        id: auto
        name: auto

    user = InputType(1, "user")
    assert user.id == 1
    assert user.name == "user"


def test_custom_field_cls():
    """Custom field_cls is applied to all fields."""

    class CustomStrawberryDjangoField(StrawberryDjangoField):
        pass

    @strawberry_django.type(User, field_cls=CustomStrawberryDjangoField)
    class UserType:
        id: int
        name: auto

    assert all(
        isinstance(field, CustomStrawberryDjangoField)
        for field in UserType._type_definition.fields
    )


def test_custom_field_cls__explicit_field_type():
    """Custom field_cls is applied to all fields."""

    class CustomStrawberryDjangoField(StrawberryDjangoField):
        pass

    @strawberry_django.type(User, field_cls=CustomStrawberryDjangoField)
    class UserType:
        id: int
        name: auto = strawberry_django.field()

    assert isinstance(
        UserType._type_definition.get_field("id"), CustomStrawberryDjangoField
    )
    assert isinstance(
        UserType._type_definition.get_field("name"), StrawberryDjangoField
    )
    assert not isinstance(
        UserType._type_definition.get_field("name"), CustomStrawberryDjangoField
    )
