# Name: Jared Ramirez
# Date: 11/292025
# Assignment 7 starter code
# Project description: I have created and completed a game of The Legend of Zelda, where I had to utilize my previous project
# assignments (4 & 6) to help me create the game. Also, I added a cucco sprite to this game that attacks link after colliding with it 5 times.

import pygame
import time
import json
import math

from pygame.locals import*
from time import sleep


class Sprite():
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 1
        self.valid = True
        self.image = pygame.image.load(image)

    def update(self):
        return self.valid

    def is_link(self):
        return False
    
    def is_tree(self):
        return False
    
    def is_treasurechest(self):
        return False
    
    def is_boomerang(self):
        return False

    def is_cucco(self):
        return False

    def when_contact(self):
        pass

    def collect(self):
        pass

    def is_closed(self):
        return False

    def is_collectable(self):
        return False

    def check_if_overlapping(self, other):
        return (
            self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y
        )

    # for the starter code, we assume that all Sprites of a certain
    # type are the same size, and thus don't need w and h saved
    # However, it would be very easy to add more attributes to be 
    # saved here!
    def marshal(self):
        return {
            "x": self.x,
            "y": self.y
        }

class Tree(Sprite):
    # variables that belong to the class, not to a specific
    # instance of the class - this is similar to Java's static variables
    TREE_HEIGHT = 75
    TREE_WIDTH = 75
    tree_image = None
    
    def __init__(self, x, y):
        if Tree.tree_image is None:
            Tree.tree_image = pygame.image.load("images/tree.png")
        super().__init__(x, y, Tree.TREE_WIDTH, Tree.TREE_HEIGHT, "images/tree.png")
    
    def update(self):
        return True

    def is_tree(self):
        return True

    def marshal(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h
        }
    
    def check_if_overlapping(self, other):
        return (
            self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y
        )

class Link(Sprite):
    LINK_WIDTH = 65
    LINK_HEIGHT = 65
    COLLISION_SPACE = 1
    link_images = None
    
    def __init__(self, x, y):
        super().__init__(x, y, Link.LINK_HEIGHT, Link.LINK_WIDTH, "images/link1.png")
        self.px = x
        self.py = y
        self.speed = 10
        self.current_link_frame = 0
        # 0 down, 1 left, 2 right, 3 up
        self.link_direction = 1
        self.num_directions = 4
        self.max_images_per_direction = 11
        self.rupees_collected = 0

        if Link.link_images is None:
            Link.link_images = []
            index = 1
            for i in range(self.num_directions):
                direction_images = []
                for j in range(self.max_images_per_direction):
                    # instead of push its append
                    direction_images.append(pygame.image.load("images/link" + str(index) + ".png"))
                    index += 1
                Link.link_images.append(direction_images)
        self.image = Link.link_images[self.link_direction][self.current_link_frame]

    def update(self):
        return True

    def save_previous_position(self):
        self.px = self.x
        self.py = self.y

    def move_yourself(self, direction):
        self.current_link_frame += 1
        if self.current_link_frame >= self.max_images_per_direction:
            self.current_link_frame = 0
        if direction == "left":
            self.x -= self.speed
            self.link_direction = 1
        elif direction == "right":
            self.x += self.speed
            self.link_direction = 2
        elif direction == "down":
            self.y += self.speed
            self.link_direction = 0
        elif direction == "up":
            self.y -= self.speed
            self.link_direction = 3
        
        # I have to update the current image i'm on
        self.image = Link.link_images[self.link_direction][self.current_link_frame]

    def get_link_direction(self):
        return self.link_direction

    def fix_collision(self, other):
        if (self.px + self.w <= other.x) and (self.x + self.w >= other.x):
            self.x = other.x - self.w - Link.COLLISION_SPACE
        elif (self.px >= other.x + other.w) and (self.x <= other.x + other.w):
            self.x = other.x + other.w + Link.COLLISION_SPACE
        # I'll sperate these two into two different if statements so its easier to read
        if (self.py + self.h <= other.y) and (self.y + self.h >= other.y):
            self.y = other.y - self.h - Link.COLLISION_SPACE
        elif (self.py >= other.y + other.h) and (self.y <= other.y + other.h):
            self.y = other.y + other.h + Link.COLLISION_SPACE

    def is_link(self):
        return True

    def marshal(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h
        }

