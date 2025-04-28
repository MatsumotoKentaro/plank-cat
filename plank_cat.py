import pyxel

# 画面サイズ
WIDTH = 128
HEIGHT = 128
TIMER_SECONDS = 60
timer = 0

# ゲームの状態
mode = "title"  # 最初はタイトル画面


class Star:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # 画面外に出たら戻す
        if self.x < 0 or self.x > pyxel.width:
            self.dx = -self.dx
        if self.y < 0 or self.y > pyxel.height:
            self.dy = -self.dy

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 0, 8, 8, 0)


stars = []


def add_star():
    x = pyxel.rndi(10, 100)
    y = pyxel.rndi(10, 100)
    dx = pyxel.rndi(-2, 2)
    dy = pyxel.rndi(-2, 2)
    stars.append(Star(x, y, dx, dy))


def play_music():
    pyxel.play(0, 0, loop=True)


def update():
    global mode, timer

    if mode == "title":
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # マウスクリックでスタート
            if 40 <= pyxel.mouse_x <= 88 and 60 <= pyxel.mouse_y <= 80:
                mode = "planking"
                timer = TIMER_SECONDS * 30
                play_music()

    elif mode == "planking":
        if timer > 0:
            timer -= 1
        else:
            mode = "finished"
            for _ in range(20):
                add_star()
    elif mode == "finished":
        for star in stars:
            star.update()


def draw():
    pyxel.cls(7)  # 白背景

    if mode == "title":
        # スタートボタン
        pyxel.rect(40, 60, 48, 20, 12)  # 赤っぽいボタン
        pyxel.text(50, 66, "START", 7)  # 白文字
    elif mode == "planking":
        seconds_left = timer // 30  # 秒単位に戻す

        # ぷるぷる演出
        shake_x = 0
        shake_y = 0
        if seconds_left <= 10:
            shake_x = pyxel.rndi(-1, 1)
            shake_y = pyxel.rndi(-1, 1)

        pyxel.text(50 + shake_x, 68 + shake_y, f"{seconds_left}s", 0)
        pyxel.blt(48 + shake_x, 50 + shake_y, 0, 0, 0, 16, 16, 0)

    elif mode == "finished":
        pyxel.cls(7)
        for star in stars:
            star.draw()
        # 喜び猫を表示（(32,0) から 32x32 を使う想定）
        pyxel.blt(48, 40, 0, 16, 0, 16, 16, 0)
        pyxel.text(30, 80, "Good job!", pyxel.frame_count % 16)  # 色をチカチカ変化


# Pyxelアプリ起動
pyxel.init(WIDTH, HEIGHT, title="Plank Cat")
pyxel.load("assets/cat.pyxres")
pyxel.run(update, draw)
