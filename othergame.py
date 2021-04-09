import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from collections import deque
import numpy

class cube(object):
    rows = 10
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(18, 228, 60)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = int((1/rows)*50)
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}
    path = [] #not currently used
    directional_path = [] #inputs dijkstra's algorithm path
    cluster_moves = [] #directional moves for clustering
    snack = ()
    cluster = False #whether the snake should do cluster moves
    updated_data = [] #updated snake body and snack nested list
    recluster = False #whether reclustering will work or not
    backup = False #whether backup was successful or not
    quit = False #when there are no other moves

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #keys = pygame.key.get_pressed() #for manual snakey

        AI = "meep" #default
        print("snake. cluster in s.move()")
        print(snake.cluster)
        if ((snake.cluster) == True):
            if (snake.cluster_moves != []):
                print("popping cluster moves")
                print(snake.cluster_moves)
                AI = snake.cluster_moves.pop(0)
                print("AI is cluster")
                if (snake.directional_path):
                    snake.directional_path = []
            else:
                print("Dij's also after clustering")
                dij_algo_master(snake.updated_data[0], snake.updated_data[1], rows, change_of_basis)



                snake.cluster = False

        # originally paths were inputted as coordinates and converted to directions in the following if statement
        # if (snake.path): #if a new box number path has been created turn it into a directional_path
        #     directions = translate_into_directions(snake.path, rows) #and repeats final direction when snake arrive at destination
        #     print("do we get into if snake.path?")
        #     snake.path = []
        #     snake.directional_path = directions

            #function makes snake.path = []
        if (snake.directional_path):
            print("HERREE")
            print(snake.directional_path)
            AI = snake.directional_path.pop(0)
            print("AI is dij or back up")
            if (((snake.backup) == True) & (len(snake.directional_path) <= 1)): #THIS MIGHT BE AN ERRRORORRROROROROR #made edit at 12pm
                snake.backup = False
                print("AI is last of backup or something")
                #body = snake.updated_data[0]
                #snack = snake.updated_data[1]
                print("finished popping back ups")
                #dij_algo_master(snake.body, snake.snack, rows, change_of_basis)
                #what if

                dij_algo_master(snake.updated_data[0], snake.updated_data[1], rows, change_of_basis)
                #this instead of above
                print("inside backup back up")
                print(snake.directional_path)
                #the if statement might rly mess things up
                if (len(snake.directional_path) > 0):
                    print("inside backup back up if statement")
                    print(snake.directional_path)
                    AI = snake.directional_path.pop(0) #this might mess things up
                    print("desired AI")
                    print(AI)
                else:
                    AI = "meep"

        if AI == "meep":
            print("this is THE meep")
            # this only works if an opening appears at the end of the backup moves
            snake.updated_data[0] = s.body  # edit at 11
            can_continue_game = dij_algo_master(snake.updated_data[0], snake.updated_data[1], rows, change_of_basis)
            if ((can_continue_game == False) & (snake.backup == False)):
                snake.directional_path = []
                print("using default")
                #edit at 1130
                snake.quit = True
                return None
                #AI = "down"  # default


        print("AI:")
        print(AI)
#fix for event part!
        if AI == "left":
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            #self.turns is a dictionary with {(position tuple) : [dirnx, dirny]}

        elif AI == "right":
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif AI == "up":
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif AI == "down":
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]



            #these are commands for a manual snakey
            # for key in keys:
            #     if keys[pygame.K_LEFT]:
            #         self.dirnx = -1
            #         self.dirny = 0
            #         self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            #         #self.turns is a dictionary with {(position tuple) : [dirnx, dirny]}
            #
            #     elif keys[pygame.K_RIGHT]:
            #         self.dirnx = 1
            #         self.dirny = 0
            #         self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            #
            #     elif keys[pygame.K_UP]:
            #         self.dirnx = 0
            #         self.dirny = -1
            #         self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            #
            #     elif keys[pygame.K_DOWN]:
            #         self.dirnx = 0
            #         self.dirny = 1
            #         self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): #i is index and c is value/location
            p = c.pos[:] #tuple

            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)






    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def translate_into_directions(box_num_path, rows):
    output = []
    for index in range(len(box_num_path)-1):
        if ((box_num_path[index] - box_num_path[index + 1]) == -1):
            output.append("right")
        if ((box_num_path[index] - box_num_path[index + 1]) == 1):
            output.append("left")
        if ((box_num_path[index] - box_num_path[index + 1]) == rows):
            output.append("up")
        if ((box_num_path[index] - box_num_path[index + 1]) == (-1 *rows)):
            output.append("down")

    return output


