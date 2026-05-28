# TextBasedGame.py
# Trevor Opheikens
# SNHU IT 140 - Intro to Scripting
# ======================================
# SECTION INDEX:
#  1. GAME MENU / INSTRUCTIONS       - Line ~12
#  2. GAME STARTER                   - Line ~20
#  3. MAIN GAME LOOP                  - Line ~26
#       - Status HUD
#       - Player Input
#       - Quit Handler
#       - Item Pickup Handler
#       - Movement Handler
#       - Inventory Handler
#       - Help Handler
#       - Invalid Command Handler
#  4. GAME MAP                        - Line ~90
#  5. PROGRAM ENTRY POINT             - Line ~106
# ======================================

# Required items to WIN
all_items = {'Map Fragment', 'Suppressed Sidearm', 'Crowbar', 'Marked Key', 'Combat Medkit', 'Breaching Charge'}
ITEM_DESCRIPTIONS = {'Map Fragment' : 'A torn piece of a tactical map. It shows you the location of a sniper tower and their line of sight. \nThis will be useful allowing you to move under cover and concealment.',
'Suppressed Sidearm' : 'A handy tool with only a few bullets. This will allow you to fire with reduced noise.',
'Crowbar' : 'A solid steel pry bar—useful for prying apart nailed boards. Could also be a good melee object.',
'Marked Key' : 'A unique looking key with a medical symbol imprinted on it. This might be useful.',
'Combat Medkit' : 'A standard issue personal medical kit. It contains bandages, wraps, and other medical items.',
'Breaching Charge' : 'Now this is some serious weaponry. \nIts a shape charge and can blow a door right off its hinges. \nA little bit of this can go a long way. Best to handle with care.'
}

INTRO_TEXT = """
You are embedded behind enemy lines with no resources or communications. Your team is scattered and likely missing.
A local told you they saw some uniformed soldiers taking a captive into a bombed-out district.
The local said these soldiers have set up a command post somewhere with in this district.
Your objective is to navigate this area and extract your captured teammate from the Enemy Commander’s Post.

Your current intel is shotty at best, so you’ll have to scavenge what you need.
There are six items located within this district you will have to collect in order to defeat the enemy commander.
Without all six, you and your buddy have no chance making it out alive.

Move carefully, pay attention to where your going, and take no unnecessary risks.

Type commands like:
  north / south / east / west (or “go north”, “head east”),
  get crowbar, pick up map fragment, grab the medkit.
  
You can enter "inventory" to see what items you have collected.
Type "help" for instructions or "quit" to exit.
  """

# --- GAME MENU/INSTRUCTIONS ---
def show_instructions():
    # Title Menu, player goal, and command options
    print()
    print('=== RESCUE PROTOCOL ===')
    print()
    print('Collect all six mission essential items before confronting the enemy commander!')
    print()
    print('Valid Commands:  go/move/head/walk/run "cardinal direction": North, South, East, West | get/pick uo/grab/collect/take "item" | Inventory | Help | Quit')
    print('-' * 150)
    print()
    # --- GAME INTRODUCTION ---
    print(INTRO_TEXT)

# --- START OF GAME ---
def main():
    show_instructions() # Shows title, intro, instructions, and exit.
    game_loop()

# --- CENTRAL FEEDBACK DISPLAY ---
def show_feedback(msg: str):
    if not msg:
        return
    print("\n" + msg + "\n")   # Adds spacing for readability

# --- ROOM ENTRY RULES ---
def check_entry_rules(next_room, inventory):
    # Crowbar gate for room 6.
    if next_room == 'Room 6' and 'Crowbar' not in inventory:
            return False, 'Wooden barricades block the entrance. You need a tool to pull them down.'

    # Boss room requires all six items.
    if next_room == 'Room 9' and 'Breaching Charge' not in inventory:
        return False, 'You cant enter the command post. You will need something to breach it.'

    return True, ''

# --- Alternate Direction Names ---
alt_dir_nam = {
    'n': 'North', 'north': 'North', 'go north': 'North', 'move north': 'North', 'head north': 'North', 'walk north': 'North', 'run north': 'North',
    's': 'South', 'south': 'South','go south': 'South', 'move south': 'South', 'head south': 'South', 'walk south': 'South', 'run south': 'South',
    'e': 'East',  'east': 'East', 'go east': 'East', 'move east': 'East', 'head east': 'East', 'walk east': 'East', 'run east': 'East',
    'w': 'West',  'west': 'West', 'go west' : 'West', 'move west': 'West', 'head west': 'West', 'walk west': 'West', 'run west': 'West'
}

def normalize_move(raw: str):
    # Normalize move commands to North/East/South/West
    s = raw.strip().lower()
    if s in alt_dir_nam:
        return alt_dir_nam[s]

    if s.startswith('go '):
        poss_dir = s.split(maxsplit=1)[1].lower()
        return alt_dir_nam.get(poss_dir)  # .get() avoids crashing if not found
    return None

