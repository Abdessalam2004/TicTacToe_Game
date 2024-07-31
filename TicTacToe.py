import os

class Player :
    def __init__(self):
        
        self.name = self.choose_name()

        self.symbol = self.choose_symbol()

    def __repr__(self) :
        return f'player_{self.name}'

    def choose_name(self ,Second_time = False):
        name = input("Enter the name of the player : " if not Second_time else "Try again with another name (It should contain just alphabets): ")

        if not Player.check_name(name): 
            return self.choose_name(True)
        else:
            return name
        

    def choose_symbol(self,Second_time = False):
        symbol = input("choose a symbol : " if not Second_time else "Try another symbol (One letter):")
        if not Player.check_symbol(symbol): 
            return self.choose_symbol(True)
        else:
            return symbol
        
    @staticmethod
    def check_name(name):
        for i in name :
            if i in "0123456789/*^$)=_('\")&!?,;:." :
                return False
        return True

    @staticmethod
    def check_symbol(symbol):
        if len(symbol) > 1 : 
            return False
        for i in symbol :
            if i in "0123456789/*^$)=_('\")&!?,;:." :
                return False
        return True
    
    

class Menu : 
    def start_menu(self, second_time = False):
        print("1. Start\n2. Quit the game\nChoose (1 or 2) : " if not second_time else "Please, choose (1 or 2) :" ,end="")
        choice = input("")
        if choice == "1" or choice == "2":
            return choice
        else:
            return self.start_menu(True)

    
    def end_menu(self, second_time = False):
        print("1. Replay\n2. Quit the game\nChoose (1 or 2) : " if not second_time else "Please, choose (1 or 2) :" ,end="")
        choice = input("")
        if choice == "1" or choice == "2":
            return choice
        else:
            return self.end_menu(True)

    def restart_menu(self, second_time = False):
        print("1. Restart with the same players\n2. Change players name and symbol\nChoose (1 or 2) : " if not second_time else "Please, choose (1 or 2) :" ,end="")
        choice = input("")
        if choice == "1" or choice == "2":
            return choice
        else:
            return self.restart_menu(True)
    
    def play_menu(self):
        pass


class Board :
    def __init__(self): 
        self.board =[]
        self.reset_board()

    def display_bord(self):
        self.clear()
        self.clear()     
        arr = [" | ".join(line) for line in self.board]
        print("\n----------\n".join(arr))

    def update_board(self,index,symbol):
        index -= 1 
        self.board[index//3][index%3] = symbol
        self.display_bord()

    
    def reset_board(self):
        self.board = []
        for i in range(3):
            line = []
            for j in range(3):
                line.append(f"{3*i+j+1}")
            self.board.append(line)

    def is_valid(self, index:int ):
        try:
            index = int(index)
            if not index in range(1,10):
                return False
        except:
            return False
        
        return self.board[(index-1)//3][(index-1)%3] == str(index)
    
    def get_line(self,x):
        for y in range(3):
            yield self.board[x][y]

    def get_column(self,y):
        for x in range(3):
            yield self.board[x][y]

    def get_diagonal_1(self):
        yield self.board[0][0]
        yield self.board[1][1]
        yield self.board[2][2]

    def get_diagonal_2(self):
        yield self.board[0][2]
        yield self.board[1][1]
        yield self.board[2][0]
    
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

class Game:
    def __init__(self, name : str):
        self.name = name
        self.players = []
        self.menu = Menu()
        self.board = Board()
        self.turn = 0
        self.last = [0,None]
    
    def Start(self):
        print(f'{self.name} Game')
        if self.menu.start_menu() == "2":
            self.Quit_game()
        self.Create_players()
        self.Engine()

    def Engine(self):
        self.board.display_bord()
        while self.Check() :
            self.Play()
        self.End()

    def Restart(self):
        self.board.reset_board()
        self.turn = 0

        if self.menu.restart_menu() == "2":
            self.Create_players()

        self.Engine()

    def Create_players(self):
        self.players = []
        for i in range(1,3):
            print(f"\nPlayer {i}:")
            player = Player()
            self.players.append(player)
        if self.players[0].name == self.players[1].name or self.players[0].symbol == self.players[1].symbol:
            self.players = [] 
            print("Try again players name's or symbol are the same")
            self.Create_players()
        

    def Check(self):
        if self.turn < 5 :
            return True
        else:
            symbol = self.players[self.last[0]].symbol
            index = self.last[1]
            
            x , y = ((index - 1)// 3, (index - 1)% 3)
            # print("test", symbol)
            # print(f"test ({x},{y})")

            if self.sub_check(symbol, self.board.get_line(x)) :
                self.winner()
                return False
            elif self.sub_check(symbol, self.board.get_column(y)):
                self.winner()
                return False
            elif index in [1,9,5] and self.sub_check(symbol, self.board.get_diagonal_1()):
                    self.winner()
                    return False
            elif index in [3,7,5] and self.sub_check(symbol, self.board.get_diagonal_2()):
                    self.winner()
                    return False
            else :
                if self.turn == 9 :
                    self.noWinner()
                    return False
                else:
                    return True 

    # sub_checkingfuncions:
    @staticmethod
    def sub_check(symbol, sequence):
        for sym in sequence:
             if sym != symbol :
                 return False
        return True 

    def Play(self):
        
        print(f'======> {self.turn}')
        print(f"turn of {self.players[self.turn % 2].name}:")
        index = input("\nYour choice : ")

        if not self.board.is_valid(index):
            print("Please enter a valid choice")
            return self.Play()
        
        index = int(index)
        self.board.update_board(index,self.players[self.turn % 2].symbol)
        self.last[0] = self.turn % 2
        self.last[1] = index
        self.turn += 1
        

    def winner(self):
        print(f'\n==> Congratulation !! Your are win .')

    def noWinner(self):
        print(f"\n==> Em ! It seem that There is no winner !")

    def End(self):
        if self.menu.end_menu() == "1":
            self.Restart()
        else:
            self.Quit_game()
       
    def Quit_game(self):
        print("Thanks for playing my game !")
        exit()



game = Game("Tic_Tac_Toe")
game.Start()
#game.Create_players()
#print(game.players)
#game.Quit_game()


# Myboard = Board()
# Myboard.display_bord()

# #Myboard.update_board(1,"X")
# Myboard.update_board(1,"X")
# Myboard.reset_board()
# Myboard.display_bord()
#myboard.display_bord()