def AI_Moves(body, head):
    print("yellooww")
    for i, c in enumerate(body):  # i is index and c is value/location
        p = c.pos[:]  # tuple

    print(head.pos)
    if head.pos == (0,0):
        print("indeed")
        return "right"
    if head.pos == (9, 0):
        return "down"
    if head.pos == (9,9):
        return "left"
    if head.pos == (0,9):
        return "up"

def dij_algo_master(body, snack_pos, rows, change_of_basis):
    body_list = []
    for i, c in enumerate(body):  # i is index and c is value/location
        p = c.pos[:]  # tuple
        body_list.append(p)
    print(snack_pos)

    dictionary = change_of_basis

    #remove boxes occupied by snake body
    edited_dictionary = edit_box_to_coord_dict(dictionary, body_list, rows)


    #create dictionary with box num key to adjacent box nums that are not part of the snake
    adjacency_dictionary = generate_adjacency_dictionary(edited_dictionary, rows)

    #start and end are box number
    tempx_start = body_list[0][0]
    tempy_start = body_list[0][1]
    start = ((tempy_start*rows) + tempx_start)#head is the first element in list
    tempx_tail = body_list[-1][0]
    tempy_tail = body_list[-1][1]
    tail = ((tempy_tail * rows) + tempx_tail)  # tail is the last element in list
    tempx_end = snack_pos[0]
    tempy_end = snack_pos[1]
    end = ((tempy_end * rows) + tempx_end)
    #possibilities list of keys in edited dict
    # possibilities = [] #edit in carr
    # for key in adjacency_dictionary:
    #     possibilities.append(key)

    mini_cluster = check_for_connection(start, end, adjacency_dictionary)
    if mini_cluster == False:
        print("can't reach snack")

        updated_body_list = []
        for i, c in enumerate(snake.updated_data[0]):  # i is index and c is value/location
            p = c.pos[:]  # tuple
            updated_body_list.append(p)
        updated_edited_dictionary = edit_box_to_coord_dict(dictionary, updated_body_list, rows)
        backup(updated_edited_dictionary, body_list[0])

        print("could not reach snack")
        return False

    else:
        dist_and_path_ans = dij(start, end, adjacency_dictionary, rows)
        dist_and_path = dist_and_path_ans[1]

    directions_results = translate_into_directions(dist_and_path, rows)
    snake.path = []
    snake.directional_path = directions_results
    return True


def cluster_algo_master(body, snack, rows, change_of_basis):
    snake.snack = snack
    body_list = []
    for i, c in enumerate(body):  # i is index and c is value/location
        p = c.pos[:]  # tuple
        body_list.append(p)

    body_size = len(body_list)
    head = body_list[0]
    unoccupied = edit_box_to_coord_dict(change_of_basis, body_list, rows)
    print("these are different meeps")
    #return input of box numbers in the directions left, right, up, down, respectively
    direct_paths = furthest_distance(unoccupied, rows, head)
    result = create_directional_path(direct_paths, rows, body_size)
    #debugging
    # print("result in cluster algo master")
    # print(result)
    # print("result")
    # print(result)
    # print(snake.directional_path)
    # print(snake.cluster_moves)
    # print(snake.cluster)
    # print(snake.recluster)


    if result == False:
        snake.cluster = False
        snake.cluster_moves = []
        dij_algo_master(body, snack, rows, change_of_basis)
    else:
        snake.cluster_moves = result
        snake.cluster = True
    return True



