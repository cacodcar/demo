import pytest

from ...energiapy.src.energiapy.components.time.period import Period
from ...energiapy.src.energiapy.represent.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.h = Period()
    m_.d = m_.h * 24
    m_.y = m_.d * 365
    m_.w = m_.d * 7
    m_.s = Period()
    return m_


def test_period(m):
    assert m.time.periods == [m.h, m.d, m.y, m.w, m.s]
    assert m.h.howmany(m.d) == 0.041666666666666664
    assert m.h.howmany(m.w) == 0.005952380952380952
    assert m.h.howmany(m.y) == 0.00011415525114155251
    assert m.d.howmany(m.h) == 24
    assert m.d.howmany(m.w) == 0.14285714285714285
    assert m.d.howmany(m.y) == 0.0027397260273972603
    assert m.w.howmany(m.h) == 168
    assert m.w.howmany(m.d) == 7
    assert m.w.howmany(m.y) == 0.019178082191780823
    assert m.y.howmany(m.h) == 8760
    assert m.y.howmany(m.d) == 365
    assert m.y.howmany(m.w) == 52.142857142857146
    assert m.h.isroot()
    assert not m.d.isroot()
    assert m.time.horizon == m.y
    assert m.h.periods == 1
    assert not m.h.flow
    assert m.d.periods == 24
    assert m.d.flow == m.h
    assert m.y.periods == 8760
    assert m.y.flow == m.h
    assert m.w.flow == m.h
    assert m.w.periods == 168
    assert m.h.time == m.time

    with pytest.raises(ValueError):
        m.fail = m.h * m.y

    with pytest.raises(ValueError):
        m.h.howmany(m.s)

    with pytest.raises(ValueError):
        m.y.howmany(m.s)
