import pygame as py
from pygame import mixer
import random

# initialize pygame fonts
py.font.init()

# Set the game window
width = 750
height = 750
window = py.display.set_mode((width, height))

# Set Game Title
py.display.set_caption("CAR COLLISION")

# Load background music
mixer.init()
mixer.music.load("bg_sound.mp3")
mixer.music.set_volume(0.7)

# Load Player Car
PLAYER_CAR = py.image.load("player_car.png")
# Set Player Car Size
PLAYER_CAR = py.transform.scale(PLAYER_CAR, (40,80))

# Load Opposing Cars
BLACK_CAR = py.image.load("black_car.png")
GREY_CAR = py.image.load("grey_car.png")
RED_CAR = py.image.load("red_car.png")
# Set Opposing Car Sizes
BLACK_CAR = py.transform.scale(BLACK_CAR, (40, 80))
GREY_CAR = py.transform.scale(GREY_CAR, (60, 100))
RED_CAR = py.transform.scale(RED_CAR, (60, 80))

# Load Background Image
BG  = py.image.load("bg.jpg")


class Car:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.car_color = color

        # creating car depending upon color
        if self.car_color == "Yellow":
            self.car_img = PLAYER_CAR
        if self.car_color == "Black":
            self.car_img = BLACK_CAR
        if self.car_color == "Grey":
            self.car_img = GREY_CAR
        if self.car_color == "Red":
            self.car_img = RED_CAR

        # create mask of car_img
        # mask tells where the pixels are and where are not
        # so that when we have a collision we can know about that
        self.mask = py.mask.from_surface(self.car_img)

    # placing car on game screen
    def draw(self, window):
        window.blit(self.car_img, (self.x, self.y))

    # returns width of car
    def get_width(self):
        return self.car_img.get_width()

    # returns height of car
    def get_height(self):
        return self.car_img.get_height()

    # move opposing cars on the window
    def move(self, value):
        self.y += value

    def collision(self, car):
        return collide(self, car)

def collide(car1, car2):
    x_offset = car2.x - car1.x
    y_offset = car2.y - car1.y
    return car1.mask.overlap(car2.mask, (x_offset, y_offset)) != None