def furthest_distance(unoccupied, rows, head):
    negative_rows = -1 * rows # for later use
    #convert head to box num
    tempx = head[0]
    tempy = head[1]
    head_box_num = ((tempy * rows) + tempx)
    output = [[head_box_num],[head_box_num],[head_box_num],[head_box_num]] #left, right, up, down

    condition = [-1, 1, negative_rows, rows]#corresponds with direction
    x_boundary = head_box_num % rows
    y_boundary = head_box_num // rows
    left_boundary = head_box_num - x_boundary - 1
    right_boundary = head_box_num + (rows - x_boundary)
    upper_boundary = head_box_num - (rows * (y_boundary + 1))
    lower_boundary = head_box_num + (rows * (rows - y_boundary + 1))
    boundary = [left_boundary, right_boundary, upper_boundary, lower_boundary]
    for index in range(4):
        constant = condition[index]
        curr = head_box_num
        keep_going = True
        while (keep_going):
            next = curr + constant
            if ((next in unoccupied) & (next != boundary[index])):
                print("woopwoop")
                output[index].append(next)
                curr = next
            else:
                keep_going = False

    return output


def create_directional_path(direct_paths, rows, body_size):
    #direct paths has a list of furthest undisturbed paths in the directions left, right, up, down respectively
    left_length = len(direct_paths[0])
    right_length = len(direct_paths[1])
    up_length = len(direct_paths[2])
    down_length = len(direct_paths[3])
    list_of_lengths = [["left", left_length], ["right", right_length], ["up", up_length], ["down", down_length]]
    #is left or right bigger?
    if (list_of_lengths[0][1] >= list_of_lengths[1][1]):
        list_of_lengths.pop(1)
    else:
        list_of_lengths.pop(0)
    #is up or down bigger?
    if (list_of_lengths[1][1] >= list_of_lengths[2][1]):
        list_of_lengths.pop(2)
    else:
        list_of_lengths.pop(1)

    #now list_of_length has two sub lists with the direction and length
    print("inside create direction path")
    print(direct_paths)
    print(list_of_lengths[0][1])
    if (((list_of_lengths[0][1]) <=2) & (list_of_lengths[1][1] <=2)):
        return False
    else:
        horizontal_length = list_of_lengths[0][1]
        vertical_length = list_of_lengths[1][1]
        if (horizontal_length >= vertical_length):
            direction = list_of_lengths[0][0]
            direction_length = list_of_lengths[0][1]
            perp_direction = list_of_lengths[1][0]
            perp_direction_length = vertical_length
            if ((perp_direction_length % 2) != 0):
                perp_direction_length -= 1
        else:
            direction = list_of_lengths[1][0]
            direction_length = list_of_lengths[1][1]
            perp_direction = list_of_lengths[0][0]
            perp_direction_length = horizontal_length
            if ((perp_direction_length % 2) != 0):
                perp_direction_length -= 1
    #generate box number path

    repeats = perp_direction_length
    path = []
    helper = {"left": "right", "right": "left", "up": "down", "down": "up"}

    if ((body_size > rows) & (body_size < (3*rows))): #edit at 945
        repeats -= 1
        int(repeats)


    while (repeats > 1):
        for boxes in range(direction_length - 2):
            path.append(direction)
        path.append(perp_direction)
        repeats -= 1
        if (repeats == 1):
            continue
        else:
            for boxes in range(direction_length - 2):
                opp_direction = helper[direction]
                path.append(opp_direction)
            path.append(perp_direction)
        repeats -= 1

    #no point in having a path longer than the body size so...
    if ((len(path)) > body_size):
        print("saving time")
        trim_amount = (len(path) - body_size)
        for trim in range(trim_amount):
            path.pop()

    #from testing sometimes clustering takes too much time. Aribitrary limit = rows*2
    if ((len(path)) > (rows*2)):
        trim_amount = (len(path) - (rows*2))
        for trim in range(trim_amount):
            path.pop()

    print("here ya go")
    print(direct_paths)
    print(path)
    return path


