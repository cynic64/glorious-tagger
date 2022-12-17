'''
For now, only implement adding data to files
'''
import csv
import sys
import tty
import termios
import math

LEADER = 0
STRING = 1
NUMBER = 2

NOT_KEY = 0
KEY = 1

def read_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

def print_tree(tree, indent_level):
        for (key, value) in tree.items():
                print('  ' * indent_level * 2, end='')

                print(f'{key} -> {value[2]}', end='')
                
                if value[0] == LEADER:
                        print()
                        print_tree(value[3], indent_level + 1)
                elif value[0] == NUMBER:
                        print(f', {value[3][0]} .. {value[3][1]}')
                else:
                        print()

def print_title(title):
        print('-' * 80)
        print(' ' * math.floor((80 - len(title)) / 2), end='')
        print(title, end='')
        print(' ' * math.ceil((80 - len(title)) / 2))
        print('-' * 80)

def select(key, tree):
        '''
        Returns key (string), value (string / int) and done (bool).
        done is set if the user presses 'n' to go to the next file.
        '''
        # Maybe we're already at the end?
        if tree[0] == STRING:
                # If it's a string, then that's the key.
                value = tree[2]
                return key, value, False
        elif tree[0] == NUMBER:
                # If it's a number, we need to read it in
                lower, upper = int(tree[3][0]), int(tree[3][1])
                n = None

                while n == None or n < lower or n > upper:
                        n = ''
                        print(f'Enter number for {key} in {tree[3][0]} .. {tree[3][1]}: ', end='')
                        sys.stdout.flush()
                        n = read_char()
                        if n == '-': n += read_char()
                        n = int(n)
                        print()

                value = n
                return key, value, False

        # Otherwise, we're still in the tree and need to select something
        ch = read_char()
        if ch == 'Q':
                sys.exit(0)
        elif ch == 'n':
                # Go to next file by returning True for done
                return None, None, True

        if ch not in tree[3].keys():
                # Invalid key, repeat the whole process
                return select(key, tree)
                
        tree = tree[3][ch]

        if tree[1] == KEY:
                # If this node has the KEY attribute, set key to the node's name
                key = tree[2]

        # Print out the current node so the user has some feedback
        if tree[0] == LEADER:
                print(tree[2] + ' -> ', end='')
                sys.stdout.flush()
        else:
                print(tree[2])

        return select(key, tree)


tree = (LEADER, NOT_KEY, 'main', {
        'q': (NUMBER, KEY, 'quality', (-9, 9)),
        'u': (NUMBER, KEY, 'universal appeal', (-9, 9)),
        'l': (NUMBER, KEY, 'i like it', (-9, 9)),
        'c': (NUMBER, KEY, 'complexity', (0, 9)),
        'g': (LEADER, KEY, 'genre', {
                'm': (LEADER, NOT_KEY, 'metal', {
                        'd': (STRING, NOT_KEY, 'death metal'),
                        'b': (STRING, NOT_KEY, 'black metal')
                }),
                'e': (LEADER, NOT_KEY, 'edm', {
                        'e': (STRING, NOT_KEY, 'edm'),
                        'h': (STRING, NOT_KEY, 'house'),
                        'd': (STRING, NOT_KEY, 'drum and bass'),
                        't': (STRING, NOT_KEY, 'techno'),
                        'T': (STRING, NOT_KEY, 'trip hop'),
                }),
                'r': (LEADER, NOT_KEY, 'rock', {
                        'r': (STRING, NOT_KEY, 'rock'),
                        'c': (STRING, NOT_KEY, 'classic rock'),
                        'm': (STRING, NOT_KEY, 'poppy metal')
                }),
                'R': (STRING, NOT_KEY, 'rap')
        }),
        'L': (NUMBER, KEY, 'lyric quality', (-9, 9)),
        'v': (NUMBER, KEY, 'valence', (-9, 9)),
        'i': (NUMBER, KEY, 'intensity', (-9, 9)),
        'h': (STRING, KEY, 'high-class'),
        'r': (STRING, KEY, 'redline'),
        's': (STRING, KEY, 'spy'),
        'G': (STRING, KEY, 'german'),
        'w': (NUMBER, KEY, 'wubby', (0, 9))
})

if len(sys.argv) < 2:
        print('Usage: interactive.py [-m COUNT] [TAGS] FILES')
        print('If -m is specified, the next COUNT arguments will be interpreted as mandatory tags.')
        sys.exit(1)


# Check for mandatory tags
# Usually files start at sys.argv[1] - but not if there are mandatory arguments
files_start_idx = 1
mandatory_tags = []
if sys.argv[1] == '-m':
        if len(sys.argv) < 3:
                print('You specified -m but didn\'t provide COUNT.')
                sys.exit(1)

        mandatory_count = int(sys.argv[2])
        if len(sys.argv) < 3 + mandatory_count:
                print(f'You specified {mandatory_count} mandatory tags but didn\'t provide enough.')
                sys.exit(1)
        mandatory_tags = sys.argv[3:3+mandatory_count]
        print('Mandatory tags:', mandatory_tags)
        files_start_idx = 3 + mandatory_count
        mandatory = True

print('Press Q to exit.')
print('Press n to move to next file.')
for path in sys.argv[files_start_idx:]:
        # Print title
        title = path.split('/')[-1]
        print_title(title)

        # Print existing contents
        f = open(path, 'r')
        print(f.read()[:-1])
        f.close()
        print('-' * 80)
        
        with open(path, 'a') as out_file:
                print('Options:')
                print_tree(tree[3], 1)

                count = 0
                while True:
                        # Maybe we have mandatory tags to go through?
                        if count < len(mandatory_tags):
                                subtree = tree[3][mandatory_tags[count]]
                                key = subtree[2]
                                count += 1
                        else:
                                key = None
                                subtree = tree

                        # Actually select
                        key, value, done = select(key, subtree)
                        if done: break

                        if key == value:
                                # This is the case with a tag like high-class. Don't write it twice.
                                string = key
                        else:
                                string = f'{key}: {value}'
                        print('Setting', string)
                        out_file.write(string + '\n')
