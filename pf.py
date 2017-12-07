##################################
# Created by: PH                 #
# Paint Fuck Interpreter v.0.0.0 #
# Date: 09.09.2017               #
##################################

import sys
import time

def print_there(pos_x, pos_y, text):
    '''Update screen at pos_x, pos_y'''
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (pos_x, pos_y, text))
    sys.stdout.flush()

GLOBAL_X = 10
GLOBAL_Y = 10

FULL_BLOCK = u"\u2588"
LIGHT_SHADE = u"\u2591"
DARK_SHADE = u"\u2593"
MEDIUM_SHADE = u"\u2592"

class CELL(object): 
    ''' define visualy cells '''
    bkg = MEDIUM_SHADE
    one = LIGHT_SHADE
    zero = FULL_BLOCK

STATE = [CELL.zero, CELL.one, CELL.bkg]


class PaintFuck(object):
    ''' main class for PAINT_FUCK'''
    filters = 'nesw*[]'
    def __init__(self, code, iterations, width, height, animate=False):
        self.w = width
        self.h = height
        self.animate = animate
        self.current_x = 0
        self.current_y = 0
        self.iterations = iterations
        self.code = code
        self.pos_in_code = 0
        self.parentesis_dict = {}

        for letter in self.code:
            if letter not in self.filters:
                self.code = self.code.replace(letter, "")

        self.create_parentesis_dict()

        self.fuck_field = [[0 for x in range(width)]for y in range(height)]

    def create_parentesis_dict(self):
        ''' match parentesis, later used for paint fuck loops '''
        open_positions = []
        for ind, elm in enumerate(self.code):
            if elm == '[':
                open_positions.append(ind)
            elif elm == ']':
                self.parentesis_dict[open_positions[-1]] = ind
                self.parentesis_dict[ind] = open_positions.pop(-1)
        print self.parentesis_dict

    def print_field(self):
        ''' Display result '''
        for row in range(len(self.fuck_field)):
            print_there(GLOBAL_X + row -1, GLOBAL_Y, STATE[2]       \
            +"".join([STATE[xx] for xx in self.fuck_field[row]]) \
            +STATE[2])

    def step(self):
        ''' possible actions '''
        if self.code[self.pos_in_code] == '*':
            self.fuck_field[self.current_y][self.current_x] = 1 if  \
                 self.fuck_field[self.current_y][self.current_x] == 0 else 0
            self.iterations = self.iterations-1

        elif self.code[self.pos_in_code] == 'e':
            self.current_x = self.current_x+1
            if self.current_x > self.w-1:
                self.current_x = 0
            self.iterations = self.iterations-1

        elif self.code[self.pos_in_code] == 'w':
            self.current_x = self.current_x-1
            if self.current_x < 0:
                self.current_x = self.w-1
            self.iterations = self.iterations-1

        elif self.code[self.pos_in_code] == 'n':
            self.current_y = self.current_y-1
            if self.current_y < 0:
                self.current_y = self.h-1
            self.iterations = self.iterations-1

        elif self.code[self.pos_in_code] == 's':
            self.current_y = self.current_y+1
            if self.current_y > self.h-1:
                self.current_y = 0
            self.iterations = self.iterations-1

        elif self.code[self.pos_in_code] == '[':
            if self.fuck_field[self.current_y][self.current_x] == 1:
                self.iterations = self.iterations-1
            else:
                self.pos_in_code = self.parentesis_dict[self.pos_in_code]
                self.iterations = self.iterations-1

        elif self.code[self.pos_in_code] == ']':
            if self.fuck_field[self.current_y][self.current_x] == 0:
                self.iterations = self.iterations-1
            else:
                self.pos_in_code = self.parentesis_dict[self.pos_in_code]
                self.iterations = self.iterations-1

    def solve(self):
        ''' main loop for executing paint fuck '''
        while self.iterations > 0 and self.pos_in_code < len(self.code):
            self.step()
            self.pos_in_code = self.pos_in_code + 1
            print_there(3, 3, self.code[self.pos_in_code])
            time.sleep(0.001)
            self.print_field()

# Binary counter
BC = "*[ss*s[*]n[e*s[*]n]*e[*nn[*n*ss*n]sse]ne[*e]*w*[*w*]*]"
XXX = "*es*e*s*w*n[[[e]w[s]e[ee]*e*[ww]es[ss]*n[*]*n[nn]w[n]" + \
      "s[w]e*e]sw[n*sw]e[e]w[s]ee[sw[e*ws]en[n]es]w[w]e]"


#PF_1 = PaintFuck(code=XXX, iterations=50000, width=50, height=50)
PF_1 = PaintFuck(code=BC, iterations=50000, width=50, height=50)
PF_1.print_field()
PF_1.solve()
