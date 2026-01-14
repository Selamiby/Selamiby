import pygame
from pygame.locals import *

class JianghenUIDesign:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('SimSun', 24)
        self.gold_color = (255, 215, 0)
        self.main_menu_buttons = [
            {'text': 'Start', 'x': width // 2 - 100, 'y': height // 2 - 50},
            {'text': 'Options', 'x': width // 2 - 100, 'y': height // 2},
            {'text': 'Quit', 'x': width // 2 - 100, 'y': height // 2 + 50}
        ]

    def draw_main_menu(self, screen):
        screen.fill((0, 0, 0))
        for button in self.main_menu_buttons:
            pygame.draw.rect(screen, self.gold_color, (button['x'], button['y'], 200, 50))
            text = self.font.render(button['text'], True, (0, 0, 0))
            screen.blit(text, (button['x'] + 80, button['y'] + 15))

    def draw_character_stats(self, screen, character):
        stats_text = [
            f'Level: {character.level}',
            f'HP: {character.hp}/{character.max_hp}',
            f'ATK: {character.atk}',
            f'DEF: {character.defense}'
        ]
        y = 50
        for stat in stats_text:
            text = self.font.render(stat, True, self.gold_color)
            screen.blit(text, (50, y))
            y += 30

    def draw_game_ui(self, screen, character, gold, experience):
        self.draw_character_stats(screen, character)
        gold_text = f'Gold: {gold}'
        gold_render = self.font.render(gold_text, True, self.gold_color)
        screen.blit(gold_render, (self.width - 150, 20))
        experience_text = f'Experience: {experience}'
        experience_render = self.font.render(experience_text, True, self.gold_color)
        screen.blit(experience_render, (self.width - 150, 50))

class Character:
    def __init__(self, name, level, hp, atk, defense):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    ui_design = JianghenUIDesign(width, height)
    character = Character('Player', 1, 100, 10, 5)
    gold = 0
    experience = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                for button in ui_design.main_menu_buttons:
                    if (button['x'] < event.pos[0] < button['x'] + 200 and
                            button['y'] < event.pos[1] < button['y'] + 50):
                        if button['text'] == 'Start':
                            # Start game logic here
                            pass
                        elif button['text'] == 'Options':
                            # Options logic here
                            pass
                        elif button['text'] == 'Quit':
                            running = False

        ui_design.draw_game_ui(screen, character, gold, experience)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()