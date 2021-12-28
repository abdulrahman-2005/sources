import socket, threading
from random import randint

class Game:
    def __init__(self):
        self.board = ["init", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.turn = "X"
        self.you = "X"
        self.oppnent = "O"
        self.winner = None
        self.game_over = False
        self.counter = 0

        print("""
         1 | 2 | 3
        -----------
         4 | 5 | 6
        -----------
         7 | 8 | 9
        """, end="\r")
    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        client, addr = server.accept()

        self.you = "X"
        self.oppnent = "O"

        threading.Thread(target=self.handle_connection, args=(client, )).start()
        server.close()
    
    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you = "O"
        self.oppnent = "X"
        threading.Thread(target=self.handle_connection, args=(client, )).start()
    
    def handle_connection(self, client):
        while not self.game_over:
            if self.turn == self.you:
                got = False
                while got is False:
                    try:
                        move = int(input("Your move 1-9: "))
                        got = True
                    except ValueError:
                        print("just numbers please")
                    except move not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        print("numbers from 1 to 9 only")
                
                if self.check_valid_move(move):
                    move = str(move)
                    client.send(move.encode('utf-8'))
                    self.apply_move(move, self.you)
                    self.turn = self.oppnent
                else: print("Invalid Move")
            else:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('utf-8'), self.oppnent)
                    self.turn = self.you

    def apply_move(self, move, player):
        move = int(move)
        if self.game_over:
            return
        self.counter += 1
        self.board[move] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print(f"you Won!")
                exit()
            if self.winner == self.oppnent:
                print(f"you Lost!")
                exit()
        else:
            if self.counter == 9:
                print(f"Tie!")
                exit()
    
    def check_valid_move(self, move):
        move = int(move)
        return self.board[move] == " "

    def check_if_won(self):
        if self.board[1] == self.board[2] == self.board[3] != " ":
            self.winner = self.board[1]
        if self.board[4] == self.board[5] == self.board[6] != " ":
            self.winner = self.board[4]
        if self.board[7] == self.board[8] == self.board[9] != " ":
            self.winner = self.board[7]

        if self.board[1] == self.board[4] == self.board[7] != " ":
            self.winner = self.board[1]
        if self.board[2] == self.board[5] == self.board[8] != " ":
            self.winner = self.board[2]
        if self.board[3] == self.board[6] == self.board[9] != " ":
            self.winner = self.board[3]
        
        if self.board[1] == self.board[5] == self.board[9] != " ":
            self.winner = self.board[1]
        if self.board[3] == self.board[5] == self.board[7] != " ":
            self.winner = self.board[3]
        
        if self.winner == "X" or self.winner == "O":
            self.game_over = True
            return True
        else:
            return False
    
    def print_board(self):
        print(f"""
        {self.board[1]} | {self.board[2]} | {self.board[3]}
        -----------
        {self.board[4]} | {self.board[5]} | {self.board[6]}
        -----------
        {self.board[7]} | {self.board[8]} | {self.board[9]}
        """, end="\r")

def app():
    init = input("1. Host a Game\n2. Join a Game\n>> ")#TODO Host With Password
    port = int(f"{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}")
    if init == "1":
        ip = input("your ip address: ") #localhost if you want
        print(f"your game id is {port} with ip: {ip}\r")
        game=Game()
        game.host_game(ip, port)
    #TODO add a hosting password functionality
    # elif init == "2":
    #     password = input("Create Password: ")
    #     print(f"your game id is {port} and password is {password}\r")
    #     game=Game(name)
    #     game.host_game("localhost", port)
    else:
        try:
            port = int(input("write the game id: "))
            ip = input("target ip address: ") #localhost if you want
            game=Game()
            game.connect_to_game(ip, port)
        except:
            print("there is no game with this id\r")
        

app()
