"""
Stay Alive!

A simple python game using curses

By: Joe Pasquantonio
"""

import time
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


class Player:
    """
    @
    Protagonist. Loves living. Hates Dying.
    """
    def __init__(self, dimensions):
        """
        a player must be aware of his world, and his place in it
        """
        self.dimensions = dimensions
        self.y = randint(1, self.dimensions[0] - 2)
        self.x = randint(1, self.dimensions[1] - 2)

    def move(self, key):
        """
        or don't, whatever it takes to stay alive
        """
        if key == KEY_RIGHT and self.x < self.dimensions[1] - 2:
            self.x = self.x + 1
        if key == KEY_LEFT and self.x > 1:
            self.x = self.x - 1
        if key == KEY_UP and self.y > 1:
            self.y = self.y - 1
        if key == KEY_DOWN and self.y < self.dimensions[0] - 2:
            self.y = self.y + 1
        return self.y, self.x


class EnemyManager:
    """
    The corporate hive mind.
    """
    def __init__(self, window, dimensions):
        self.window = window
        self.dimensions = dimensions
        self.employees = []
        self.level = 0
        self.employee_limit = self.level + 2

    def increase_level(self, loops):
        if loops % 100000 == 0:
            self.level += 1
            self.employee_limit += 1

    def spawn(self, window, what):
        """
        Management hires another useless temp.
        """
        if what == 0:
            e = TopEnemy(self.dimensions, randint(500, 1000))
        if what == 1:
            e = LeftEnemy(self.dimensions, randint(250, 1000))
        if what == 2:
            e = RightEnemy(self.dimensions, randint(250, 1000))
        if what == 3:
            e = BottomEnemy(self.dimensions, randint(500, 1000))

        window.addch(e.y, e.x, e.character)
        self.employees.append(e)

    def move_employees(self, loops):
        for e in self.employees:
            if loops % e.interval == 0:
                if e.y < self.dimensions[0] - 2 and e.character == 'v':
                    self.window.addch(e.y, e.x, ord(' '))
                    e.update_position()
                    self.window.addch(e.y, e.x, e.character)
                elif e.x < self.dimensions[1] - 2 and e.character == '>':
                    self.window.addch(e.y, e.x, ord(' '))
                    e.update_position()
                    self.window.addch(e.y, e.x, e.character)
                elif e.y > 1 and e.character == '^':
                    self.window.addch(e.y, e.x, ord(' '))
                    e.update_position()
                    self.window.addch(e.y, e.x, e.character)
                elif e.x > 1 and e.character == '<':
                    self.window.addch(e.y, e.x, ord(' '))
                    e.update_position()
                    self.window.addch(e.y, e.x, e.character)
                else:
                    self.fire_employee(e)

    def fire_employee(self, e):
        """
        You're Fired!
        """
        self.window.addch(e.y, e.x, ord(' '))
        self.employees.remove(e)


class Enemy:
    """
    Takes many forms.

    Hates players, loves killing.
    """
    def __init__(self, dimensions, y = None, x = None):
        self.y = y
        self.x = x
        self.dimensions = dimensions


class TopEnemy(Enemy):
    """
    v

    An enemy that spawns from the top of the map and moves downward
    """
    def __init__(self, dimensions, m):
        Enemy.__init__(self, dimensions, 1, randint(1, dimensions[1] - 2))
        self.interval = m
        self.character = 'v'

    def update_position(self):
        self.y += 1


class LeftEnemy(Enemy):
    """
    >

    An enemy that spawns from the left and move to the right
    """
    def __init__(self, dimensions, m):
        Enemy.__init__(self, dimensions, randint(1, dimensions[0] - 2), 1)
        self.interval = m
        self.character = '>'

    def update_position(self):
        self.x += 1


class RightEnemy(Enemy):
    """
    <

    An enemy that spawns from the right and moves to the left
    """
    def __init__(self, dimensions, m):
        Enemy.__init__(self,
                       dimensions,
                       randint(1, dimensions[0] - 2),
                       dimensions[1] - 2)
        self.interval = m
        self.character = '<'

    def update_position(self):
        self.x -= 1


