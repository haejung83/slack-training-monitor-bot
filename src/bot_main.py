from bot_configuration import BotConfiguration
from bot_command_loader import BotCommandLoader
from bot_training import TrainingBot

print("Start [TrainingBot]")

# Load a configuration
config = BotConfiguration()
config.load('config/configuration.json')
config.info()

# Load available commands
command_loader = BotCommandLoader()
command_loader.load('config/command.json')
command_loader.info()

# Create and start training bot
TrainingBot(config, command_loader).start()