# --- Alternate Item Pickup Names ---
coll_verbs = {'get', 'pickup', 'collect', 'take', 'grab'}
connecting_words = {'the', 'a', 'an'}

def normalize_get(raw: str):
    s = raw.strip().lower()

    #handle "pick up item" (two word verb)
    if s.startswith('pick up '):
        rest = s[len('pick up '):].strip()
        if not rest:
            return None
        parts = rest.split()
        if parts and parts[0] in connecting_words:
            parts = parts[1:]
        item = ' '.join(parts).strip()
        return item.title() if item else None

    # single word verbs (get, grab, take, etc.)
    parts = s.split()
    if not parts:
        return None
    verb, rest = parts[0], parts[1:]
    if verb in coll_verbs and rest:
        if rest[0] in connecting_words:
            rest = rest[1:]
        item = ' '.join(rest).strip()
        return item.title() if item else None

    return None

# --- New State ---
def get_new_state(direction, current_room, inventory, _status):
    exits_dict = rooms[current_room]['exits']

    # 1) Direction must exist from here
    if direction not in exits_dict:
        return current_room, 'You can’t go that way.'

    next_room = exits_dict[direction]

    # 2) Crowbar needed to enter Room 6
    if next_room == 'Room 6' and 'Crowbar' not in inventory:
        return current_room, 'Wooden barricades block the entrance. You need a tool to pull them down.'

    # 3) Breaching Charge needed to enter Room 9
    if next_room == 'Room 9' and 'Breaching Charge' not in inventory:
        return current_room, 'You can’t enter the command post. You need something to breach it.'

    # Passed all simple checks
    return next_room, None



# --- MAIN GAME LOOP ---

def game_loop():
    current_room = 'Room 1'  # Starts in "Room 1"
    inventory = []
    status = {'spotted_by_sniper': False, 'clinic_unlocked': False}

    while True:
        # --- STATUS HUD ---
        room_name = rooms[current_room]['name']
        print(f'\nYou are in the {room_name}.')
        item_here = rooms[current_room]['item']

        # --- ITEM VISIBILITY ---
        if current_room == 'Room 7' and item_here == 'Combat Medkit':
            # Clinic logic: locked case unless you have the Marked Key
            if 'Marked Key' not in inventory:
                print("You notice a locked medical case with a red cross. The medkit inside is sealed tight.")

            else:
                # One-time unlock message
                if not status.get('clinic_unlocked', False):
                    print('You use the Marked Key to unlock the medical case.')
                    status['clinic_unlocked'] = True
                print('The medical case is open.')
                print(f'You see a {item_here} here.')

        elif item_here:
            # Normal rooms show their item once
            print(f'You see a {item_here} here.')

        exits_dict = rooms[current_room]['exits']
        print('Exits:')
        for direction, next_room in exits_dict.items():
            desc = exit_disc.get(current_room, {}).get(direction, rooms[next_room]['name'])
            print(f'  {direction}: {desc}')

        # --- PLAYER INPUT ---
        raw = input('Enter move> ')
        command = raw.strip().lower()
        direction = normalize_move(raw)
        wanted_item = normalize_get(raw)

        # --- QUIT HANDLER ---
        if command == 'quit':
            print('Exiting the game... Thanks for playing!')
            break

        # --- ITEM PICKUP HANDLER ---
        elif wanted_item is not None:
            item_name = wanted_item  # already normalized by normalize_get()
            item_here = rooms[current_room]['item']
            can_pick = True
            msg = ''

            if not item_here:
                msg = "There's nothing to pick up."
                can_pick = False
            elif item_name.casefold() != item_here.casefold():
                msg = f'The {item_name} is not here.'
                can_pick = False
            elif (current_room == 'Room 7'
                  and item_here == 'Combat Medkit'
                  and 'Marked Key' not in inventory):
                msg = 'The medical case is locked. You need a Marked Key to open it.'
                can_pick = False

            if can_pick:
                inventory.append(item_here)
                rooms[current_room]['item'] = None
                print(f'You picked up the {item_here}.')
                desc = ITEM_DESCRIPTIONS.get(str(item_here), '')
                if desc:
                    print(desc)
            else:
                show_feedback(msg)

        # --- MOVEMENT HANDLER ---
        elif direction is not None:
            direction_key = direction
            next_room, msg = get_new_state(direction_key, current_room, inventory, status)
            if msg:
                show_feedback(msg)
                continue

            # --- Movement Allowed ---
            show_feedback(msg)
            print()
            current_room = next_room

            # Guards at Weapons Depot (Room 8)
            if current_room == 'Room 8':
                if 'Suppressed Sidearm' not in inventory:
                    print('Guards spot you approaching the weapons depot without a distraction.')
                    print('They open fire... \nGAME OVER.')
                    break

                else:
                    print('You use the Suppressed Sidearm to distract the guards. Its safe to move in.')

            # --- SNIPER RISK LOGIC ---
            if current_room in {'Room 3', 'Room 4', 'Room 5', 'Room 7'} and 'Map Fragment' not in inventory:
                if not status.get('spotted_by_sniper', False):
                    print("The sniper spots you moving without cover! He’s tracking you now...")
                    status['spotted_by_sniper'] = True
                else:
                    print('The sniper fires! You’ve been taken out.'
                            '\nHint: The Map Fragment helps you avoid the sniper watch.'
                            '\nGAME OVER.')
                    break
                # else: you have the Map Fragment → safe

            # --- BOSS ROOM OUTCOME ---
            if current_room == 'Room 9':
                missing = sorted(list(all_items - set(inventory)))

                if 'Combat Medkit' not in inventory:
                    print('You breached the Command Post and the enemy commander was defeated!'
                            '\nUpon entering the rubbled post, you find you missing buddy. It looks like they were brutally interrogated.'
                            "\nYour buddies wounds are too severe and they don't make it out alive."
                            '\n MISSION FAILED.')
                    return

                if missing:
                    # When you have the medkit  but the player is missing other gear.
                    print('You successfully breached the command post but you missing gear critical for your escape!.')
                    print(', '.join(missing))
                    print('\nYou can’t complete the rescue properly.'
                          '\n MISSION FAILED.')
                    return

                else:
                # All required items are present in player inventory
                    print('You successfully breached the command post and neutralized the enemy commander.'
                        '\nUpon entering the rubbled post, you discover your buddy. It looks like he was brutally interrogated.'
                        '\nYou use your Combat Medkit to patch them up just enough to keep them alive while you two make your escape.'
                        '\nMISSION COMPLETED SUCCESSFULLY.')
                    return

        # --- INVENTORY HANDLER ---
        elif command == 'inventory':
            print(f'Inventory: {inventory if inventory else "None"}')

        # --- HELP HANDLER ---
        elif command in ('help', '?'):
            print('Commands: go/move/head   north/south/east/west | get/take/grab/collect <item name> | inventory | help | quit')

        # --- INVALID COMMAND HANDLER ---
        else:
            print('Invalid command.')