def backup(edited_dictionary, head_coord):
    print("WE MADE IT into the function BABBYY")
    options = furthest_distance(edited_dictionary, rows, head_coord)
    print("WE MADE IT BABBYY")
    print(options)

    result = make_directional_path(options)

    if (len(result) > 0):
        snake.directional_path = result
        snake.backup = True
    else:
        snake.directional_path = []
        snake.backup = False
    return None


def make_directional_path(direct_paths):
    dict_of_direction_lengths = {}
    left_length = len(direct_paths[0])
    dict_of_direction_lengths[left_length] = "left"
    right_length = len(direct_paths[1])
    dict_of_direction_lengths[right_length] = "right"
    up_length = len(direct_paths[2])
    dict_of_direction_lengths[up_length] = "up"
    down_length = len(direct_paths[3])
    dict_of_direction_lengths[down_length] = "down"

    #answer = [max_length, corresponding direction]
    max_length = max(dict_of_direction_lengths)

    output = []
    for repetition in range(max_length - 1):
        output.append(dict_of_direction_lengths[max_length])
    print("There is a solution")
    print(output)
    return output





def generate_box_to_coord_dict(rows):
    output = {}
    for item in range((rows**2)):
        x = item % rows
        y = item // rows
        output[item] = (x, y)
    return output

def edit_box_to_coord_dict(dictionary, body_list, rows):
    output = dictionary.copy()
    body_listy = body_list.copy()
    body_listy.pop(0)
    for snake_block in body_listy:
        box = ((snake_block[1]*rows) + snake_block[0])
        del output[box]
    return output

