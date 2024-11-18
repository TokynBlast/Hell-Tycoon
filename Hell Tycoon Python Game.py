import pytgm as tgm
import time
import sys
import os
import random
import threading

red = tgm.graphics.color(255, 0, 0)
res = tgm.graphics.res

title = f'''{red}  _    _      _ _   _______                          
 | |  | |    | | | |__   __|                         
 | |__| | ___| | |    | |_   _  ___ ___   ___  _ __  
 |  __  |/ _ \\ | |    | | | | |/ __/ _ \\ / _ \\| '_ \\
 | |  | |  __/ | |    | | |_| | (_| (_) | (_) | | | |
 |_|  |_|\\___|_|_|    |_|\\__, |\\___\\___/ \\___/|_| |_|
                          __/ |                      
                         |___/{res}'''

# Name:[price,size,spawn/min]
population = {'Demon Pod': [10, 1, 0.5], 'Flogger Hotel': [10, 5, 1], 'Pity Mansion': [50, 15, 4], "Bart's Torture School":[80,25,8], 'Breeding Pit':[100,10]}
# Name:[price,area]
expansion = {'Volcanic Pits': [50, 25], 'Manequin Town': [100, 50], 'Sould Yard':[250, 95], 'Lava Pits':[400, 125]}
# Name:[price,size,souls/min]
torture = {'Screaming Bull': [5, 3, 1], 'Bamboo Growth':[8,2,1.5], 'Worst Fear':[10,4,2], 'Iron Maiden':[20,4,4],  'Drug cocktail':[30,2,6], 'Hot Boxing':[43,5,8]}
global SpPM, SoPM
souls = 50
area = 20
population_ = 15
SoPM = 0 # Souls Per Minute
SpPM = 0 # Spawn Per Minute


def SOP_Update():
    def updater():
        global population_, souls
        while True:
            time.sleep(20)
            
            population_ += SpPM
            souls += SoPM

            
    update_thread = threading.Thread(target=updater)
    update_thread.daemon = True
    update_thread.start()

    

def getch():
    try:
        if sys.platform.startswith('win'):
            import msvcrt
            g = msvcrt.getch()
            if g == b'K': return 'ArrowLeft'
            elif g == b'M': return 'ArrowRight'
            elif g == b'H': return 'ArrowUp'
            elif g == b'P': return 'ArrowDown'
            elif g == b'\r': return 'Enter'
            else:
                return g
        else:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch += sys.stdin.read(2)
                return ch.encode('utf-8')
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception as e:
        print(f"Error in getch: {e}")
        return None


def typewrite(text, Min=0.1, Max=0.3):
    stop_typing = False

    def keyP():
        nonlocal stop_typing
        getch()
        stop_typing = True

    keypress_thread = threading.Thread(target=keyP)
    keypress_thread.daemon = True
    keypress_thread.start()

    for char in text:
        if stop_typing:
            break
        sys.stdout.write(char)
        sys.stdout.flush()
        delay = random.uniform(Min, Max)
        time.sleep(delay)

    if stop_typing:
        sys.stdout.write(text[len(char):])
        sys.stdout.flush()
    
    print()

tgm.graphics.cls()
print('Press any button to skip\n')
typewrite('''Hey there boss!
Oh? a new boss? that makes sense,
the last "Lucifer" SUCKED at his job!
He was defeated by a cup and a FUCKING mug!
But you? I think you have a little potential!
The previous devil left you with some souls!
And her annoying daughter, Charlie...
She's trying to get demons into heaven...
It's probably because the dumb bitch MATED WITH God!
Worst of all? It was here!
IN HELL! Well... in a closet...
Like who on earth would do that?!
Besides Pinkle...
Everybody hates her!
Anyways...\n\n''',0,.2)

input("Press the 'Enter' key to continue")

tabs = [population, expansion, torture]
tab_num = 0

# Cursor: ►
cursor_num = 0

SOP_Update()

while True:
    tgm.graphics.cls()
    print(title, end='\n\n')

    print(f'''Souls:  {souls}
Area:   {area}\n\n''')

    current = tabs[tab_num]

    headers = ['Population', 'Expansion', 'Torture']
    header_display = []
    
    for index, header in enumerate(headers):
        if index == tab_num:
            header_display.append(f"{red}{header}{res}")
        else:
            header_display.append(header)
    
    print(f'''┌──────────┬─────────┬───────┐
│{header_display[0]}│{header_display[1]}│{header_display[2]}│
├──────────┴─────────┴───────┤''')

    for index, item in enumerate(current):
        cursor = '► ' if index == cursor_num else '  '

        price = str(current[item][0])
        total_length = 26  
        item_length = len(item)
        price_length = len(price)
        
        spaces_needed = total_length - item_length - price_length - 2
        spaces = ' ' * spaces_needed
        
        print(f'│{cursor}{item} {spaces}◊{price}│')
        
    print('└────────────────────────────┘')
    choi = getch()
    
    if choi == 'ArrowUp':
        cursor_num = max(0, cursor_num - 1)
    elif choi == 'ArrowDown':
        cursor_num = min(len(current) - 1, cursor_num + 1)
    elif choi == 'ArrowRight':
        tab_num = (tab_num + 1) % len(tabs)
        cursor_num = 0
    elif choi == 'ArrowLeft':
        tab_num = (tab_num - 1) % len(tabs)
        cursor_num = 0
    elif choi == 'Enter':
        try:
            selected = list(current.keys())[cursor_num]
            if current[selected][0] > souls:
                print(f"You can't buy {selected}, you need {current[selected][0] - souls} more souls!")
            else:
                souls -= current[selected][0]
                print(f'You bought {selected}!')
                if current != expansion:
                    if area >= current[selected][1]:
                        area -= current[selected][1]
                        if current == torture:
                            SoPM += current[selected][2]
                        if current == population:
                            SpPM += current[selected][2]
                    else:
                        print("You can't buy {selected}! You don't have enough area!")
                else:
                    area += current[selected][1]            
                
        except Exception as e:
            print(f"Error selecting item: {e}")
        time.sleep(3)
