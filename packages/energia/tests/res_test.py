import pytest

from ...energiapy.src.energiapy.components.commodity.resource import Resource
from ...energiapy.src.energiapy.components.measure.basis import Unit
from ...energiapy.src.energiapy.modeling.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.batli = Unit()
    m_.feni = Resource(m_.batli)
    m_.pao = Resource()
    return m_


def test_res(m):
    assert m.feni.basis == m.batli
    assert not m.pao.basis
