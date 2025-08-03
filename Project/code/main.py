from main_menu import Menu
from login import *

# Main function to run the whole project
def main():
    pygame.init()
    # Set fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # success_code[0]: Boolean, success_code[1]: username

    success_code = Login(screen).run()
    if success_code is None: # Esc
        pygame.quit()
        return

    username = success_code[1]
    Menu(screen, username).run()

# Run the project
if __name__ == '__main__':
    main()