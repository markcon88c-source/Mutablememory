import critter.import_wall_core as import_wall_core
import critter.import_wall_experimental as import_wall_experimental

from critter.import_wall_core import *
from critter.import_wall_experimental import *

__all__ = (
    import_wall_core.__all__
    + import_wall_experimental.__all__
)
