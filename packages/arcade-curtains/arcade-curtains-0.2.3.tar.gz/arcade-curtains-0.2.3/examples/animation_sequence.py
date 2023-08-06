import arcade

from arcade_curtains import Curtains, BaseScene, Sequence, KeyFrame


class CircleSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textures = [
            arcade.make_soft_circle_texture(100, arcade.color.WHITE, 255, 255),
            arcade.make_soft_circle_texture(100, arcade.color.GREEN, 255, 255)
        ]
        self.texture = self.textures[0]
        self.center_x = 70
        self.center_y = 70

    def toggle_texture(self, *args, **kwargs):
        self.set_texture(int(not self.textures.index(self.texture)))


class SmallScene(BaseScene):
    def setup(self):
        self.sprites = arcade.SpriteList()
        self.actor = CircleSprite()
        self.sprites.append(self.actor)

    def enter_scene(self, previous_scene):
        down = KeyFrame(position=self.actor.position)
        up = KeyFrame(position=(430, 430))
        sequence = Sequence(loop=True)
        sequence.add_keyframes((0, down), (.5, up), (1, down))
        self.actor.animate(sequence)


class Window(arcade.Window):
    def __init__(self):
        super().__init__(500, 500, 'move')
        self.curtains = Curtains(self)
        self.curtains.add_scene('scene1', SmallScene())

    def setup(self):
        self.curtains.set_scene('scene1')


def run(window):
    window.setup()
    try:
        arcade.run()
    except KeyboardInterrupt:
        pass


run(Window())
