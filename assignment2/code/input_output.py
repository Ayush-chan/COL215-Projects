from classes import Gates,Connections,Clubed_gates
from assignment1 import read_gate_dimensions

with open('dimensions_file.txt', 'r') as file:
    gates=[]
    connections=Connections()
    while True:
        line1 = file.readline().strip()  # Read first line and remove extra spaces
        line2 = file.readline().strip()  # Read second line and remove extra spaces
        
        if not line1:
            break
        if line1[0]== "w":  # Break if no more lines (reached end of file)
            connections.new_connection(line1)
            if line2:
                connections.new_connection(line2)

        if line1[0]=="g":
            gates.append(Gates(line1,line2))

    same_wire_gates=[]
    gates_map_id={}
    clubed_gate_list=[]
    for gate in gates:
        gates_map_id[gate.gate]=gate
    i=0
    connections.l.sort(key=len,reverse=True)
    for same_wire_connection in connections.l:
        for gate_pin_tpl in same_wire_connection:
            if gate_pin_tpl[0] in gates_map_id:
                same_wire_gates.append(gates_map_id[gate_pin_tpl[0]])
                gates_map_id.pop(gate_pin_tpl[0])
        if len(same_wire_gates):
            i+=1
            # print("same_wire_gates", same_wire_gates)
            width,height,dict_coordinates = read_gate_dimensions(same_wire_gates)
            clubed_gate_list.append(Clubed_gates(width,height,dict_coordinates,i))
            # print(width,height,dict_coordinates)
        same_wire_gates = []
    boundX,boundY,coord_of_dabba = read_gate_dimensions(clubed_gate_list)
    # print("bounding_box",boundX,boundY)

    final_dict={}
    for fake_id in coord_of_dabba:
        origin_of_dabba = coord_of_dabba[fake_id]
        list_of_cord_inside_dabba = clubed_gate_list[fake_id-1].clubed_coordinates
        # print(list_of_cord_inside_dabba)
        for key, value in list_of_cord_inside_dabba.items():
            final_coordinate = tuple(a + b for a, b in zip(origin_of_dabba, value))
            x,y =final_coordinate
            final_dict[key] = final_coordinate
            # print(f"g{key} {x} {y}")
    # print("final dict 1st",final_dict)
    wire_length1=connections.cal_len_overall(final_dict,gates)
    # print("next code")
    total_width,total_length,final_dict2=read_gate_dimensions(gates)
    # print(total_width,total_length,final_dict2)
    wire_length2 = connections.cal_len_overall(final_dict2,gates)
    # print(wire_length1,wire_length2)
    if wire_length1<wire_length2:
        # print("if condition")
        print("bounding_box",boundX,boundY)
        # print("final_dict",final_dict)
        for key, value in final_dict.items():
            x,y=value
            print(f"g{key} {x} {y} ")
        print("wire_length",wire_length1)
    else:
        print("bounding_box",total_width,total_length)
        for key, value in final_dict2.items():
            x,y=final_dict[key]
            print(f"g{key} {x} {y} ") 
        print("wire_length",wire_length2)      

