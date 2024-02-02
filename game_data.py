"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - position: an integer representing the position of the location on the world map
        - brief_description: a brief description of the location used after the first visit
        - long_description: a long description of the location use for a first time visit or when look is called
        - actions: a list of strings of available commands/directions to move at this location
        - location_items: items that are available at this location or None if there are no items
        - visited: True if the location has been visited before, otherwise False

    Representation Invariants:
        - self.position >= -1
        - self.brief_description != '' and self.long_description != ''
        - len(self.brief_description) <= len(self.long_description)
        - # TODO
    """
    position: int
    brief_description: str
    long_description: str
    actions: list[str]
    location_items: list
    visited: bool

    def __init__(self, position: int, brief: str, long: str) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.
        self.position = position
        self.brief_description = brief
        self.long_description = long
        self.location_items = []
        self.visited = False

        # TODO: Complete this method


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: the name of the item
        - curr_position: the current position of the item on the map, represented as an integer
        - target_position: the position where the item must be deposited for points, represented as an integer
        - target_points: the amount of points the item will give for being deposited at target_position.

    Representation Invariants:
        - self.name != ''
        - self.curr_position >= 0 and self.target_position >= 0
        - # TODO
    """
    name: str
    curr_position: int
    target_position: int
    target_points: int

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.curr_position = start
        self.target_position = target
        self.target_points = target_points


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: the x coordinate of the player, represented as an integer
        - y: the y coordinate of the player, represented as an integer
        - inventory: the player's inventory of items, represented as a list
        - victory: a variable that remains False until the player wins the game
        - score: the total score of the player in the game
        - moves: the total number of "moves" the player has made so far

    Representation Invariants:
        - self.x >= 0 and self.y >= 0
        - all([isinstance(item, Item) for item in self.inventory])
        - self.score >= 0 and self.moves >= 0
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """
        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.score = 0
        self.moves = 0

    def available_actions(self, grid: list[list[int]], location: Location) -> list[str]:
        """
        Return the available actions of this player at in this location.
        The actions should depend on the items available in the location
        and the x,y position of the player on the world map.
        """

        actions = []
        x = self.x
        y = self.y

        # Directions
        if (y - 1 >= 0) and (grid[y - 1][x] != -1):
            actions.append('North')

        if (y + 1 <= len(grid) - 1) and (grid[y + 1][x] != -1):
            actions.append('South')

        if (x + 1 <= len(grid[y]) - 1) and (grid[y][x + 1] != -1):
            actions.append('East')

        if (x - 1 >= 0) and (grid[y][x - 1] != -1):
            actions.append('West')

        # Pick up / Drop
        if location.location_items:  # location_items != []
            actions.append("Pick up")

        if self.inventory:  # self.inventory != []
            actions.append("Drop")

        return actions

    def go(self, direction: str) -> None:
        """Change the player's x and y coordinate to reflect the direction they are travelling in.
        This function is only called when the move is valid (in the do_actions function) therefore, no need
        to check again in this method.
        """
        if direction == 'north':
            self.y -= 1

        elif direction == 'south':
            self.y += 1

        elif direction == 'east':
            self.x += 1

        else:
            self.x -= 1

        self.moves += 1
        return

    def open_inventory(self) -> None:
        """Displays the names of the items in the player's inventory
        """
        item_names = [item.name for item in self.inventory]

        if item_names:
            print(f"This is what is in your bag: {item_names}")

        else:
            print("Your bag is empty. *crickets*")
        print()

        return

    def pick_up(self, location: Location) -> None:
        """Add an item to the items of the location the player is currently at and remove the item
        from the player's inventory. Update the player's score if the picked up the item from its
        target location. This is a mutating method and returns None.
        """
        item_names = [item.name.lower() for item in location.location_items]

        print(f"You found: {item_names}")

        done = False
        pick_choice = ''
        while not done:
            pick_choice = input("Which item would you like to pick up?").lower()
            if pick_choice in item_names:
                done = True
            else:
                print("That item is not here.\n")

        # find the index of the item
        pick_index = 0
        for i in range(len(item_names)):
            if pick_choice == item_names[i]:
                pick_index = i

        # drop pick up item from location and adjust points if needed
        item = location.location_items.pop(pick_index)
        self.inventory.append(item)
        print(f"You picked up the {item.name}.\n")

        if item.target_position == location.position:
            self.score -= item.target_points

    def drop(self, location: Location) -> None:
        """Remove an item from the player's intventory and add it to the items of the location
        in which the player is currently at. Update the player's score if they dropped the item into its
        target location. This is a mutating method and returns None.
        """
        item_names = [item.name.lower() for item in self.inventory]

        print(f"You have: {item_names}")

        done = False
        drop_choice = ''
        while not done:
            drop_choice = input("Which item would you like to drop?").lower()
            if drop_choice in item_names:
                done = True
            else:
                print("You don't have that item.\n")

        # find the index of the item
        drop_index = 0
        for i in range(len(item_names)):
            if drop_choice == item_names[i]:
                drop_index = i

        # drop item into location and adjust points if needed
        item = self.inventory.pop(drop_index)
        location.location_items.append(item)
        print(f"You dropped the {item.name}.\n")

        if item.target_position == location.position:
            self.score += item.target_points


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations: a list representation of the locations in this world
        - items: a list representation of the items in this world

    Representation Invariants:
        - len(self.map) > 0 and all([len(row) > 0 for row in self.map])
    """

    map: list[list[int]]
    locations: list[Location]
    items: list[Item]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)

        self.locations = self.load_locations(location_data)

        self.items = self.load_items(items_data)

        for item in self.items:
            index = item.curr_position
            self.locations[index].location_items.append(item)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        grid = []
        for line in map_data:
            temp = line.split()
            temp = [int(item) for item in temp]
            grid.append(temp)
        return grid

    def load_locations(self, location_data: TextIO) -> list[Location]:
        """
        Initialize every Location from open file location_data and store each Location in a list and
        return the list of Locations.
         """

        locations = []
        line = location_data.readline()
        while line:
            position = int(line)
            brief = location_data.readline().strip()
            line = location_data.readline().strip()
            long = ''
            while line != 'END':
                long += line + '\n'
                line = location_data.readline().strip()

            location = Location(position, brief, long)
            locations.append(location)
            location_data.readline()  # skip the blank line
            line = location_data.readline()

        return locations

    def load_items(self, items_data: TextIO) -> list[Item]:
        """
        Initialize every Item from open file item_data and store each Item in a list and
        return the list of Items.
        """

        items = []
        for line in items_data:
            parts = line.split()
            curr_position, target_position, target_points = int(parts.pop(0)), int(parts.pop(0)), int(parts.pop(0))
            name = ' '.join(parts)

            item = Item(name, curr_position, target_position, target_points)
            items.append(item)

        return items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        y_length = len(self.map)
        x_length = len(self.map[0])
        if not (0 <= y <= y_length) or not (0 <= x <= x_length):
            return None

        position = self.map[y][x]
        if position == -1:
            return None

        else:
            return self.locations[position]

    def do_actions(self, p: Player, location: Location, choice: str) -> None:
        """
        this function does stuff
        """
        valid_choices = p.available_actions(self.map, location)
        valid_choices = [action.lower() for action in valid_choices]
        valid_choices.extend(["look", "inventory", "score", "quit"])

        if choice not in valid_choices:
            print("Invalid option. Please try again.\n")
            return

        elif choice == 'north' or choice == 'east' or choice == 'south' or choice == 'west':
            p.go(choice)

        elif choice == 'pick up':
            p.pick_up(location)

        elif choice == 'drop':
            p.drop(location)

        # [menu] options
        elif choice == 'inventory':
            p.open_inventory()

        return
