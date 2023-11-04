from .color import Color
from .position import Pos
from .rug import Rug


class Board:
    def __init__(self) -> None:
        self.fields = [[Color.EMPTY for _ in range(7)] for _ in range(7)]
        """7x7 pálya, kezdetben teljesen üres"""

    def __repr__(self) -> str:
        return "\n".join(map(str, self.fields))

    def get(self, pos: Pos) -> Color:
        return self.fields[pos.row][pos.col]

    def _set(self, pos: Pos, color: Color) -> None:
        self.fields[pos.row][pos.col] = color

    def place_rug(self, rug: Rug) -> None:
        for pos in rug.pos.as_tuple():
            self._set(pos, rug.color)

    def get_region_area(self, pos: Pos) -> int:
        """Visszaadja a megadott pozíciót lefedő szőnyegrégió méretét

        A régió az azonos színű szőnyegek összefüggő területe.
        Ha a megadott mező üres, akkor 0-t ad vissza.
        """
        color = self.get(pos)
        if color == Color.EMPTY:
            return 0

        visited = set[Pos]()
        queue = [pos]
        while queue:
            pos = queue.pop()
            if pos in visited:
                continue
            visited.add(pos)
            for neighbor in pos.neighbors():
                if self.get(neighbor) == color:
                    queue.append(neighbor)
        return len(visited)
