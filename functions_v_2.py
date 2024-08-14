def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game(game_state,object_relations):
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before ." )
    print("You don't remember why you are here and what had happened before.")
    print("You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"],game_state,object_relations)


def play_room(room,game_state,object_relations):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room # get current room
    # display to user that he finished the game if current room is target room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    # display to user current room and ask for action
    else:
        print("You are now in " + room["name"])
        intended_action = input(f"What would you like to do in {room['name']}? Type '1' to show all objects or '2' to examine an object!").strip()
        if intended_action == "1":
            explore_room(room,object_relations)
            play_room(room,game_state,object_relations)
        elif intended_action == "2":
            examine_item(input(f"What would you like to examine in {room['name']}?").strip(),object_relations,game_state)
        else:
            print("Not sure what you mean. Type '1' to show all objects or '2' to examine an object!.")
            play_room(room,game_state,object_relations)
        linebreak()

def explore_room(room,object_relations):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

# define function to move to another room
def get_next_room_of_door(door, current_room, object_relations):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room
        
# define function to examine item
def examine_item(item_name,object_relations,game_state):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            # action for item of type "door"
            if(item["type"] == "door"):
                # check whether user has key for the door
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                # if user has key for the door, get next room
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room,object_relations)
                else:
                    output += "It is locked but you don't have the key."
            # action for item of other types (not "door")
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room,object_relations,game_state)
    else:
        play_room(current_room,object_relations,game_state)