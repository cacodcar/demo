import pytest

from ...energiapy.src.energiapy.components.measure.basis import Unit
from ...energiapy.src.energiapy.modeling.model import Model
from ..src.energia.components.commodity.misc import Land


@pytest.fixture
def m():
    m_ = Model()
    m_.acre = Unit()
    m_.farm = Land(m_.acre)
    m_.desert = Land()
    return m_


def test_res(m):
    assert m.farm.basis == m.acre
    assert not m.desert.basis
