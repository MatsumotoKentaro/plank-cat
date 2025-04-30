import pyxel

from mini_ui import Button, Column, Label


class Cat:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 16
        self.dy = 0
        self.timer = 0

    def update(self):
        if self.timer > 10 or self.timer == 0:
            self.dy = 0
        else:
            self.dy = pyxel.rndi(-1, 1)

    def draw(self):
        # 猫のドット絵
        pyxel.blt(self.x, self.y, 0, 0, 0, 13, 16, 7)
        pyxel.blt(self.x + 13, self.y + self.dy, 0, 13, 0, 9, 16, 7)
        pyxel.blt(self.x + 22, self.y, 0, 22, 0, 10, 16, 7)


class App:
    def __init__(self):
        self.width = 64
        self.height = 96
        # 状態
        self.state = "ready"  # ready, running, done
        self.is_hurry = False
        self.timer = 60  # 秒
        self.count_mod = 0

        pyxel.init(self.width, self.height, title="Plank Cat")
        # pyxel.mouse(True)
        pyxel.load("assets/cat.pyxres")
        self.timer_label = Label("", color=0)
        self.cat = Cat()
        self.column = Column(
            0,
            0,
            self.width,
            self.height,
            8,
            [
                Label("PLANK CAT"),
                Button(
                    "START",
                    self.on_start,
                    0,
                    0,
                    40,
                    16,
                    color_text=0,
                    color_rect=0,
                    center_x=True,
                ),
                self.timer_label,
                self.cat,
            ],
        )

        pyxel.run(self.update, self.draw)

    def on_start(self):
        if self.state != "running":
            self.state = "running"
            self.is_hurry = False
            self.timer = 60
            self.count_mod = pyxel.frame_count % 30
            pyxel.sounds[0].speed = 30
            pyxel.sounds[1].speed = 30
            pyxel.playm(0, 0, True)

    def update(self):
        self.timer_label.text = f"{self.timer:02}"
        if self.state == "running":
            if pyxel.frame_count % 30 == self.count_mod and self.timer > 0:
                self.timer -= 1
                if self.timer == 0:
                    self.state = "done"
                    pyxel.stop()
            if not self.is_hurry and self.timer <= 20:
                self.is_hurry = True
                pos = pyxel.play_pos(0)
                pyxel.stop()
                speed = 15
                pyxel.sounds[0].speed = speed
                pyxel.sounds[1].speed = speed
                pyxel.playm(0, (pos[0] * 48 + pos[1]) * speed, True)
        self.cat.timer = self.timer
        self.column.update()

    def draw(self):
        pyxel.cls(7)  # 白背景
        self.column.draw()


App()
