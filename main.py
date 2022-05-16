"""
This is a game called Treato Dreams.

Overview:

While their human is at work, a dog has fallen asleep and is having a puppy dream that
they are in the park and yummy treats and icky vegetables are falling from the sky.

The object of the game is to eat treats while avoiding vegetables.

Rules:

• Each treat eaten increases the player score by (50 * level)
• Each vegetable eaten decreases player lives by 1
• The player starts with 3 lives
• On Level 1, 4 treats spawn and increment by 2 per level
• On Level 1, 4 vegetables spawn and increment by 3 per level
• After all food objects have been eaten or fallen off the screen, the player advances to the next level
• Between a score of 5,000 and 50,000 inclusive, every 5,000 the player will receive an extra life
    • eg: 5,000, 10,000, 15,000 and on
• If all lives are lost, the player loses the game


Credits:

Thank you to the follow folks for sound effects:
• danlucaz for SCORE
• alanmcki for LOSE
• samsterbirdiesr for LOSE_LIFE
• bloodpixelhero for the musical theme

Thank you to my dog Simon for being this inspiration behind this game.

Images were all downloaded via ShutterStock


"""


# IMPORTS
import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# CREATE WINDOW
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treato Dreams")



# NONFOOD
BG = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'background.png')), (WIDTH, HEIGHT))
DOG_SLEEPING = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'bedroom_dog_sleeping.png')), (WIDTH, HEIGHT))
DOG_OPEN_MOUTH = pygame.transform.scale(pygame.image.load(os.path.join('Images','dog_open_mouth.png')), (60,99))
DOG_DREAMING = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'bedroom_dog_dreaming.png')), (WIDTH, HEIGHT))

# FOOD
BURGER = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'burger.png')), (25*2,24*2))
CARROT = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'carrot.png')), (24*2, 30*2))
CHICKEN_NUGGETS = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'chicken_nuggets.png')), (25*2, 13*2))
FRIES = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'fries.png')), (21*2,25*2))
HOT_DOG = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'hot-dog.png')), (25*2,13*2))
LETTUCE = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'lettuce.png')), (13*2, 25*2))
PIZZA = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'pizza.png')), (22*2,25*2))
TOMATO = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'tomato.png')), (25*2,25*2))

# SOUND
LOSE = pygame.mixer.Sound(os.path.join('Sounds', 'lose-tone_by_alanmcki.wav'))
LOSE_LIFE = pygame.mixer.Sound(os.path.join('Sounds', 'lose-life_samsterbirdiesr.wav'))
SCORE = pygame.mixer.Sound(os.path.join('Sounds', 'score_by_danlucaz.wav'))
pygame.mixer.Sound.set_volume(LOSE_LIFE, .5)
pygame.mixer.Sound.set_volume(SCORE, 1.0)

# GLOBAL VARS
FPS = 60
clock = pygame.time.Clock()

# MUSIC
pygame.mixer.music.load(os.path.join('Sounds', 'theme_by_bloodpixelhero.wav'))
pygame.mixer.music.play(-1)

# GAME
class Character:
    def __init__(self, x, y, health=100, score=0, lives=3, level=0):
        self.x = x
        self.y = y
        self.max_health = health
        self.character_img = DOG_OPEN_MOUTH
        self.mask = pygame.mask.from_surface(self.character_img)
        self.score = score
        self.lives = lives
        self.level = level

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y + - 75))

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()

    def add_to_score(self, value):
        extra_life_scores = [5000, 10000, 15000, 20000, 25000, 30000, 45000, 50000]
        value = 50 * self.level
        for extra_life_score in extra_life_scores:
            if self.score < extra_life_score <= self.score + value:
                self.lives += 1

        self.score += value

class Food:
    TREATO_MAP =  {
                "chicken nuggets": (CHICKEN_NUGGETS),
                "burger": (BURGER),
                "fries": (FRIES),
                "hot dog": (HOT_DOG),
                "pizza": (PIZZA),
                 }


    VEGETABLE_MAP = {
                    "carrot": (CARROT),
                    "lettuce": (LETTUCE),
                    "tomato": (TOMATO)
                    }


    def __init__(self, x, y, food_type, value = 50):
        self.x = x
        self.y = y
        self.food_type = food_type
        self.value = value
        self.food_img = None

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= HEIGHT and self.y >= 0)

    def collision(self, obj):
        """
        This function determines when the player and a food object collide,
        resulting in a score or a lost life.
        """
        return collide(self, obj)

class Treatos(Food):

    def __init__(self, x, y, food_type, value=50):
        super().__init__(x, y, food_type, value)
        self.food_type = food_type
        self.food_img = self.TREATO_MAP[food_type]
        self.mask = pygame.mask.from_surface(self.food_img)

    def draw(self, window):
        window.blit(self.food_img, (self.x, self.y))

    def get_width(self):
        return self.food_img.get_width()

    def get_height(self):
        return self.food_img.get_height()


class Vegetables(Food):
    def __init__(self, x, y, food_type, value=50):
        super().__init__(x, y, food_type, value=50)
        self.food_type = food_type
        self.food_img = self.VEGETABLE_MAP[food_type]
        self.mask = pygame.mask.from_surface(self.food_img)

    def draw(self, window):
        window.blit(self.food_img, (self.x, self.y))

    def get_width(self):
        return self.food_img.get_width()

    def get_height(self):
        return self.food_img.get_height()



