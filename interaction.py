# Defines interactions and their internal logic
import interactions.multiple_choice as multiple_choice
import interactions.text as text
import interactions.upload_drive as upload_drive
import interactions.ai as ai
import interactions.new_conversation_alert as new_conversation_alert
import interactions.pre_register_user as pre_register_user
import interactions.register_user as register_user
import interactions.redirect_message as redirect_message
import interactions.owned_users_threads as owned_users_threads
import interactions.conversational_interface as conversational_interface
import interactions.if_general_or_user as if_general_or_user
import interactions.switch_user as switch_user
import interactions.switch_pending_conversation as switch_pending
import interactions.exit_level as exit_level
import interactions.attend_new_message as attend_new_message
import interactions.if_bifurcation as if_bifurcation
import interactions.ls_command as ls_command
import interactions.list_users as list_users
import interactions.list_cases as list_cases
import interactions.list_pending_conversations as list_pending
import interactions.create_case as create_case
import interactions.close_case as close_case
import interactions.close_pending_conversation as close_pending
import interactions.follow_back as follow_back
import interactions.list_agents as list_agents
import interactions.pre_switch_agent as pre_switch_agent
import interactions.switch_agent as switch_agent
import conversation

def get_next_interaction_name(interaction, message):
    interaction_type = interaction.get('type')
    next_interaction_function = {
        'text': text.get_next_interaction,
        'multiple_choice': multiple_choice.get_next_interaction,
        'upload_drive': upload_drive.get_next_interaction,
        'ai': ai.get_next_interaction,
        'new_conversation_alert': new_conversation_alert.get_next_interaction,
        'pre_register_user': pre_register_user.get_next_interaction,
        'register_user': register_user.get_next_interaction,
        'redirect_message': redirect_message.get_next_interaction,
        'owned_users_threads': owned_users_threads.get_next_interaction,
        'conversational_interface': conversational_interface.get_next_interaction,
        'if_general_or_user': if_general_or_user.get_next_interaction,
        'switch_user': switch_user.get_next_interaction,
        'exit_level': exit_level.get_next_interaction,
        'attend_new_message': attend_new_message.get_next_interaction,
        'if_bifurcation': if_bifurcation.get_next_interaction,
        'list_users': list_users.get_next_interaction,
        'list_cases': list_cases.get_next_interaction,
        'list_pending': list_pending.get_next_interaction,
        'create_case': create_case.get_next_interaction,
        'close_case': close_case.get_next_interaction,
        'ls_command': ls_command.get_next_interaction,
        'switch_pending': switch_pending.get_next_interaction,
        'close_pending': close_pending.get_next_interaction,
        'follow_back': follow_back.get_next_interaction,
        'list_agents': list_agents.get_next_interaction,
        'pre_switch_agent': pre_switch_agent.get_next_interaction,
        'switch_agent': switch_agent.get_next_interaction,
    }
    return next_interaction_function[interaction_type](interaction, message)

def run_interaction(interaction, message):
    interaction_type = interaction.get('type')
    logic_function = {
        'text': text.logic,
        'multiple_choice': multiple_choice.logic,
        'upload_drive': upload_drive.logic,
        'ai': ai.logic,
        'new_conversation_alert': new_conversation_alert.logic,
        'pre_register_user': pre_register_user.logic,
        'register_user': register_user.logic,
        'redirect_message': redirect_message.logic,
        'owned_users_threads':owned_users_threads.logic,
        'conversational_interface': conversational_interface.logic,
        'if_general_or_user': if_general_or_user.logic,
        'switch_user': switch_user.logic,
        'exit_level': exit_level.logic,
        'attend_new_message': attend_new_message.logic,
        'if_bifurcation': if_bifurcation.logic,
        'list_users': list_users.logic,
        'list_cases': list_cases.logic,
        'list_pending': list_pending.logic,
        'create_case': create_case.logic,
        'close_case': close_case.logic,
        'ls_command': ls_command.logic,
        'switch_pending': switch_pending.logic,
        'close_pending': close_pending.logic,
        'follow_back': follow_back.logic,
        'list_agents': list_agents.logic,
        'pre_switch_agent': pre_switch_agent.logic,
        'switch_agent': switch_agent.logic,
    }
    return logic_function[interaction_type](interaction, message)


