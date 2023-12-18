import pygame, random, math, sys
from button import Button


#Setup Display
pygame.init()

WIDTH = 1280
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Game Variables
hangman_status = 0
words = ["python", "programacion", "juego", "ahorcado", "computadora"]
#word = ""
guessed = []
images = []

 # Button Variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 500
A = 65
for i in range(26):
    
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts

LETTER_FONT = pygame.font.SysFont(None, 40)
WORD_FONT = pygame.font.SysFont(None, 60)
TITLE_FONT = pygame.font.SysFont(None, 70)

"""global hangman_status
FPS = 60
clock = pygame.time.Clock()
run = True"""

BG = pygame.image.load("assets\Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def get_random_word():
    """Get a word from a list"""
    return random.choice(words)

def show_message(message):
    """Show message"""
    pygame.time.delay(1000)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

word = get_random_word().upper()

# Load Images

def load_images():
    for i in range(8):
        image = pygame.image.load("images\hangman" + str(i) + ".png")
        images.append(image)

load_images()

def restart():
    """Restart Game Variables"""
    global word, guessed, letters, hangman_status
    hangman_status = 0
    word = get_random_word().upper()
    guessed =[]
    for letter in letters:
        letter[3] = True


def play():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    game_over = False  # Bandera para controlar el estado del juego


    while run:

        clock.tick(FPS)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        window.fill(BLACK)

        # Draw title
        text = TITLE_FONT.render('HANGMAN', 1, WHITE)
        window.blit(text, (WIDTH/2 - text.get_width()/2, 20))

        #draw word
        show_word = ""
        for letter in word:
            if letter in guessed:
                show_word += letter + " "
            else:
                show_word += "_ "
        text = WORD_FONT.render(show_word, 1, WHITE)
        window.blit(text, (400, 350))

        #draw buttons
        for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(window, WHITE, (x, y), RADIUS, 3)
                text = LETTER_FONT.render(ltr, 1, WHITE)
                window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


        PLAY_BACK = Button(image=None, pos=(940, 660), 
                    text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(window)

        window.blit(images[hangman_status], (100, 100))
        pygame.display.update()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar evento de reinicio (por ejemplo, presionar la tecla 'R')
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                        m_x, m_y = pygame.mouse.get_pos()
                        for letter in letters:
                                x, y, ltr, visible = letter
                                dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                                if dis < RADIUS:
                                    letter[3] = False
                                    guessed.append(ltr)
                                    if ltr not in word:
                                        hangman_status += 1

        if game_over:
             # Muestra la última imagen del ahorcado antes del mensaje
            if hangman_status == 6:
                #hangman_status += 1
                window.blit(images[hangman_status], (100, 100))
                #pygame.display.update()
                pygame.time.delay(1000)
                

            show_message('You lose!')
            restart()
            main_menu()
            game_over = False  # Reinicia la bandera
        
        """Creo que debería haber una condición aquí para poder volver \n
            a cargar la imagen del muñeco ahorcado"""


        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                #hangman_status += 1
                #window.blit(images[hangman_status], (100, 100))
                break


        if won:

            show_message(word)

            show_message("You WON!")
            restart()
            main_menu()

        if hangman_status >= 7:
            game_over = True # Marca el juego como terminado

            #hangman_status += 1
            
            #window.blit(images[hangman_status], (100, 100))
            #pygame.display.update()

            #show_message('You lose!')
            #restart()
            #main_menu()

            #pygame.display.update()

        # Actualizar la lógica del juego aquí

        # Limpiar la pantalla
        #window.fill((0, 0, 0))
        
        # Dibujar los elementos del juego aquí

        # Actualizar la pantalla
        #pygame.display.flip()



    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def run_game():
    main_menu()
    
run_game()