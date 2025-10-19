import msvcrt
import time
import os
import threading
import random


size = os.get_terminal_size()
screen_width = size.columns //2  
screen_height = size.lines -3
char = ""
player_x = screen_width//2
player_y = screen_height//2
direction = ""
past_positions = []
score = 0
running = True
apple_x = random.randint(3,screen_width-3)
apple_y = random.randint(3,screen_height-3)

lost = False
#message = "Press any key to start"

def user_inp():
    global char, running
    while running:    
        if msvcrt.kbhit(): 
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':       # Up arrow
                    char = "w"
                elif key == b'P':     # Down arrow
                    char = "s"
                elif key == b'K':     # Left arrow
                    char = "a"
                elif key == b'M':     # Right arrow
                    char = "d"
                else:
                    continue
                continue
            try:
                key = key.decode().lower()
                if key in ("w","a","s","d"):
                    char = key
                else:
                    continue
            except UnicodeDecodeError:
                continue
        time.sleep(0.001)


    
def game_update():
    global player_x, player_y, apple_x, apple_y, char, running, past_positions, score, direction, lost
    while running:
        # Clear the console
        print("\033[H", end="")

        #Handle player logic
        if char == "a" and direction != "right":
            direction = "left"
        elif char == "d" and direction != "left":
            direction = "right"
        elif char == "s" and direction != "up":
            direction = "down"
        elif char == "w" and direction != "down":
            direction = "up"
        
        if direction == "up":
            player_y -= 1
        elif direction == "down":
            player_y += 1
        elif direction == "right":
            player_x += 1
        elif direction == "left":
            player_x -= 1

        #check if player intersected themselves
        for i in range(len(past_positions)):
            if past_positions[i][1] == player_x and past_positions[i][0] == player_y and char !="":
                lost = True    
        
        if player_x < 3 or player_x > screen_width - 3 or player_y > screen_height-3 or player_y < 3:
            lost = True
        
        #Draw Canvas
        grid = []
        for j in range(screen_height):
            row_arr = []
            for i in range(screen_width):
                if(j == 2 or j == screen_height - 2):
                    row_arr.append("--")
                elif(i== 2 or i == screen_width - 2):
                    row_arr.append("|")
                else:
                    row_arr.append("  ")
            grid.append(row_arr)
        
        #apple logic
        if(apple_x == player_x and apple_y == player_y):
            apple_x = random.randint(3, screen_width - 3)
            apple_y = random.randint(3, screen_height - 3)
            score += 1
 
        #update snake body
        past_positions.insert(0, [player_y, player_x])
        if len(past_positions) > score + 3:
            past_positions.pop()
                        
        for i in range(len(past_positions)):
            grid[past_positions[i][0]][past_positions[i][1]] = "██"
       
        ##draw snake head
        grid[player_y][player_x] = "██"
        
        #draw app
        grid[apple_y][apple_x] = "()"
        print(f"{'score':>10} {score}")
        for i in range(screen_height):
                print("".join(grid[i]))
        print("\033[J", end="")
        if lost:
            print(f"Game Over, you have a score of {score}")
            inp = input("enter anything to try again or q to quit: ")
            if(inp == "q"):
                running = False
            else:
                player_x = screen_width//2
                player_y = screen_height//2
                direction = ""
                past_positions = []
                score = 0
                running = True
                apple_x = random.randint(3,screen_width-3)
                apple_y = random.randint(3,screen_height-3)
                lost = False
                running = True   
                os.system("cls")
        time.sleep((0.2)/(1+score/5))
    
if __name__ == "__main__":
    os.system("cls")
    threading.Thread(target=user_inp, daemon=True).start()
    game_update()  