def main(level):
    # start background music
    mixer.music.play(-1)

    # initializing variables
    run_game = True
    frames_per_second = 60
    score = 0
    winning_score = 0

    # Setting font family to 'comicsans' and font size to 50px
    label_font = py.font.SysFont("comicsans", 35)
    popup_font = py.font.SysFont("comicsans", 60)

    # array of opposing cars displayed on screen
    opposing_cars = []

    # setting cars wave size and their speeds
    if level == "Easy":
        cars_wave_size = 20
        cars_speed = 1
        winning_score = cars_wave_size * 5
    if level == "Medium":
        cars_wave_size = 30
        cars_speed = 4
        winning_score = cars_wave_size * 5
    if level == "Hard":
        cars_wave_size = 40
        cars_speed = 7
        winning_score = cars_wave_size * 5

    # Player Car Moving Speed
    player_car_speed = 10

    # player car created
    player_car = Car(300, 650, "Yellow")

    time_clock = py.time.Clock()

    cars_collide = False # Bool varaible for Game End Condition
    timer = 0 # timer to quit game after collision
    win = False # Bool variable for Game Win Condition
    car_copy = None # variable for no collision of opposing cars

    # For each iteration of while loop we want to refresh the window
    def redraw_window():
        # set background image
        window.blit(BG, (0, 0))
        # rgb value of orange color
        orange_color = (252, 186, 3)
        # displaying level with orange color
        level_label = label_font.render("Level:  {}".format(level), 1, orange_color)
        # displaying score with orange color
        score_label = label_font.render("Score:  {}".format(score), 1, orange_color)

        # calculate left padding of score label
        score_left_padding = width - score_label.get_width() - 10

        # position level
        window.blit(level_label, (10, 10))
        # position score
        window.blit(score_label, (score_left_padding, 10))

        # display opposing cars on screen
        for car in opposing_cars:
            car.draw(window)

        # display player car on screen
        player_car.draw(window)

        # Result to display on cars collision
        if cars_collide:
            # display following message
            hit_label = popup_font.render("You Lose: {}".format(score), 1, orange_color)
            window.blit(hit_label, (width / 2 - hit_label.get_width() / 2, 350))

        # Result to display on Win
        if win:
            # display following message
            win_label = popup_font.render("You Win: {}".format(score), 1, orange_color)
            window.blit(win_label, (width / 2 - win_label.get_width() / 2, 350))

        py.display.update() # redraw the screen

    # Loop until the user quits the game
    while run_game:
        # run the game at 60 frames per second
        time_clock.tick(frames_per_second)

        # call redraw_window function
        redraw_window()

        # After collision end the game after 3sec
        if cars_collide or win:
            timer += 1
            # exit the game if timer equals 3
            if timer > frames_per_second * 5:
                quit()

        if len(opposing_cars) == 0:
            # loop upto cars_wave_size
            for i in range(cars_wave_size):
                #while True:
                    # x value of asteroid
                x_value = random.randrange(50, width - 100)
                    # check for valid x range
                    # if (50 < x_value < 150) or (170 < x_value < 270) or (290 < x_value < 390) or (310 < x_value < 410) or (430 < x_value < 530) or (550 < x_value < 650):
                    # break
                # y value of asteroid is negative because opposing cars are to be created off the screen
                if level == "Easy":
                    y_value = random.randrange(-3000, -100)
                if level == "Medium":
                    y_value = random.randrange(-5000, -100)
                if level == "Hard":
                    y_value = random.randrange(-7000, -100)

                # random car
                random_car = random.choice(['Black', 'Grey', 'Red'])

                # opposing car created
                opposing_car = Car(x_value, y_value, random_car)

                if car_copy is not None:
                    if opposing_car.collision(car_copy):
                        opposing_car.y -= 50

                # add car to opposing_cars array
                opposing_cars.append(opposing_car)

                car_copy = opposing_car

        # Loop through events that occurs
        for event in py.event.get():
            # Quit the game
            if event.type == py.QUIT:
                quit()

        # get player commands
        key = py.key.get_pressed()

        if (not cars_collide) and (not win):
            # if 'a' is pressed move left
            if (key[py.K_a]) and (player_car.x - player_car_speed > 0):
                player_car.x -= player_car_speed
            # if 'd' is pressed move right
            if (key[py.K_d]) and (player_car.x + player_car_speed + player_car.get_width() < width):  # right
                player_car.x += player_car_speed
            # if 'w' is pressed move up
            if (key[py.K_w]) and (player_car.y - player_car_speed > 0):  # up
                player_car.y -= player_car_speed
            # if 's' is pressed move down
            if (key[py.K_s]) and (player_car.y + player_car_speed + player_car.get_height() + 15 < height):  # down
                player_car.y += player_car_speed

        # move opposing cars downward
        for car in opposing_cars:
            # pause movement of opposing_cars if player_car hit opposing_car
            if (not cars_collide) and (not win):
                car.move(cars_speed)

            # player_car hits opposing car
            if player_car.collision(car):
                # play collision sound
                collision_sound = mixer.Sound("crash.wav")
                collision_sound.play()

                cars_collide = True
                opposing_cars.remove(car)

            if car.y >= height + car.get_height():
                score += 5  # increase score by 5
                opposing_cars.remove(car)
                # set win to True score exceeds winning score 50
                if (score >= winning_score):
                    win = True

# Main Menu
def menu():
    # Font to be used for main menu
    menu_font = py.font.SysFont("comicsans", 50)
    level_font = py.font.SysFont("comicsans", 40)
    # variable to handle game quit or run
    run_game = True
    while run_game:
        # rgb value of orange
        orange_color = (252, 186, 3)
        white_color = (255, 255, 255)
        # Label to be shown before game start and after game ends
        menu_label = menu_font.render("Main Menu", 1, orange_color)
        easy_level = level_font.render("Press 1 for EASY Level", 1, white_color)
        medium_level = level_font.render("Press 2 for MEDIUM Level", 1, white_color)
        hard_level = level_font.render("Press 3 for HARD Level", 1, white_color)

        # place label on the window
        x_value = width/2 - menu_label.get_width()/2 # center position
        y_value = 150
        window.blit(menu_label, (x_value, y_value)) # position Menu Label
        window.blit(easy_level, (x_value - 70, y_value + 100)) # position Easy Label
        window.blit(medium_level, (x_value - 70, y_value + 150)) # position Medium Label
        window.blit(hard_level, (x_value - 70, y_value + 200)) # position Hard Label

        py.display.update()

        # check for events and loop through them
        for event in py.event.get():
            # Quit game
            if event.type == py.QUIT:
                run_game = False
        keys = py.key.get_pressed()
        if keys[py.K_1]:
            main("Easy")
        if keys[py.K_2]:
            main("Medium")
        if keys[py.K_3]:
            main("Hard")

    py.quit()

menu()