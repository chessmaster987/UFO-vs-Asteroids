import pygame
import random as rd
from random import randrange
from pygame import font, time
import sqlite3
import datetime

# Initialize Pygame
pygame.init()

# Set window title
pygame.display.set_caption('UFO vs Asteroids')

# Initialize the clock to control the frame rate
FPS = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = width, height = (1500, 800)
main_window = pygame.display.set_mode(screen)

# Load images and scale them
image_obj = pygame.transform.scale(pygame.image.load(
    './imgs/ufo.png').convert_alpha(), (45, 45))
image_enemy = pygame.transform.scale(pygame.image.load(
    './imgs/asteroid.png').convert_alpha(), (70, 50))
image_weapon = pygame.transform.scale(pygame.image.load(
    './imgs/weapon.png').convert_alpha(), (45, 35))
image_bckg = pygame.transform.scale(pygame.image.load(
    './imgs/background.jpg').convert(), screen)

# Background movement variables
bckgX = 0
bckgX2 = image_bckg.get_width()
image_bckg_speed = 3

# UFO initial position and speed
obj_x = width // 2
obj_y = height // 2
obj_speed = 10

# Database initialization
def init_db():
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_name TEXT,
                        score INTEGER,
                        game_time TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_record(player_name, score):
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()
    game_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO records (player_name, score, game_time) 
                      VALUES (?, ?, ?)''', (player_name, score, game_time))
    conn.commit()
    conn.close()

# Function to retrieve data from the database
def fetch_records():
    conn = sqlite3.connect('game_records.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT player_name, score, game_time FROM records''')
    records = cursor.fetchall()
    conn.close()
    return records

# Function to display the game archive
def display_archive():
    records = fetch_records()
    main_window.fill(BLACK)
    font = pygame.font.Font(None, 36)
    headers = ["Player Name", "Score", "Game Time"]
    header_text = " | ".join(headers)
    header_surface = font.render(header_text, True, WHITE)
    header_rect = header_surface.get_rect(topleft=(50, 50))
    main_window.blit(header_surface, header_rect.topleft)

    y_offset = header_rect.bottom + 20
    for record in records:
        record_text = " | ".join(map(str, record))
        record_surface = font.render(record_text, True, WHITE)
        record_rect = record_surface.get_rect(topleft=(50, y_offset))
        main_window.blit(record_surface, record_rect.topleft)
        y_offset += record_rect.height + 5
    
    back_button = Button(width // 2 - 100, height - 100, 200, 50, "Back", back_to_menu)
    back_button.draw(main_window)
    
    pygame.display.flip()

# Initialize the database
init_db()

# Function to create an enemy
def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy_rect = pygame.Rect(width, rd.randint(0, height), *enemy.get_size())
    enemy_speed = rd.randint(5, 10)
    return [enemy, enemy_rect, enemy_speed]

# Function to create a weapon
def create_weapon():
    weapon_x = rd.randrange(0, width)
    weapon_y = 0
    weapon = pygame.Surface((20, 20))
    obj_rect = pygame.Rect(
        obj_x, obj_y, image_obj.get_width(), image_obj.get_height())
    weapon_rect = pygame.Rect(weapon_x, weapon_y, *weapon.get_size())
    weapon_speed = 1
    return [weapon, weapon_rect, weapon_speed]


# Set up events for creating enemies and weapons
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1000)  # time of creating asteroids
CREATE_WEAPON = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_WEAPON, 2000)  # time of creating weapons

# Set up font for displaying the score
my_font = font.SysFont(None, 36)

# Initialize score
score = 0

# Lists to store enemies and weapons
enemies = []
weapons = []

# Define Button class
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def clicked(self):
        # Perform action associated with the button
        if self.action:
            self.action()

# Function to start the game
def start_game():
    global game_state
    game_state = "enter_name"

# Function to initialize game variables
def initialize_game():
    global obj_x, obj_y, score, enemies, weapons
    obj_x = width // 2
    obj_y = height // 2
    score = 0
    enemies = []
    weapons = []

# Function to handle game archive
def game_archive():
    global game_state
    game_state = "archive"
    display_archive()

def back_to_menu():
    global game_state
    game_state = "menu"

# Function to quit the game
def quit_game():
    pygame.quit()
    exit()