def generate_adjacency_dictionary(edited_dictionary, rows):
    #when rows is 3 output will look like:
    # {0: [1,3], 1: [0,2,4], etc...
    output = {}
    for key in edited_dictionary:
        connections = []
        if ((key % rows) != 0):
            left = (key - 1)
            connections.append(left)
        if ((key % rows) != (rows-1)):
            right = (key + 1)
            connections.append(right)
        if ((key // rows) != 0):
            up = (key - rows)
            connections.append(up)
        if ((key // rows) != (rows - 1)):
            down = (key + rows)
            connections.append(down)
        output[key] = connections
    return output


def check_for_connection(start, end, graph):
    # check to see if there exists a connection between start and end
    unvisited = []
    visited = []
    connections = []
    links = []
    if start not in graph:
        return False
    for initial_connections in graph[start]:
        unvisited.append(initial_connections)
        connections.append(initial_connections)
    while (unvisited != []):
        curr = unvisited.pop(0)
        visited.append(curr)

        if curr in graph:
            links = graph[curr]
            for link in links:

                if ((link not in visited) & (link not in unvisited)):
                    unvisited.append(link)
                connections.append(link)
                if (link == end): #this if statement was added to avoid going through every connection
                    break #stop expanding connections if current connection is the snack

    #this was the original code which I've kept as backup
    # however the addition of the break statement improves the average time and space complexity
    # Now the search method is depth first search because it pops(0), so it continues looking at the expansions
    # of the original adjacent box before exploring others
    if end not in connections:
        #debugging
        #print(connections)
        return False
    else:
        return True

def gen_adjacency_dictionary_with_tail(tail, adjacency_dictionary, rows, change_of_basis):
    #this function is not currently in use however its intended purpose was to
    #develop cluster and/or backup moves based on where the tail will not be in x moves
    #this function simply adds the x last grid boxes of the snake back into the adjacency dictionary
    #re-adds tail and connections to adjacency dictionary
    output = adjacency_dictionary.copy()
    tail_coord = change_of_basis[tail]
    connections = []
    if tail_coord[0] != 0:
        left = (tail_coord[1]*rows + (tail_coord[0] - 1))
        connections.append(left)
    if tail_coord[0] != (rows-1):
        right = (tail_coord[1] * rows + (tail_coord[0] + 1))
        connections.append(right)
    if tail_coord[1] != 0:
        up = (((tail_coord[1] - 1)*rows) + tail_coord[0])
        connections.append(up)
    if tail_coord[1] != (rows - 1):
        down = (((tail_coord[1] + 1)*rows) + tail_coord[0])
        connections.append(down)
    if connections == []:
        return adjacency_dictionary
    else:
        output[tail] = connections
        return output


def dij(start, end, graph, rows):
    #possibilities is simply a list of box numbers
    #possibilities = [0,1,2,3...((rows**2)-1)]
    possibilities = []
    for key in graph:
        possibilities.append(key)

    #the graph is the adjacency dictionary
    queue = deque([start])
    visited = {}
    unvisited = {}
    for box in possibilities:
        unvisited[box] = float("inf")
    path_to_visited = {}
    path_to_unvisited = {start : [start]}
    prev = [None]*(rows**2)
    node = None
    dist = 0
    while (len(queue) > 0) and (node != end):
        node = queue.popleft()

        #don't revisit node
        if node in visited:
            continue
        else:
            visited[node] = dist
            path_to_visited[node] = path_to_unvisited[node]


            del unvisited[node]

        for connection in graph[node]:
            if connection not in unvisited:
                continue
            elif unvisited[connection] > (dist + 1):
                unvisited[connection] = dist + 1
                path_to_unvisited[connection] = path_to_visited[node] + [connection]
                prev[connection] = node

        #pick the closest unvisited
        if node == end:
            break
        new = min(unvisited, key=unvisited.get)

        #if there is no path possible
        if unvisited[new] == 100:
            return None, []

        #update distance and new node
        dist = unvisited[new]
        queue.append(new)

    print("inside dij function")
    print(visited[end])
    print(path_to_visited[end])
    return visited[end], path_to_visited[end]



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:#if snack is in snake
            print("can i make this go off???")
            continue
        else:
            break
    return (x, y)



def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack, change_of_basis

    width = 700
    rows = 25
    cube.rows = rows
    cube.w = width

    change_of_basis = generate_box_to_coord_dict(rows)

    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (0, 0))
    snack = cube(randomSnack(rows, s), color=(183, 7, 54))
    flag = 1


    clock = pygame.time.Clock()
    dij_algo_master(s.body, snack.pos, rows, change_of_basis) #for when the game starts
    number_of_moves = 0

    global boarders
    boarders = []
    for side in range(4):
        for n in range(rows + 2):
            if side == 0:  # left
                n -= 1
                boarders.append((-1, n))
            if side == 1:  # right
                n -= 1
                boarders.append((rows, n))
            if side == 2:  # up
                n -= 1
                boarders.append((n, -1))
            if side == 3:  # down
                n -= 1
                boarders.append((n, rows))



    life_score = 0
    while flag:
        life_score += 1

        pygame.time.delay(50)
        clock.tick(10)

        #if no moves could be generated
        if (s.quit == True):
            s.quit = False
            print('Score:' + str(len(snake.updated_data[0])))
            data_collection(rows, life_score, len(snake.updated_data[0]), "Could not generate another move")
            message_box('You Lost!', 'You could not generate another move. Your length was: ' + str(len(s.body)) + " and your score is: " + str(life_score))
            #s.reset((0, 0))
            pygame.quit()
            pass



        snake.updated_data = [s.body, snack.pos]
        s.move() #tells snake to move
        snake.updated_data = [s.body, snack.pos]
        number_of_moves += 1
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(183, 7, 54))
            #every time snack is eaten:
            number_of_moves = 0
            print("nomnomnom")
            snake.updated_data = [s.body, snack.pos]  # edit at 1045

            #debigging
            # print("debugging")
            # print("snake.direction_path")
            # print(snake.directional_path)
            # print("snake.cluster")
            # print(snake.cluster_moves)
            # print("snake backup")
            # print(snake.backup)


            if ((len(s.body)) >= rows):
                print("body length")
                print(len(s.body))
                cluster_algo_master(snake.updated_data[0], snake.updated_data[1], rows, change_of_basis)
                #DIJ_algo_master function called elsewhere so it creates the path based on the new position
                print("STARTING CLUSTER MASTER")
            else:
                dij_algo_master(snake.updated_data[0], snake.updated_data[1], rows, change_of_basis)

        #if runs out of time
        if (number_of_moves > ((4 * rows - 4) * 1.5)):
            print('Score:' + str(len(s.body)))
            data_collection(rows, life_score, len(snake.updated_data[0]), "Ran out of time")
            message_box('You Lost!', 'You ran out of time. Your length was: ' + str(len(s.body)) + " and your score is: " + str(life_score))
            life_score = 0
            s.reset((0, 0))
            break

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score:' + str(len(s.body)))
                data_collection(rows, life_score, len(snake.updated_data[0]), "Bumped into self")
                message_box('You Lost!', 'You bumbed into yourself. Your length was: ' + str(len(s.body)) + " and your score is: " + str(life_score))
                life_score = 0
                s.reset((0, 0))
                break



        #if it travels outside boarder
        for x in range(len(s.body)):
            if s.body[x].pos in boarders:
                print('Score:' + str(len(s.body)))
                data_collection(rows, life_score, len(snake.updated_data[0]), "Bumped into boarder")
                message_box('You Lost!', 'You bumbed into the boarder. Your length was: ' + str(len(s.body)) + " and your score is: " + str(life_score))
                life_score = 0
                s.reset((0, 0))
                break


        redrawWindow(win)

    pass

def data_collection(board_width, score, body_length, reason_for_end):
    #generates text and writes it in dataa_collection.txt
    #text is formatted as:
    #Trial: 0, Board width: 10, Score: 498, Body length: 47, Reason for end of game: Could not generate another move
    f = open("data_collection.txt", "+a")
    trials = count_lines("data_collection.txt")
    f.write("Trial: " + str(trials) + " Board width: " + str(board_width) + ", Score: " + str(score) + ", Body length: " + str(body_length) + ", Reason for end of game: " + reason_for_end + " \n")
    f.close()


def count_lines(fname):
    #counts number of lines in file which corresponds with number of trials
    num_lines = 0
    with open(fname, 'r') as f:
        for line in f:
            num_lines += 1
    return num_lines


def data_analysis():
    #generates data for a box plot/box and whiskers plot
    fname = "data_collection.txt"
    scores = []
    lengths = []
    with open(fname, 'r') as f:
        strings = f.readlines()
        for s in strings:
            string = s.split(",")
            #Board width index = 1
            # score index = 2
            # length = 3
            board_width = int(str(string[1][-2]) + str(string[1][-1]))
            if board_width == 10:
                score_temp = string[2].split(" ")
                score = score_temp[2]
                length_temp = string[3].split(" ")
                length = length_temp[3]
                scores.append(int(score))
                lengths.append(int(length))
    average_score = numpy.average(scores)
    average_length = numpy.average(lengths)
    min_score = min(scores)
    min_length = min(lengths)
    max_score = max(scores)
    max_length = max(lengths)
    s_low = numpy.quantile(scores, 0.25)
    l_low = numpy.quantile(lengths, 0.25)
    s_up = numpy.quantile(scores, 0.75)
    l_up = numpy.quantile(lengths, 0.75)
    s_std = numpy.std(scores)
    l_std = numpy.std(lengths)
    print(scores)
    print(lengths)

    print("Average score: " + str(average_score) + " and average length: " + str(average_length))
    print("Score range: " + str(min_score) + " to " + str(max_score) + " and length range: " + str(min_length) + " to " + str(max_length))
    print("Score lower quartile: " + str(s_low) + " and upper quartile: " + str(s_up))
    print("Length lower quartile: " + str(l_low) + " and upper quartile: " + str(l_up))
    print("Score standard deviation: " + str(s_std))
    print("Length standard deviation: " + str(l_std))



if __name__ == '__main__':
    main()
  # data_analysis()
