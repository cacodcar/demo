import pytest

from ...energiapy.src.energiapy.components.commodity.cash import Cash
from ...energiapy.src.energiapy.components.space.location import Loc
from ...energiapy.src.energiapy.represent.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.ny = Loc()
    m_.cs = Loc()
    m_.ht = Loc()
    m_.tx = m_.cs + m_.ht
    m_.usa = m_.ny + m_.tx
    m_.eu = Loc()
    m_.ind = Loc()
    m_.maitri = Loc()
    m_.usd = Cash(m_.usa)
    m_.eur = Cash(m_.eu)
    m_.inr = Cash(m_.ind, m_.maitri)
    m_.eur == m_.usd * 0.8
    m_.inr == m_.usd / 80
    return m_


def test_cash(m):
    assert m.currencies == [m.usd, m.eur, m.inr]
    assert m.usd.exchange == {m.eur: 1.25, m.inr: 80.0}
    assert m.eur.exchange == {m.usd: 0.8, m.inr: 64.0}
    assert m.inr.exchange == {m.usd: 0.0125, m.eur: 0.01}
    assert m.usa.currency == m.usd
    assert m.ny.currency == m.usd
    assert m.tx.currency == m.usd
    assert m.cs.currency == m.usd
    assert m.ht.currency == m.usd
    assert m.eu.currency == m.eur
    assert m.ind.currency == m.inr
    assert m.maitri.currency == m.inr
    assert set(m.inr.locs) == {m.ind, m.maitri}
    assert m.usd.howmany(m.eur) == 1.25
    assert m.usd.howmany(m.inr) == 80
    assert m.eur.howmany(m.usd) == 0.8
    assert m.eur.howmany(m.inr) == 64
    assert m.inr.howmany(m.usd) == 0.0125
    assert m.inr.howmany(m.eur) == 0.01
