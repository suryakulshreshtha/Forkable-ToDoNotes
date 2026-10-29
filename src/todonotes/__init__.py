"""Forkable-ToDoNotes — a standalone, offline-first notes + to-do app.

Layers (each one only talks to the layer directly below it):

    web.py      HTTP routes + HTML templates   (Flask)
    service.py  rules: validation, defaults    (plain Python)
    storage.py  SQL, and nothing else          (sqlite3, standard library)

Read docs/README.md for the guided, chapter-by-chapter tour.
"""

__version__ = "0.2.0"
APP_NAME = "Forkable-ToDoNotes"