class BottomEnemy(Enemy):
    """
    ^

    An enemy that spawns at the bottom of that map and moves upward
    """
    def __init__(self, dimensions, m):
        Enemy.__init__(self,
                       dimensions,
                       dimensions[0] - 2,
                       randint(1, dimensions[1] - 2))
        self.interval = m
        self.character = '^'

    def update_position(self):
        self.y -= 1


def format_time(start):
    return int(time.time() - start)

def game(r, c, y, x):
    rows = r
    cols = c
    begin_y = y
    begin_x = x

    # Create game window
    curses.initscr()
    window = curses.newwin(rows, cols, y, x)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    window.nodelay(1)
    window.addstr(0, 21, " STAY ALIVE! ")
    dimensions = window.getmaxyx()

    # initialize player
    player = Player(dimensions)

    # initialize Enemy Management, #1 corporation in killing players
    mgmt = EnemyManager(window, dimensions)

    # draw player
    window.addch(player.y, player.x, ord('@'))

    # Game variables
    gameover = False
    key = None
    start_time = time.time()
    loop_count = -1

    # game loop
    while key != ord('q'):
        # loop tracking
        loop_count += 1
        window.addstr(0, 40, " Loops: {} ".format(loop_count))

        # Time keeping
        seconds = format_time(start_time)
        window.addstr(0, 2, " Time: {} ".format(seconds))

        # Player movement
        key = window.getch()
        window.addch(player.y, player.x, ord(' '))
        player.move(key)
        window.addch(player.y, player.x, ord('@'))

        ### Enemy actions ###
        # Show information
        window.addstr(19, 2, " Enemies: {} ".format(len(mgmt.employees)))
        window.addstr(19, 20, " Limit: {} ".format(mgmt.employee_limit))
        window.addstr(19, 40, " Level: {} ".format(mgmt.level))

        # Spawn enemies
        if len(mgmt.employees) < mgmt.employee_limit and loop_count > 5000:
            if mgmt.level <= 2:
                mgmt.spawn(window, 0)
            elif mgmt.level <= 4 and mgmt.level > 2:
                if randint(0, 10) < 5:
                    mgmt.spawn(window, 0)
                else:
                    mgmt.spawn(window, 1)
            elif mgmt.level <= 8 and mgmt.level > 4:
                rn = randint(0, 30)
                if rn < 10:
                    mgmt.spawn(window, 0)
                elif rn >= 10 and rn < 20:
                    mgmt.spawn(window, 1)
                else:
                    mgmt.spawn(window, 2)
            else:
                rn = randint(0, 40)
                if rn < 10:
                    mgmt.spawn(window, 0)
                elif rn >= 10 and rn < 20:
                    mgmt.spawn(window, 1)
                elif rn >= 20 and rn < 30:
                    mgmt.spawn(window, 2)
                else:
                    mgmt.spawn(window, 3)

        # move enemies
        mgmt.move_employees(loop_count)

        # check player collisions
        for e in mgmt.employees:
            if e.y == player.y and e.x == player.x:
                gameover = True

        # increase level
        mgmt.increase_level(loop_count)

        # pause game, NOTE: Fucks up time keeping but fixable
        if key == ord(' '):
            key = -1
            while key != ord(' '):
                key = window.getch()
            continue

        if gameover:
            key = ord('q')

    curses.beep()
    curses.endwin()
    score = "Level: {}, Time: {}, Loop Count: {}\n".format(mgmt.level,
                                                           seconds,
                                                           loop_count)
    print "Gameover."
    print "Stats: " + score

    # write scores to a file
    with open('scores.txt', 'a') as filewriter:
        filewriter.write(score)

if __name__ == "__main__":
    window = [20, 60, 0, 0]
    game(window[0], window[1], window[2], window[3])
