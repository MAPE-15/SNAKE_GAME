import tkinter
import random


class Snake:

    # velocity default --> 400 milisecond --> how fast is the snake
    def __init__(self, velocity=400):


        # ------------------------------------------------------- BACKGROUND --------------------------------------------------
        self.image = tkinter.Canvas(bg='green', width=600, height=600)
        self.image.pack()        

        x, y = 0, 0
        size = 30
    
        for i in range(int(self.image['height']) // size):
            for a in range(int(self.image['width']) // size):
            
                if i % 2 == 0:
                
                    if a % 2 == 0:
                        self.image.create_rectangle(x, y, x + size, y + size, outline='#81E171', fill='#81E171')
                    
                    else:
                        self.image.create_rectangle(x, y, x + size, y + size, outline='#169E00', fill='#169E00')

                else:
                    if a % 2 == 0:
                        self.image.create_rectangle(x, y, x + size, y + size, outline='#169E00', fill='#169E00')
                    
                    else:
                        self.image.create_rectangle(x, y, x + size, y + size, outline='#81E171', fill='#81E171')

                
                x += size

            x = 0
            y += size
        # ------------------------------------------------------- BACKGROUND --------------------------------------------------


        # how fast is the snake in miliseconds, time = 500 --> every half a second makes a move
        self.time = velocity

        # if snake touches another body part
        self.lost = False

        # all snake's body parts and their coords as a value
        self.parts = {}

        
        # all snake's body X coords as values
        self.Xs_snake = {}
        # all snake's body Y coords as values
        self.Ys_snake = {}

        # what body part moves on X axis (-30/30 --> Left/Right)
        self.Xs_move = {}
        # what body part moves on Y axis (-30/30 --> Up/Down)
        self.Ys_move = {}

        
        # number of turns made
        self.num_turns = 0
        # value --> which body part
        self.turns = {}

        # move made when made a turn on X axis
        self.x_moves_made = []
        # move made when made a turn on Y axis
        self.y_moves_made = []
        
        # number of body parts
        self.body_parts = 0
        # size of each body part (rectangle)
        self.snake_size = 30


        # random coords for thehead to spawn
        self.Xs_snake['x' + str(self.body_parts)] = random.randrange(self.snake_size * 3, int(self.image['width']) - self.snake_size, self.snake_size)
        self.Ys_snake['y' + str(self.body_parts)] = random.randrange(self.snake_size * 3, int(self.image['height']) - self.snake_size, self.snake_size)

        # spawn the head at these random coords
        self.image.create_rectangle(self.Xs_snake['x' + str(self.body_parts)], self.Ys_snake['y' + str(self.body_parts)],
                                    self.Xs_snake['x' + str(self.body_parts)] + self.snake_size, self.Ys_snake['y' + str(self.body_parts)] + self.snake_size,
                                    fill='red', outline='black', tag='part' + str(self.body_parts))
        
        # add to parts dict head's coords
        self.parts['part' + str(self.body_parts)] = self.image.coords('part' + str(self.body_parts))

        # also add to Xs and Ys move, the head first is moving right
        self.Xs_move['x_move' + str(self.body_parts)] = 30
        self.Ys_move['y_move' + str(self.body_parts)] = 0


        self.generate_apple()
        self.move_snake()

        self.image.bind_all('<Up>', self.change_direction)
        self.image.bind_all('<Down>', self.change_direction)
        self.image.bind_all('<Left>', self.change_direction)
        self.image.bind_all('<Right>', self.change_direction)



    def generate_body_part(self):
        # if this function is called, dd one to body_parts, that's also points
        # also create a new bodypart which will be spawn right from the last body part (at the tail) of thh snake, which this ceates a new tail
        
        self.body_parts += 1
        # print('POINTS:', self.body_parts)


        if self.body_parts % 5 == 0 and self.time > 50:
            self.time -= 25

        
        # coords of the new body part are the same as the last bodypart (tail) of the snake
        self.Xs_snake['x' + str(self.body_parts)] = self.Xs_snake['x' + str(self.body_parts - 1)] 
        self.Ys_snake['y' + str(self.body_parts)] = self.Ys_snake['y' + str(self.body_parts - 1)]

    
        if self.Xs_move['x_move' + str(self.body_parts - 1)] == 30 and self.Ys_move['y_move' + str(self.body_parts - 1)] == 0:
            self.Xs_snake['x' + str(self.body_parts)] -= self.snake_size

        elif self.Xs_move['x_move' + str(self.body_parts - 1)] == -30 and self.Ys_move['y_move' + str(self.body_parts - 1)] == 0:
            self.Xs_snake['x' + str(self.body_parts)] += self.snake_size

        elif self.Ys_move['y_move' + str(self.body_parts - 1)] == 30 and self.Xs_move['x_move' + str(self.body_parts - 1)] == 0:
            self.Ys_snake['y' + str(self.body_parts)] -= self.snake_size

        elif self.Ys_move['y_move' + str(self.body_parts - 1)] == -30 and self.Xs_move['x_move' + str(self.body_parts - 1)] == 0:
            self.Ys_snake['y' + str(self.body_parts)] += self.snake_size
            

        # spawn that new body part, every body part is colored as yellow, also add its unique part and Xs and Ys move
        self.image.create_rectangle(self.Xs_snake['x' + str(self.body_parts)], self.Ys_snake['y' + str(self.body_parts)],
                                    self.Xs_snake['x' + str(self.body_parts)] + self.snake_size, self.Ys_snake['y' + str(self.body_parts)] + self.snake_size,
                                    fill = '#fff421', outline = 'black', tag = 'part' + str(self.body_parts))

        
        self.parts['part' + str(self.body_parts)] = self.image.coords('part' + str(self.body_parts))

        self.Xs_move['x_move' + str(self.body_parts)] = self.Xs_move['x_move' + str(self.body_parts - 1)]
        self.Ys_move['y_move' + str(self.body_parts)] = self.Ys_move['y_move' + str(self.body_parts - 1)]
        
        

    def generate_apple(self):

        # -------------------------------------------------- SPAWN APPLE -------------------------------------------------------
        self.x_apple, self.y_apple = random.randrange(0, int(self.image['width']) - 30, 30), random.randrange(0, int(self.image['height']) - 30, 30)
        self.image.create_oval(self.x_apple + 5, self.y_apple + 5, self.x_apple + 25, self.y_apple + 25, outline='#9E0707', fill='#9E0707', tag='apple')
        # -------------------------------------------------- SPAWN APPLE -------------------------------------------------------



    def move_snake(self):

        # ------------------------------------------------ MAKING TURNS --------------------------------------
        if len(self.turns) >= 1:

            keys_x_move = list(self.Xs_move.keys())
            keys_y_move = list(self.Ys_move.keys())

            keys_turns_reversed = list(self.turns.keys())[::-1]
            
            for _ in self.turns:

                for turns in keys_turns_reversed:

                    self.Xs_move[keys_x_move[self.turns[turns]]] = self.x_moves_made[list(self.turns.keys()).index(turns)]
                    self.Ys_move[keys_y_move[self.turns[turns]]] = self.y_moves_made[list(self.turns.keys()).index(turns)]


            for turn in self.turns:
                self.turns[turn] += 1


            remove = [turns_key for turns_key, count_above in self.turns.items() if count_above > self.body_parts]
            
            for remove_pair in remove:
                
                del self.turns[remove_pair]
                self.x_moves_made.pop(0)
                self.y_moves_made.pop(0)
        # ------------------------------------------------ MAKING TURNS --------------------------------------



        # ------------------------------------------ GOES BEYOND PLAY BOARD -------------------------------------
        for x_snake, y_snake, x_move, y_move in zip(self.Xs_snake, self.Ys_snake, self.Xs_move, self.Ys_move):
        
            if self.Xs_snake[x_snake] == int(self.image['width']) and self.Xs_move[x_move] == 30:
                
                self.Xs_snake[x_snake] = -self.snake_size
                
                self.image.delete('part' + x_snake[1:])
                del self.parts['part' + x_snake[1:]]

                if x_snake[1:] == '0':
                    color = 'red'

                else:
                    color = '#fff421'
                    
                self.image.create_rectangle(self.Xs_snake[x_snake], self.Ys_snake[y_snake],
                                            self.Xs_snake[x_snake] + self.snake_size, self.Ys_snake[y_snake] + self.snake_size,
                                            fill=color, outline='black', tag='part' + x_snake[1:])



            elif self.Xs_snake[x_snake] == -self.snake_size and self.Xs_move[x_move] == -30:
                
                self.Xs_snake[x_snake] = int(self.image['width']) 
                
                self.image.delete('part' + x_snake[1:])
                del self.parts['part' + x_snake[1:]]

                if x_snake[1:] == '0':
                    color = 'red'

                else:
                    color = '#fff421'

                
                self.image.create_rectangle(self.Xs_snake[x_snake], self.Ys_snake[y_snake],
                                            self.Xs_snake[x_snake] + self.snake_size, self.Ys_snake[y_snake] + self.snake_size,
                                            fill=color, outline='black', tag='part' + x_snake[1:])



            elif self.Ys_snake[y_snake] == int(self.image['height']) and self.Ys_move[y_move] == 30:
                
                self.Ys_snake[y_snake] = -self.snake_size
                
                self.image.delete('part' + y_snake[1:])
                del self.parts['part' + y_snake[1:]]

                if y_snake[1:] == '0':
                    color = 'red'

                else:
                    color = '#fff421'
                
                self.image.create_rectangle(self.Xs_snake[x_snake], self.Ys_snake[y_snake],
                                            self.Xs_snake[x_snake] + self.snake_size, self.Ys_snake[y_snake] + self.snake_size,
                                            fill=color, outline='black', tag='part' + y_snake[1:])



            elif self.Ys_snake[y_snake] == -self.snake_size and self.Ys_move[y_move] == -30:
                
                self.Ys_snake[y_snake] = int(self.image['height'])
                
                self.image.delete('part' + y_snake[1:])
                del self.parts['part' + y_snake[1:]]

                if y_snake[1:] == '0':
                    color = 'red'

                else:
                    color = '#fff421'
                
                self.image.create_rectangle(self.Xs_snake[x_snake], self.Ys_snake[y_snake],
                                            self.Xs_snake[x_snake] + self.snake_size, self.Ys_snake[y_snake] + self.snake_size,
                                            fill=color, outline='black', tag='part' + y_snake[1:])
        # ------------------------------------------ GOES BEYOND PLAY BOARD -------------------------------------



        # ------------------------------------------------- HEAD TOUCHED BODY GAME OVER ----------------------------------------------

        Xs_snake_except_0 = list(self.Xs_snake.keys())[1:]
        Ys_snake_except_0 = list(self.Ys_snake.keys())[1:]
        
        for x_snake, y_snake in zip(Xs_snake_except_0, Ys_snake_except_0):

            if self.Xs_snake['x0'] == self.Xs_snake[x_snake] and self.Ys_snake['y0'] == self.Ys_snake[y_snake]:

                self.image.create_rectangle(0, 0, int(self.image['width']), int(self.image['height']), fill = 'black')
                self.image.create_text(int(self.image['width']) - (int(self.image['width']) / 2), int(self.image['height']) / 2.5, text='GAME OVER', font='Purisa 40', fill='white')
                self.image.create_text(int(self.image['width']) - (int(self.image['width']) / 2), int(self.image['height']) / 2, text='POINTS: ' + str(self.body_parts), font='Purisa 30', fill='white')
                self.lost = True
        # ------------------------------------------------- HEAD TOUCHED BODY GAME OVER----------------------------------------------



        # ------------------------------------------- MOVE SNAKE PARTS --------------------------------------
        for i in range(self.body_parts + 1):
            self.image.move('part' + str(i), self.Xs_move['x_move' + str(i)], self.Ys_move['y_move' + str(i)])
            
            self.parts['part' + str(i)] = self.image.coords('part' + str(i))
            self.Xs_snake['x' + str(i)] = self.image.coords('part' + str(i))[0]
            self.Ys_snake['y' + str(i)] = self.image.coords('part' + str(i))[1]
        # ------------------------------------------- MOVE SNAKE PARTS --------------------------------------



        # ------------------------------------------------------------- TAKE AN APPLE ---------------------------------------------------------------
        if (self.parts['part0'][0] >= self.x_apple and self.parts['part0'][2] <= self.x_apple + 30) and (self.parts['part0'][1] >= self.y_apple and self.parts['part0'][3] <= self.y_apple + 30):
            self.image.delete('apple')
            self.generate_apple()
            self.generate_body_part()
        # ------------------------------------------------------------- TAKE AN APPLE ---------------------------------------------------------------

    
        if not self.lost:
            self.image.after(self.time, self.move_snake)



    def change_direction(self, event):

        self.event = event
        self.direction = self.event.keysym
        

        if self.direction == 'Right':

            if len(self.Xs_snake) > 1:

                # can't do a 180 angle turn
                if self.Xs_snake['x0'] + 30 == self.Xs_snake['x1']:
                    pass

                else:
                    self.Xs_move['x_move0'] = 30
                    self.Ys_move['y_move0'] = 0

                    self.x_moves_made.append(30)
                    self.y_moves_made.append(0)

                    
                    self.num_turns += 1
                    self.turns['turn' + str(self.num_turns)] = 0


            # if just the head, just chane the head's move            
            else:
                self.Xs_move['x_move0'] = 30
                self.Ys_move['y_move0'] = 0
       


        elif self.direction == 'Left':

            if len(self.Xs_snake) > 1:

                if self.Xs_snake['x0'] - 30 == self.Xs_snake['x1']:
                    pass
            
                else:
                    self.Xs_move['x_move0'] = -30
                    self.Ys_move['y_move0'] = 0

                    self.x_moves_made.append(-30)
                    self.y_moves_made.append(0)
                    
                    self.num_turns += 1
                    self.turns['turn' + str(self.num_turns)] = 0

                    
            else:
                self.Xs_move['x_move0'] = -30
                self.Ys_move['y_move0'] = 0
                


        elif self.direction == 'Up':

            if len(self.Ys_snake) > 1:

                if self.Ys_snake['y0'] - 30 == self.Ys_snake['y1']:
                    pass

                else:
                    self.Xs_move['x_move0'] = 0
                    self.Ys_move['y_move0'] = -30

                    self.x_moves_made.append(0)
                    self.y_moves_made.append(-30)
                    
                    self.num_turns += 1
                    self.turns['turn' + str(self.num_turns)] = 0

                    
            else:
                self.Xs_move['x_move0'] = 0
                self.Ys_move['y_move0'] = -30



        elif self.direction == 'Down':

            if len(self.Ys_snake) > 1:

                if self.Ys_snake['y0'] + 30 == self.Ys_snake['y1']:
                    pass

                else:
                    self.Xs_move['x_move0'] = 0
                    self.Ys_move['y_move0'] = 30

                    self.x_moves_made.append(0)
                    self.y_moves_made.append(30)

                    self.num_turns += 1
                    self.turns['turn' + str(self.num_turns)] = 0


            else:
                self.Xs_move['x_move0'] = 0
                self.Ys_move['y_move0'] = 30

s1 = Snake(velocity=150)
