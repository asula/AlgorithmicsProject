# Marit Asula

from collections import defaultdict
from random import randint
from random import random
from math import sqrt


#Generates random graph with given size and edge probability
def generate_random_graph(size,edge_probability):

    graph = defaultdict(list)
    for i in range(1,size+1):
        for j in range(1,size+1):
            r = random()
            if r <=p:
                graph[i].append(j)
                graph[j].append(i)
    return graph

# Generates grid graph given the length of one side
def generate_square_graph(side):
    
    size = side**2
    graph = defaultdict(list)
    for i in range(1,size+1):
        if i%side != 0:
            graph[i].append(i+1)
            graph[i+1].append(i)
            
        if i <= size - side:
            graph[i].append(i+side)
            graph[i+side].append(i)
    return graph
                                   

# Simulation of one person moving and the other one staying put
# in a given graph
def random_walk_one(graph):
    
    size = len(graph)
    
    person_1_pos = randint(1,size)
    person_2_pos = randint(1,size)

    traversed = 0
    while person_1_pos != person_2_pos:
        neighbours = graph[person_2_pos]
        r = randint(0,len(neighbours)-1)
        person_2_pos = graph[person_2_pos][r]
        traversed +=1
    return traversed

# Simulates the next best step when moving towards a certain place
def move_towards_place(current_place,destination_place,graph):
    size = len(graph)
    side = int(sqrt(size))

    if current_place == destination_place:
        new_pos = current_place

    elif destination_place in graph[current_place]:
        new_pos = destination_place
    elif is_on_the_same_line_vert(current_place,destination_place,graph):
            if destination_place > current_place:
                new_pos = current_place + side
            else:
                new_pos = current_place - side
            
    elif is_on_the_same_line_horz(current_place,destination_place,graph):
            if destination_place > current_place:
                new_pos = current_place +1
            else:
                new_pos = current_place -1
    
    else:
        if current_place%side != 0 and destination_place%side!= 0:
            if current_place%side < destination_place%side:
                new_pos = current_place + 1
            else:
                new_pos = current_place - 1
        
        elif current_place%side == 0:
            if current_place < destination_place:
                new_pos = current_place + side
            else:
                new_pos = current_place - side
                
        elif destination_place%side == 0:

            if current_place < destination_place:
                new_pos = current_place + 1
            else:
                new_pos = current_place - 1
        else:
            new_pos = -1

    return new_pos

# Controls if destination place is on the same vertical line
# with current place
def is_on_the_same_line_vert(current_place,destination_place,graph):
    size = len(graph)
    side = int(sqrt(size))

    if abs(current_place-destination_place)%side==0:
        return True
    else:
        return False
    
# Controls if destination place is on the same horizontal line
# with current place
def is_on_the_same_line_horz(current_place,destination_place,graph):
    
    size = len(graph)
    side = int(sqrt(size))
    row_indx = current_place%side
    
    if row_indx != 0:
        gap_start = current_place - row_indx +1
        gap_end = current_place + (side - row_indx)
    else:
        gap_start = current_place - side + 1
        gap_end = current_place
   
    if destination_place >= gap_start and destination_place <= gap_end :
        return True
    else:
        return False
       

# Chooses randomly one place from a list of given places
def choose_probable_place(probable_places):
    
    r = randint(0,len(probable_places)-1)
    place = probable_places[r]

    return place


# Simulates the situation where both persons are moving around
# Takes in following parameters (besides the graph itself):
# 1. visit_probable_places - a boolean, which shows if there exist
#    places where the persons would look beforehand
# 2. percentage (prob) - percentage of more probable places out of all
#    the places
# 3. walk_probability - probability that one of the persons moves each turn,
#    (the other one always moves), which helps to simulate different speeds
#    of the persons.
def random_walk_both(graph,visit_probable_places,prob,walk_prob):
    size = len(graph)

    person_1_pos = randint(1,size)
    person_2_pos = randint(1,size)

    if visit_probable_places:

        probable_places = set()
        while len(probable_places)< size*prob:
            r = randint(1,size)
            probable_places.add(r)
        probable_places = list(probable_places)

        r1 = randint(0,len(probable_places)-1)
        r2 = randint(0,len(probable_places)-1)

        place_1 = choose_probable_place(probable_places)
        place_2 = choose_probable_place(probable_places)

    
    traversed = 0
    while person_1_pos != person_2_pos:
        person_1_pos_old = person_1_pos
        person_2_pos_old = person_2_pos
        r = random()
        if visit_probable_places:
            if r <= walk_prob:
                person_1_pos = move_towards_place(person_1_pos,place_1,graph)
                
                if person_1_pos_old == person_1_pos:
                    place_1 = choose_probable_place(probable_places)
                
            person_2_pos = move_towards_place(person_2_pos,place_2,graph)
            if person_2_pos_old == person_2_pos:
                place_2 = choose_probable_place(probable_places)
            
            
        else:
            if r <= walk_prob:
                neighbours_p1 = graph[person_1_pos]
                r1 = randint(0,len(neighbours_p1)-1)
                person_1_pos = graph[person_1_pos][r1]

            neighbours_p2 = graph[person_2_pos]  
            r2 = randint(0,len(neighbours_p2)-1)
            person_2_pos = graph[person_2_pos][r2]
            
        traversed +=1
        
        #print str(traversed) + '. ', person_1_pos, person_2_pos
        if person_1_pos_old == person_2_pos and \
           person_2_pos_old == person_1_pos:
            break
    return traversed



