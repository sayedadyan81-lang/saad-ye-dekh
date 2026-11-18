import random
import time

# Map layout: each room connects to adjacent rooms
HOUSE_MAP = {
    "Bedroom": ["Hallway"],
    "Hallway": ["Bedroom", "Kitchen", "Living Room", "Basement Stairs"],
    "Kitchen": ["Hallway", "Backyard"],
    "Living Room": ["Hallway", "Front Door"],
    "Basement Stairs": ["Hallway", "Basement"],
    "Basement": ["Basement Stairs"],
    "Backyard": ["Kitchen"],
    "Front Door": ["Living Room"]
}

# Five difficulty levels: (Name, Entity Move Chance %, Stalking Accuracy %)
DIFFICULTIES = {
    "1": ("Ghost (Very Easy)", 40, 30),
    "2": ("Easy", 55, 50),
    "3": ("Normal", 70, 70),
    "4": ("Hard", 85, 85),
    "5": ("Nightmare", 100, 95)
}

def play_game():
    print("=== FIVE DAYS IN THE DARK ===")
    print("Survive 5 days. Collect 3 Keys to unlock the Front Door, or outlast the clock.\n")
    
    print("Choose Difficulty:")
    for k, v in DIFFICULTIES.items():
        print(f"  {k}. {v[0]}")
    
    choice = input("\nEnter difficulty (1-5): ").strip()
    diff_name, move_chance, track_chance = DIFFICULTIES.get(choice, DIFFICULTIES["3"])
    print(f"\nStarting on {diff_name} mode...\n")
    time.sleep(1)

    player_room = "Bedroom"
    entity_room = "Basement"
    keys_found = 0
    key_locations = random.sample(["Kitchen", "Basement", "Backyard", "Living Room"], 3)
    hiding = False

    for day in range(1, 6):
        print(f"\n==================== DAY {day} OF 5 ====================")
        # Each day lasts 6 turns (hours from 12 AM to 6 AM)
        for hour in range(6):
            clock = "12 AM" if hour == 0 else f"{hour} AM"
            print(f"\n--- Day {day} | {clock} | Keys: {keys_found}/3 ---")
            print(f"Location: {player_room}")
            
            # Proximity warning
            if entity_room in HOUSE_MAP[player_room]:
                print("WARNING: You hear heavy footsteps right outside the door!")
            elif entity_room == player_room and not hiding:
                print("\nTHE ENTITY FOUND YOU! GAME OVER.")
                return

            # Player Action
            hiding = False
            print("\nActions:")
            print("  1. Move to another room")
            print("  2. Search room for a key")
            print("  3. Hide in the shadows")
            
            action = input("Choose action (1-3): ").strip()

            if action == "1":
                neighbors = HOUSE_MAP[player_room]
                print("\nConnected rooms:")
                for idx, room in enumerate(neighbors, 1):
                    print(f"  {idx}. {room}")
                move_choice = input("Where do you go? ").strip()
                if move_choice.isdigit() and 1 <= int(move_choice) <= len(neighbors):
                    player_room = neighbors[int(move_choice) - 1]
                    print(f"You crept into the {player_room}.")
                    
                    if player_room == "Front Door" and keys_found >= 3:
                        print("\nYou unlocked the Front Door and escaped into the night! YOU WIN!")
                        return
                else:
                    print("You hesitated and stayed put.")

            elif action == "2":
                print(f"You quietly search the {player_room}...")
                time.sleep(1)
                if player_room in key_locations:
                    key_locations.remove(player_room)
                    keys_found += 1
                    print(f"SUCCESS! You found a rusty key! ({keys_found}/3)")
                else:
                    print("Nothing here.")

            elif action == "3":
                hiding = True
                print("You hold your breath and hide in the dark...")
            else:
                print("Invalid choice. You froze in fear.")

            # Entity AI Turn (Follows the player)
            if random.randint(1, 100) <= move_chance:
                entity_neighbors = HOUSE_MAP[entity_room]
                
                # Smart tracking: move toward player's room or adjacent room
                if random.randint(1, 100) <= track_chance:
                    if player_room in entity_neighbors:
                        entity_room = player_room
                    else:
                        # Find a room connected to both entity and player
                        bridge = [r for r in entity_neighbors if player_room in HOUSE_MAP[r]]
                        entity_room = random.choice(bridge) if bridge else random.choice(entity_neighbors)
                else:
                    entity_room = random.choice(entity_neighbors)

            # Check Encounter after Entity moves
            if entity_room == player_room:
                if hiding:
                    print("\nThe entity walks right past your hiding spot... It didn't see you!")
                else:
                    print(f"\nThe entity lunges out of the dark in the {player_room}!")
                    print("GAME OVER.")
                    return

        print(f"\n6 AM chimes. Sunlight pierces the windows. You survived Day {day}!")
        # Reset positions slightly for the next night
        player_room = "Bedroom"
        entity_room = "Basement"
        time.sleep(1.5)

    print("\nYOU SURVIVED ALL 5 DAYS! YOU ESCAPED THE NIGHTMARE!")

if __name__ == "__main__":
    play_game()
