from classes import Gate

def take_input(gates , file):

    while True:
        line = file.readline().strip()  # Read first line and remove extra spaces        
        if not line:
            break
        # if line1[0]== "w":  # Break if no more lines (reached end of file)
        #     connections.new_connection(line1)
        #     if line2:
        #         connections.new_connection(line2)

        if line[0]== "g":
            gates.append(Gate(line , file.readline().strip()))

        elif line[0:10]== "wire_delay":  # Break if no more lines (reached end of file)
            wire_delay = int(line[11:])

        else:
            l = line.split(" ")
            out = l[1].split(".")
            out_gate = int(out[0][1:])
            out_pin = int(out[1][1:])

            input = l[2].split(".")
            input_gate = int(input[0][1:])
            input_pin = int(input[1][1:])

            gates[out_gate-1].out.append((out_pin, (input_gate , input_pin)))
            gates[input_gate-1].has_primary_input = False
            gates[input_gate-1].input_pins.append(input_pin)
    return wire_delay

def move_ahead(current_gate , paths, current_path,gates):
    last = current_gate.is_last_gate
    if last:
        current_path.append((current_gate.id , current_gate.primary_pin.pin_id))
        paths.append(current_path)
        return
    else:
        for data in current_gate.out :
            new = current_path.copy()
            new.append((current_gate.id , data[0]))
            new.append(data[1])
            move_ahead(current_path=new, current_gate = 
                       gates[data[1][0]-1] , gates= gates, paths=paths)

def make_connections(paths):
    gates_used_till_now=[]
    basline = {}
    temp = []
    latest_key = 0
    for gp in paths[0][0::2]:
        gates_used_till_now.append(gp[0])
        basline[gp[0]] = []

    for path in paths[1:] :
        for gp in path:
            if gp[0] not in gates_used_till_now:
                gates_used_till_now.append(gp[0])
                temp.append(gp[0])
            elif gp[0] in basline:
                if temp:
                    temp.reverse()
                    basline[gp[0]].append(temp)
                    temp = []
                latest_key = gp[0]
            else:
                for key in basline:
                    if gp[0] in basline[key]:
                        if temp:
                            temp.reverse()
                            basline[key].append(temp)
                            temp = []
                        latest_key = key
        if temp:
            # temp.reverse()
            # print(latest_key)
            basline[latest_key].append(temp)
            temp = []
    return basline

def horizonal_placement(list_of_gates_id, dict_of_gates):
    coord_dict = {}
    first_gate_id = list_of_gates_id[0]
    coord_dict[first_gate_id] = (0,0)
    temp = (dict_of_gates[first_gate_id].width , dict_of_gates[first_gate_id].height)
    for gate_id in list_of_gates_id[1:]:
        for_minus =    (0,dict_of_gates[gate_id].height)
        coordinate = tuple (a - b for a,b in zip(temp, for_minus))
        coord_dict[gate_id] = coordinate
        for_plus = (dict_of_gates[gate_id].width , 0 )
        temp = tuple (a + b for a,b in zip(temp,for_plus))
    return coord_dict
    pass

def verticle_up_placement(list_of_gates_id , dict_of_gates):
    
    coord_dict = {}
    first_gate_id = list_of_gates_id[0]
    coord_dict[first_gate_id] = (0,0)
    temp = (dict_of_gates[first_gate_id].width , dict_of_gates[first_gate_id].height)
    for gate_id in list_of_gates_id[1:]:
        for_minus =    (dict_of_gates[gate_id].width,0)
        # print("for minnus",for_minus)
        # print("temp", temp)
        coordinate = tuple (a - b for a,b in zip(temp, for_minus))
        a = (0, coordinate[1])
        coord_dict[gate_id] = a
        for_plus = (0, dict_of_gates[gate_id].height )
        temp = tuple (a + b for a,b in zip(temp,for_plus))
    return coord_dict    