def get_name():
    global player_name, game_state
    name = ""
    input_active = True
    input_box = pygame.Rect(width // 2 - 100, height // 2 - 32, 200, 64)
    font = pygame.font.Font(None, 48)
    prompt_font = pygame.font.Font(None, 36)
    prompt_text = "Enter your name"

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        main_window.fill((0, 0, 0))
        # Render and display the prompt text
        prompt_surface = prompt_font.render(prompt_text, True, WHITE)
        prompt_rect = prompt_surface.get_rect(center=(width // 2, height // 2 - 80))
        main_window.blit(prompt_surface, prompt_rect)

        # Render and display the input text
        txt_surface = font.render(name, True, WHITE)
        main_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(main_window, WHITE, input_box, 2)
        pygame.display.flip()

    player_name = name
    game_state = "game"
    initialize_game()

# Get player's name
#player_name = get_name()

# Initialize buttons for the main menu
start_button = Button(width // 2 - 100, height // 2 - 100, 200, 50, "Start Game", start_game)
archive_button = Button(width // 2 - 100, height // 2, 200, 50, "Game Archive", game_archive)
quit_button = Button(width // 2 - 100, height // 2 + 100, 200, 50, "Quit Game", quit_game)
back_button = Button(width // 2 - 100, height - 100, 200, 50, "Back", back_to_menu)

# Main game state
game_state = "menu"

# Main game loop
running = True
while running:
    # Control the frame rate
    FPS.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "game":
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_WEAPON:
                weapons.append(create_weapon())
        elif game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.rect.collidepoint(event.pos):
                    start_button.clicked()
                if archive_button.rect.collidepoint(event.pos):
                    archive_button.clicked()
                if quit_button.rect.collidepoint(event.pos):
                    quit_button.clicked()
        elif game_state == "enter_name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    get_name()
        elif game_state == "archive":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                back_button.clicked()

    if game_state == "menu":
        main_window.fill(BLACK)
        start_button.draw(main_window)
        archive_button.draw(main_window)
        quit_button.draw(main_window)
        pygame.display.flip()
    elif game_state == "enter_name":
        get_name()
    elif game_state == "game":
        # Background scrolling
        bckgX -= image_bckg_speed
        bckgX2 -= image_bckg_speed
        if bckgX < -image_bckg.get_width():
            bckgX = image_bckg.get_width()
        if bckgX2 < -image_bckg.get_width():
            bckgX2 = image_bckg.get_width()

        # Draw the background
        main_window.blit(image_bckg, (bckgX, 0))
        main_window.blit(image_bckg, (bckgX2, 0))

        # Draw the UFO
        main_window.blit(image_obj, (obj_x, obj_y))

        # Handle UFO movement
        keys = pygame.key.get_pressed()
        obj_rect = pygame.Rect(
            obj_x, obj_y, image_obj.get_width(), image_obj.get_height())
        if keys[pygame.K_LEFT] and not obj_rect.left <= 0:
            obj_x -= obj_speed
        if keys[pygame.K_RIGHT] and not obj_rect.right >= width:
            obj_x += obj_speed
        if keys[pygame.K_UP] and not obj_rect.top <= 0:
            obj_y -= obj_speed
        if keys[pygame.K_DOWN] and not obj_rect.bottom >= height:
            obj_y += obj_speed

        # Display the score
        main_window.blit(my_font.render(
            str(score), True, (255, 0, 0)), (width // 2, 5))

        # Handle enemies
        for enemy in enemies:
            # Move enemy and blit to screen
            enemy[1] = enemy[1].move(-enemy[2], 0)
            main_window.blit(image_enemy, enemy[1])

            # Remove enemies that go off screen
            if enemy[1].left < 0:
                enemies.pop(enemies.index(enemy))

            # Check for collision with object
            if enemy[1].colliderect(pygame.Rect(obj_x, obj_y, image_obj.get_width(), image_obj.get_height())):
                text = my_font.render(
                    f'{player_name} EARNED {score} POINTS', True, (0, 255, 0))
                text_rect = text.get_rect()
                text_x = width // 2 - text_rect.width // 2
                text_y = height // 2 - text_rect.height // 2
                main_window.blit(text, [text_x, text_y])
                pygame.display.flip()
                pygame.time.delay(2000)

                # Insert record into database
                insert_record(player_name, score)

                game_state = "menu"

        # Handle weapons
        for weapon in weapons:
            # Move weapon and blit to screen
            weapon[1] = weapon[1].move(0, weapon[2])
            main_window.blit(image_weapon, weapon[1])

            # Remove weapons that go off screen
            if weapon[1].bottom >= height:
                weapons.pop(weapons.index(weapon))

            # Check for collision with object
            if weapon[1].colliderect(pygame.Rect(obj_x, obj_y, image_obj.get_width(), image_obj.get_height())):
                weapons.remove(weapon)
                score += 1

    # Update the display
    pygame.display.flip()
