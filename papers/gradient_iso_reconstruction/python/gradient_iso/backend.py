"""Load an unchanged, provenance-recorded VICE geometry implementation.

Default: the exact three-module snapshot under python/vendor. Set
VICE_MEASEVAL_SOURCE to a live SourceCode/python checkout to opt into changes.
"""
import os
from pathlib import Path
import sys

configured = os.environ.get("VICE_MEASEVAL_SOURCE")
candidate = Path(configured) if configured else Path(__file__).resolve().parents[1] / "vendor"
if not (candidate / "vice_measeval").is_dir():
    raise ImportError("Set VICE_MEASEVAL_SOURCE to GUI_VICE-MeasurementEvalKit/"
                      "SourceCode/python, or restore the recorded vendor snapshot.")
sys.path.insert(0, str(candidate.resolve()))

from vice_measeval.backend.numeric.model.point_set import PointSet
from vice_measeval.backend.numeric.model.sampled_field import SampledField
from vice_measeval.backend.numeric.geometry.levelset.edge_intersector import (
    EdgeIntersector, EdgeIntersections,
)

__all__ = ["PointSet", "SampledField", "EdgeIntersector", "EdgeIntersections"]
