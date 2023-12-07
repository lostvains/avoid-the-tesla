import sys
import time
import random
import pygame
import threading

from operator import eq

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('Avoid the TESLA!')
screen = pygame.display.set_mode([1280, 720])

character = pygame.image.load('assets/character.png')
character_rectangle = character.get_rect()
character_rectangle.x, character_rectangle.y = (character_rectangle.width, 720 - character_rectangle.height)
character_jumping = False
character_jumping_sound = pygame.mixer.Sound('assets/jumping.mp3')

teslas = [
    pygame.image.load(f'assets/tesla_{index}.png')
    for index in range(1, 5)
]
tesla_rectangles = [
    tesla.get_rect()
    for tesla in teslas
]
tesla = None
tesla_spawned = False
tesla_spawning_sound = pygame.mixer.Sound('assets/spawning.mp3')

broke = False
background_music = pygame.mixer.Sound('assets/bgm.mp3')

def spawn_tesla():
    global tesla, tesla_spawned
    if tesla_spawned:
        return None
    else:
        tesla_spawned = True
        def spawning_process():
            tesla_spawning_sound.play()

            global tesla, tesla_spawned
            tesla = random.choice(teslas)
            tesla_rectangle = tesla_rectangles[teslas.index(tesla)]
            tesla_rectangle.x, tesla_rectangle.y = 1280 - tesla_rectangle.width, 720 - tesla_rectangle.height

            while tesla_rectangle.x > - 500:
                tesla_rectangle.x -= random.uniform(1.6, 2.3)
                time.sleep(0.00000001)
            
            delay = random.uniform(1.0, 3.0)
            time.sleep(delay)
            tesla_spawned = False
            tesla = None
            return None
        spawning_thread = threading.Thread(target=spawning_process, daemon=True)
        return spawning_thread.start()

def character_jump():
    global character_jumping
    if character_jumping:
        return None
    else:
        character_jumping = True
        def jumping_process():
            character_jumping_sound.play()

            global character_jumping
            character_rectangle_destination_y = character_rectangle.y

            while character_rectangle.y > character_rectangle_destination_y - 300:
                character_rectangle.y -= random.uniform(1.0, 1.5)
                time.sleep(0.001)

            while character_rectangle.y < character_rectangle_destination_y:
                character_rectangle.y += 0.5
                time.sleep(0.001)
            time.sleep(0.1)

            character_jumping = False
            return None
        jumping_thread = threading.Thread(target=jumping_process, daemon=True)
        return jumping_thread.start()

def give_mental_illness():
    if broke:
        tk = __import__('tkinter', fromlist=['Tk']).Tk
        showinfo = __import__('tkinter.messagebox', fromlist=['showinfo']).showinfo
        root = tk()
        root.withdraw()
        return showinfo('WHAT?!', 'You are NOT able to even complete this SIMPLE game with shitty quality? HOW DARE YOU?!')
    else:
        return None

background_music_channel = background_music.play(-1)
background_music_channel.set_volume(0.25)
while 1:
    for event in pygame.event.get():
        if eq(event.type, pygame.QUIT):
            pygame.quit()
            sys.exit(0)
        elif eq(event.type, pygame.KEYDOWN):
            if any(eq(event.key, key) for key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]):
                character_jump()
    
    screen.fill([255, 255, 255])
    screen.blit(character, character_rectangle)
    spawn_tesla()
    if tesla:
        tesla_rectangle = tesla_rectangles[teslas.index(tesla)]
        screen.blit(tesla, tesla_rectangle)
        if character_rectangle.colliderect(tesla_rectangle):
            broke = True
            give_mental_illness()
            pygame.quit()
            sys.exit(0)
    else:
        print('A tesla has already spawned.')
    pygame.display.flip()
