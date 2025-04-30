import pyxel

# 画面サイズ
WIDTH = 64
HEIGHT = 96

# 状態
state = "ready"  # ready, running, done
is_hurry = False
timer = 60  # 秒
cound_mod = 0


def update():
    global state, timer, is_hurry, count_mod

    if state == "running":
        if pyxel.frame_count % 30 == count_mod and timer > 0:
            timer -= 1
            if timer == 0:
                state = "done"
                pyxel.stop()
        if not is_hurry and timer <= 20:
            is_hurry = True
            pos = pyxel.play_pos(0)
            pyxel.stop()
            speed = 15
            pyxel.sounds[0].speed = speed
            pyxel.sounds[1].speed = speed
            pyxel.playm(0, (pos[0] * 48 + pos[1]) * speed, True)

    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        if state != "running":
            state = "running"
            is_hurry = False
            timer = 60
            count_mod = pyxel.frame_count % 30
            pyxel.sounds[0].speed = 30
            pyxel.sounds[1].speed = 30
            pyxel.playm(0, 0, True)


def draw():
    pyxel.cls(7)  # 白背景

    # タイトル
    pyxel.text(WIDTH // 2 - 18, 10, "PLANK CAT", 0)

    # STARTボタン
    pyxel.rect(WIDTH // 2 - 20, 30, 40, 16, 7)
    pyxel.rectb(WIDTH // 2 - 20, 30, 40, 16, 0)
    pyxel.text(WIDTH // 2 - 10, 35, "START", 0)

    # 残り時間（中央に表示）
    pyxel.text(WIDTH // 2 - 4, 55, f"{timer:02}", 0)

    # 猫のドット絵
    pyxel.blt(WIDTH // 2 - 16, 70, 0, 0, 0, 13, 16, 7)
    pyxel.blt(WIDTH // 2 + 6, 70, 0, 22, 0, 10, 16, 7)
    if timer > 10 or timer == 0:
        pyxel.blt(WIDTH // 2 - 3, 70, 0, 13, 0, 9, 16, 7)
    else:
        dy = pyxel.rndi(-1, 1)
        pyxel.blt(WIDTH // 2 - 3, 70 + dy, 0, 13, 0, 9, 16, 7)


pyxel.init(WIDTH, HEIGHT, title="Plank Cat")
pyxel.load("assets/cat.pyxres")
pyxel.run(update, draw)