def collide(obj1, obj2):
    """
    This function determines when pixels overlap between objects; ie: collide.
    It is passed to the collision function.
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y - 20      # - 20 to increase offset so that the collision occurs higher on the screen
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
def main():
    run = True
    character = Character(275, 500)

    character.level = 0
    player_vel = 5
    main_font = pygame.font.Font(os.path.join('quinque-five-font','Quinquefive-0Wonv.ttf'), 15)
    lost_font = pygame.font.Font(os.path.join('quinque-five-font','Quinquefive-0Wonv.ttf'), 28)

    lost = False
    lost_timer = 0

    treato_list = []
    vegetable_list = []
    treato_count = 4
    vegetable_count = 4
    food_vel = 1




    def redraw_window():
        WIN.blit(BG,(0,0))
        lives_label = main_font.render(f"Lives:{character.lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level:{character.level}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score:{character.score}", 1, (255, 255, 255))


        WIN.blit(lives_label, (WIDTH/2 - lives_label.get_width()/2 ,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, 10))

        for treat in treato_list:
            treat.draw(WIN)
        for vegetable in vegetable_list:
            vegetable.draw(WIN)


        character.draw(WIN)

        if lost:
            lost_label = lost_font.render("Heck! You lost", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 250))


        pygame.display.update()
    while run:
        clock.tick(FPS)
        redraw_window()

        if character.lives <= 0:
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(LOSE)
            lost = True
            lost_timer += 1

        if lost:
            if lost_timer > FPS*(pygame.mixer.Sound.get_length(LOSE)):
                run = False
            else:
                continue


        if len(treato_list) == 0:
            character.level += 1
            for t in range(treato_count):
                treato = Treatos(
                                random.randrange(50, WIDTH - 100),
                                random.randrange(-1500, -50),
                                random.choice(["burger",
                                               "chicken nuggets",
                                               "hot dog",
                                               "fries",
                                               "pizza",
                                               ])
                                )
                treato_list.append(treato)
            for v in range(vegetable_count):
                vegetable = Vegetables(
                                       random.randrange(50, WIDTH - 100),
                                       random.randrange(-1500, -50),
                                       random.choice(["carrot",
                                                      "lettuce",
                                                      "tomato",
                                                     ])
                                      )
                vegetable_list.append(vegetable)
            treato_count += 2
            vegetable_count += 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and character.x - player_vel > 0: #left with arrow
            character.x -= player_vel
        if keys[pygame.K_a] and character.x - player_vel > 0: #left with "a"
            character.x -= player_vel
        if keys[pygame.K_RIGHT] and character.x + player_vel + character.get_width() < WIDTH: #right with arrow
            character.x += player_vel
        if keys[pygame.K_d] and character.x + player_vel + character.get_width() < WIDTH: #right with "d"
            character.x += player_vel

        for treat in treato_list[:]:
            treat.move(food_vel)
            if treat.collision(character):
                character.add_to_score(50 * character.level)
                pygame.mixer.Sound.play(SCORE)
                treato_list.remove(treat)
            elif treat.y + treat.get_height() > HEIGHT:
                treato_list.remove(treat)

        for vegetable in vegetable_list[:]:
            vegetable.move(food_vel)
            if vegetable.collision(character):
                character.lives -= 1
                pygame.mixer.Sound.play(LOSE_LIFE)
                vegetable_list.remove(vegetable)
            elif vegetable.y + vegetable.get_height() > HEIGHT:
                vegetable_list.remove(vegetable)

    main_menu()

def main_menu():
    run = True
    title_font = pygame.font.Font(os.path.join('quinque-five-font','Quinquefive-0Wonv.ttf'), 25)
    sub_title_font = pygame.font.Font(os.path.join('quinque-five-font','Quinquefive-0Wonv.ttf'), 10)
    pygame.mixer.music.unpause()

    while run:
        WIN.blit(DOG_SLEEPING,(0,0))
        title_label = title_font.render("Treato Dreams", 1, (255, 255, 255))
        sub_title_label = sub_title_font.render("Press any key to continue...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 150))
        WIN.blit(sub_title_label, (WIDTH / 2 - sub_title_label.get_width() / 2, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                opening_scene()

    quit()

def opening_scene():
    run = True
    exposition_font = pygame.font.Font(os.path.join('quinque-five-font','Quinquefive-0Wonv.ttf'), 10)

    while run:
            WIN.blit(DOG_DREAMING, (0, 0))
            exposition = exposition_font.render("During a nap while your human is at work", 1, (255, 255, 255))
            exposition_cont = exposition_font.render("You have the most amazing puppy dream", 1, (255, 255, 255))
            exposition_cont_two = exposition_font.render("Treatos are falling from the sky!", 1, (255, 255, 255))
            exposition_cont_three = exposition_font.render("But be careful! There are vegetables falling too!", 1, (255, 255, 255))
            sub_title_label = exposition_font.render("Press any key to continue...", 1, (255, 255, 255))
            WIN.blit(exposition, (WIDTH/2 - exposition.get_width()/2, 100))
            WIN.blit(exposition_cont, (WIDTH/2 - exposition_cont.get_width()/2, 125))
            WIN.blit(exposition_cont_two, (WIDTH / 2 - exposition_cont_two.get_width() / 2, 150))
            WIN.blit(exposition_cont_three, (WIDTH / 2 - exposition_cont_three.get_width() / 2, 175))
            WIN.blit(sub_title_label, (WIDTH / 2 - sub_title_label.get_width() / 2, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    main()

    quit()

main_menu()