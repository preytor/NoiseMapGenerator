


class Label:
    def __init__(self, text, color, x, y, font) -> None:
        self.label = font.render(text, True, color)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.label, (self.x, self.y))



class Fps():
    def __init__(self, text, color, x, y, font) -> None:
        self.label = font.render(text, True, color)
        self.x = x
        self.y = y
        self.font = font
        self.color = color

    def draw(self, text, screen):
        self.label = self.font.render(str(text), True, self.color)
        screen.blit(self.label, (self.x, self.y))