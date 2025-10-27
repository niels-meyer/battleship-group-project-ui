import json
import uuid
from InquirerPy import inquirer

class Stats:
    def __init__(self):
        self.id = uuid.uuid4()
        self.winNumber = 0
        self.loseNumber = 0
        self.eloScore = 500
        self.name = None
    
    def createNew(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.winNumber = 0
        self.loseNumber = 0
        self.eloScore = 500
    
    def loadFromFile(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.name = data['name']
            self.id = data['id']
            self.winNumber = data['winNumber']
            self.loseNumber = data['loseNumber']
            self.eloScore = data['eloScore']
    
    def saveToFile(self):
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

    def updateStats(self, won):
        if won:
            self.winNumber += 1
            self.eloScore += 10
        else:
            self.loseNumber += 1
            self.eloScore -= 10

stats = Stats()

def mainMenueSelectionHandler():
    mainMenueSelection = inquirer.select(
    message="Welcom to Battleships! What do you want to do?",
    choices=["Play", "Stats", "Rules", "Exite"],
    ).execute()
    match mainMenueSelection:
        case "Play":
            print("Starting a new game...")
        case "Stats":
            statsMenueSelectionHandler()
        case "Rules":
            print("Displaying rules...")
        case "Exite":
            print("Exiting the game...")


def statsMenueSelectionHandler():
    if (stats.name is None):
        print("No stats available. Please create a profile first or load the data from a file.")
        statsMenueSelectionCreation = inquirer.select(
        message="What do you want to do?",
        choices=["Create New Profile", "Load from File", "Back to Main Menu"],
        ).execute()
        match statsMenueSelectionCreation:
            case "Create New Profile":
                print("Enter your username: ")
                username = str(input())
                stats.createNew(username)
                stats.saveToFile()
            case "Load from File":
                print("Enter the filename to load from (including path): ")
                filename = str(input())
                stats.loadFromFile(filename)
            case "Back to Main Menu":
                mainMenueSelectionHandler()
    statsMenueSelection = inquirer.select(
    message="What do you want to do?",
    choices=["View Stats", "Save Stats","Loade new Stats from File", "Back to Main Menu"],
    ).execute()
    match statsMenueSelection:
        case "View Stats":
            print(f"Name: {stats.name}")
            print(f"Wins: {stats.winNumber}")
            print(f"Losses: {stats.loseNumber}")
            print(f"ELO Score: {stats.eloScore}")
            statsMenueSelectionHandler()
        case "Save Stats":
            stats.saveToFile()
            statsMenueSelectionHandler()
        case "Loade new Stats from File":
            print("Enter the filename to load from (including path): ")
            filename = str(input())
            stats.loadFromFile(filename)
            statsMenueSelectionHandler()
        case "Back to Main Menu":
            mainMenueSelectionHandler()

mainMenueSelectionHandler()
print(stats.id)