# --- GAME MAP ---
rooms = { # Stating Room is "Room 1".
    'Room 1' : {'name' : 'Forward Observation Post', 'item' : None, 'exits' : {'East':'Room 2'}},
    'Room 2' : {'name' : 'Supply Cache', 'item' : 'Map Fragment', 'exits' : {'South' : 'Room 3', 'West' : 'Room 1'}},
    'Room 3' : {'name' : 'Alley-way', 'item' : 'Suppressed Sidearm', 'exits' : {'North' : 'Room 2', 'South' : 'Room 4'}},
    'Room 4' : {'name' : 'Maintenance Room', 'item' : 'Crowbar', 'exits' : {'North' : 'Room 3', 'East' : 'Room 6', 'South' : 'Room 7', 'West' : 'Room 5'}},
    'Room 5' : {'name' : 'Rubble Courtyard', 'item' : 'Marked Key', 'exits' : {'East' : 'Room 4'}},
    'Room 6' : {'name' : 'Sniper Tower', 'item' : None, 'exits' : {'West' : 'Room 4', 'South' : 'Room 9'}},
    'Room 7' : {'name' : 'Abandoned Field Clinic', 'item' : 'Combat Medkit', 'exits' : {'North' : 'Room 4', 'South' : 'Room 8'}},
    'Room 8' : {'name' : 'Weapon Storage Depot', 'item' : 'Breaching Charge', 'exits' : {'North' : 'Room 7'}},
    'Room 9' : {'name' : 'Enemy Commanders Post', 'item' : None , 'exits' : {'North' : 'Room 6'}},
}
exit_disc = {
    'Room 1': {
        'East' : 'There is a supply cache this way. It looks abandoned and it does not look like anyone is watching it.'
    },
    'Room 2': {
        'South' : 'Looking south, theres an alley-way I can get closer to the commanders post. Looks safe enough.',
        'West' : 'West will take me back to the forward observation post.'
    },
    'Room 3' : {
        'North' : 'This way leads back to the supply cache.',
        'South' : 'It looks like theres some kind of maintenance office ahead.'
    },
    'Room 4' : {
        'North' : 'This goes back to the Alley-way.',
        'East' : 'There is a tall towering building this way. \nThe top floor would have a good vantage point. That must be where the sniper is. Best be careful.',
        'South' : 'This way, there looks to be some sort of field clinic. This place should have medical supplies.',
        'West' : 'Theres lots of rubble over here. I should be able to pass through it.'
    },
    'Room 5' : {'East' : 'I can take this way back to the maintenance room.'},
    'Room 6' : {'South' : 'Theres a door here that says "Commanders Post".\nMy friend must be inside!.',
                'West' : 'I can head back to the maintenance room this way'
                },
    'Room 7' : {'North' : 'North goes back to the maintenance room.',
                'South' : 'I can see the Weapons Depot this way. \nThat place should have something I can use to get into the commanders post. \nOnly problem is, theres some heavily armored guards. I will have to distract them.'},
    'Room 8' : {'North' : 'Looks like the only way back is North.'}}

if __name__ == '__main__':
    main()