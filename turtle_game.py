#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random

from constants import *

FPS = 30
WIDTH, HEIGHT = 800, 600

# def draw(self):
#     self.sprites.update()
#     self.sprites.draw(self.screen)

#     self.trash_items.update()
#     self.trash_items.draw(self.screen)

#     self.players.update()
#     self.players.draw(self.screen)

#     pygame.display.flip()

class Button(pygame.sprite.Sprite):
    """The buttons that control the game"""
    def __init__(self, button_type):
        super().__init__()

        self.button_type = button_type
        
        self.images = {}
        self.images[START_BUTTON] = pygame.image.load("assets/start_button.png")
        self.images[HOW_TO_PLAY_BUTTON] = pygame.image.load("assets/how_to_play_button.png")  
        self.images[PLAY_AGAIN_BUTTON] = pygame.image.load("assets/play_again_button.png")

        self.image = self.images[button_type]

        self.rect = self.image.get_rect()


    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2


class Backdrop(pygame.sprite.Sprite):
    """An object that holds the background of the scene"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/oceanfloor.png")

        self.rect = self.image.get_rect()

        self.x = WIDTH / 2
        self.y = HEIGHT / 2

    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2


    def update(self):
        self.set_pos(self.x - 1, self.y)

        if self.x == WIDTH / 2 - WIDTH:
            self.set_pos(WIDTH / 2 + WIDTH, self.y)

    
class Trash(pygame.sprite.Sprite):
    """Items of trash"""
    def __init__(self, trash_type):
        super().__init__()

        self.trash_type = trash_type
        self.trash_speed = 4

        self.trash_types = [
            "bottle", "trash", "can", "straw", "paper"
        ]

        self.images = {}
        self.images["bottle"] = pygame.image.load("assets/bottle.png")
        self.images["trash"] = pygame.image.load("assets/trash.png")
        self.images["can"] = pygame.image.load("assets/can.png")
        self.images["straw"] = pygame.image.load("assets/straw.png")
        self.images["paper"] = pygame.image.load("assets/paper.png")

        self.image = self.images[self.trash_type]

        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()


    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2


    def update(self):
        self.set_pos(self.x - self.trash_speed, self.y)

        if self.x > WIDTH:
            self.kill()



class Character(pygame.sprite.Sprite):
    """Main character for our demo"""
    def __init__(self, input_dict):
        super().__init__()

        self.input = input_dict

        self.images = {}
        self.images["right"] = pygame.image.load(
            "assets/turtle1.png"
        )

        self.image = self.images["right"]

        self.rect = self.image.get_rect()

        self.collisionrect = self.image.get_rect()
        self.collisionrect.x + 5
        self.collisionrect.w -= 20
        self.collisionrect.h -= 30

        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.ax, self.ay = 0, 0

        self.a = 2.4
        self.drag = 0.22
        self.min_vel = 0.2
        self.max_vel = 12.0

        self.set_pos(self.x, self.y)
    

    def set_pos(self, x, y):
        """Sets the character's position with correct origin"""
        self.x, self.y = x, y

        # self.rect.x = self.rect.w / 10

        self.rect.y = y - self.rect.h / 2
        self.collisionrect.y = self.rect.y - 4


    def handle_input(self):
        """Calculates acceleration based on input values"""
        self.ax, self.ay = 0, 0

        if self.input["up"]:
            self.ay -= self.a
        if self.input["down"]:
            self.ay += self.a
        if self.input["left"]:
            self.ax -= self.a
        if self.input["right"]:
            self.ax += self.a
        

    def apply_acceleration(self):
        """Calculates the acceleration based on velocity"""
        self.vx += self.ax
        self.vy += self.ay
        

    def apply_drag(self):
        """Calculates the effect of drag on velocity"""
        self.vx *= 1 - self.drag
        self.vy *= 1 - self.drag


    def apply_velocity(self):
        """Updates position based on constrained velocity"""
        if -self.min_vel < self.vx < self.min_vel:
            self.vx = 0
        if -self.min_vel < self.vy < self.min_vel:
            self.vy = 0

        if self.vx < -self.max_vel:
            self.vx = -self.max_vel
        elif self.vx > self.max_vel:
            self.vx = self.max_vel

        self.set_pos(self.x + self.vx, self.y + self.vy)


    def update_animation(self):
        """Changes character's appearance for animation"""
        if self.vx > 0:
            self.image = self.images["right"]
        elif self.vx < 0:
            self.image = self.images["left"]
    

    def update(self):
        """Updates character sprite"""
        self.handle_input()

        self.apply_acceleration()
        self.apply_drag()
        self.apply_velocity()

        self.update_animation()