class TreasureChest(Sprite):
    CHEST_W = 50
    CHEST_H = 50
    chest_image = None
    rupee_item = None
    RUPEE_FRAME_TIMER = 5
    RUPEE_EXPIRE_TIMER = 40

    def __init__(self, x, y):
        super().__init__(x, y, TreasureChest.CHEST_H, TreasureChest.CHEST_W, "images/treasurechest.png")
        self.is_open = False
        self.rupee_frame_timer = 0
        self.rupee_expire_timer = 0

        if TreasureChest.chest_image is None:
            TreasureChest.chest_image = pygame.image.load("images/treasurechest.png")
        if TreasureChest.rupee_item is None:
            TreasureChest.rupee_item = pygame.image.load("images/rupee.png")

    def update(self):
        if self.is_open:
            if self.rupee_frame_timer > 0:
                self.rupee_frame_timer -= 1
            if self.rupee_expire_timer > 0:
                self.rupee_expire_timer -= 1
        
        # condition return for chest being open and timer expires 'false'
        # not is an option to write within python
        return not (self.is_open and self.rupee_expire_timer == 0)

    def is_closed(self):
        return not self.is_open

    def is_collectable(self):
        return self.is_open and self.rupee_frame_timer == 0

    def when_contact(self):
        if not self.is_open:
            self.is_open = True
            self.rupee_frame_timer = TreasureChest.RUPEE_FRAME_TIMER
            self.rupee_expire_timer = TreasureChest.RUPEE_EXPIRE_TIMER
            if TreasureChest.rupee_item:
                self.image = TreasureChest.rupee_item
        
    def collect(self):
        if self.is_open and self.rupee_frame_timer == 0:
            self.rupee_expire_timer = 0

    def is_treasurechest(self):
        return True

    def marshal(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h
        }

class Boomerang(Sprite):
    BOOMERANG_H = 25
    BOOMERANG_W = 25
    boomerang_images = None

    def __init__(self, x, y, direction):
        super().__init__(x, y, Boomerang.BOOMERANG_H, Boomerang.BOOMERANG_W, "images/boomerang1.png")
        self.speed = 12

       # animating the boomerang frames like in js
        if Boomerang.boomerang_images is None:
            Boomerang.boomerang_images = []
            for i in range(1, 5):  
                Boomerang.boomerang_images.append(pygame.image.load("images/boomerang" + str(i) + ".png"))
        self.current_frame = 0
        self.frame_counter = 0
        
        # Set initial image
        self.image = Boomerang.boomerang_images[self.current_frame]

        # fly direction 0 D, 1 L, 2 R, 3 U
        if direction == 0:
            self.dx = 0
            self.dy = 1
        elif direction == 1:
            self.dx = -1
            self.dy = 0
        elif direction == 2:
            self.dx = 1
            self.dy = 0
        elif direction == 3:
            self.dx = 0
            self.dy = -1
        
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= 5:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % 4
            self.image = Boomerang.boomerang_images[self.current_frame]
        
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        return True

    def is_boomerang(self):
        return True

    def marshal(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h
        }

