"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    with (open("map.txt") as map_file, open("locations.txt", encoding='utf-8') as locations_file,
          open("items.txt") as items_file):
        w = World(map_file, locations_file, items_file)
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate

    allowed_moves = 20
    grid = w.map
    menu = ["look", "inventory", "score", "quit"]
    choice = ''

    while not p.victory and p.moves <= allowed_moves:
        location = w.get_location(p.x, p.y)

        # Depending on whether it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)
        if choice == 'look':
            pass

        elif location.visited:
            print(location.brief_description)

        else:
            print(location.long_description)
            location.visited = True
            if location.visit_points != 0:
                p.score += location.visit_points
                print(f"You got {location.visit_points} points for visiting this location!")

        print("What to do? \n")
        print("[menu]")
        for action in p.available_actions(grid, location):
            print(action)
        choice = input("\nEnter action: ").lower()

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ").lower()

        if choice == "quit":
            break
        w.do_actions(p, location, choice)

    if p.victory:
        print("Congratulations! You have successfully retrieved all of your crucial belongings! \n"
              "With all of them in hand, you stride confindently into the Exam Centre,\n"
              "ready to complete your final quest - the computer science exam.\n"
              "After a long journey, it is time to focus and apply your knowledge to the true test.\n"
              "Best of luck to you, and may your code be bug-free.")
        print(f'You had {allowed_moves - p.moves} remaining. You completed the game with {p.score} points.')

    else:
        if p.moves > allowed_moves:
            print("As you rush toward your next destination and check your watch, you realize with a sinking feeling \n"
                  "that the exam has already begun. Despite your utmost efforts, the race against the clock comes to \n"
                  "a melancholic end. It appears the journey until now has all been for naught. However, in every \n"
                  "defeat lies a lesson. Keep your head high, and you will be better equipped for success!")
        else:
            print("Regrettably, the quest to find all of your items scattered across the campus \n"
                  "proved to be a challenge too arduous to complete. You have made the difficult decision to quit, \n"
                  "leaving your items unclaimed. The path to success is filled with failures, and it seems as though\n"
                  "this is one of those moments. Stay resilient, and may fortune favour you in the future.")

        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
