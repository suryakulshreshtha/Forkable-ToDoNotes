"""Entry script for PyInstaller.

PyInstaller needs a plain script to start from. Pointing it at
src/todonotes/__main__.py directly would break that module's package imports,
so this tiny file imports the package properly and hands over to it.
"""

from todonotes.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
