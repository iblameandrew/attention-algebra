"""Public API for the ``attention_algebra`` package.

The three layers of the Cognitive Grammar compiler are exposed as
top-level classes so that the typical user code is::

    from attention_algebra import AlgebraAnalyst, Composer, SpectrogramReader

For programmatic composition, the smaller utilities (``strip_think_tags``,
``strip_code_fences``) are also re-exported.
"""

from .algebra import AlgebraAnalyst
from .composition import Composer
from .config import ModelFactory
from .parser import ValidationResult, are_complementary, validate_expression
from .spectrum import SpectrogramReader, SpectrumResult
from .utils import strip_code_fences, strip_think_tags

__all__ = [
    "AlgebraAnalyst",
    "Composer",
    "ModelFactory",
    "SpectrogramReader",
    "SpectrumResult",
    "ValidationResult",
    "are_complementary",
    "strip_code_fences",
    "strip_think_tags",
    "validate_expression",
]

__version__ = "0.5.0"