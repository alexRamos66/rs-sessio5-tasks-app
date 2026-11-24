"""Model de dades de les tasques de Tasks_app."""

import json


class Task:
    def __init__(self, id, titol, assignatura, estat="pendent"):
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat

    def to_dict(self):
        return {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, dades):
        return cls(
            dades["id"],
            dades["titol"],
            dades["assignatura"],
            dades["estat"],
        )

    @classmethod
    def from_json(cls, text):
        return cls.from_dict(json.loads(text))

    def __str__(self):
        return f"[{self.id}] {self.titol} ({self.assignatura}) - estat: {self.estat}"

    def __repr__(self):
        return (
            f"Task({self.id!r}, {self.titol!r}, "
            f"{self.assignatura!r}, {self.estat!r})"
        )

    def __eq__(self, altre):
        if not isinstance(altre, Task):
            return NotImplemented
        return self.to_dict() == altre.to_dict()
