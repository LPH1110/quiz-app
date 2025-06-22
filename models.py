from typing import List

class Question:
    def __init__(self, id: str, title: str, options: List[str]):
        self.id = id
        self.title = title
        self.options = options