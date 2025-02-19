from utils import *
import pygame

WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Pyaint")
STATE = "COLOR"
Change = False

def init_grid(rows, columns, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(columns):    #use _ when variable is not required
            grid[i].append(color)
    return grid

def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))

def draw_mouse_position_text(win):
    pos = pygame.mouse.get_pos()
    pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
    try:
        row, col = get_row_col_from_pos(pos)
        text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
        win.blit(text_surface, (5 , HEIGHT - TOOLBAR_HEIGHT))
    except IndexError:
        for button in buttons:
            if not button.hover(pos):
                continue
            if button.text == "Clear":
                text_surface = pos_font.render("Clear Everything", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Erase":
                text_surface = pos_font.render("Erase", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "FillBucket":
                text_surface = pos_font.render("Fill Bucket", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Brush":
                text_surface = pos_font.render("Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Change":
                text_surface = pos_font.render("Swap Toolbar", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Shapes":
                text_surface = pos_font.render("Expand for Shape Options", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Curves":
                text_surface = pos_font.render("Expand for Curve Options", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Draw Circle":
                text_surface = pos_font.render("Draw Circle", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Draw Heart":
                text_surface = pos_font.render("Draw Heart", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Draw Arc":
                text_surface = pos_font.render("Draw Arc", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Draw Bezier":
                text_surface = pos_font.render("Draw Bezier Curve", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Draw BSpline":
                text_surface = pos_font.render("Draw BSpline", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "- - - - - - -":
                text_surface = pos_font.render("Toggle for Solid/Dotted", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break

            r,g,b = button.color
            text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)
            
            win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
        
        for button in brush_widths:
            if not button.hover(pos):
                continue
            if button.width == size_small:
                text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_medium:
                text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_large:
                text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break    

def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    draw_brush_widths(win)
    draw_mouse_position_text(win)
    pygame.display.update()

def draw_brush_widths(win):
    brush_widths = [
        Button(rtb_x - size_small/2, 480, size_small, size_small, drawing_color, None, None, "ellipse"),    
        Button(rtb_x - size_medium/2, 510, size_medium, size_medium, drawing_color, None, None, "ellipse") , 
        Button(rtb_x - size_large/2, 550, size_large, size_large, drawing_color, None, None, "ellipse")  
    ]
    for button in brush_widths:
        button.draw(win)
        # Set border colour
        border_color = BLACK
        if button.color == BLACK:
            border_color = GRAY
        else:
            border_color = BLACK
        # Set border width
        border_width = 2
        if ((BRUSH_SIZE == 1 and button.width == size_small) or (BRUSH_SIZE == 2 and button.width == size_medium) or (BRUSH_SIZE == 3 and button.width == size_large)): 
            border_width = 4
        else:
            border_width = 2
        # Draw border
        pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height), border_width) #border

def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= COLS:
        raise IndexError
    return row, col

def paint_using_brush(row, col, size):
    if BRUSH_SIZE == 1:
        grid[row][col] = drawing_color
    else: #for values greater than 1        
        r = row-BRUSH_SIZE+1
        c = col-BRUSH_SIZE+1
        
        for i in range(BRUSH_SIZE*2-1):
            for j in range(BRUSH_SIZE*2-1):
                if r+i<0 or c+j<0 or r+i>=ROWS or c+j>=COLS:
                    continue
                grid[r+i][c+j] = drawing_color         

# Checks whether the coordinated are within the canvas
def inBounds(row, col):
    if row < 0 or col < 0:
        return 0
    if row >= ROWS or col >= COLS:
        return 0
    return 1

def fill_bucket(row, col, color):
   
  # Visiting array
  vis = [[0 for i in range(101)] for j in range(101)]
     
  # Creating queue for bfs
  obj = []
     
  # Pushing pair of {x, y}
  obj.append([row, col])
     
  # Marking {x, y} as visited
  vis[row][col] = 1
     
  # Until queue is empty
  while len(obj) > 0:
     
    # Extracting front pair
    coord = obj[0]
    x = coord[0]
    y = coord[1]
    preColor = grid[x][y]
   
    grid[x][y] = color
       
    # Popping front pair of queue
    obj.pop(0)
   
    # For Upside Pixel or Cell
    if inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
      obj.append([x + 1, y])
      vis[x + 1][y] = 1
       
    # For Downside Pixel or Cell
    if inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
      obj.append([x - 1, y])
      vis[x - 1][y] = 1
       
    # For Right side Pixel or Cell
    if inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
      obj.append([x, y + 1])
      vis[x][y + 1] = 1
       
    # For Left side Pixel or Cell
    if inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
      obj.append([x, y - 1])
      vis[x][y - 1] = 1


run = True

clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_width = 40
button_height = 40
button_y_top_row = HEIGHT - TOOLBAR_HEIGHT/2  - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT/2   + 1
button_space = 42

size_small = 25
size_medium = 35
size_large = 50

rtb_x = WIDTH + RIGHT_TOOLBAR_WIDTH/2
brush_widths = [
    Button(rtb_x - size_small/2, 480, size_small, size_small, drawing_color, None, "ellipse"),    
    Button(rtb_x - size_medium/2, 510, size_medium, size_medium, drawing_color, None, "ellipse") , 
    Button(rtb_x - size_large/2, 550, size_large, size_large, drawing_color, None, "ellipse")  
]

button_y_top_row = HEIGHT - TOOLBAR_HEIGHT/2  - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT/2   + 1
button_space = 42


# Adding Buttons
buttons = []

for i in range(int(len(COLORS)/2)):
    buttons.append( Button(100 + button_space * i, button_y_top_row, button_width, button_height, COLORS[i]) )

for i in range(int(len(COLORS)/2)):
    buttons.append( Button(100 + button_space * i, button_y_bot_row, button_width, button_height, COLORS[i + int(len(COLORS)/2)]) )

#Right toolbar buttonst
# need to add change toolbar button.
#for i in range(10):
   # if i == 0:
    #    buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,name="Change"))#Change toolbar buttons
    #else:
     #   buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,"B"+str(i-1), BLACK))#append tools

buttons.append(Button(WIDTH - button_space, button_y_top_row, button_width, button_height, WHITE, "Erase", BLACK))  # Erase Button
buttons.append(Button(WIDTH - button_space, button_y_bot_row, button_width, button_height, WHITE, "Clear", BLACK))  # Clear Button
buttons.append(Button(WIDTH - 3*button_space + 5, button_y_top_row,button_width-5, button_height-5, name = "FillBucket",image_url="assets/paint-bucket.png")) #FillBucket
buttons.append(Button(WIDTH - 3*button_space + 45, button_y_top_row,button_width-5, button_height-5, name = "Brush",image_url="assets/paint-brush.png")) #Brush
buttons.append(Button(HEIGHT - 2*button_width,button_height+350,button_width,button_height,GRAY,"Shapes",BLACK))
buttons.append(Button(HEIGHT - 2*button_width,button_height+200,button_width,button_height,GRAY,"Curves",BLACK))
buttons.append(Button(HEIGHT - 2*button_width,button_height,button_width,button_height,SILVER,"- - - - - - -",BLACK))




draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT/2 - 30, 60, 60,drawing_color)
buttons.append(draw_button)

def get_circle_coordinates(X,Y,radius):
    list= []
    for i in range(5):
        list.append((X-5,Y-2+i))
        list.append((X+5,Y-2+i))

    for i in range(3):
        list.append((X-2-i,Y-5+i))
        list.append((X - 2 - i, Y + 5 - i))
        list.append((X + 4 - i, Y - 3 - i))
        list.append((X + 4 - i, Y + 3 + i))

    for i in range(3):
        list.append((X-1+i,Y-5))
        list.append((X - 1 + i, Y + 5))
    return list

def get_dotted_circle_coordinates(X,Y):
    list = []
    for i in range(5):
        list.append((X - 5, Y - 2 + i))

    for i in range(3):
        list.append((X - 2 - i, Y + 5 - i))

    for i in range(3):
       list.append((X - 1 + i, Y + 5))

    for i in range(3):
        list.append((X + 4 - i, Y + 3 + i))

    for i in range(5):
        list.append((X + 5, Y - 2 + i))

    for i in range(3):
        list.append((X + 4 - i, Y - 3 - i))

    for i in range(3):
        list.append((X - 1 + i, Y - 5))

    for i in range(3):
        list.append((X - 2 - i, Y - 5 + i))

    return list

def draw_circle():
    radius = 5
    pos = pygame.mouse.get_pos()
    dotted = True
    x, y = get_row_col_from_pos(pos)
    if DOTTED:
         coordinates = get_dotted_circle_coordinates(x,y)
         for i in range(0,len(coordinates),2):
             x, y = coordinates[i]
             if inBounds(x,y):
                grid[x][y] = drawing_color
    else:
        coordinates = get_circle_coordinates(x, y, radius)
        for i in coordinates:
            x, y = i
            if inBounds(x,y):
                grid[x][y] = drawing_color

def get_heart_coordinates(X,Y):
    list = []
    for i in range(3):
        list.append((X - i, Y - i))
        list.append((X - i, Y + i))
        list.append((X-3,Y-3-i))
        list.append((X - 3, Y + 3 + i))

    for i in range(2):
        list.append((X - 2 + i, Y - 6 - i))
        list.append((X - 2 + i, Y + 6 + i))
        list.append((X + i, Y - 7 ))
        list.append((X + i, Y + 7 ))

    for i in range(7):
        list.append((X + 2 + i, Y - 6 + i))
        list.append((X + 2 + i, Y + 6 - i))

    return list

def get_dotted_heart_coordinates(X,Y):
    list = []
    for i in range(3):
        #list.append((X - i, Y - i))
        list.append((X - i, Y + i))

    for i in range(3):
        list.append((X - 3, Y + 3 + i))

    for i in range(2):
        list.append((X - 2 + i, Y + 6 + i))

    for i in range(2):
        list.append((X + i, Y + 7))

    for i in range(7):
        list.append((X + 2 + i, Y + 6 - i))

    for i in range(1,7):
        list.append((X + 8 - i, Y - i))

    for i in range(2):
        list.append((X + 1 - i, Y - 7))

    for i in range(2):
        list.append((X - 1 - i, Y - 7 + i))

    for i in range(3):
        list.append((X - 3, Y - 5 + i))

    for i in range(2):
        list.append((X - 2 + i, Y - 2 + i))




    return list

def draw_heart():
    radius = 5
    pos = pygame.mouse.get_pos()
    dotted = True
    x, y = get_row_col_from_pos(pos)
    if DOTTED:
         coordinates = get_dotted_heart_coordinates(x,y)
         for i in range(0,len(coordinates),2):
             x, y = coordinates[i]
             if inBounds(x,y):
                grid[x][y] = drawing_color
    else:
        coordinates = get_heart_coordinates(x, y)
        for i in coordinates:
            x,y = i
            if inBounds(x,y):
                grid[x][y] = drawing_color

def paintarc(row,col):
    if DOTTED:
        # grid[row][col]=drawing_color
        for i in range(5):
            if(i%2!=0):
                if inBounds(row-i,col-4+i):
                    grid[row-i][col-4+i]=drawing_color
            x=row-i
            y=col-4+i
        if inBounds(x,y+1):
            grid[x][y+1]=drawing_color
        for i in range(4):
            if(i%2!=0):
                if inBounds(x+i,y+2+i):
                    grid[x+i][y+2+i]=drawing_color
            
        
            
    else:
        
        for i in range(4):
            if inBounds(row-i,col-4+i):
                grid[row-i][col-4+i]=drawing_color
            x=row-i
            y=col-4+i
        if inBounds(x,y+1):
            grid[x][y+1]=drawing_color
        if inBounds(x,y+2):
            grid[x][y+2]=drawing_color
        for i in range(4):
            if inBounds(x+i,y+2+i):
                grid[x+i][y+2+i]=drawing_color

def draw_bezier():
    pos = pygame.mouse.get_pos()
    x, y = get_row_col_from_pos(pos)
    step=1

    if DOTTED:
        step=2
    
    for i in range(0,3,1):
        for j in range(i,i+3,step):
            a=x-i-3
            b=y+j+2*i
            if inBounds(a,b):
                grid[a][b] = drawing_color
                
    for i in range(0,2,1):
        for j in range(i,i+2,step):
            a=x-i-1
            b=y+j+i-4
            if inBounds(a,b):
                grid[a][b] = drawing_color
                
    if inBounds(x,y-5):
        grid[x][y-5] = drawing_color
    
    for i in range(0,3,1):
        for j in range(i,i+3,step):
            a=x+i+3
            b=y+j+2*i
            if inBounds(a,b):
                grid[a][b] = drawing_color
                
    for i in range(0,2,1):
        for j in range(i,i+2,step):
            a=x+i+1
            b=y+j+i-4
            if inBounds(a,b):
                grid[a][b] = drawing_color
                
def get_solid_bspline_coordinates(X,Y):
    list= []
    for i in range(4):
        list.append((X + i, Y - 7 - i))
        list.append((X - i, Y - 7 + i))
    list.append((X,Y))
    for i in range(4):
        list.append((X + i, Y + 7 - i))
        list.append((X - i, Y + 7 + i))
    for i in range(4):
        list.append((X - i, Y - i))
        list.append((X + i, Y + i))
    return list

def get_dotted_bspline_coordinates(X,Y):
    list= []
    for i in range(0,4,2):
        list.append((X + i, Y - 7 - i))
        list.append((X - i, Y - 7 + i))
    list.append((X,Y))
    for i in range(0,4,2):
        list.append((X + i, Y + 7 - i))
        list.append((X - i, Y + 7 + i))
    for i in range(0,4,2):
        list.append((X - i, Y - i))
        list.append((X + i, Y + i))
    return list

def draw_bspline():
    pos = pygame.mouse.get_pos()
    x, y = get_row_col_from_pos(pos)
    if DOTTED:
        coordinates = get_dotted_bspline_coordinates(x,y)
    else:
        coordinates = get_solid_bspline_coordinates(x,y)

    for i in coordinates:
            x, y = i
            if inBounds(x,y):
                grid[x][y] = drawing_color
   
clicks = 0
while run:
    clock.tick(FPS) #limiting FPS to 60 or any other value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #if user closed the program
            run = False
        
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)

                if STATE == "COLOR":
                    paint_using_brush(row, col, BRUSH_SIZE)

                elif STATE == "FILL":
                    fill_bucket(row, col, drawing_color)
                elif STATE == "DRAW CIRCLE":
                    draw_circle()
                elif STATE == "DRAW HEART":
                    draw_heart()
                elif STATE == "ARC": #Draws an arc
                    paintarc(row,col)
                elif STATE == "DRAW BEZIER":
                    draw_bezier()
                elif STATE == "DRAW BSPLINE":
                    draw_bspline()
                    
            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        break

                    if button.name == "FillBucket":                        
                        STATE = "FILL"
                        break
                    
                    if button.name == "Change":
                        Change = not Change
                        for i in range(10):
                            if i == 0:
                                buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,name="Change"))
                            else:
                                if Change == False:  
                                    buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,"B"+str(i-1), BLACK))
                                if Change == True:
                                   buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,"C"+str(i-1), BLACK))
                        break
                     
                    if button.name == "Brush":
                        STATE = "COLOR"
                        break

                    if button.text == "Shapes":
                        buttons.append(Button(HEIGHT - 2 * button_width,button_height + 300, button_width, button_height,WHITE, "Draw Circle", BLACK))
                        buttons.append(Button(HEIGHT - 2 * button_width, button_height + 250, button_width, button_height, WHITE, "Draw Heart", BLACK))


                        break

                    if button.text == "Curves":
                        buttons.append(
                            Button(HEIGHT - 2 * button_width, button_height + 150, button_width, button_height, WHITE,
                                   "Draw Arc", BLACK))
                        buttons.append(
                            Button(HEIGHT - 2 * button_width, button_height + 100, button_width, button_height, WHITE,
                                   "Draw Bezier", BLACK))
                        buttons.append(
                            Button(HEIGHT - 2 * button_width, button_height + 50, button_width, button_height, WHITE,
                                   "Draw BSpline", BLACK))

                        break

                    if button.text == "Draw Circle":
                        STATE = "DRAW CIRCLE"
                        break

                    if button.text == "Draw Heart":
                        STATE = "DRAW HEART"
                        break
                    if button.text=="Draw Arc":
                        STATE="ARC"
                        break
                    if button.text == "Draw Bezier":
                        STATE = "DRAW BEZIER"
                        break
                    if button.text == "Draw BSpline":
                        STATE = "DRAW BSPLINE"
                        break
                    if button.text == "- - - - - - -":
                        if DOTTED:
                            DOTTED = False
                            buttons.remove(button)
                            buttons.append(Button(HEIGHT - 2*button_width,button_height,button_width,button_height,SILVER,"- - - - - - -",BLACK))
                        else:
                            DOTTED = True
                            buttons.remove(button)
                            buttons.append(Button(HEIGHT - 2*button_width,button_height,button_width,button_height,GRAY,"- - - - - - -",BLACK))
                        
                        break
                    
                    drawing_color = button.color
                    draw_button.color = drawing_color
                    
                    break
                
                for button in brush_widths:
                    if not button.clicked(pos):
                        continue
                    #set brush width
                    if button.width == size_small:
                        BRUSH_SIZE = 1
                    elif button.width == size_medium:
                        BRUSH_SIZE = 2
                    elif button.width == size_large:
                        BRUSH_SIZE = 3

                    STATE = "COLOR"
        
    draw(WIN, grid, buttons)

pygame.quit()