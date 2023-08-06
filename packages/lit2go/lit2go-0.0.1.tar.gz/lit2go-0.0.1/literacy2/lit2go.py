def show_usage():
  commands = ['home', 'next', 'back', 'check', 'progress']

  print('\nUsage:')
  print('  lit2go <command> [options]')
  print('\nCommands:')
  for c in commands:
    print(f'  {c}')

  print()

if __name__ == "__main__":
    show_usage()