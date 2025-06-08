import pygame
from random import randint

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        self.surface = pygame.image.load('/Users/colinleong/Documents/Programming/Python_Projects/Pygame_Projects/Flappy_Bird/images/bird.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() // 7, self.surface.get_height() // 7))
        self.rect = self.surface.get_rect(center = (200,100))
        self.gravity = 0

    def jump(self):
        self.gravity = -14

    def update(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.y > 590 or self.rect.y < -120:
            self.die()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def die(self):
        global game_active
        game_active = False

class Pipe(pygame.sprite.Sprite):
    def __init__(self, pipe_y_pos):
        self.up_surface = pygame.image.load('/Users/colinleong/Documents/Programming/Python_Projects/Pygame_Projects/Flappy_Bird/images/pipe_up.tiff').convert_alpha()
        self.up_surface = pygame.transform.scale(self.up_surface, (100, 500))
        self.up_rect = self.up_surface.get_rect(midbottom = (1000, pipe_y_pos))

        self.down_surface = pygame.image.load('/Users/colinleong/Documents/Programming/Python_Projects/Pygame_Projects/Flappy_Bird/images/pipe_down.tiff').convert_alpha()
        self.down_surface = pygame.transform.scale(self.down_surface, (100, 500))
        self.down_rect = self.down_surface.get_rect(midtop = (1000, pipe_y_pos + 250))

    def update(self):
        self.up_rect.x -= 4
        self.down_rect.x -= 4

        if self.up_rect.x <= -100:
            pipes.remove(self)

    def draw(self, screen):
        screen.blit(self.up_surface, self.up_rect)
        screen.blit(self.down_surface, self.down_rect)

def display_score():
    global score
    score = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f'Score: {score}', False, 'Blue')
    score_rect = score_surface.get_rect(center = (500,50))
    screen.blit(score_surface, score_rect)
    return score

# Set up
pygame.init()
screen = pygame.display.set_mode((1000,570))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)

# Background
sky_surface = pygame.image.load('/Users/colinleong/Documents/Programming/Python_Projects/Pygame_Projects/Flappy_Bird/images/background.jpg').convert()
sky_surface = pygame.transform.scale(sky_surface, (sky_surface.get_width() * 1.2, sky_surface.get_height() * 1.2))

# Start screen
game_name = text_font.render('Flappy Bird', False, 'Black')
game_name_rect = game_name.get_rect(center = (500, 50))
instructions = text_font.render('Press [space] to start', False, 'Black')
instructions_rect = instructions.get_rect(center = (500,500))

# Bird
bird = Bird()

pipes = []

# Spawn timer
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1500)

game_active = False
start_time = 0

while True:
    for event in pygame.event.get():
        # Close window
        if event.type == pygame.QUIT:
            print('Program terminated...')
            pygame.quit()
            exit()
        
        # Jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_active:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
            bird.jump()

        # Spawn new pipe
        elif event.type == spawn_timer:
            new_pipe = Pipe(randint(0,350))
            pipes.append(new_pipe)

    if game_active:
        screen.blit(sky_surface, (0,0))

        bird.update()
        bird.draw(screen)

        # Move pipe
        for pipe in pipes:
            pipe.update()

            if bird.rect.colliderect(pipe.up_rect) or bird.rect.colliderect(pipe.down_rect):
                bird.die()

        for pipe in pipes:
            pipe.draw(screen)

        score = display_score()

    else:
        pipes.clear()
        screen.blit(sky_surface, (0,0))

        # Reset bird
        bird.rect = bird.surface.get_rect(center = (200,285))
        bird.draw(screen)

        # Start screen
        screen.blit(game_name, game_name_rect)
        screen.blit(instructions, instructions_rect)

        try:
            if score:
                score_message = text_font.render(f'Score: {score}', False, 'Blue')
                score_message_rect = score_message.get_rect(center = (500,285))
                screen.blit(score_message, score_message_rect)
                
        except NameError:
            pass

    pygame.display.update()
    clock.tick(60)