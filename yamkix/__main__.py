# -*- coding: utf-8 -*-
"""Allow yamkix to be executable through `python -m yamkix`."""
from __future__ import absolute_import

from .yamkix import main

if __name__ == "__main__":  # pragma: no cover
    main()