class Cucco(Sprite):
    CUCCO_H = 50
    CUCCO_W = 50

    num_cucco = 0
    angry = False
    num_hits = 0
    disappeared = 0
    linkx = 0
    linky = 0
    happy_images = None
    angry_images = None

    def __init__(self, x, y):
        super().__init__(x, y, Cucco.CUCCO_H, Cucco.CUCCO_W, "images/cucco1.png")
        self.px = x
        self.py = y

        if Cucco.happy_images is None:
            Cucco.happy_images = []
            Cucco.happy_images.append(pygame.image.load("images/cucco1.png"))
            Cucco.happy_images.append(pygame.image.load("images/cucco2.png"))
            Cucco.happy_images.append(pygame.image.load("images/cucco3.png"))
            Cucco.happy_images.append(pygame.image.load("images/cucco4.png"))

        if Cucco.angry_images is None:
            Cucco.angry_images = []
            Cucco.angry_images.append(pygame.image.load("images/angrycucco1.png"))
            Cucco.angry_images.append(pygame.image.load("images/angrycucco2.png"))
            Cucco.angry_images.append(pygame.image.load("images/angrycucco3.png"))
            Cucco.angry_images.append(pygame.image.load("images/angrycucco4.png"))

        # Now i have to declare my variables similar as link
        # xdir and ydir are similar to boomerang's
        self.xdir = 1
        self.ydir = 1
        self.direction = 0
        self.current_frame = 0
        self.frame_counter = 0
        self.attraction_to_link = False
        # imma need a timer like in chest but for the cuccos to attack link
        self.attraction_to_link_timer = 0
        self.speed = 3
        self.angry_speed = 9

        self.image = Cucco.happy_images[self.direction * 2 + self.current_frame]
        Cucco.num_cucco += 1
    
    def update(self):
        # I need to take cucco's previous position before updating since i'm going to need it for collision
        # and for a "hard fix/reset" later
        self.px = self.x
        self.py = self.y

        # the first update logic will be the cucco's angry reset
        if Cucco.num_cucco == 1 or Cucco.disappeared >= 3:
            Cucco.angry = False
            Cucco.num_hits = 0
            Cucco.disappeared = 0

        # then I should update my animation frames before setting my image "state"
        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % 2
        # image state
        if Cucco.angry:
            image_list = Cucco.angry_images
        else:
            image_list = Cucco.happy_images
        self.image = image_list[self.direction * 2 + self.current_frame]

        # set my attack time logic to be attached to link "DONT FORGET TO INDENT CODE
        if self.attraction_to_link:
            # this should follow link
            self.x = Cucco.linkx - self.w // 2
            self.y = Cucco.linky - self.h // 2
            self.attraction_to_link_timer -= 1
            if self.attraction_to_link_timer <= 0:
                self.valid = False
                Cucco.num_cucco -= 1
                Cucco.disappeared += 1
                return False
            return True

        # this will be my cuccos's standard movement logic
        if not Cucco.angry:
            self.x += self.xdir * self.speed
            self.y += self.ydir * self.speed
            # for xdir 0 = L and 1 = R
            if self.xdir < 0:
                self.direction = 0
            else:
                self.direction = 1
            # now when angry
        else:
            dx = Cucco.linkx - self.x
            dy = Cucco.linky - self.y
            length = math.sqrt((dx * dx) + (dy * dy))
            if length < 0.001:
                length = 0.001
            direction_to_go_x = dx / length
            direction_to_go_y = dy / length
            self.x += direction_to_go_x * self.angry_speed
            self.y += direction_to_go_y * self.angry_speed

            # thhis will help me redirect direction based on movement (0 = L, 1 = R)
            if direction_to_go_x < 0:
                self.direction = 0
            else:
                self.direction = 1
        return True

    # I have to adjust cuccos collsion boundary when angry
    def fix_collision(self, other):
        # When angry don't collide with other sprites
        if Cucco.angry:
            return

        # hard code test fixing to see if the cucco collision is being handled properly
        collision_is_handled = False

        if (self.px + self.w <= other.x) and (self.x + self.w >= other.x):
            self.x = other.x - self.w
            # this should technically bounce
            self.xdir = -self.xdir
            # redirect facing based on xdir
            if self.xdir < 0:
                self.direction = 0
            else:
                self.direction = 1
            collision_is_handled = True

        elif (self.px >= other.x + other.w) and (self.x <= other.x + other.w):
            self.x = other.x + other.w
            self.xdir = -self.xdir
            # redirect based on new xdir
            if self.xdir < 0:
                self.direction = 0
            else:
                self.direction = 1
            collision_is_handled = True

        # now top and bottom
        if (self.py + self.h <= other.y) and (self.y + self.h >= other.y):
            self.y = other.y - self.h
            self.ydir = -self.ydir
            collision_is_handled = True

        elif (self.py >= other.y + other.h) and (self.py <= other.y + other.h):
            self.y = other.y + other.h
            self.ydir = -self.ydir
            collision_is_handled = True

        # I'm going to have to hard code this fix since I can't get the cuccos to collide with trees nor chests
        # after colliding with link
        if not collision_is_handled:
            overlaps_left = (self.x + self.w) - other.x
            overlaps_right = (other.x + other.w) - self.x
            overlaps_top = (self.y + self.h) - other.y
            overlaps_bottom = (other.y + other.h) - self.y
            
            # this should help me figure out where the smallest overlap is
            # Ive just reappleid min from the javascript project we had to do
            min_overlaps = min(overlaps_left, overlaps_right, overlaps_top, overlaps_bottom)
            # this should redirect the cucco to its direction and reverse the speed back to normal
            if min_overlaps == overlaps_left:
                self.x = other.x - self.w
                # Force bounce left
                self.xdir = -1
                self.direction = 0
            elif min_overlaps == overlaps_right:
                self.x = other.x + other.w
                # Force bounce right
                self.xdir = 1
                self.direction = 1
            elif min_overlaps == overlaps_top:
                # Force bounce up
                self.y = other.y - self.h
                self.ydir = -1
            elif min_overlaps == overlaps_bottom:
                # Force bounce down
                self.y = other.y + other.h
                self.ydir = 1 

    def is_cucco(self):
        return True

    def marshal(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h
        }

            
