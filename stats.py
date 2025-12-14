import json
import uuid
import os
from constants import STATS_PRINT_MESSAGE

class Stats:
    def __init__(self):
        self.id = uuid.uuid4()
        self.winNumber = 0
        self.loseNumber = 0
        self.eloScore = 500
        self.name = None
    
    def create_new(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.winNumber = 0
        self.loseNumber = 0
        self.eloScore = 500
    
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.name = data['name']
                self.id = data['id']
                self.winNumber = data['winNumber']
                self.loseNumber = data['loseNumber']
                self.eloScore = data['eloScore']
            print(STATS_PRINT_MESSAGE.successLoadMessage)
        except:
            print('\033[91m' + "Error: Path: {" + filename + "} does not exist")
    
    def save_to_file(self):
        if not hasattr(self, 'name'):
            print("Enter your username: ")
            self.name = str(input())
        
        # Create stats directory if it doesn't exist
        os.makedirs("stats", exist_ok=True)
        
        data = {
            'name': self.name,
            'id': str(self.id),
            'winNumber': self.winNumber,
            'loseNumber': self.loseNumber,
            'eloScore': self.eloScore
        }
        with open("stats/" + str(self.id) + ".json", 'w') as f:
            json.dump(data, f, indent=4)

    def update_stats(self, won):
        if won:
            self.winNumber += 1
            self.eloScore += 10
        else:
            self.loseNumber += 1
            self.eloScore -= 10

    def print_stats(self):
        lines = [
            f"Name: {self.name}",
            f"Wins: {self.winNumber}",
            f"Losses: {self.loseNumber}",
            f"ELO Score: {self.eloScore}"
        ]

        width = max(len(line) for line in lines) + 2

        print("  +" + "-" * width + "+")
        for line in lines:
            print(f"  | {line.ljust(width - 1)}|")
        print("  +" + "-" * width + "+")