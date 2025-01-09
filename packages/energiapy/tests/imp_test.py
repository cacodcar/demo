import pytest

from ...energiapy.src.energiapy.components.impact.categories import Environ
from ...energiapy.src.energiapy.components.impact.categories import Social
from ...energiapy.src.energiapy.modeling.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.gwp = Environ()
    m_.eut = Environ()
    m_.mrh = Social()
    return m_


def test_impact(m):
    assert m.gwp.impact == m.impact
    assert m.eut.impact == m.impact
    assert m.mrh.impact == m.impact
    assert m.impact.environs == [m.gwp, m.eut]
    assert m.impact.socials == [m.mrh]