class Model():
    filename = "map.json"
    
    def __init__(self):
        self.sprites = []
        self.link = Link(485, 395)
        self.sprites.append(self.link)
        self.items_i_can_add = []
        self.items_i_can_add.append(Tree(0, 0))
        self.items_i_can_add.append(TreasureChest(0, 0))
        self.items_i_can_add.append(Cucco(0, 0))
        self.item_num = 0

        self.load_map()

    def load_map(self):
        # reset the fish count if we're loading (or reloading)
        # the map
        # Fish.reset_fish()
        View.current_room_x = 0
        View.current_room_y = 0
        
        self.sprites = [self.link]
        # example of adding a hardcoded fish
        # self.sprites.append(Fish(200,100,Fish.FISH_WIDTH, Fish.FISH_HEIGHT))

        try:
            with open(Model.filename) as file:
                data = json.load(file)

                # This will aid me in loading link position
                # Reminder, I lazy loaded link earlier
                if "linkX" in data and "linkY" in data:
                    self.link.x = data["linkX"]
                    self.link.y = data["linkY"]
                    self.link.px = data["linkX"]
                    self.link.py = data["linkY"]

                # now trees
                if "trees" in data:
                    for entry in data["trees"]:
                        tree = Tree(entry["x"], entry["y"])
                        self.sprites.append(tree)

                # same for the chest
                if "treasurechest" in data:
                    for entry in data["treasurechest"]:
                        chest = TreasureChest(entry["x"], entry["y"])
                        self.sprites.append(chest)
                
                # same for cucos
                if "cuccos" in data:
                    Cucco.num_cucco = 0 # reset the cucco count
                    for entry in data["cuccos"]:
                        cucco = Cucco(entry["x"], entry["y"])
                        self.sprites.append(cucco)

        except FileNotFoundError:
            # if the file cant be found, we just makea defaullt map
            pass      

    def save_map(self):
        # create lists for each type of sprite you want to save
        trees = []
        chests = []
        cuccos = []

        # go through all sprites availabe
        for s in self.sprites:
            if s.is_tree():
                trees.append(s.marshal())
            elif s.is_treasurechest():
                chests.append(s.marshal())
            elif s.is_cucco():
                cuccos.append(s.marshal())

        map_to_save = {
            "linkX": self.link.x,
            "linkY": self.link.y,
            "trees": trees,
            "treasurechest": chests,
            "cuccos": cuccos
        }

        # Save to file
        with open(Model.filename, "w") as f:
            json.dump(map_to_save, f)

    def update(self):
        # this will save link's prev position
        #self.link.save_previous_position()

        # then I have to update all the sprites and get rid of the ones that are no longer valid
        sprites_to_remove = []

        # condition so not all cuccos are removed and 1 is left
        cuccos_remaining = sum(1 for s in self.sprites if s.is_cucco())
        for sprite in self.sprites:
            if not sprite.update():
                if not sprite.is_link():
                    if sprite.is_cucco():
                        if cuccos_remaining <= 1:
                            sprite.valid = True
                            # the '.valid = True' means dont remove the LAST remaining cucco
                            continue
                        cuccos_remaining -= 1
                    sprites_to_remove.append(sprite)

        for sprite in sprites_to_remove:
            self.sprites.remove(sprite)

        # I have to collsion check link
        for sprite in self.sprites:
            if sprite.is_link():
                continue

            if sprite.is_tree():
                if self.check_collision(self.link, sprite):
                    self.link.fix_collision(sprite)
            
            elif sprite.is_treasurechest():
                if self.check_collision(self.link, sprite):
                    self.link.fix_collision(sprite)

                    if sprite.is_closed():
                        sprite.when_contact()
                    elif sprite.is_collectable():
                        sprite.collect()
                        self.link.rupees_collected += 1

        # check the collisions with boomerang
        boomerang_to_remove = []
        for sprite in self.sprites:
            if not sprite.is_boomerang():
                continue

            for other in self.sprites:
                if other.is_tree() and self.check_collision(sprite, other):
                    boomerang_to_remove.append(sprite)
                    break
                elif other.is_treasurechest() and self.check_collision(sprite, other):
                    if other.is_closed():
                        other.when_contact()
                    elif other.is_collectable():
                        other.collect()
                        self.link.rupees_collected += 1
                    boomerang_to_remove.append(sprite)
                    break

        for boomerang in boomerang_to_remove:
            self.sprites.remove(boomerang)
        
        # checking for cucco collisions
        for sprite in self.sprites:
            if not sprite.is_cucco():
                continue

            for other in self.sprites:
                if sprite == other:
                    continue
                #Collision with tree or chest redirection WHEN NOT ANGRY
                if not Cucco.angry and (other.is_tree() or other.is_treasurechest()) and self.check_collision(sprite, other):
                    sprite.fix_collision(other)
                # collsion check w/link
                elif other.is_link() and self.check_collision(sprite, other):
                    # cuccos state happy vs angry
                    if sprite.attraction_to_link:
                        sprite.x = other.x
                        sprite.y = other.y
                    elif not sprite.attraction_to_link:
                        Cucco.num_hits += 1
                        if Cucco.num_hits >= 5 and Cucco.num_cucco > 1:
                            Cucco.angry = True
                        if Cucco.angry:
                            sprite.attraction_to_link = True
                            sprite.attraction_to_link_timer = 20
                            sprite.x = other.x
                            sprite.y = other.y
                        else:
                            # im bored and tired
                            sprite.fix_collision(other)

                # my num_hit logic should increase when colliding with link or boomerang
                elif other.is_boomerang() and self.check_collision(sprite, other):
                    Cucco.num_hits += 1
                    sprite.fix_collision(other)
                    if Cucco.num_hits >= 5 and Cucco.num_cucco > 1:
                        Cucco.angry = True
                
        # checking my room boundaries
        self.check_room_shift()

    def check_room_shift(self):
        room_left = View.get_current_room_x()
        room_right = View.get_current_room_x() + View.room_w
        room_up = View.get_current_room_y()
        room_down = View.get_current_room_y() + View.room_h
        
        if self.link.x < room_left:
            View.move_room_left()
            new_room_right = View.get_current_room_x() + View.room_w
            self.link.x = new_room_right - self.link.w
        elif self.link.x + self.link.w > room_right:
            View.move_room_right()
            new_room_left = View.get_current_room_x()
            self.link.x = new_room_left
        
        if self.link.y < room_up:
            View.move_room_up()
            new_room_down = View.get_current_room_y() + View.room_h
            self.link.y = new_room_down - self.link.h
        elif self.link.y + self.link.h > room_down:
            View.move_room_down()
            new_room_up = View.get_current_room_y()
            self.link.y = new_room_up

    def check_collision(self, sprite_a, sprite_b):
        if sprite_a.x > sprite_b.x + sprite_b.w:
            return False
        if sprite_a.x + sprite_a.w < sprite_b.x:
            return False
        if sprite_a.y > sprite_b.y + sprite_b.h:
            return False
        if sprite_a.y + sprite_a.h < sprite_b.y:
            return False
        return True

    def clear_map(self):
 
        # standard room scroll_position
        View.current_room_x = 0
        View.current_room_y = 0
        # If I dont reset the cucco counters, the game will eventually crash, unforunately
        Cucco.num_cucco = 0
        Cucco.angry = False
        Cucco.num_hits = 0
        Cucco.disappeared = 0
        self.sprites = [self.link]

    # pos was passed as the mouse position tuple - pos[0] is x, 
    # pos[1] is y
    def add_tree(self, x, y):
        new_tree = Tree(x, y)

        # Overlapping checkshould happen here
        for sprite in self.sprites:
            if new_tree.check_if_overlapping(sprite):
                return False
        self.sprites.append(new_tree)
        return True

    def add_chest(self, x, y):
        new_chest = TreasureChest(x, y)
        for sprite in self.sprites:
            if (new_chest.x < sprite.x + sprite.w and
                new_chest.x + new_chest.w > sprite.x and
                new_chest.y < sprite.y + sprite.h and
                new_chest.y + new_chest.h > sprite.y):
                return False
        self.sprites.append(new_chest)
        return True
    
    def add_boomerang(self):
                # in python // stands for floor division while / stands for regular division W3sxhools
        link_center_x = self.link.x + self.link.w // 2
        link_center_y = self.link.y + self.link.h // 2
        bx = link_center_x - Boomerang.BOOMERANG_W // 2
        by = link_center_y - Boomerang.BOOMERANG_H // 2
        new_boomerang = Boomerang(bx, by, self.link.get_link_direction())
        self.sprites.append(new_boomerang)

    def loop_item(self):
        self.item_num = (self.item_num + 1) % len(self.items_i_can_add)
    
    # ill have two "getters" to get the current item and its num
    def get_current_item(self):
        return self.items_i_can_add[self.item_num]

    def get_current_item_num(self):
        return self.item_num

    def add_my_item(self, x, y):
        select = self.items_i_can_add[self.item_num]
        new_item = None
        is_cucco = False
        if select.is_tree():
            new_item = Tree(x, y)
        elif select.is_treasurechest():
            new_item = TreasureChest(x, y)
        elif select.is_cucco():
            new_item = Cucco(x, y)
            is_cucco = True
        # ill check for overlap
        if new_item != None:
            can_add = True
            for sprite in self.sprites:
                if new_item.check_if_overlapping(sprite):
                    can_add = False
                    break
            if can_add:
                self.sprites.append(new_item)
            elif is_cucco:
                Cucco.num_cucco -= 1



