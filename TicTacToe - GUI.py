import customtkinter
from PIL import Image
import time
from random import randint

class Player :
    def __init__(self):
        self.name = None
        self.symbol = None
        self.score = 0

    def __repr__(self) :
        return f'player_{self.name}'
    
    def reset(self):
        print(f"{self.name} is reseted")
        self.name = None
        self.symbol = None
        self.score = 0
        
    @staticmethod
    def check_name(name):
        if len(name) > 8 or len(name) == 0:
            return False  
        for i in name :
            if i in "0123456789/*^$)=_('\")&!?,;:." :
                return False
        return True    

class Board:
    def __init__( self, first_player_symbol,check_function, continue_function):
        self.board = [[f"{3*i+j}" for j in range(3)] for i in range(3)]
        self.boxes = []
        self.current_symbol = first_player_symbol
        self.check_function = check_function
        self.continue_function = continue_function

    def display(self):
        print(self.board)
    
    def update_board( self, index, symbol):
        self.board[index//3][index%3] = symbol

    def create_graphic_board( self, root):
        board_frame = customtkinter.CTkFrame( root, width=420, height = 420, fg_color="#292929", corner_radius=0)
        board_frame.place( x=290, y=120)
        for i in range(9):
            box = customtkinter.CTkButton( board_frame, text=None, width= 136, height= 136, corner_radius=0, fg_color="#292929",
                                          hover_color="#363636", command=self.functions_generator(i))
            self.boxes.append(box)
            box.grid( row = i//3, column= i%3, padx = 1.5, pady = 1.5)
        component.image( board_frame, "frames/v_rectangle2.png", 140, 210,size=(5,420))
        component.image( board_frame, "frames/v_rectangle2.png", 279, 210,size=(5,420))
        component.image( board_frame, "frames/h_rectangle2.png", 210, 140,size=(420,5))
        component.image( board_frame, "frames/h_rectangle2.png", 210, 279,size=(420,5))

    def box_function( self, index):
        if self.current_symbol == "x":
            img = customtkinter.CTkImage(dark_image= Image.open("frames/X_play_icon.png"), size =(120,120))
        else:
            img = customtkinter.CTkImage(dark_image= Image.open("frames/O_play_icon.png"), size =(120,120))
        self.boxes[index].configure(state="disabled", image = img)
        self.update_board( index, self.current_symbol)
        self.check_function( index, self.current_symbol)
        self.continue_function()

    def functions_generator( self, index):
        def function():
            self.box_function(index)
        return function
    
    def disable_boxes( self):
        for box in self.boxes:
            box.configure( state = "disabled")

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

class Player_bar:
    def __init__( self):
        self.round_label = None
        self.result_label = None

    def set( self, round, result):
        self.round_label.configure(text=f"ROUND {round}")
        self.result_label.configure(text=f"{result[0]}   |   {result[1]}")
    
    def show_graphic( self, root, x_player_name, o_player_name):
        main_frame = customtkinter.CTkFrame( root, width= 1000, height = 100, fg_color="#292929")
        main_frame.place(x= 0, y = 0)

        width = len(x_player_name)*5
        player_1 = customtkinter.CTkFrame( main_frame, width = 300, height= 80, fg_color="transparent")
        player_1.place(x= 40, y = 10)
        component.image(player_1, "frames/x_avatar.png", x=40, y=40, size=(60,60))
        component.text( player_1, x_player_name, x=(90+width)/300, y=150/300)

        game_info = customtkinter.CTkFrame( main_frame, width = 200, height= 80, fg_color="transparent")
        game_info.place( x=400, y = 0)

        self.round_label = customtkinter.CTkLabel( game_info, text=f"ROUND 0", width= 200, height= 30,
                                                   font=fonts.round_font(), text_color="#008080", fg_color="White") 
        self.round_label.place(x = 0, y=10)

        self.result_label = customtkinter.CTkLabel( game_info, text="0   |   0", width= 200, height= 30, font=fonts.result_font(),
                                                    text_color="White", fg_color="#008080") 
        self.result_label.place(x = 0, y=40)

        width = len(o_player_name)*5
        player_2 = customtkinter.CTkFrame( main_frame, width = 300, height= 80, fg_color="transparent")
        player_2.place(x= 660, y = 10)
        component.image(player_2, "frames/o_avatar.png", x=260, y=40, size=(60,60))
        component.text( player_2, o_player_name, x=(205-width)/300, y=150/300)


class fonts:
    @staticmethod
    def menu_font():
        return ("Roboto",22,"bold")
    
    @staticmethod
    def entry_font():
        return ("Roboto",20,"bold")
    
    @staticmethod
    def general_font():
        return ("Roboto",20,"bold")

    @staticmethod
    def message_font():
        return ("Roboto",15,"bold")
    
    @staticmethod
    def round_font():
        return ("Roboto",25,"bold")

    @staticmethod
    def result_font():
        return ("Roboto",20,"bold")
    
    @staticmethod
    def message_font2():
        return ("Roboto",22,"bold")

class component:
    @staticmethod
    def image( root, path, x, y, anchor="center", size = (100,100)):
        img = customtkinter.CTkImage(dark_image = Image.open(path),size=size)
        label = customtkinter.CTkLabel(root, text=None, image=img, width=size[0], height=size[1])
        if x < 1 or y < 1:
            label.place(relx=x,rely=y,anchor=anchor)
        else:
            label.place(x = x, y = y,anchor=anchor)

    @staticmethod
    def text( root, txt, x, y, anchor="center", bg_color="#292929", color="White"):
        label = customtkinter.CTkLabel(root, text=txt, text_color=color,bg_color=bg_color, font=fonts.general_font())
        label.place(relx=x,rely=y,anchor=anchor)

    @staticmethod
    def menu( root, text1, text2, command1, command2):
        button_1 = customtkinter.CTkButton(root, text=text1, command=command1, hover_color="#00ADAD", bg_color="#292929", text_color="#1E1E1E",
                                           fg_color="#008080",width=250, height=57, corner_radius= 11, font=fonts.menu_font())
        button_2 = customtkinter.CTkButton(root, text=text2, command=command2, hover_color="#00ADAD", bg_color="#292929", text_color="#1E1E1E",
                                           fg_color="#008080",width=250, height=57, corner_radius= 11, font=fonts.menu_font())
        button_1.place( x=374, y=185)
        button_2.place( x=374, y=271)
    
    @staticmethod
    def entry( root, text):
        entry_ = customtkinter.CTkEntry(root, placeholder_text = text, placeholder_text_color="#AEAEAE",fg_color="#D9D9D9", text_color="#292929",
                                        border_color="#D9D9D9", font=fonts.entry_font(), width=400, height=48)
        entry_.place( relx=0.3, rely=0.2) #(x=300/y=150)
        return entry_
    
    @staticmethod
    def XO_choice( root, command1, command2, prec_choice = "ox"):
        O_img = customtkinter.CTkImage(dark_image = Image.open("frames/O_icon.png"),size=(100,100))
        X_img = customtkinter.CTkImage(dark_image = Image.open("frames/X_icon.png"),size=(100,100))

        button_1 = customtkinter.CTkButton(root, text=None, command=command1, image=X_img, hover_color="#00ADAD", bg_color="#292929",
                                           fg_color="#D9D9D9",width=160, height=160, corner_radius= 11, font=fonts.menu_font())
        button_2 = customtkinter.CTkButton(root, text=None, command=command2, image=O_img,hover_color="#00ADAD", bg_color="#292929",
                                           fg_color="#D9D9D9",width=160, height=160, corner_radius= 11, font=fonts.menu_font())
        if prec_choice == 'x':
            button_1.configure(state = "disabled", fg_color="#818080")

        if prec_choice == 'o':
            button_2.configure(state = "disabled", fg_color="#818080")

        button_1.place( relx=0.32, rely=0.4)
        button_2.place( relx=0.52, rely=0.4)
        
        return [button_1,button_2]

    @staticmethod
    def next_button( root, command):
        img = customtkinter.CTkImage(dark_image = Image.open("frames/next.png"),size=(25,25))
        button_ = customtkinter.CTkButton(root, text="Next", image=img, compound="right",command=command, hover_color="#00ADAD", bg_color="#292929", text_color="#1E1E1E",
                                           fg_color="#008080",width=50, height=50, corner_radius= 2000, font=fonts.menu_font())
        button_.place( relx = 0.6, rely = 0.75)

    @staticmethod
    def popup_message( root, text):
        top_level = customtkinter.CTkToplevel( root, fg_color="#008080")
        top_level.geometry("400x150+400+200")
        top_level.resizable(False,False)
        top_level.grab_set()
        top_level.focus()
        top_level.overrideredirect(True)

        frame = customtkinter.CTkFrame( top_level, width=400, height=150, border_color ='#008080', border_width=2, corner_radius=0)
        frame.pack()

        label = customtkinter.CTkLabel( frame, text=text, font=fonts.message_font(), width=350, wraplength=330, anchor="center")
        label.place( relx = 0.05, rely = 0.2)
       
        ok_button = customtkinter.CTkButton( frame, text="Ok", command=top_level.destroy, hover_color="#00ADAD", bg_color="#292929", text_color="#1E1E1E",
                                            fg_color="#008080", corner_radius= 2000, font=fonts.message_font() ,width=100)
        ok_button.place( relx = 0.65, rely=0.6)

    @staticmethod
    def result_message( root, text, next_frame):
        main_frame = customtkinter.CTkFrame( root, fg_color="#008080")
        main_frame.place( relx=0.3, rely=0.4)
        second_frame = customtkinter.CTkFrame( main_frame, width=400, height=100, border_color ='#008080', border_width=2, corner_radius=0)
        second_frame.pack()
        label = customtkinter.CTkLabel( second_frame, text=text, font=fonts.message_font2(), width=350, wraplength=330, anchor="center")
        label.place( relx = 0.05, rely = 0.3)
        main_frame.after( 4000, next_frame)

class game_gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 600
        self.resizable(False,False)
        self.geometry(f"{self.width}x{self.height}")
        self.background_image = customtkinter.CTkImage(dark_image = Image.open("frames/main.png"),size=(1000,600))
        self.main_label = None
        #self.bind('<Configure>', self.resize_window)

        #logic part:
        self.players = [ Player(), Player()]
        self.instant_entry = None
        self.selected_symbol = None
        self.buttons = None
        self.board = None
        self.player_bar = None
        self.turn = 1
        self.x_player_index = None
        self.round = 1

    def resize_window(self,event):
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.background_image.configure(size = (self.width,self.height))
        print("the window was resized ")

    def opening( self):
        self.main_label = customtkinter.CTkLabel(self, text=None, bg_color="#292929", width=self.width, height=self.height)
        self.main_label.pack()
        component.image(self.main_label, "frames/logo.png", x = 0.5, y = 0.35)
        component.text(self.main_label, "X or O ? Enjoy !!!", x = 0.5, y = 0.5)
        self.main_label.after(2000,self.main_label.destroy)

    def starting( self):
        self.main_label = customtkinter.CTkLabel(self,text =None ,image=self.background_image)
        self.main_label.pack()
        component.menu(self.main_label, "Start", "Quit", self.create_players, self.quit_game)
    
    def create_players( self, second_player = False):
        print("we are here")
        self.main_label.destroy()
        self.main_label = customtkinter.CTkLabel(self, text=None, image=self.background_image)
        self.main_label.pack()

        if not second_player:
            text = "First player name ..." 
            self.buttons = component.XO_choice(self.main_label, self.select_x, self.select_o)
        else:
            text = "Second player name ..."
            self.buttons = component.XO_choice(self.main_label, self.select_x, self.select_o, self.players[0].symbol)

        self.instant_entry = component.entry(self.main_label, text)
        component.text( self.main_label, "Choose your symbol :", 0.42, 0.35, anchor="center", bg_color="#292929") 
        component.next_button(self.main_label, self.submit)

    def Create_playground( self, first_time = True):
        for i in range(2):
            print(f"Player name: {self.players[i].name} his symbol: {self.players[i].symbol}")
        
        self.main_label.destroy()
        self.main_label = customtkinter.CTkLabel(self, text=None, image=self.background_image)
        self.main_label.pack()
        self.x_player_index = 0 if self.players[0].symbol == "x" else 1
        #Setting player_info_bar:
        self.player_bar = Player_bar()
        self.player_bar.show_graphic( self.main_label, x_player_name=self.players[self.x_player_index].name, o_player_name=self.players[1-self.x_player_index].name)
        if not first_time:
            self.player_bar.set( self.round, ( self.players[self.x_player_index].score, self.players[1 - self.x_player_index].score))

        #Setting the game_board with a random first player:
        first_player = randint( 0, 1)
        self.board = Board( self.players[first_player].symbol, self.Check, self.Continue)
        self.board.create_graphic_board( self.main_label)

        self.current_player(self.board.current_symbol)
    
    def Continue(self):
        self.board.current_symbol = "x" if self.board.current_symbol == "o" else "o"
        self.turn += 1
        self.current_player(self.board.current_symbol)

    def Check( self, index, symbol):
        print("Checking")
        if self.turn < 5 :
            pass
        else:
            x , y = (index // 3, index % 3)

            if self.sub_check(symbol, self.board.get_line(x)) :
                self.winner()
                
            elif self.sub_check(symbol, self.board.get_column(y)):
                self.winner()
                
            elif index in [0,4,8] and self.sub_check(symbol, self.board.get_diagonal_1()):
                self.winner()
                    
            elif index in [2,4,6] and self.sub_check(symbol, self.board.get_diagonal_2()):
                self.winner()
            
            else :
                if self.turn == 9 :
                    self.noWinner()
                else:
                    pass  
    
    def winner(self):
        print(f"{self.board.current_symbol} is win")
        winner_index = 0 if self.players[0].symbol == self.board.current_symbol else 1
        self.players[winner_index].score += 1

        self.board.disable_boxes()
        component.result_message( self.main_label, f"{self.players[winner_index].name} is win", self.end_game)

    def noWinner(self):
        self.board.disable_boxes()
        component.result_message( self.main_label, "Hmm, it seem that there is no winner !", self.end_game)

    def end_game( self):
        self.turn = 1
        self.main_label.destroy()
        self.main_label = customtkinter.CTkLabel(self,text =None ,image=self.background_image)
        self.main_label.pack()
        component.menu(self.main_label, "Replay", "Quit", self.replay_game, self.quit_game)

    def replay_game( self):
        self.main_label.destroy()
        self.main_label = customtkinter.CTkLabel(self,text =None ,image=self.background_image)
        self.main_label.pack()
        component.menu(self.main_label, "Same players", "New players",
                                                         self.replay_with_same_players, self.replay_with_other_players)

    def replay_with_same_players( self):
        self.round += 1
        self.Create_playground( first_time = False)
    
    def replay_with_other_players( self):
        self.round = 1
        [player.reset() for player in self.players ]
        self.create_players()

    def quit_game( self):
        print("Thanks to trying my game!!")
        exit()
    
    # Auxiliary functions :
    def select_x(self):
        if self.selected_symbol =="o":
            self.buttons[1].configure(border_width=0)
        #highlight x button
        self.buttons[0].configure(border_color ="#004d4d",border_width=3)
        self.selected_symbol = "x"
    def select_o(self):
        if self.selected_symbol == "x":
            self.buttons[0].configure(border_width=0)
        #highlight o button
        self.buttons[1].configure(border_color ="#004d4d",border_width=3)
        self.selected_symbol = "o"  
    def submit(self):
        name_validation = Player.check_name(self.instant_entry.get())
        if not name_validation:
            component.popup_message( self.main_label, "The name should contain 8 or fewer characters.")
        elif self.selected_symbol == None :
            component.popup_message( self.main_label, "Please, select a symbol !")
        else:
            if self.players[0].name == None:
                #submiting first player info
                self.players[0].name = self.instant_entry.get()
                self.players[0].symbol = self.selected_symbol  
                self.create_players(second_player=True)
            
            else:
                #submiting second player info
                self.players[1].name = self.instant_entry.get()
                self.players[1].symbol = "x" if self.players[0].symbol == "o" else "o"
                self.Create_playground()
    @staticmethod
    def sub_check(symbol, sequence): # sub_checkingfuncions:
        for sym in sequence:
             if sym != symbol :
                 return False
        return True 
    def current_player( self, symbol):
        try:
            self.current_state.destroy()
        except:
            pass
        self.current_state = customtkinter.CTkLabel( self.main_label, text =f"current symbol: {symbol}", fg_color="#292929", font=fonts.general_font())
        self.current_state.place( x= 420, y=560)

    # Run function : 
    def run(self):
        self.opening()
        self.starting()
        self.mainloop()

        


game = game_gui()
game.run()








""" logo_img = customtkinter.CTkImage(light_image = Image.open("frames/logo-2.png"),size=(100,100))
       
        label = customtkinter.CTkLabel(self.main_label, text=None,bg_color="#292929", image=logo_img)
        label.place(relx=0.5, rely=0.35, anchor='center')

        label = customtkinter.CTkLabel(self.main_label, text ="X or O ? Enjoy !!!",bg_color="#292929")
        label.place(relx=0.5, rely=0.5, anchor='center') """
