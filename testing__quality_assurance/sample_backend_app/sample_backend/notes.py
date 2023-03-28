"""
Implementation of the repository pattern for notes.

With an app this simple we might not need a repository and just use the ORM directly,
but using the pattern will help illustrate when to use tests at different levels (unit/integrated/functional).
"""

from . import services


class NotesRepository:
    def store(self):
        pass

    def delete(self):
        pass