class View():
    # rrom tracking from javascript
    current_room_x = 0
    current_room_y = 0
    room_w = 800
    room_h = 600
    
    def __init__(self, model):
        SCREEN_SIZE = (800,600)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 32)
        self.model = model
    
    @staticmethod
    def get_current_room_x():
        return View.current_room_x
    
    @staticmethod
    def get_current_room_y():
        return View.current_room_y
    
    @staticmethod
    def move_room_left():
        View.current_room_x = max(0, View.current_room_x - View.room_w)
        print("Moved left, current room is:", View.current_room_x)
    
    @staticmethod
    def move_room_right():
        View.current_room_x = View.current_room_x + View.room_w
        print("Moved right, current room is:", View.current_room_x)
    
    @staticmethod
    def move_room_up():
        View.current_room_y = max(0, View.current_room_y - View.room_h)
        print("Moved up, current room is:", View.current_room_y)
    
    @staticmethod
    def move_room_down():
        View.current_room_y = View.current_room_y + View.room_h
        print("Moved down, current room is:", View.current_room_y)

    def update(self):
        # change background color if the user is in edit_mode
        if Controller.edit_mode:
            self.screen.fill([146, 203, 146]) #light green
        else:
            self.screen.fill([72, 152, 72]) #dark forest green

        # drawing thr sprites to my game screen
        scroll_x = View.current_room_x
        scroll_y = View.current_room_y
        
        for sprite in self.model.sprites:
            if sprite.is_link():
                location = (sprite.x - scroll_x, sprite.y - scroll_y)
                size = (sprite.w, sprite.h)
                self.screen.blit(pygame.transform.scale(sprite.image, size), location)
            elif sprite.is_treasurechest():
                location = (sprite.x - scroll_x, sprite.y - scroll_y)
                size = (sprite.w, sprite.h)
                if sprite.is_open:
                    image = TreasureChest.rupee_item if TreasureChest.rupee_item else sprite.image
                else:
                    image = TreasureChest.chest_image if TreasureChest.chest_image else sprite.image
                self.screen.blit(pygame.transform.scale(image, size), location)
            elif sprite.is_cucco():
                location = (sprite.x - scroll_x, sprite.y - scroll_y)
                size = (sprite.w, sprite.h)
                self.screen.blit(pygame.transform.scale(sprite.image, size), location)
            else:
                location = (sprite.x - scroll_x, sprite.y - scroll_y)
                size = (sprite.w, sprite.h)
                self.screen.blit(pygame.transform.scale(sprite.image, size), location)

        # Draw mode context
        if Controller.edit_mode:
            # Draw mu green box
            GREEN_BOX_COLOR = (76,187, 23)
            BOX_SIZE = 100
            pygame.draw.rect(self.screen, GREEN_BOX_COLOR, (0, 0, BOX_SIZE, BOX_SIZE))
            
            # show the sprite in the box
            current_item = self.model.get_current_item()
            if current_item.is_tree():
                item_showcase = Tree(0, 0)
                # similar to assignment 4 image should be centered this time asw ell
                item_showcase_x = (BOX_SIZE - item_showcase.w) // 2
                item_showcase_y = (BOX_SIZE - item_showcase.h) // 2
                item_showcase_location = (item_showcase_x, item_showcase_y)
                item_showcase_size = (item_showcase.w, item_showcase.h)
                self.screen.blit(pygame.transform.scale(item_showcase.image, item_showcase_size), item_showcase_location)
            elif current_item.is_treasurechest():
                item_showcase = TreasureChest(0, 0)
                item_showcase_x = (BOX_SIZE - item_showcase.w) // 2
                item_showcase_y = (BOX_SIZE - item_showcase.h) // 2
                item_showcase_location = (item_showcase_x, item_showcase_y)
                item_showcase_size = (item_showcase.w, item_showcase.h)
                item_showcase_image = TreasureChest.chest_image if TreasureChest.chest_image else item_showcase.image
                self.screen.blit(pygame.transform.scale(item_showcase_image, item_showcase_size), item_showcase_location)
            elif current_item.is_cucco():
                item_showcase = Cucco(0, 0)
                item_showcase_x = (BOX_SIZE - item_showcase.w) // 2
                item_showcase_y = (BOX_SIZE - item_showcase.h) // 2
                item_showcase_location = (item_showcase_x, item_showcase_y)
                item_showcase_size = (item_showcase.w, item_showcase.h)
                self.screen.blit(pygame.transform.scale(item_showcase.image, item_showcase_size), item_showcase_location)
        
        # ruppe counter at the top of screen
        font = pygame.font.SysFont(None, 32)
        text_string = "Rupees collected: " + str(self.model.link.rupees_collected)
        WHITE_COLOR_TEXT = (255, 255, 255)
        text_surface = font.render(text_string, True, WHITE_COLOR_TEXT)
        text_width = text_surface.get_width()
        screen_width = self.screen.get_width()
        text_x = (screen_width - text_width) // 2
        text_y = 10
        self.screen.blit(text_surface, (text_x, text_y))
        pygame.display.flip()

