import random
from collections import defaultdict

iterations = 0


class Trie:
    """
    Implement a trie with insert, search, and startsWith methods.
    """
    def __init__(self):
        self.root = defaultdict()

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def has_prefix(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True


class Grid:

    def __init__(self, width, height):
        self.grid = [['_' for col in range(0, width)] for row in range(0, height)]
        self.free_cells = width * height
        self.width = width
        self.height = height
        # Start with a single set of all X's
        # self.all_sets = {'_': [set([(x, y) for x in range(0, width) for y in range (0, height)])]}

    def get(self, pos):
        return self.grid[pos[1]][pos[0]]

    def add_letter(self, pos, letter):
        self.grid[pos[1]][pos[0]] = letter
        self.free_cells -= 1

    def set_letter(self, pos, letter):
        self.grid[pos[1]][pos[0]] = letter

    def remove_letter(self, pos):
        self.grid[pos[1]][pos[0]] = "_"
        self.free_cells += 1

    def free(self, pos):
        if pos[0] < 0 or pos[0] >= self.width or pos[1] < 0 or pos[1] >= self.height:
            return False
        return self.grid[pos[1]][pos[0]] == "_"

    def complete(self):
        return self.free_cells == 0

    def neighbours(self, pos):
        x = pos[0]
        y = pos[1]
        return [n for n in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)] if 0 <= n[0] < self.width and 0 <= n[1] < self.height]


    # def get_neighbour_set(self, pos, letter_sets):
    #     neighbours = self.neighbours(pos)
    #     for letter_set in letter_sets:
    #         for neighbour in neighbours:
    #             if neighbour in letter_set:
    #                 return letter_set
    #     return None
    #
    # def build_letter_sets(self):
    #     all_sets = {}
    #     for y in range(0, self.height):
    #         for x in range(0, self.width):
    #             pos = (x, y)
    #             letter = self.grid[pos[1]][pos[0]]
    #             letter_sets = all_sets.get(letter)
    #             if letter_sets is None:
    #                 letter_sets = []
    #                 all_sets[letter] = letter_sets
    #
    #             neighbour_set = self.get_neighbour_set(pos, letter_sets)
    #             if neighbour_set is None:
    #                 neighbour_set = set()
    #                 letter_sets.append(neighbour_set)
    #             neighbour_set.add(pos)
    #     return all_sets
    #
    # def get_bad_cell(self):
    #     all_sets = self.build_letter_sets()
    #     for (letter, letter_sets) in all_sets.items():
    #         for neighbour_set in letter_sets:
    #             if len(neighbour_set) <= 3:
    #                 return neighbour_set.pop()
    #     return None

    # def find_letter_set(self, pos, letter):
    #     # find any existing set that contains a neighbour of the given position
    #     letter_sets = self.all_sets.get(letter, [])
    #     neighbours = self.neighbours(pos)
    #     for letter_set in letter_sets:
    #         for neighbour in neighbours:
    #             if neighbour in letter_set:
    #                 return letter_set
    #     # If none found then create a new one
    #     new_letter_set = set()
    #     letter_sets.append(new_letter_set)
    #     self.all_sets[letter] = letter_sets
    #     return new_letter_set

    # def add_letter_set(self, pos, letter):
    #     # Get the set we have recorded for this letter and position
    #     self.find_letter_set(pos, letter).add(pos)

    # def remove_letter_set(self, pos, letter):
    #     # Get the set we have recorded for this letter and position
    #     cur_set = self.find_letter_set(pos, letter)
    #     # Remove the set
    #     self.all_sets.get(letter).remove(cur_set)
    #     # Rebuild it position by position
    #     for cur_pos in cur_set:
    #         if cur_pos != pos:
    #             self.add_letter_set(cur_pos, letter)

    # def min_contiguous_area(self, blocking_pos, min_area):
    #     self.add_letter(blocking_pos, 'X')  # temporarily fill this position
    #
    #     # For each neighbour
    #     for pos in self.free_neighbours(blocking_pos):
    #         if not self.min_free_cells(pos):
    #             self.remove_letter(blocking_pos)
    #             return False
    #
    #     self.remove_letter(blocking_pos)  # un-fill this position
    #
    #     return True

    # def min_set_size(self, pos):

    # def free_neighbours(self, pos):
    #     return [n for n in [(pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] + 1)] if self.free(n)]


    def block(self, start_pos):
        # Returns all the cells that form part of the same block as this cell
        visited = set()

        queue = [start_pos]

        letter = self.get(start_pos)

        while queue:

            pos = queue.pop(0)
            if pos not in visited:

                visited.add(pos)

                # For each neighbour of the same letter, add it to the queue
                for neighbour in self.neighbours(pos):
                    if self.get(neighbour) == letter:
                        queue.append(neighbour)
        return visited


def print_grid(grid):
    for row in grid.grid:
        for letter in row:
            print(letter, "", end="")
        print()
    print()


# aspell dump master | grep -v \' | grep -v [A-Z] | grep -v -e '^[a-z]\{1,3\}$' > clean.txt
def get_words_by_length():
    # Sort words by length
    words = defaultdict(list)
    with open("clean.txt", "r") as f:
        for word in f.read().splitlines():
            words[len(word)].append(word)
    return words


def get_words_trie():
    # Build word Trie
    words_trie = Trie()
    with open("clean.txt", "r") as f:
        for word in f.read().splitlines():
            words_trie.insert(word)
    return words_trie