class Game():
    def __init__(self):
        pygame.init()

        self.trash_types = [
            "bottle", "trash", "can", "straw", "paper"
        ]


        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.score = 0

        self.running = True

        self.timer = 0
        self.time_limit = 20

        self.game_section = TITLE

        self.input = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.backdrop1 = Backdrop()
        self.backdrop1.set_pos(WIDTH / 2, HEIGHT / 2)

        self.backdrop2 = Backdrop()
        self.backdrop2.set_pos(WIDTH / 2 + WIDTH, HEIGHT / 2)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.backdrop1)
        self.sprites.add(self.backdrop2)

        self.character = Character(self.input)
        self.character.set_pos(-80, HEIGHT / 2)

        self.players = pygame.sprite.Group()
        self.sprites.add(self.character)
        
        self.trash_items = pygame.sprite.Group()

        self.title_buttons = pygame.sprite.Group()
        

        self.start_button = Button(START_BUTTON)
        self.start_button.set_pos(WIDTH / 2, HEIGHT / 2)
        
        self.how_to_play_button = Button(HOW_TO_PLAY_BUTTON)
        self.how_to_play_button.set_pos(WIDTH / 2, HEIGHT / 2)

        self.title_buttons.add(self.start_button)
        self.title_buttons.add(self.how_to_play_button)

        self.play_again_button = Button(PLAY_AGAIN_BUTTON)
        self.play_again_button.set_pos(WIDTH / 2, HEIGHT / 2)


    def update(self):
        """Updates the game"""
        self.clock.tick(FPS)

        self.handle_input()
        self.sprites.update()
        self.update_trash()

        self.draw()

        pygame.display.flip()


    def draw(self):
        self.sprites.update()
        self.sprites.draw(self.screen)

        self.trash_items.update()
        self.trash_items.draw(self.screen)

        self.players.update()
        self.players.draw(self.screen)

        pygame.display.flip()


    def update_trash(self):
        if self.timer >= self.time_limit:
            self.timer = 0
            trash_piece = Trash(random.choice(self.trash_types))
            trash_piece.set_pos(800, random.randint(0, WIDTH))

            self.trash_items.add(trash_piece)
        else:
            self.timer += 1

        for trash_item in self.trash_items:
            if trash_item.rect.colliderect(self.character.collisionrect):
                self.score += 10
                trash_item.kill()
                print(self.score)


    def handle_input(self):
        """Updates the input dictionary"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_w:
                    self.input["up"] = True
                elif event.key == pygame.K_s:
                    self.input["down"] = True
                # elif event.key == pygame.K_a:
                #     self.input["left"] = True
                # elif event.key == pygame.K_d:
                #     self.input["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.input["up"] = False
                elif event.key == pygame.K_s:
                    self.input["down"] = False
                # elif event.key == pygame.K_a:
                #     self.input["left"] = False
                # elif event.key == pygame.K_d:
                #     self.input["right"] = False

# def __init__(self, pos):
#     walls.append(self)
#     self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
#     self.image = pygame.image.load("coral1.jpg")



def main():
    """Main entry point for script"""
    game = Game()

    while game.running:
        game.update()


if __name__ == '__main__':
    main()