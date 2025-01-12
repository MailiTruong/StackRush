import pygame
import serial
from Block import Block
from Player import Player
from pathlib import Path

pygame.mixer.init()
metronome_sound = pygame.mixer.Sound("./Sound/Metronome.wav")  
metronome_sound.set_volume(1)

#game class to handle the whole game
class Game:

    def __init__(self):
        self.blocks = pygame.sprite.Group()
        self.orientation = 'left'
        self.is_playing = False
        self.screen = pygame.display.get_surface()
        self.run = True
        self.score = 0
        self.time_since_last_increase = 0
        self.is_paused = False
        self.player = Player()
        self.players = []

    #function to automate the blocks creation
    def spawn_block(self):
        block = Block()
        #every 20 blocks I only want to see the 2 last blocks
        if len(self.blocks) >= 1 and len(self.blocks) % 20 == 0:
            blocks = pygame.sprite.Group()
            self.blocks.sprites()[-2].rect.y = self.screen.get_height() - block.height
            self.blocks.sprites()[-1].rect.y = self.screen.get_height() - 30 
            blocks.add(self.blocks.sprites()[-2])
            blocks.add(self.blocks.sprites()[-1])
            self.blocks = blocks

        if len(self.blocks) == 0:
            block.rect.x = (self.screen.get_width() // 2) - block.width // 2
            block.rect.y = self.screen.get_height() - block.height
            block.moving = False  
        #if the first block is placed then the other block move and they go one onto the other, they spawn from left to right
        if len(self.blocks) >= 1:
            block.update_block_velocity(self.blocks.sprites()[-1])
            block.rect.y = self.screen.get_height() - 15 * (len(self.blocks)+1) 
            block.moving = True
            if self.orientation == 'left':                    
                block.dir = -1
                block.rect.x = self.screen.get_width()
                self.orientation = 'right'
            elif self.orientation == 'right':
                block.dir = 1
                block.rect.x = -block.width
                self.orientation = 'left' 

        self.blocks.add(block)

    def handle_block_stop(self):
        moving_block = self.blocks.sprites()[-1]
        moving_block.stop()
        if self.time_since_last_increase % (1 / moving_block.velocity) < 0.1:
            if not pygame.mixer.get_busy():
                metronome_sound.play() 

        if len(self.blocks) > 1:
            static_block = self.blocks.sprites()[-2]
            if moving_block.rect.x >= static_block.rect.x + static_block.width or moving_block.rect.x + moving_block.width <= static_block.rect.x:
                self.game_over()
            else:
                overlap_width = moving_block.width - abs(moving_block.rect.x - static_block.rect.x)
                self.player.block_width_difference.append(str(overlap_width))
                moving_block.update_block_width(overlap_width)
                moving_block.update_block_rect(static_block)
                self.spawn_block()
                self.blocks.sprites()[-1].update_block_width(overlap_width)
                self.score += 1

    #function to create and display the leaderboard
    def display_leaderboard(self):
        font = pygame.font.SysFont("monospace", 16)
        title_text = font.render(f"Top 10 players", True, (0, 0, 0))
        title_x = self.screen.get_width() // 2 - title_text.get_width() // 2
        title_y = 100
        self.screen.blit(title_text, (title_x, title_y))
        for i, player in enumerate(self.sorted_players[:10]):
            score_text = font.render(f"{i + 1}. {player.name} : {player.highscore}", True, (0, 0, 0))
            self.screen.blit(score_text, (title_x + 8, title_y + 50 + i * 30))
    
    #pause function with what it handles
    def pause(self):
        self.load_players()
        self.sorted_players = sorted(self.players, key=lambda x: x.highscore, reverse=True)#sorts the list based on highscores to then do the leaderboard
        self.is_paused = not self.is_paused

    #start function that resets everything
    def start(self, menu_player_name):
        self.spawn_block()
        self.spawn_block()
        self.player = Player()  # Create a new Player instance
        self.player.name = menu_player_name
        self.player.load_player()

    #game over function to store the data and clears the lists
    def game_over(self):
        self.player.score = self.score
        self.player.update_highscore()
        self.player.load_csv()
        self.score = 0
        self.is_playing = False
        self.blocks = pygame.sprite.Group()
    
    #handle inputs for the game this time not the menu
    def check_event(self, event, menu_player_name):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and self.is_playing:
                self.pause()
            
            if event.key == pygame.K_SPACE:
                if not self.is_playing:
                    self.is_paused = False
                    self.is_playing = True
                    self.start(menu_player_name)
                else:
                    # Handling space press while playing
                    self.handle_block_stop()


    def update(self, dt):
        if self.is_paused:
            self.display_leaderboard()
        else:#display score
            font = pygame.font.SysFont("monospace", 16)
            score_text = font.render(f"Score : {self.score}", 1, (0, 0, 0))
            self.player.score = self.score
            self.screen.blit(score_text, (20, 20))

            if len(self.blocks) > 0:#as soon as the first block spawns (that is static), the rest will be moving blocks 
                moving_block = self.blocks.sprites()[-1]
                self.time_since_last_increase += dt
                if (self.time_since_last_increase >= 3):#every three seconds the speed increases
                    moving_block.velocity += 30
                    self.time_since_last_increase = 0
                moving_block.move(dt)#so I need to update the movement of the block
                if moving_block.rect.x >= self.screen.get_width():#gameover when block goes off screen
                    self.game_over()
                elif moving_block.rect.x < -100:
                    self.game_over()

            self.blocks.draw(self.screen)
    
    #adds all the players to the list of players
    def load_players(self):
        self.players = []
        for file in Path("./Players").iterdir(): 
            if file.is_file():
                if file.suffix == ".csv":
                    player = Player()
                    player.name = file.stem
                    player.load_player()
                    self.players.append(player)
