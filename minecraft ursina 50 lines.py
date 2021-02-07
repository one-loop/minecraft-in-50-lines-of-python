from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina() # make the game object
grass_texture, stone_texture, brick_texture, dirt_texture, sky_texture, arm_texture = load_texture('assets/grass_block.png'), load_texture('assets/stone_block.png'), load_texture('assets/brick_block.png'), load_texture('assets/dirt_block.png'), load_texture('assets/skybox.png'), load_texture('assets/arm_texture.png') # import textures
punch_sound, block_pick = Audio('assets/punch_sound', loop=False, autoplay=False), 1
window.fps_counter.enabled, window.exit_button.visible = False, False

def update():
    global block_pick
    if held_keys['left mouse'] or held_keys['right mouse']: hand.active()
    else: hand.passive()
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

class Voxel(Button):
    # when you click on a voxel (like a block) it places another voxel
    def __init__(self, position=(0,0,0), texture=grass_texture):
        super().__init__(parent = scene, position = position, model = 'assets/block', origin_y = 0.5, texture = texture, color = color.color(0, 0, random.uniform(0.9, 1)), scale=0.5)
    def input(self, key):
        if self.hovered:
            if key ==  'left mouse down':
                punch_sound.play() # if the mouse button is clicked, create a new block on that position
                if block_pick == 1: voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2: voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3: voxel = Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 4: voxel = Voxel(position=self.position + mouse.normal, texture=dirt_texture)
            if key == 'right mouse down': # if the mouse button is pressed, destroy the Voxel
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(parent = scene, model = 'sphere', texture = sky_texture, scale = 150, double_sided=True)

class Hand(Entity):
    def __init__(self):
        super().__init__(parent = camera.ui, model = 'assets/arm', texture = arm_texture, scale = 0.2, rotation = Vec3(150, -10, 0), position = Vec2(0.4, -0.6))
    def active(self):
        self.position = Vec2(0.3, -0.5)
    def passive(self):
        self.position = Vec2(0.4, -0.6)

for z in range(20): # make a for loop to display the blocks in all the dimensions
    for x in range(20):
        voxel =  Voxel((x, 0, z))

player, sky, hand = FirstPersonController(), Sky(), Hand() # make the player object (it can already walk, run, jump etc)
app.run()
