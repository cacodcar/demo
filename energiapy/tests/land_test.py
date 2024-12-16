import pytest

from ...energiapy.src.energiapy.components.measure.basis import Basis
from ...energiapy.src.energiapy.components.use.land import Land
from ...energiapy.src.energiapy.represent.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.acre = Basis()
    m_.farm = Land(m_.acre)
    m_.desert = Land()
    return m_


def test_res(m):
    assert m.farm.basis == m.acre
    assert not m.desert.basis
