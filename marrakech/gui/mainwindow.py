import random
import time
import PySimpleGUI as sg  # type: ignore

from ..model.color import Color
from ..model.directions import Direction, RotationDirection
from ..model.game_state import GameState
from ..model.position import Pos
from ..model.rug import RugPos


def fig_img(direction: Direction) -> str:
    "img/fig_{direction.value}.png"


class MainWindow:
    def __init__(self, game: GameState):
        # sg.theme_previewer()
        sg.theme("DarkBrown5")
        sg.set_options(font=("Calibri", 14))
        self.game = game
        self.selected_tiles = list[Pos]()
        self.layout = []
        for row in range(7):
            self.layout.append(
                [
                    sg.Button(
                        size=(5, 2),
                        pad=(0, 0),
                        border_width=1,
                        key=(row, col),
                        image_filename=fig_img(self.game.figure_dir)
                        if Pos(row, col) == self.game.figure_pos
                        else "img/fig_none.png",
                    )
                    for col in range(7)
                ]
            )
        self.rotate_btns = [
            sg.Button("↺", size=(2, 1), key=RotationDirection.LEFT),
            sg.Button("–", size=(2, 1), key=RotationDirection.NONE),
            sg.Button("↻", size=(2, 1), key=RotationDirection.RIGHT),
        ]
        self.layout.append([sg.Text("Forgatás: ")] + self.rotate_btns)
        self.player_panels = []
        for player in self.game.players:
            self.player_panels.append(
                [
                    [
                        sg.Text(
                            f"""{player.name}{" (active)"
                                if player == self.game.current_player()
                                else ""}""",
                            text_color="black"
                            if player.color in (Color.YELLOW, Color.MAGENTA)
                            else "white",
                            background_color=player.color.name,
                            key=f"{player.name}_name",
                        ),
                    ],
                    [
                        sg.Text("🪙"),
                        sg.Text(player.money, size=(4, 1), key=f"{player.name}_money"),
                        sg.Text(
                            player.rugs_left, size=(2, 1), key=f"{player.name}_rugs"
                        ),
                        sg.Text("szőnyeg"),
                    ],
                ]
            )
        self.layout.extend(self.player_panels)
        self.window = sg.Window("Marrakech", self.layout)

    def update(self):
        for row in range(7):
            for col in range(7):
                self.window[(row, col)].update(
                    image_filename="img/fig_none.png", image_size=(51, 51)
                )
        for rug in self.game.rugs:
            for pos in rug.pos.as_tuple():
                direction = rug.pos.direction
                if pos != rug.pos.start:
                    direction = direction.rotate(RotationDirection.LEFT)
                    direction = direction.rotate(RotationDirection.LEFT)
                self.window[pos.as_tuple()].update(
                    button_color=rug.color.name,
                    image_filename=f"img/{rug.color.name.lower()}_{direction.name.lower()}.png",
                    image_size=(51, 51),
                )
        self.window[self.game.figure_pos.as_tuple()].update(
            image_filename=f"img/fig_{self.game.figure_dir.value}.png",
            image_size=(51, 51),
        )
        for player in self.game.players:
            self.window[f"{player.name}_name"].update(
                f"""{player.name}{" (active)"
                                if player == self.game.current_player()
                                else ""}"""
            )
            self.window[f"{player.name}_money"].update(player.money)
            self.window[f"{player.name}_rugs"].update(player.rugs_left)
        self.window.refresh()

    def rotate(self, direction: RotationDirection):
        self.game.turn_figure(direction)
        for btn in self.rotate_btns:
            btn.update(disabled=True)
        self.update()

    def enable_rotate(self):
        for btn in self.rotate_btns:
            btn.update(disabled=False)

    def move(self):
        faces = [1, 2, 2, 3, 3, 4]
        roll = random.choice(faces)
        sg.popup_ok(f"{roll}-t dobtál.")
        for _ in range(roll):
            time.sleep(0.3)
            self.game.step_with_figure()
            self.update()
            time.sleep(0.3)
        color = self.game.board.get(self.game.figure_pos)
        if color not in (Color.EMPTY, self.game.current_player().color):
            for player in self.game.players:
                if player.color == color:
                    area = self.game.board.get_region_area(self.game.figure_pos)
                    sg.popup_ok(
                        f"{player.name} szőnyegére léptél.\nFizess neki {area} pénzt!"
                    )
                    break
        self.game.move_figure(0)
        self.update()
        self.selected_tiles.clear()

    def place_rug(self):
        try:
            rugpos = RugPos.from_tuple(tuple(self.selected_tiles))
            valid = self.game.get_valid_rug_places()
            if rugpos not in valid:
                raise ValueError("Ide nem teheted a szőnyeget!")
            else:
                self.game.place_rug(rugpos)
                self.game.next_player()
                self.update()
                self.enable_rotate()
        except Exception as e:
            sg.popup_ok(e)
            self.selected_tiles.clear()

    def start(self):
        while not self.game.is_game_over():
            event, _ = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            if isinstance(event, RotationDirection):
                self.rotate(event)
                sg.popup_ok("Dobj a kockával!")
                self.move()
                sg.popup_ok("Kattints a két mezőre, ahova szőnyeget szeretnél tenni!")
            elif isinstance(event, tuple):
                self.selected_tiles.append(Pos(*event))
                if len(self.selected_tiles) == 2:
                    self.place_rug()
            self.update()
        self.window.close()
        print(self.game.get_scoreboard())
