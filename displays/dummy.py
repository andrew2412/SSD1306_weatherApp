from displays.display import display

class dummy(display):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getSize(self):
        return (self.width, self.height)

    def draw(self, image):
        image.show()
