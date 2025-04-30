import pyxel


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
        pyxel.load("assets/cat.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
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

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.state != "running":
                self.state = "running"
                self.is_hurry = False
                self.timer = 60
                self.count_mod = pyxel.frame_count % 30
                pyxel.sounds[0].speed = 30
                pyxel.sounds[1].speed = 30
                pyxel.playm(0, 0, True)

    def draw(self):
        pyxel.cls(7)  # 白背景

        # タイトル
        pyxel.text(self.width // 2 - 18, 10, "PLANK CAT", 0)

        # STARTボタン
        pyxel.rect(self.width // 2 - 20, 30, 40, 16, 7)
        pyxel.rectb(self.width // 2 - 20, 30, 40, 16, 0)
        pyxel.text(self.width // 2 - 10, 35, "START", 0)

        # 残り時間（中央に表示）
        pyxel.text(self.width // 2 - 4, 55, f"{self.timer:02}", 0)

        # 猫のドット絵
        pyxel.blt(self.width // 2 - 16, 70, 0, 0, 0, 13, 16, 7)
        pyxel.blt(self.width // 2 + 6, 70, 0, 22, 0, 10, 16, 7)
        if self.timer > 10 or self.timer == 0:
            pyxel.blt(self.width // 2 - 3, 70, 0, 13, 0, 9, 16, 7)
        else:
            dy = pyxel.rndi(-1, 1)
            pyxel.blt(self.width // 2 - 3, 70 + dy, 0, 13, 0, 9, 16, 7)


App()
