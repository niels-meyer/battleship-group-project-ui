import json
import uuid

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
        with open(filename, 'r') as f:
            data = json.load(f)
            self.name = data['name']
            self.id = data['id']
            self.winNumber = data['winNumber']
            self.loseNumber = data['loseNumber']
            self.eloScore = data['eloScore']
    
    def save_to_file(self):
        if not hasattr(self, 'name'):
            print("Enter your username: ")
            self.name = str(input())
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