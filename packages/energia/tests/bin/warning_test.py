"""Warning Tests
"""

import pytest
from src.energiapy.core.nirop.warnings import (InconsistencyWarning,
                                               OverWriteWarning)
from src.energiapy.environ.horizon import Horizon

from .test_fixtures import scenario_ok


def test_overwrite_warning(scenario_ok):
    """Overwrite Warning
    if another Horizon is defined, it should raise a warning
    """
    with pytest.warns(OverWriteWarning):
        scenario_ok.h = Horizon(birth=[4])
