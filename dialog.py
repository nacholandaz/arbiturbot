# Loads dialog and interacts with the file
import yaml

dialog = yaml.load(open('dialogs/dialog.yaml', 'rb'), Loader=yaml.FullLoader)

def get_interaction(interaction_name): return dialog.get(interaction_name)

def next_interaction_name(interaction_name):
    interaction = get_interaction(interaction_name)
    if get(interaction_name): return interaction.get('next_interaction')
