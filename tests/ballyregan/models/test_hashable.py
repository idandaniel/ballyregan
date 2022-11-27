import pytest

from src.ballyregan.models import HashableBaseModel


class DummyHashable(HashableBaseModel):
    attribute: str


@pytest.mark.parametrize('first_model, second_model', [
    (DummyHashable(attribute="a"), DummyHashable(attribute="a"))
])
def test_hashed_models_equel(first_model, second_model):
    assert hash(first_model) == hash(second_model)


@pytest.mark.parametrize('first_model, second_model', [
    (DummyHashable(attribute="a1"), DummyHashable(attribute="a2"))
])
def test_hashed_models_not_equel(first_model, second_model):
    assert hash(first_model) != hash(second_model)

    