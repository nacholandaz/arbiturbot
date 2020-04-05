# Loads dialog and interacts with the file
import yaml
import os

import user

dialogs = { dialog.replace('.yaml', ''): yaml.load(open(f'dialogs/{dialog}', 'rb'), Loader=yaml.FullLoader)
           for dialog in os.listdir('dialogs') if '.yaml' in dialog }

def dialog_by_user_type(user_id):
    user_type = user.get_user_type(user_id)
    return dialogs.get(user_type)

def get_interaction(interaction_name, user_id):
    dialog = dialog_by_user_type(user_id)
    return dialog.get(interaction_name)

def next_interaction_name(interaction_name, user_id):
    interaction = get_interaction(interaction_name, user_id)
    if get(interaction_name): return interaction.get('next_interaction')