def get_data(sizes,probabilities,iters):
    gtype = 'random'
    path = 'C:\\Users\\Marit\\Desktop\\gdata_'+str(iters)+'_'+str(gtype)+'.txt'
    f = open(path,'w')
    
    f.write('GRAPH_SIZE')
    f.write('\t')
    f.write('PROBABILITY')
    f.write('\t')
    f.write('ONE_WALKS')
    f.write('\t')
    f.write('BOTH_WALK')
    f.write('\t')
    f.write('ITERATIONS')
    f.write('\n')
    
    for probability in probabilities:
        for size in sizes:
            print probability, size
            
            sum_1 = 0
            sum_2 = 0
            graph = generate_graph(size,probability)
            for i in range(iters):
                sum_1+= random_walk_constant(graph)
                sum_2+= random_walk_both(graph)

            avg_1 = float(sum_1)/float(iters)
            avg_2 = float(sum_2)/float(iters)

            f.write(str(size))
            f.write('\t')
            f.write(str(probability))
            f.write('\t')
            f.write(str(avg_1))
            f.write('\t')
            f.write(str(avg_2))
            f.write('\t')
            f.write(str(iters))
            f.write('\n')
    f.close()   
    return

def get_data_square(wps,iters,side,p):
    gtype = 'square3'
    path = 'C:\\Users\\Marit\\Desktop\\gdata_'+str(iters)+'_SIDE_'+str(side)+'.txt'
    f = open(path,'w')
    
    f.write('WALK_PROBABILITY')
    f.write('\t')
    #f.write('ONE_WALKS')
    #f.write('\t')
    #f.write('BOTH_WALK_RAND_ALWAYS')
    #f.write('\t')
    f.write('BOTH_WALK_RAND_SOMETIMES')
    f.write('\t')
    #f.write('BOTH_WALK_PROB_ALWAYS')
    #f.write('\t')
    f.write('BOTH_WALK_PROB_SOMETIMES')
    f.write('\t')
    f.write('ITERATIONS')
    f.write('\n')
    graph = generate_square_graph(side)
    for wp in wps:
        print wp
 
        
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
  
        for i in range(iters):
            #sum3+= random_walk_both(graph,True,p,1)
            sum5+= random_walk_both(graph,True,p,wp)
            #sum1+= random_walk_constant(graph)
            #sum2+= random_walk_both(graph,False,0,1)  
            sum4+= random_walk_both(graph,False,0,wp)

        #avg1 = float(sum1)/float(iters)
        #avg2 = float(sum2)/float(iters)
        #avg3 = float(sum3)/float(iters)
        avg4 = float(sum4)/float(iters)
        avg5 = float(sum5)/float(iters)
        
        size = side**2
        f.write(str(wp))
        f.write('\t')
        '''f.write(str(avg1))
        f.write('\t')
        f.write(str(avg2))
        f.write('\t')'''
        f.write(str(avg4))
        f.write('\t')
        #f.write(str(avg3))
        #f.write('\t')
        f.write(str(avg5))
        f.write('\t')
        f.write(str(iters))
        f.write('\n')

    f.close()   
    return
    

sizes = [1000,2000,5000,10000]
probabilities = [0.5,0.6,0.7,0.8,0.9,1]
iters = 100
sides = [20,40,80,160,320]
walk_probabilities = [0.2,0.4,0.7,0.9,1]
ppp= [0.01,0.05,0.1,0.2,0.4,]


wp = 0.7
#p = 0.1

#get_data_square(walk_probabilities,iters,160,p)

# AlgorithmicsProject 
