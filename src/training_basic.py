from botConfiguration import BotConfiguration
from botCommandLoader import BotCommandLoader
from trainingBot import TrainingBot

print("Start [TrainingBot]")

# Load a configuration
config = BotConfiguration()
config.load('config/configuration.json')
config.info()

# Load available commands
commandLoader = BotCommandLoader()
commandLoader.load('config/command.json')
commandLoader.info()

# Create and start training bot
TrainingBot(config, commandLoader).start()


