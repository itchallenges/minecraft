from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

window.fps_counter.enabled = False
window.exit_button.enabled = False

grass_texture = load_texture('assets/grass_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
stone_texture = load_texture('assets/stone_block.png')
cracked_stone_texture = load_texture('assets/cracked_stone_block.png')

add_sound = Audio('assets/add_block.mp3', loop = False, autoplay = False)
destroy_sound = Audio('assets/destroy_block.mp3', loop = False, autoplay = False)


class Voxel(Button):
    """
    A class to represent a voxel
    """
    def __init__(self, position = (0, 0, 0), texture = grass_texture, life = 1):
        """
        Constructs all the necessary attributes for the voxel object
        """
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1.0)),
            scale = 0.5,
            life = life
        )
    
    def input(self, key):
        """
        Default function to handle user input
        """
        if self.hovered:
            # Adding a new block
            if key == 'left mouse down':
                add_sound.play()
                if block_pick == 1:
                    # mouse.normal is the surface we are looking at with the mouse
                    voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture, life = 1)
                elif block_pick == 2:
                    voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture, life = 2)
                elif block_pick == 3:
                    voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture, life = 3)

            # Removing an existing block
            if key == 'right mouse down':
                add_sound.play()
                if self.texture == grass_texture:
                    destroy_sound.play()
                    destroy(self)
                elif self.texture == dirt_texture:
                    self.life -= 1
                    if self.life == 0:
                        destroy_sound.play()
                        destroy(self)
                elif self.texture == stone_texture or self.texture == cracked_stone_texture:
                    self.life -= 1
                    if self.life == 0:
                        destroy_sound.play()
                        destroy(self)
                    elif self.life == 1:
                        self.texture = cracked_stone_texture

class Arm(Entity):
    """
    A class to represent the player arm
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the arm object
        """
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            color = color.rgb(232, 212, 186),
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.5, -0.7)
        )


# Creating the voxel terrain
for z in range(40):
    for x in range(40):
        voxel = Voxel(position = (x, 0, z))

# Creating the player
player = FirstPersonController()
player.position = Vec3(20, 0, 20)

# Creating the arm
arm = Arm()

# Creating the sky
sky = Sky()

block_pick = 1


def update():
    """
    Default update function that gets called automatically
    """
    global block_pick

    # Selecting a block type
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3

    # Arm animation when adding or removing a block
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.position = Vec2(0.4, -0.6)
    else:
        arm.position = Vec2(0.5, -0.7)

    # When shift is pressed, the player stoops and becomes slower
    if held_keys['left shift'] or held_keys['right shift']:
        camera.position = Vec3(0, -0.6, 0.3)
        player.speed = 2.5
    else:
        camera.position = Vec3(0, 0, 0)
        player.speed = 5


app.run()