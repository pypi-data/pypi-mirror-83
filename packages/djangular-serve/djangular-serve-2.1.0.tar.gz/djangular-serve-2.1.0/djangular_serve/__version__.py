import os
from pathlib import Path # noqa

here = Path(__file__).resolve(strict=True).parent.parent
__all__ = ["__version__"]

with open(os.path.join(os.path.dirname(here), '../VERSION')) as version_file:
    __version__ = version_file.read().strip()
