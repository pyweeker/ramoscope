
import sys
import os

import arcade



print("https://www.slideshare.net/tzanany/escaping-the-python-sandbox")
print("https://blog.teclado.com/python-abc-abstract-base-classes/")

"""
LIFETIME AND WEAKREF

https://stackoverflow.com/questions/2436302/when-to-use-weak-references-in-python

"""

from collections import *
import collections


import ctypes


# https://koor.fr/Python/API/python/collections/UserDict/Index.wp



# https://stackoverflow.com/questions/1396668/get-object-by-id   important+++

# darkness 30200e ; chocolate 473114
# Constants
SCREEN_WIDTH = 1800 #1000
SCREEN_HEIGHT = 1000 #650



# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

PLAYER_START_X = 64
PLAYER_START_Y = 256

# Layer Names from our TileMap
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_LADDERS = "Ladders"


DECAL_X = 300
DECAL_Y = 200

DECTEXT = 200

ATOMGAP = 0x30 # len listx =  283940
KGAP = 0xBB80 # hex(48*1000)


HEXGROUND =  0x7f7dc8e4d880

HEXTOP =  0x7f7dc9b4cf40

if HEXGROUND > HEXTOP:
    print("HEXGROUND superior")
else:
    print("HEXTOP superior")


listx = []

for x in range(HEXGROUND,HEXTOP,KGAP):
    print(x)
    listx.append(x)

print("len listx = ", len(listx))

x=input("hex")
# 48 dec = 30 hex



class Foobar():


    def __init__(self):
        self.tag = True





    @property
    def pos_XY(self):

        mini = str(id(self))[11:]
        mini = int(mini)
        #micro = mini // 10
        #micro = mini // 5

        micro = mini // 3

        pos_XY = tuple((DECAL_X, DECAL_Y + micro))

        
        return pos_XY
    
        
        



