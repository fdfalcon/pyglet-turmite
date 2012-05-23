#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------
# Copyright (c) 2012, Francisco Falcon
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------



# Rules (http://en.wikipedia.org/wiki/Langton%27s_ant)
#
# At a white square, turn 90º right, flip the color of the square, move forward one unit
# At a black square, turn 90º left, flip the color of the square, move forward one unit
#

from pyglet import window, clock, font, gl, graphics


#Dimensions of the screen
window_width = 800
window_height = 600
cell_size = 10
columns = window_width / cell_size
rows = window_height / cell_size

print "Number of columns: %d" % columns
print "Number of rows: %d" % rows

class Ant:
    def __init__(self, posx, posy):
        #Initial position of the ant
        self.posx = posx
        self.posy = posy
        self.dir = 2                        #initial direction: right
        self.dirs = (
                    (-1, 0),                #left
                    (0, 1),                 #up
                    (1, 0),                 #right
                    (0, -1)                 #down
                    )


    def turn(self, direction):
        if direction == 'right':
            self.dir = (self.dir + 1) % 4
        elif direction == 'left':
            self.dir = (self.dir + 3) % 4

        self.posx = (self.posx + self.dirs[self.dir][0]) % columns
        self.posy = (self.posy + self.dirs[self.dir][1]) % rows



class Grid(window.Window):

    def __init__(self, width, height):
        #Let all of the standard stuff pass through
        window.Window.__init__(self, width=width, height=height)

        #Initial position of the ant: middle of the grid
        self.ant = Ant(columns/2, rows/2)

        #False = black cell. True = white cell.
        self.cells = [[False] * columns for i in range(rows)]
        self.steps = 0


    def rectangle(self, x1, y1, x2, y2):
        graphics.draw(4, gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))


    def draw_grid(self):
        gl.glColor4f(0.23, 0.23, 0.23, 1.0)
        #Horizontal lines
        for i in range(rows):
            graphics.draw(2, gl.GL_LINES, ('v2i', (0, i * cell_size, window_width, i * cell_size)))
        #Vertical lines
        for j in range(columns):
            graphics.draw(2, gl.GL_LINES, ('v2i', (j * cell_size, 0, j * cell_size, window_height)))


    def draw(self):
        self.clear()

        #White color for white cells
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)

        for f in range(len(self.cells)):
            current_row = self.cells[f]
            for c in range(len(current_row)):
                if current_row[c]:
                    self.rectangle(c * cell_size, f * cell_size, c * cell_size + cell_size, f * cell_size + cell_size)

        self.draw_grid()

        #ant's color
        gl.glColor4f(1.0, 0.23, 0.23, 1.0)

        self.rectangle(self.ant.posx * cell_size, self.ant.posy * cell_size,
        self.ant.posx * cell_size + cell_size, self.ant.posy * cell_size + cell_size)


    def main_loop(self):
        #Create a font for our Steps label
        ft = font.load('Arial', 16)
        #The pyglet.font.Text object to display the steps
        steps_text = font.Text(ft, y=10, color=(1.0, 0.0, 0.0, 1.0))

        clock.set_fps_limit(60)

        while not self.has_exit:
            self.dispatch_events()

            self.move()
            self.draw()

            #Tick the clock
            clock.tick()
            #Show the number of steps performed by the ant
            steps_text.text = "Steps: %d" % self.steps
            steps_text.draw()
            self.flip()


    def move(self):
        #Is the ant on a white cell? => Make the cell black, turn 90º right, move forward one cell
        if self.cells[self.ant.posy][self.ant.posx]:
            self.cells[self.ant.posy][self.ant.posx] = False
            self.ant.turn('right')
        #Is the ant on a black cell? => Make the cell white, turn 90º left, move forward one cell
        else:
            self.cells[self.ant.posy][self.ant.posx] = True
            self.ant.turn('left')

        self.steps += 1


if __name__ == "__main__":
    h = Grid(window_width, window_height)
    h.main_loop()