def next_letter_positions(grid, positions, include_taken=False):
    # Given a set of letter positions, returns
    # a set of new valid letter positions
    cur_positions = set(positions)
    next_positions = set()
    for pos in positions:
        for next_pos in grid.neighbours(pos):
            if next_pos not in cur_positions and (include_taken or grid.free(next_pos)):
                next_positions.add(next_pos)

    # Return the positions in order that they apply to make words
    return sorted(next_positions, key=lambda pos: pos[1] * 100 + pos[0])


def populate_cell(grid, word_num, word_positions, available_positions, max_letters):
    if max_letters == 0:
        return word_positions
    for pos in available_positions:
        word_positions.append(pos)
        grid.add_letter(pos, str(word_num))
        new_available_positions = next_letter_positions(grid, word_positions)
        random.shuffle(new_available_positions)
        return populate_cell(grid, word_num, word_positions, new_available_positions, max_letters - 1)
    return word_positions


def blocked_cells(grid, positions):
    # Returns true if any of the positions in positions blocks free cells in the grid
    for pos in positions:
        # Count the size of any free block surrounding this position
        for neighbour in grid.neighbours(pos):
            if grid.free(neighbour):
                block = grid.block(neighbour)
                if len(block) <= 3:
                    return True
    return False


def populate_word(grid, word_num):
    # populate the grid with words until it's full
    # if it's not full but no words could be populated then backtrack?
    global iterations
    if grid.complete():
        return True

    free_cells = []
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            pos = (x, y)
            if grid.free(pos):
                free_cells.append(pos)
    random.shuffle(free_cells)

    for free_cell in free_cells:

        available_word_positions = [free_cell]
        word_positions = []

        random_word_length = random.randint(4, 8)

        iterations = iterations + 1

        word_positions = populate_cell(grid, word_num, word_positions, available_word_positions, random_word_length)

        print_grid(grid)

        # if the position cannot fit at least 4 letters
        if len(word_positions) < 4:
            for pos in word_positions:
                grid.remove_letter(pos)
        elif blocked_cells(grid, word_positions):
            # or if it blocks a free cell then remove it from the grid and try the next free cell
            for pos in word_positions:
                grid.remove_letter(pos)
        # Otherwise, try the next word
        else:
            if populate_word(grid, chr(ord(word_num) + 1)):
                # And if successful, exit the loop
                return True
            else:
                # No possibilities found with the current word in the current position so remove it from the grid and try the next free cell
                for pos in word_positions:
                    grid.remove_letter(pos)

        # Otherwise, try the next free cell

    print_grid(grid)
    # All the free cells have been exhausted so return false
    return False


def populate_grid(grid):

    complete = populate_word(grid, 'A')

    print_grid(grid)

    print("Grid complete: ", complete)
    print("Iterations: ", iterations)



def get_word_positions(grid):

    # Default dictionary returns a list for new keys
    word_positions = defaultdict(list)

    # iterate through all the positions from top to bottom and left to right
    # for each position, add it to the list of position for that letter
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            pos = (x, y)
            letter = grid.get(pos)
            word_positions[letter].append(pos)

    return word_positions


def add_words(grid, words_by_length):

    word_positions = get_word_positions(grid)

    words = []

    for letter, word_positions in word_positions.items():
        word_length = len(word_positions)
        random_word = random.choice(words_by_length[word_length])
        words.append(random_word)
        print(random_word)
        for i in range(0, word_length):
            grid.set_letter(word_positions[i], random_word[i])

    return words


def word_at(grid, word_positions):
    return ''.join([grid.get(pos) for pos in word_positions])


def add_and_sort(word_positions, pos):
    new_word_positions = word_positions + [pos]
    # Return the positions in order that they apply to make words
    return sorted(new_word_positions, key=lambda pos: pos[1] * 100 + pos[0])


# Given a populated grid, a set of word positions, try to find the next available position
# that creates a new valid word
def populate_cell_2(word_trie, grid, word_positions):
    # prefix = word_at(grid, word_positions)
    valid_words = []
    available_positions = next_letter_positions(grid, word_positions, include_taken=True)
    for pos in available_positions:
        new_word_positions = add_and_sort(word_positions, pos)
        # grid.add_letter(pos, str(word_num))
        new_prefix = word_at(grid, new_word_positions)
        if word_trie.search(new_prefix):
            valid_words += [new_word_positions]
        if word_trie.has_prefix(new_prefix):
            valid_words += populate_cell_2(word_trie, grid, new_word_positions)
    return valid_words


def find_another_grid(grid, words_trie, exclude):

    new_grid = Grid(4, 6)

    word_positions = populate_cell_2(words_trie, grid, [(0, 0)])

    if len(word_positions) > 0:
        print(word_at(grid, word_positions))

    return new_grid

    # for y in range(0, grid.height):
    #     for x in range(0, grid.width):
    #         # For each position, see if we can find a word that matches
    #         pos = (x, y)
    #         letter = grid.get(pos)
    #         next_letter_positions(new_grid, word_positions)


def start():

    grid = Grid(4, 6)

    populate_grid(grid)

    words_by_length = get_words_by_length()

    words_trie = get_words_trie()

    while True:
        # Define an initial word grid
        words1 = add_words(grid, words_by_length)

        print_grid(grid)

        # See if it's possible to create any other word grid

        grid1 = find_another_grid(grid, words_trie, words1)

if __name__ == '__main__':
    start()