class Controller():
    edit_mode = False
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    self.keep_going = False
                elif event.key == K_LEFT:
                    self.key_left = True
                elif event.key == K_RIGHT:
                    self.key_right = True
                elif event.key == K_UP:
                    self.key_up = True
                elif event.key == K_DOWN:
                    self.key_down = True
                elif event.key == K_SPACE:
                    self.model.add_boomerang()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.key_left = False
                elif event.key == K_RIGHT:
                    self.key_right = False
                elif event.key == K_UP:
                    self.key_up = False
                elif event.key == K_DOWN:
                    self.key_down = False
                elif event.key == K_c:
                    self.model.clear_map()
                    print("Map cleared and game reset")
                elif event.key == K_e:
                    Controller.edit_mode = not Controller.edit_mode
                elif event.key == K_l:
                    self.model.load_map()
                    print("Map loaded")
                elif event.key == K_s:
                    self.model.save_map()
                    print("Map saved")
            elif event.type == MOUSEBUTTONUP:
                if Controller.edit_mode:
                    pos = pygame.mouse.get_pos()
                    mouse_x, mouse_y = pos[0], pos[1]
                    # edit box
                    if mouse_x < 100 and mouse_y < 100:
                        # loop through the sprite items
                        self.model.loop_item()
                    else:
                        game_room_x = mouse_x + View.get_current_room_x()
                        game_room_y = mouse_y + View.get_current_room_y()
                        
                        current_item = self.model.get_current_item()
                        if current_item.is_tree():
                            # this will be snap to grid section of the trees
                            grid_size = 75
                            x = (game_room_x // grid_size) * grid_size
                            y = (game_room_y // grid_size) * grid_size
                            self.model.add_my_item(x, y)
                        else:
                            self.model.add_my_item(game_room_x, game_room_y)
        
        # Handle Link movement - save previous position before moving
        if self.key_left or self.key_right or self.key_up or self.key_down:
            self.model.link.save_previous_position()
        
        if self.key_left:
            self.model.link.move_yourself("left")
        if self.key_right:
            self.model.link.move_yourself("right")
        if self.key_up:
            self.model.link.move_yourself("up")
        if self.key_down:
            self.model.link.move_yourself("down")
        
        # I have to give/set link's position to cucco's so they can attack him
        Cucco.linkx = self.model.link.x + self.model.link.w // 2
        Cucco.linky = self.model.link.y + self.model.link.h // 2

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
pygame.font.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye!")