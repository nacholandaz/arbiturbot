import os

from clint.arguments import Args
from clint.textui import puts, colored, indent, prompt
import os
from datetime import datetime

args = Args()

def is_on():
  return int(os.getenv('CLI_ON')) == 1

def set_mode(args):
  if '--user' in args:
    return 'user'
  return 'agent'

def get_intro(mode, user):
  if mode == 'user':
    return f'Arrancando en modo usuario({user}), conversar...'
  return f'Arrancando en modo agente({user}), conversar...'

def puts_reply(meta_chat):
  with indent(4, quote=' >'):
    user_id = meta_chat['chatId']
    text = meta_chat['body']
    chat_user = os.getenv('CLI_USER')
    if user_id == chat_user:
      puts(colored.blue(f'({datetime.now()}){user_id}- {text}'))
    else:
      puts(colored.green(f'({datetime.now()}){user_id}- {text}'))
    return True

def get_user(mode):
  users = {'agent':'5218117649489@c.us', 'user': '5218186861502@c.us'}
  return users.get(mode)

def hard_reset():
    from app import hard_reset
    hard_reset()
    return True

if __name__ == '__main__':
    from app import respond
    # Standard non-empty input
    os.environ['CLI_ON'] = "1"
    mode = set_mode(args)
    user = get_user(mode)
    os.environ['CLI_USER'] = user
    puts('Recuerda que no puedes tener el server y el cli prendido a la vez')
    puts(colored.red(get_intro(mode, user)))
    quit_loop = False

    while quit_loop == False:
      text = prompt.query("Mensaje a enviar('exit' para salir):")
      if text == 'exit':
        break
      data = {'body': text, 'author': user}
      try:
        respond(data)
      except:
        break

    delete = prompt.query("Desea eliminar el historial de conversacion (Y/N)?")
    if delete == 'Y': hard_reset()
    os.environ['CLI_ON'] = 'False'
    os.environ['CLI_USER'] = 'None'
