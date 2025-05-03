from datetime import date

import pyxel

from libs.mini_ui.mini_ui import (
    Blank,
    Button,
    Column,
    Label,
    TransButton,
    Widget,
    load,
    save,
)


class Cat(Widget):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 16
        self.dy = 0
        self.is_purupuru = False

    def update(self):
        if self.is_purupuru:
            self.dy = pyxel.rndi(-1, 1)
        else:
            self.dy = 0

    def draw(self):
        # 猫のドット絵
        pyxel.blt(self.x, self.y, 0, 0, 0, 13, 16, 7)
        pyxel.blt(self.x + 13, self.y + self.dy, 0, 13, 0, 9, 16, 7)
        pyxel.blt(self.x + 22, self.y, 0, 22, 0, 10, 16, 7)


class UpButton(TransButton):
    def __init__(self, on_pressed, w, h, color, x=0, y=0):
        super().__init__(on_pressed, w, h, x, y)
        self.color = color

    def draw(self):
        x1 = self.x
        y1 = self.y + self.h - 1
        x2 = self.x + self.w - 1
        y2 = y1
        x3 = (2 * self.x + self.w - 1) / 2
        y3 = self.y
        pyxel.tri(x1, y1, x2, y2, x3, y3, self.color)


class DownButton(TransButton):
    def __init__(self, on_pressed, w, h, color, x=0, y=0):
        super().__init__(on_pressed, w, h, x, y)
        self.color = color

    def draw(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.w - 1
        y2 = y1
        x3 = (2 * self.x + self.w - 1) / 2
        y3 = self.y + self.h - 1
        pyxel.tri(x1, y1, x2, y2, x3, y3, self.color)


class AppState:
    def __init__(self, app):
        self.app = app

    def on_start(self):
        pass

    def on_up(self):
        pass

    def on_down(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class ReadyState(AppState):
    def on_start(self):
        self.app.set_state(RunningState(self.app))

    def on_up(self):
        self.app.timer_limit += 1
        if self.app.timer_limit > 99:
            self.app.timer_limit = 99
        save("timer_limit", self.app.timer_limit)

    def on_down(self):
        self.app.timer_limit -= 1
        if self.app.timer_limit < 10:
            self.app.timer_limit = 10
        save("timer_limit", self.app.timer_limit)

    def update(self):
        self.app.timer_label.text = f"{self.app.timer_limit:2}"


class RunningState(AppState):
    def __init__(self, app):
        super().__init__(app)
        self.timer = self.app.timer_limit
        self.count_mod = 0
        self.is_hurry = False
        self.app.start_music()

    def update(self):
        self.count_mod += 1
        if self.count_mod % 30 == 0:
            self.timer -= 1
            if self.timer <= 0:
                self.app.set_state(DoneState(self.app))
            if not self.is_hurry and self.timer <= 20:
                self.is_hurry = True
                self.app.speedup_music()

        self.app.timer_label.text = f"{self.timer:2}"
        self.app.cat.is_purupuru = 0 < self.timer and self.timer < 10


class DoneState(AppState):
    def __init__(self, app):
        super().__init__(app)
        self.app.stop_music()
        self.timer = 5
        self.count_mod = 0
        today = date.today().strftime("%Y-%m-%d")
        today_count_loaded = load(today)
        today_count = int(today_count_loaded) if today_count_loaded is not None else 0
        today_count += 1
        save(today, today_count)

    def update(self):
        self.app.timer_label.text = "FINISHED!"
        self.count_mod += 1
        if self.count_mod % 30 == 0:
            self.timer -= 1
            if self.timer <= 0:
                self.app.set_state(ReadyState(self.app))


class App:
    def __init__(self):
        self.width = 64
        self.height = 96

        pyxel.init(self.width, self.height, title="Plank Cat")
        # pyxel.mouse(True)
        pyxel.load("assets/cat.pyxres")
        self.timer_label = Label("", color=0)
        up_button = UpButton(self.on_up, 7, 4, 0)
        down_button = DownButton(self.on_down, 7, 4, 0)
        button = Button(
            "START",
            self.on_start,
            w=40,
            h=16,
            color_text=0,
            color_rect=0,
        )
        self.cat = Cat()
        self.column = Column(
            children=[
                Label("PLANK CAT"),
                Blank(h=8),
                button,
                Blank(h=2),
                up_button,
                Blank(h=2),
                self.timer_label,
                Blank(h=2),
                down_button,
                Blank(h=2),
                self.cat,
            ],
        )
        timer_limit = load("timer_limit")
        self.timer_limit = int(timer_limit) if timer_limit is not None else 60

        self.state = ReadyState(self)

        pyxel.run(self.update, self.draw)

    def set_state(self, state):
        self.state = state

    def on_start(self):
        self.state.on_start()

    def on_up(self):
        self.state.on_up()

    def on_down(self):
        self.state.on_down()

    def update(self):
        self.state.update()
        self.column.update()

    def draw(self):
        pyxel.cls(7)
        self.column.draw()

    def start_music(self):
        speed = 30
        pyxel.sounds[0].speed = speed
        pyxel.sounds[1].speed = speed
        pyxel.playm(0, 0, True)

    def speedup_music(self):
        speed = 15
        pos = pyxel.play_pos(0)
        pyxel.stop()
        pyxel.sounds[0].speed = speed
        pyxel.sounds[1].speed = speed
        pyxel.playm(0, (pos[0] * 48 + pos[1]) * speed, True)

    def stop_music(self):
        pyxel.stop()


App()