def verticle_down_placement(list_of_gates_id , dict_of_gates):
    
    coord_dict = {}
    first_gate_id = list_of_gates_id[0]
    coord_dict[first_gate_id] = (0,0)
    temp = (dict_of_gates[first_gate_id].width , 0)
    for gate_id in list_of_gates_id[1:]:
        for_minus =    (dict_of_gates[gate_id].width,dict_of_gates[gate_id].height)
        # print("for minnus",for_minus)
        # print("temp", temp)
        coordinate = tuple (a - b for a,b in zip(temp, for_minus))
        a = (0, coordinate[1])
        coord_dict[gate_id] = a
        for_minus_in_temp = (0, dict_of_gates[gate_id].height )
        temp = tuple (a - b for a,b in zip(temp,for_minus_in_temp))
    return coord_dict  

def normalise_coordinate(dict_of_coord, dict_of_gates):
    min_x = 0
    min_y = 0
    first_key = next(iter(dict_of_coord))
    max_x = dict_of_gates[first_key].width
    max_y = dict_of_gates[first_key].height
    for key in dict_of_coord:
        temp_x = dict_of_coord[key][0]+ dict_of_gates[key].width
        temp_y = dict_of_coord[key][1]+ dict_of_gates[key].height
        if temp_x > max_x:
            max_x = temp_x
        if temp_y > max_y:
            max_y = temp_y
        if dict_of_coord[key][0]<min_x:

            min_x = dict_of_coord[key][0]
        if dict_of_coord[key][1]<min_y:
            min_y =  dict_of_coord[key][1]
        
    if min_x <0 or min_y < 0:

        shift = (0-min_x,0-min_y)
        for key in dict_of_coord:
          dict_of_coord[key]  = tuple (a + b for a,b in zip(dict_of_coord[key],shift))
    
    return (max_x - min_x, max_y - min_y)

def divide_in_two(list_of_list_of_gates_id):
    upper_list =[]
    lower_list = []
    for list_of_gate_id in list_of_list_of_gates_id[0::2]:
        upper_list.append(list_of_gate_id)
    for list_of_gate_id in list_of_list_of_gates_id[1::2]:
        lower_list.append(list_of_gate_id)  
    return (lower_list,upper_list)

def shift_from_gate(gate_id, baseline_coord_dict,shift):
    bool_shift = False
    for gate_key in baseline_coord_dict:
        if bool_shift:
            baseline_coord_dict[gate_key] = tuple (a + b for a,b in zip(baseline_coord_dict[gate_key],shift))
        if gate_key == gate_id:
            bool_shift = True

def answer_calculation_of_path(ans_coordinates,paths,dict_of_gates,wire_delay):
    delay = 0
    path_index = 0
    for i in range(len(paths)):
        current_path_gates = []
        current_gate_delay = 0
        current_wire_length = 0
        
        for gp in paths[i][0::2]:
            current_path_gates.append(gp[0])
        for gates in current_path_gates:
            current_gate_delay += dict_of_gates[gates].delay

        for j in range(1,len(paths[i])-1,2):
            gp1 = paths[i][j]
            gp2 = paths[i][j+1]
            g1_coord = ans_coordinates[gp1[0]]
            g2_coord = ans_coordinates[gp2[0]]
            pin_coord_wrt_g1 = (dict_of_gates[gp1[0]].pins[gp1[1]-1].x,dict_of_gates[gp1[0]].pins[gp1[1]-1].y)
            pin_coord_wrt_g2 = (dict_of_gates[gp2[0]].pins[gp2[1]-1].x,dict_of_gates[gp2[0]].pins[gp2[1]-1].y)
            temp = tuple (a + b - c- d for a,b,c,d in zip(g2_coord, pin_coord_wrt_g2, g1_coord, pin_coord_wrt_g1))
            current_wire_length += sum(abs(x) for x in temp)
        current_delay = current_gate_delay + wire_delay * current_wire_length
        if current_delay > delay:
            path_index = i
            delay = current_delay

    return (path_index , delay)

def print_answer(final_x_y, path, critical_path_delay, ans_dict ):
    keys = list(ans_dict.keys())
    keys.sort()

    print("bounding_box", final_x_y[0], final_x_y[1])
    print("critical_path", end = " ")
    for gp in path:
        print(f"g{gp[0]}.p{gp[1]}", end =" ")
    print()
    print("critical_path_delay",critical_path_delay )
    for key in keys:
        print(f"g{key} {ans_dict[key][0]} {ans_dict[key][1]}")
    pass






