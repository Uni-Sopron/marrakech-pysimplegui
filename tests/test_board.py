from marrakech.model.board import Board
from marrakech.model.color import Color
from marrakech.model.directions import Direction
from marrakech.model.position import Pos
from marrakech.model.rug import Rug, RugPos


def test_init() -> None:
    board = Board()
    assert len(board.fields) == 7
    for row in board.fields:
        assert len(row) == 7
        for field in row:
            assert field == Color.EMPTY


def test_get() -> None:
    board = Board()
    for i in range(7):
        for j in range(7):
            assert board.get(Pos(i, j)) == Color.EMPTY


def test_set() -> None:
    board = Board()
    for i in range(7):
        for j in range(7):
            assert board.get(Pos(i, j)) == Color.EMPTY
            board._set(Pos(i, j), Color.RED)
            assert board.get(Pos(i, j)) == Color.RED


def test_place_rug() -> None:
    board = Board()
    board.place_rug(Rug(RugPos(Pos(1, 1), Direction.RIGHT), Color.RED))
    assert board.get(Pos(1, 1)) == Color.RED
    assert board.get(Pos(1, 2)) == Color.RED
    # on the sides
    assert board.get(Pos(1, 0)) == Color.EMPTY
    assert board.get(Pos(1, 3)) == Color.EMPTY
    # above and below
    assert board.get(Pos(0, 1)) == Color.EMPTY
    assert board.get(Pos(0, 2)) == Color.EMPTY
    assert board.get(Pos(2, 1)) == Color.EMPTY
    assert board.get(Pos(2, 2)) == Color.EMPTY
    board.place_rug(Rug(RugPos(Pos(2, 2), Direction.UP), Color.BLUE))
    assert board.get(Pos(2, 2)) == Color.BLUE
    assert board.get(Pos(1, 2)) == Color.BLUE
    # on the sides
    assert board.get(Pos(1, 1)) == Color.RED
    assert board.get(Pos(2, 1)) == Color.EMPTY
    assert board.get(Pos(1, 3)) == Color.EMPTY
    assert board.get(Pos(2, 3)) == Color.EMPTY
    # above and below
    assert board.get(Pos(0, 2)) == Color.EMPTY
    assert board.get(Pos(3, 2)) == Color.EMPTY
