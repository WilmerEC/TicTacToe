import os
import sys
import shutil
from os import system, name
from time import sleep

# Helper functions
def clearConsole():
    if name == "nt":
        _ = system('cls')
    else:
        _ = system("clear")

def printInstructions():
        print("\n\n")

# I'll add validations once I have the whole thing up and running with correct inputs. 
def evaluate_num_to_shape(value):
    if value==1:
        return "X"
    elif value==2:
        return "O"
    elif value==0:
        return " "

# I'll add validations once I have the whole thing up and running with correct inputs. 
def evaluate_shape_to_num( value):
    if value=="X":
        return 1
    elif value=="O":
        return 2
    elif value==" " or value=="":
        return 0


# This is some weird stuff ngl. i dont like this bruh
class game:
    def __init__(self):
        self._p1_shape = None
        self._p2_shape = None
        self._current_p = None # We'll set this by default to p1_shape later
        self._game_map = [[None for _ in range(3)] for _ in range(3)]
        self._translation = {
                             "TL": (0,0), "TM": (1,0), "TR": (2,0), 
                             "CL": (0,1), "CM": (1,1), "CR": (2,1), 
                             "BL": (0,2), "BM": (1,2), "BR": (2,2)
                            }
        self._winner = None
        self._loop = False
        self._commands = [ "TL", "TM", "TR", "CL", "CM", "CR", "BL", "BM", "BR", "$help", "$quit"]
    
    # This is some pretty weird stuff to initialize class properties
    @property
    def p1_shape(self):
        return self._p1_shape
    
    @property
    def p2_shape(self):
        return self._p2_shape
    
    @property
    def game_map(self):
        return self._game_map
    
    @property
    def current_p(self):
        return self._current_p

    @property
    def winner(self):
        return self._winner
    
    @property
    def loop(self):
        return self.loop

    # There's no modifying this property so there's no need for a setter.
    @property
    def commands(self):
        return self._commands
    # There's no modifying these values as of the current development plans for this program, -
    # - so I won't be adding a setter for this property
    @property
    def translation(self):
        return self._translation

    @p1_shape.setter
    def p1_shape(self, value):
        self._p1_shape = value

    @p2_shape.setter
    def p2_shape(self, i, j, value):
        self._game_map[i][j] = value
    
    @current_p.setter
    def current_p(self, value):
        self._current_p = value
    
    @winner.setter
    def winner(self, value):
        self._winner = value

    @loop.setter
    def loop(self, value):
        self._loop = value
    # This is where the abomination ends

    def pickShape(self):
        # Validating P1
        p1_shape = input("Pick shape for P1: ")
        while len(p1_shape) > 1 or ((p1_shape != "X" and p1_shape != "x") and (p1_shape != "O" and p1_shape != "o")):
            p1_shape = input("Wrong input, please choose either X or O: ")
        
        # Validating P2
        p2_shape = input("Pick shape for P2: ")
        while len(p2_shape) > 1 or ((p2_shape != "X" and p2_shape != "x") and (p2_shape != "O" and p2_shape != "o")) or (p1_shape == p2_shape):
            p2_shape = input("Wrong input, please choose either X or O: ")
        
        # Setting them once validated
        self._p1_shape = p1_shape
        self._p2_shape = p2_shape
        self.current_p = self.p1_shape # This can safely be done since the game loop will start after this method is completed

    def printMap(self):
        clearConsole()
        print("   +   +   ")
        print(f" {evaluate_num_to_shape(self._game_map[0][0])} + {evaluate_num_to_shape(self._game_map[1][0])} + {evaluate_num_to_shape(self._game_map[2][0])} ")
        print("   +   +   ")
        print(" ++++++++++")
        print("   +   +   ")
        print(f" {evaluate_num_to_shape(self._game_map[0][1])} + {evaluate_num_to_shape(self._game_map[1][1])} + {evaluate_num_to_shape(self._game_map[2][1])} ")
        print("   +   +   ")
        print(" ++++++++++")
        print("   +   +   ")
        print(f" {evaluate_num_to_shape(self._game_map[0][2])} + {evaluate_num_to_shape(self._game_map[1][2])} + {evaluate_num_to_shape(self._game_map[2][2])} ")
        print("   +   +   ")
        #print("   +   +   ")

        
    def printHelp(self):
        print("\n\nInput follows this format: T - Top, M - Mid, B - Bottom, L - Left, C - Center, R - Right\nE.g.: TR: Top Right\n\n")
        input()
        clearConsole() # Might turn this on again later, we'll see
    
    def start_game(self):
        clearConsole()
        width, height = shutil.get_terminal_size()
        introduction_text = "Welcome to TicTacToe!"
        sys.stdout.write(f"\033[{0};{width//2}H{introduction_text}!\n\n") # this is really not necessary, but why not :P
        self.pickShape()
        self._loop = True
        #print("\t\t")
    
    def game_loop(self):
        
        self.printMap()
        while self._loop:
            
            user_input = self.appropiate_input() # need to add validation to this
            if user_input == "$quit":
                option = input("\nDo you want to clear console when quitting? [Y]:")
                print("\n\nQuitting game...\n\n")
                sleep(2) # let's pretend it's actually releasing memory and doing other stuff in the background lolololol
                if option=="Y":
                    clearConsole()
                break
            elif user_input=="$help":
                self.printHelp()
            elif user_input=="$printmap":
                self.print_map()
                input()
            else:
                self.update_map_data(user_input, self._current_p)
                if self._current_p == "X":
                    self._current_p = "O"
                elif self._current_p == "O":
                    self._current_p = "X"

            self.printMap()

            if self.check_board():
                if self._winner:
                    again = input(f"\n\nWinner is: {self._winner}! Restart game? [Y/N]: ")
                    if again=="Y":
                        self.restart_game()
                        user_input = None
                    else:
                        print("\n\nThanks for playing! Now quitting...")
                        sleep(2)
                        clearConsole()
                elif not self.winner:
                    again = input(f"\n\nIt's a TIE! Restart game? [Y/N]: ")
                    if again=="Y":
                        self.restart_game()
                        user_input = None
                    else:
                        print("\n\nThanks for playing! Now quitting...")
                        sleep(2)
                        clearConsole()

    
    ''' 
    Disclaimer: This approach probably isn't ideal for bigger scale projects as it's complexity is:

    - O(N): best case scenario  
    and
    - O(N*M): worst case scenario
    
    Since the list for this project is rather small and the project really is only a console project,
    it'll do just fine, but I really want to put emphasis on the complexity of using it in a bigger scaled project.
    ''' # To-Do: Validate all the inputs to make sure whatever the player is passing in is correct. Update: Done   
    def appropiate_input(self):
        user_input = input(f"\n\n>>>>>> Currently playing [{self.current_p}]:")
        while True:
            for i in range(len(self._commands)):
                if user_input==self._commands[i]:
                    return user_input
            user_input = input("Wrong input! Try again with a correct one (type $help for command format):")
           
    def check_board(self):
        diagonal_win = ( 
                            (self._game_map[0][0]!=0 and (self._game_map[0][0]==self._game_map[1][1] and self._game_map[0][0]==self._game_map[2][2])) or 
                            (self._game_map[2][0]!=0 and (self._game_map[2][0]==self._game_map[1][1] and self._game_map[2][0]==self._game_map[0][2])) 
                       ) 
        
        vertical_win = (
                            (self._game_map[0][0]!=0 and (self._game_map[0][0]==self._game_map[0][1] and self._game_map[0][0]==self._game_map[0][2])) or
                            (self._game_map[1][0]!=0 and (self._game_map[1][0]==self._game_map[1][1] and self._game_map[1][0]==self._game_map[1][2])) or
                            (self._game_map[2][0]!=0 and (self._game_map[2][0]==self._game_map[2][1] and self._game_map[2][0]==self._game_map[2][2]))
                       )
        
        horizontal_win = (
                            (self._game_map[0][0]!=0 and (self._game_map[0][0]==self._game_map[1][0] and self._game_map[0][0]==self._game_map[2][0])) or
                            (self._game_map[0][1]!=0 and (self._game_map[0][1]==self._game_map[1][1] and self._game_map[0][1]==self._game_map[2][1])) or
                            (self._game_map[0][2]!=0 and (self._game_map[0][2]==self._game_map[1][2] and self._game_map[0][2]==self._game_map[2][2]))
                         )

        if diagonal_win:
            if self._game_map[0][0] == self._game_map[2][2]:
                self.winner = evaluate_num_to_shape(self._game_map[0][0])
            else:
                self.winner = evaluate_num_to_shape(self._game_map[0][2])    
            self._loop = False
            return True
        elif vertical_win:
            if self._game_map[0][0]==self._game_map[0][2]:
                self.winner = evaluate_num_to_shape(self._game_map[0][0]) 
            elif self._game_map[1][0]==self._game_map[1][2]:
                self.winner = evaluate_num_to_shape(self._game_map[1][0])
            else:
                self.winner = evaluate_num_to_shape(self._game_map[2][0])
            self._loop = False
            return True
        elif horizontal_win:
            if self._game_map[0][0]==self._game_map[2][0]:
                self.winner = evaluate_num_to_shape(self._game_map[0][0]) 
            elif self._game_map[0][1]==self._game_map[2][1]:
                self.winner = evaluate_num_to_shape(self._game_map[1][0])
            else:
                self.winner = evaluate_num_to_shape(self._game_map[2][2])
            self._loop = False
            return True
        #tie = True
        for i in range(3):
            for j in range(3):
                if self._game_map[i][j] == 0:
                    return False
        return True
            
    def restart_game(self):
        self._p1_shape = None
        self._p2_shape = None
        self._current_p = None
        self._winner = None
        self._loop = True
        self.restart_map()
        clearConsole()
        self.pickShape()

    def update_map_data(self, command, value):
        x, y = self._translation[command]
        self._game_map[x][y] = evaluate_shape_to_num(value)
        # print(f"Value Updated: game_map[{x}][{y}]: {self._game_map[x][y]}") # Only uncomment this once the problem with the 2D list has been fixed

    # This is not exactly required by the program, but it helps me debug
    def print_map_value(self, command):
        x, y = self._translation[command]
        print(f"\ngame_map[{x}][{y}]: {self._game_map[x][y]}")
    
    # I didn't plan this one, but its useful ngl
    def restart_map(self):
        for i in range(3):
            for j in range(3):
                self._game_map[i][j] = 0
    
    # Tbh, this is only while im learning python cuz idk what is going on with the list [ map in c++ (': ]
    def print_map(self): # Update: I ended up liking it a lot so I will keep it permanently.
        for i in range(3):
            print(f"game_map[{0}][{i}]: {self._game_map[0][i]} \t game_map[{1}][{i}]: {self._game_map[1][i]} \t game_map[{2}][{i}]: {self._game_map[2][i]} ")

# int main() // I'm coming from C++ so I'm going to have to get used to a lot of this.
if __name__ == "__main__":
    tic = game()
    tic.restart_map() 
    tic.start_game()
    tic.game_loop()



# ========== It is safe to assume everything below works ========== #

# tic.update_map_data("TL", 2) #
# tic.update_map_data("BL", 1) #
# tic.update_map_data("BR", 3) #
# tic.print_map_value("BM") #
# tic.print_map() #
# print("\n\nX:", i, "Y:", j, "\n\n") #
# tic.game_map[0][0] = 1 # 
# tic.game_map[0][1] = 0 #
# print("game_map[0][0]: ", tic.game_map[0][0], "\ngame_map[0][1]: ", tic.game_map[0][1]) #