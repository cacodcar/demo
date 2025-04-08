import pytest

from ...energiapy.src.energiapy.components.impact.categories import (Env,
                                                                     Soc)
from ...energiapy.src.energiapy.modeling.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.gwp = Env()
    m_.eut = Env()
    m_.mrh = Soc()
    return m_


def test_impact(m):
    assert m.gwp.impact == m.impact
    assert m.eut.impact == m.impact
    assert m.mrh.impact == m.impact
    assert m.impact.environs == [m.gwp, m.eut]
    assert m.impact.socials == [m.mrh]
