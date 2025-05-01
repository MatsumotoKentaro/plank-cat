import pyxel


class Widget:
    def update(self):
        pass

    def draw(self):
        pass


# テキスト表示
class Label(Widget):
    def __init__(self, text, x=0, y=0, color=0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pyxel.text(self.x, self.y, self.text, self.color)


# ボタン（矩形＋テキスト＋クリック）
class Button(Widget):
    def __init__(
        self,
        text,
        on_pressed,
        x=0,
        y=0,
        w=50,
        h=16,
        color_text=1,
        color_rect=1,
        center_x=True,
        fill=False,
    ):
        self.text = text
        self.on_pressed = on_pressed
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_text = color_text
        self.color_rect = color_rect
        self.center_x = center_x
        self.fill = fill

    def update(self):
        if (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            and self.x <= pyxel.mouse_x <= self.x + self.w
            and self.y <= pyxel.mouse_y <= self.y + self.h
        ):
            self.on_pressed()

    def draw(self):
        if self.fill:
            pyxel.rect(self.x, self.y, self.w, self.h, self.color_rect)
        else:
            pyxel.rectb(self.x, self.y, self.w, self.h, self.color_rect)

        text_x = self.x + 4
        if self.center_x:
            text_x = self.x + self.w // 2 - pyxel.FONT_WIDTH * len(self.text) // 2
        text_y = self.y + self.h // 2 - pyxel.FONT_HEIGHT // 2
        pyxel.text(text_x, text_y, self.text, 0)


class Blank(Widget):
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h


# 縦に並べるレイアウト
class Column(Widget):
    def __init__(
        self,
        x=0,
        y=0,
        w=None,
        h=None,
        spacing=0,
        children=[],
        center=True,
        align="center",
    ):
        self.x = x
        self.y = y
        self.w = w if w is not None else pyxel.width
        self.h = h if h is not None else pyxel.height
        self.spacing = spacing
        self.children = children
        self.center = center  # Y軸の中央揃え
        self.align = align  # 'left', 'center', 'right'
        self._layout()

    def _layout(self):
        total_height = self.spacing
        # x方向の配置y方向の高さの合計
        child_heights = []
        for child in self.children:
            if hasattr(child, "w"):
                child_width = child.w
            elif hasattr(child, "text"):
                child_width = pyxel.FONT_WIDTH * len(getattr(child, "text", ""))
            else:
                child_width = 0

            if self.w is not None:
                if self.align == "left":
                    child.x = self.x
                elif self.align == "center":
                    child.x = self.x + self.w // 2 - child_width // 2
                else:
                    child.x = self.x - child_width
            else:
                child.x = self.x - child_width // 2

            if hasattr(child, "h"):
                child_height = child.h
            elif hasattr(child, "text"):
                child_height = pyxel.FONT_HEIGHT
            else:
                child_height = 0
            child_heights.append(child_height)

            total_height += child_height + self.spacing

        pos_y = (
            self.y + self.h // 2 - total_height // 2 + self.spacing
            if self.center
            else self.y + self.spacing
        )
        for i, child in enumerate(self.children):
            child.y = pos_y
            pos_y += child_heights[i] + self.spacing

    def update(self):
        for child in self.children:
            child.update()
        self._layout()

    def draw(self):
        for child in self.children:
            child.draw()
