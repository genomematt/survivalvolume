#!/usr/bin/env -S nix shell nixpkgs#uv --command uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "survivalvolume @ git+https://github.com/genomematt/survivalvolume.git@main",
#
#     # OR: Pin to a specific immutable commit for 100% reproducibility:
#     # "survivalvolume @ git+https://github.com/genomematt/survivalvolume.git@<YOUR_COMMIT_HASH>",
# ]
# ///

import survivalvolume
# ... rest of your script ...