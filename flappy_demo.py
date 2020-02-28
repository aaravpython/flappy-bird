import pygame
import sys
import time
import random


pygame.init()

size = [700, 700]
WHITE = (255, 255, 255)
pipe_c = (255, 0, 183)

intial_ball_x = 110
intial_ball_y = 350
current_ball_x = intial_ball_x
current_ball_y = intial_ball_y
first_pipe_x = 250

pipe_dx = 150
dy = 1
current_pipes = []


image = pygame.image.load('bird.png')
image = pygame.transform.scale(image,(50,50))
# def draw_circle(x, y):
# pygame.draw.circle(screen, (255, 0, 0), [x, y], 10)


def ball_fall(current_ball_y):
    current_ball_y += dy
    if current_ball_y > size[1]:
        current_ball_y = size[1]
    return current_ball_y


def jump_ball(location):
    location -= dy
    if location < 0:
        location = 0
    return location


def create_pipes():
    for i in range(0, 4):
        if i == 0:
            current_pipes.append(pipe(first_pipe_x, random.randint(0, 330), random.randint(395, 630)))
        else:
            current_pipes.append(pipe(first_pipe_x + (pipe_dx * i), random.randint(70, 330), random.randint(395, 630)))


screen = pygame.display.set_mode(size,pygame.FULLSCREEN)


class pipe:
    def __init__(self, intial_pipe_x, y_1, y_2):
        self.pipe_x = intial_pipe_x
        self.y_1 = y_1
        self.y_2 = y_2


create_pipes()


def is_pipe_out_of_frame(foo):
    return foo.pipe_x < 0


def move_pipe(pipes):
    dx = 1
    for foo in pipes:
        foo.pipe_x -= dx
    if is_pipe_out_of_frame(pipes[0]):
        pipes = add_new_pipe_at_last(pipes)
    return pipes


def add_new_pipe_at_last(pipes):
    pipes.pop(0)
    pipes.append(pipe(first_pipe_x + (pipe_dx * 3), random.randint(70, 330), random.randint(395, 630)))
    return pipes


def is_bird_in_pipe(c_p):
    if (current_ball_x + 50) > c_p.pipe_x and current_ball_x < (c_p.pipe_x + 10):
        # print('in pipe')
        return True
    else:
        return False


def is_player_out():
    for foo in current_pipes:
        if is_bird_in_pipe(foo):
            if current_ball_y <= foo.y_1 or (current_ball_y + 50) >= foo.y_2:
                return True
            else:
                return 'in pipe,give score'
    return 'out pipe, do not give score'

score = 0
current_level=0
font = pygame.font.Font('freesansbold.ttf', 32)


def level():
    return int(int(score/59)/5)


def update_screen():
    global score
    global current_ball_y

    white = (255, 255, 255)
    blue = (0, 0, 255)
    background = (25, 0, 84)
    screen.fill(background)
    # draw_circle(current_ball_x, current_ball_y)
    for foo in current_pipes:
        pygame.draw.rect(screen, pipe_c, (foo.pipe_x, 0, 10, foo.y_1))
        pygame.draw.rect(screen, pipe_c, (foo.pipe_x, foo.y_2, 10, 305))

    text = font.render(f'Score:{int(score/59)}', True, white)
    textrect = text.get_rect()

    if int(score/59) < 100:
        textrect.center = (size[1] * 0.90, size[0] * 0.90)
    else:
        textrect.center = (size[1] * 0.87, size[0] * 0.90)

    screen.blit(image,(current_ball_x, current_ball_y))
    screen.blit(text, textrect)

    global current_level
    level_x = level()
    delta = 0.0009

    if delta * level_x >= 0.01:
        pass
    else:
        current_level = level_x
    time.sleep(0.01 - delta * current_level)
    show_l = font.render(f'Level:{int(level_x)}', True, white)
    show_l_rect = show_l.get_rect()
    show_l_rect.center = (size[0] * 0.1, size[1] * 0.9)
    screen.blit(show_l, show_l_rect)
    pygame.display.update()

    check = is_player_out()
    if check == 'in pipe,give score':
        score += 1
        check = False
    elif check == 'out pipe, do not give score':
        check = False
    if check:
        pygame.mixer.music.pause()
        effect = pygame.mixer.Sound('out.wav')
        effect.play()
        time.sleep(1)
        # print("you are out")
        print(int(score/59))

        with open('hello.txt', 'r') as f:
            data = f.readline()
        data = int(data)

        i = 0
        new_background = (255, 0, 128)
        while i <= 700:
            pygame.draw.rect(screen, new_background, [100, 0, i, 700])
            i = i + 1
            # time.sleep(0.01)
            pygame.display.update()

        if int(score/59) > data:
            with open('hello.txt', 'w') as f:
                f.write(str(int(score/59)))

            final_screen3 = font.render(f'New high score', True, white)
            final_screen3_rect = final_screen3.get_rect()
            final_screen3_rect.center = (size[0] * 0.5, size[1] * 0.5)
            screen.blit(final_screen3, final_screen3_rect)

            final_screen2 = font.render(f'high score:{int(score/59)}', True, white)
            final_screen2_rect = final_screen2.get_rect()
            final_screen2_rect.center = (size[0] * 0.5, size[1] * 0.6)
            screen.blit(final_screen2, final_screen2_rect)

        else:
            print("You are out")
            final_screen1 = font.render(f'your score:{int(score/59)}', True, white)
            final_screen1_rect = final_screen1.get_rect()
            final_screen1_rect.center = (size[0] * 0.5, size[1] * 0.5)
            screen.blit(final_screen1, final_screen1_rect)

            final_screen2 = font.render(f'high score:{int(data)}', True, white)
            final_screen2_rect = final_screen2.get_rect()
            final_screen2_rect.center = (size[0] * 0.5, size[1] * 0.6)
            screen.blit(final_screen2, final_screen2_rect)
            pygame.display.update()

        pygame.display.update()
        time.sleep(2)
        sys.exit()




time_x = 0.002
number = 5
# level_x = 1


pygame.mixer.music.load('back_sound.wav')
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            effect1 = pygame.mixer.Sound('jump.wav')
            effect1.play(1)
            for i in range(0, 100):
                current_ball_y = jump_ball(current_ball_y)
                current_pipes = move_pipe(current_pipes)
                # current_pipes = move_pipe(current_pipes)
                update_screen()
    update_screen()
    current_pipes = move_pipe(current_pipes)
    current_ball_y = ball_fall(current_ball_y)

pygame.quit()