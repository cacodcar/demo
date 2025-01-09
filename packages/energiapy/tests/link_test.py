import pytest

from ...energiapy.src.energiapy.components.measure.basis import Basis
from ...energiapy.src.energiapy.components.spatial.linkage import Link
from ...energiapy.src.energiapy.components.spatial.location import Loc
from ...energiapy.src.energiapy.modeling.model import Model


@pytest.fixture
def m():
    m_ = Model()
    m_.mile = Basis(label='Mile')
    m_.km = m_.mile * 1.60934
    m_.htown = Loc()
    m_.sd = Loc()
    m_.mum = Loc()
    m_.ny = Loc()
    m_.grid = Link(source=m_.htown, sink=m_.sd, dist=1400, basis=m_.mile)
    m_.sea = Link(source=m_.ny, sink=m_.mum, dist=10000, basis=m_.km, bi=True)
    return m_


def test_link(m):
    assert m.space.links == [m.grid, m.sea, m.sea_]
    assert m.space.sources == [m.htown, m.ny, m.mum]
    assert m.space.sinks == [m.sd, m.mum, m.ny]

    assert m.grid.space == m.space
    assert not m.sea.bi
    assert not m.sea_.bi
    assert m.sea.sib == m.sea_
    assert m.sea_.sib == m.sea
    assert m.sea.source == m.ny
    assert m.sea.sink == m.mum
    assert m.sea_.source == m.mum
    assert m.sea_.sink == m.ny
    assert m.htown.source()
    assert not m.sd.source()
    assert m.mum.source()
    assert m.ny.source()
    assert not m.htown.sink()
    assert m.sd.sink()
    assert m.mum.sink()
    assert m.ny.sink()
    assert m.ny.links(m.mum) == m.mum.links(m.ny) == [m.sea, m.sea_]
    assert m.htown.links(m.sd) == m.sd.links(m.htown) == [m.grid]
    assert m.htown.connected(m.sd)
    assert not m.htown.connected(m.mum)
