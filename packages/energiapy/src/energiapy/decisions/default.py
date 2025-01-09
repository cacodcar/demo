# """Default Decisions"""

# from .action import Action
# from .conseq import Conseq
# from .flow import Flow


# from ..components.impact.categories import Econ
# from ..components.impact.categories import Environ
# from ..components.impact.categories import Social

# from ..components.commodity.misc import Cash
# from ..components.commodity.misc import Land
# from ..components.commodity.misc import Material
# from ..components.commodity.resource import Resource
# from ..components.game.player import Player
# from ..components.task.process import Process
# from ..components.spatial.linkage import Link
# from ..components.spatial.location import Loc
# from ..components.temporal.period import Period
# from ..components.types.basic import Name
# from ..components.types.defined import Index

# setup = Action(Process, label='Capacitate an Operation')
# dismantle = -setup

# produce = Action(Process, label='Operate an Operation')
# consume = Flow(Resource, label='Resource consumed by Process operation')
# produce = -consume

# transport = Action
# receive = Flow(Resource, Material, label='Resource transported at Loc')
# deliver = -receive

# store = Action
# charge = Flow(Resource, Material, label='Resource stored at Loc')
# discharge = -charge

# buy = Action(Player, label='Trade a Resource')
# sell = -buy

# use = Flow(Resource, Material, Land, label='Resource Flow caused by Operation Setup')
# dispose = -use

# recover = Flow(Resource, label='Resource seepage during Process operation')
# lose = -recover

# earn = Conseq(Econ, Cash, label='Economic Consequence')
# spend = -earn

# abate = Conseq(Environ, label='Environmental Consequence')
# emit = -abate

# benefit = Conseq(Social, label='Social Consequence')
# detriment = -benefit


# setup.use = use
# setup.dispose = dispose

# operate.consume = consume
# operate.produce = produce
