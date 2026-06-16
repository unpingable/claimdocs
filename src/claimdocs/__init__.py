"""claimdocs — write documentation claims as data; refuse to render strong claims
without declared basis. Docs that fail closed.

claimdocs verifies declared BASES, not truth itself. A basis may resolve or match a
structural check; whether it ADEQUATELY supports an edge is a separate admission
decision unless the basis kind has a specific mechanical verifier. Rendering preserves
claim mode and never upgrades it. See CHARTER.md.
"""
__version__ = "0.0.1"

from .config import Vocabulary, load_vocabulary, find_config  # noqa: F401
from .linter import Report, lint  # noqa: F401
from .builder import build  # noqa: F401
