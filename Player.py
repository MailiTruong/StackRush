import pygame
import csv
import os

#player class to keep player data
class Player:

    def __init__(self):
        self.name = ''
        self.score = 0
        self.highscore = 0
        self.block_width_difference = []
        self.header = ["score", "highscore", "block width difference"]

    #write player data on csv file
    def load_csv(self):
        if os.path.exists(f'./Players/{self.name}.csv') == False:
            with open(f'./Players/{self.name}.csv', 'a', newline='') as player_file:
                csv_writer = csv.writer(player_file)
                csv_writer.writerow(self.header)
        with open(f'./Players/{self.name}.csv', 'a', newline = '') as player_file:
            csv_writer = csv.writer(player_file)
            player_data = [self.score, self.highscore, ', '.join(self.block_width_difference)]

            csv_writer.writerow(player_data)
        
    #modify highscore if the player has a better score
    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

    #function to download a player's data from csv to a player instance
    def load_player(self):
        if os.path.exists(f'./Players/{self.name}.csv'):
            with open(f'./Players/{self.name}.csv', 'r', newline='') as player_file:
                csv_reader = list(csv.reader(player_file))
                for row in csv_reader[1:]:  # Skip header row
                    if row:
                        self.highscore = int(row[1])