class MyGame(arcade.Window):
    

    def __init__(self):
        """
        Initializer for the game
        """

        # Call the parent class and set up the window
        #super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        super().__init__(1800, 1000, "RAMoscope")

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.memobjs_data = None

        self.exit_sprite = None



        # Our 'physics' engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")


    def setup(self):

        self.memobjs_data = list()
        
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        
        #map_name = f":resources:tiled_maps/map_with_ladders.json"
        map_name = f"./resources/tiled_maps/map_with_ladders_2.json"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
        }

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE

        # --- Other stuff
        # Set the background color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

            print(f"self.tile_map.tiled_map.background_color   {self.tile_map.tiled_map.background_color}")
            #print(f"self.tile_map.tiled_map.__dict__   {self.tile_map.tiled_map.__dict__}")


        self.scene.add_sprite_list("Memobjs_spritelist", use_spatial_hash=True)


        image_source = ":resources:images/tiles/signExit.png"
        self.exit_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.exit_sprite.center_x = 0
        self.exit_sprite.center_y = 0
        self.scene.add_sprite("Exit", self.exit_sprite)

        print(f"DEBUG   self.scene   {type(self.scene)} {self.scene.__dict__} ")

        print(f"DEBUG   self.scene {dir(self.scene.__dict__)} ")



        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            [
                self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
                self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS),
            ],
            gravity_constant=GRAVITY,
            ladders=self.scene.get_sprite_list(LAYER_NAME_LADDERS),
        )

    
    def mini_id(self,obj):
        
        mini = str(id(obj))[11:]
        return mini



    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        self.camera.use()
        #print(f" self.camera.__dict__ line 244  {self.camera.__dict__}")

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            #arcade.csscolor.BLACK,
            arcade.csscolor.NAVY,
            #arcade.csscolor.MAROON,
            18,
        )


        #print("self.scene['name_mapping']['Memobjs_spritelist']  =  ", self.scene['name_mapping']['Memobjs_spritelist'])

        

        #for obj in self.memobjs_data:
        #for obj in self.scene["name_mapping"]["Memobjs_spritelist"]: # TypeError: 'Scene' object is not subscriptable
        #for obj in self.scene["name_mapping"]["Memobjs_spritelist"]
        

        #for obj in self.Memobjs_spritelist
        for obj in self.memobjs_data:  
            try:
                arcade.draw_text(f" {obj}  size {sys.getsizeof(obj)}  ", obj.pos_XY[0] + DECTEXT -self.camera.position[0], obj.pos_XY[1]-self.camera.position[1], arcade.color.GREEN, 20)
            except AttributeError: # 'MyGame' object has no attribute 'Memobjs_spritelist'
                pass


        #try:
        #    #arcade.draw_text("Simple line of text in 12 point", self.baz.pos_XY[0] + DECTEXT, self.baz.pos_XY[1], arcade.color.GREEN, 20)
        #    arcade.draw_text(f" {self.baz}  size {sys.getsizeof(self.baz)}  ", self.baz.pos_XY[0] + DECTEXT, self.baz.pos_XY[1], arcade.color.GREEN, 20)

        #except AttributeError: # AttributeError: 'MyGame' object has no attribute 'baz'
        #    pass

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


        elif key == arcade.key.X:
            #self.vraifaux = bool()

            print("\n      /////////////////////////////////////////////////////////////// key release X //////////////////////////   \n")
            baz = Foobar()

            self.memobjs_data.append(baz)

            #baz2 = Foobar()
            #baz3 = Foobar()
            #baz4 = Foobar()
            #baz5 = Foobar()
            #baz6 = Foobar()


            print(f">>  baz  id {id(baz)}  sys.getsizeof(baz)  {sys.getsizeof(baz)}  mini {self.mini_id(baz)}")

            #print(f">> baz2  id {id(baz2)}  sys.getsizeof(baz)  {sys.getsizeof(baz2)}  mini {self.mini_id(baz2)}")
            #print(f">> baz3  id {id(baz3)}  sys.getsizeof(baz)  {sys.getsizeof(baz3)}  mini {self.mini_id(baz3)}")
            #print(f">> baz4  id {id(baz4)}  sys.getsizeof(baz)  {sys.getsizeof(baz4)}  mini {self.mini_id(baz4)}")
            #print(f">> baz5  id {id(baz5)}  sys.getsizeof(baz)  {sys.getsizeof(baz5)}  mini {self.mini_id(baz5)}")
            #print(f">> baz6  id {id(baz6)}  sys.getsizeof(baz)  {sys.getsizeof(baz6)}  mini {self.mini_id(baz6)}")

            #self.baz = baz

            #print(f">>> self.baz  id {id(self.baz)}  sys.getsizeof(self.baz)  {sys.getsizeof(self.baz)}  mini {self.mini_id(self.baz)}")

            
            #print("self.baz = Foobar() on X release !")

            #print(f" self.baz {self.baz}    if {id(self.baz)}   mini {self.mini_id(self.baz)}")



            memobj = arcade.Sprite("./resources/images/items/logo_python.png", TILE_SCALING)
            memobj.center_x = baz.pos_XY[0]
            memobj.center_y = baz.pos_XY[1]
            self.scene.add_sprite("Memobjs_spritelist", memobj)

            


            

        elif key == arcade.key.I:

            print(" \n Introspection with I key release \n")
            


            for k,v in self.__dict__.items():

                


                if hasattr(v, 'tag'):
                
                    print(k, " -> ",v)
                    print(f"k  {k}    type{type(k)}      v  {v}      id  {id(v)}        type{type(v)}      hexid {hex(id(v))}    pos_XY {v.pos_XY} ")

                else:
                    #print('§')
                    pass







    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, 0.2)

    def update(self, delta_time):
        """Movement and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS, LAYER_NAME_BACKGROUND]
        )

        # Update walls, used with moving platforms
        self.scene.update([LAYER_NAME_MOVING_PLATFORMS])

        # See if the wall hit a boundary and needs to reverse direction.
        for wall in self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS):

            if (
                wall.boundary_right
                and wall.right > wall.boundary_right
                and wall.change_x > 0
            ):
                wall.change_x *= -1
            if (
                wall.boundary_left
                and wall.left < wall.boundary_left
                and wall.change_x < 0
            ):
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if (
                wall.boundary_bottom
                and wall.bottom < wall.boundary_bottom
                and wall.change_y < 0
            ):
                wall.change_y *= -1

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_COINS)
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:

            # Figure out how many points this coin is worth
            if "Points" not in coin.properties:
                print("Warning, collected a coing without a Points property.")
            else:
                points = int(coin.properties["Points"])
                self.score += points

            # Remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        # Position the camera
        self.center_camera_to_player()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    
    arcade.run()


if __name__ == "__main__":
    main()