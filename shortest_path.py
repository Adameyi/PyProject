import queue
import time
import curses
from curses import wrapper

mazes = [
    [
        # Sample Maze 1 (9x9):
        ["#", "#", "#", "#", "#", "#", "O", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", " ", "#", "#", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", " ", " ", "#", " ", "#", "#", "#"],
        ["#", " ", "#", " ", "#", " ", " ", " ", "X"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
        ["#", " ", "#", " ", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
    ],
    [
        # Sample Maze 2 (6x7):
        ["#", "#", "#", "#", "#", "#"],
        ["O", " ", " ", " ", " ", "#"],
        ["#", "#", " ", "#", " ", "#"],
        ["#", " ", " ", "#", " ", "#"],
        ["#", " ", "#", "#", " ", "#"],
        ["#", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "X", "#", "#"],
    ],
    [
        # Sample Maze 3 (9x9):
        ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "X"],
        ["#", " ", "#", "#", "#", "#", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", " ", " ", "#", " ", "#", " ", "#"],
        ["#", "#", "#", " ", " ", " ", " ", " ", "#"],
        ["#", " ", " ", " ", "#", " ", "#", "#", "#"],
        ["O", " ", "#", " ", "#", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
    ],
    [
        # Sample Maze 4 (10x10):
        ["#", "#", "#", "#", "#", "#", "O", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", "#", "#", "#", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
        ["#", " ", " ", " ", "#", " ", "#", " ", " ", "#"],
        ["#", "#", "#", " ", " ", " ", " ", " ", "#", "#"],
        ["#", " ", " ", " ", "#", " ", "#", " ", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "X", "#", "#", "#", "#", "#", "#"]
    ],
    [
        # Sample Maze 5 (7x7):
        ["#", "#", "#", "#", "O", "#", "#"],
        [" ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "X"],
        [" ", " ", "#", " ", "#", "#", "#"],
        ["#", " ", "#", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#"],
    ],
    [
        # Sample Maze 6 (16x13):
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", "#", "#", "#", " ", "#", "#", " ", " ", " ", "#"],
        ["#", " ", "#", " ", " ", "#", " ", "#", "#", " ", "#", "#", "#"],
        ["#", " ", "#", " ", " ", "#", " ", "#", "#", " ", "#", " ", "#"],
        ["O", " ", "#", "#", "#", "#", " ", "#", "#", " ", "#", " ", "X"],
        ["#", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],
        ["#", " ", "#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],
        ["#", " ", " ", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]
]


# Output the mazes


def print_mazes(mazes, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(mazes):
        for j, value in enumerate(row):
            try:
                if (i, j) in path:
                    stdscr.addstr(i, j*2, "X", RED)
                else:
                    stdscr.addstr(i, j*2, value, BLUE)
            except curses.error:
                pass
            except TypeError:
                pass

# Find starting position


def find_start(mazes, start):
    for i, row in enumerate(mazes):
        for j, value in enumerate(row):
            if value == start:
                return i, j  # Return starting (X,Y) coordinates

    return None  # Starting (X,Y) coordinates not found


def find_path(mazes, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(mazes, start)

    q = queue.Queue()  # FIFO data structure
    # Insert Coords into the queue ((current position, [array path required to reach node])).
    q.put((start_pos, [start_pos], 0))

    visited = set()

    while not q.empty():
        # Grab first element (current node), Second element (path array), Third element (hops)
        current_pos, path, hops = q.get()

        stdscr.clear()  # Clear screen
        print_mazes(mazes, stdscr, path)  # Print mazes

        stdscr.refresh()  # Refresh to update (See what is written)

        # Segment coordinates into tuple.
        try:
            row, col = current_pos
        except TypeError:
            pass

        # Look at the coordinates of the current node/position, Is it an 'X'?
        try:
            if mazes[row][col] == end:
                return path, hops  # X found, return the path and hops.

            neighbours = find_neighbours(mazes, row, col)
            for neighbour in neighbours:
                if neighbour in visited:
                    continue

                rw, cl = neighbour

                # Check for a Wall (#)
                if mazes[rw][cl] == '#':
                    continue

                new_path = path + [neighbour]
                q.put((neighbour, new_path, hops + 1))
                visited.add(neighbour)
        except UnboundLocalError:
            pass
    return None, None  # X not found

# Adjacent Movement


def find_neighbours(mazes, row, col):
    neighbours = []

    if row > 0:  # Go UP (Row -1)
        neighbours.append((row - 1, col))
    if row + 1 < len(mazes):  # Go DOWN (Row + 1)
        neighbours.append((row + 1, col))

    if col > 0:  # Go LEFT (Col - 1)
        neighbours.append((row, col - 1))
    if row + 1 < len(mazes[0]):  # Go RIGHT (Col + 1)
        neighbours.append((row, col + 1))
    return neighbours

# stdscr - Standard output screen (Used to output mazes)


def main(stdscr):
    # ID(1), text color, background color.
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    for i, maze in enumerate(mazes):
        start_time = time.time()
        path, hops = find_path(maze, stdscr)
        end_time = time.time()
        print(
            f"Maze {i+1}: Found path in {hops} hops.\nTotal time taken: {end_time - start_time:.6f} seconds.")
        print(f"\nPath: {path}\n\n")

    exit()
    # stdscr.getch()  # Wait, get character, then exit.


wrapper(main)  # Initialize curses model, call main function
