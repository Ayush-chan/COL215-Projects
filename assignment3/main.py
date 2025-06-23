from classes import Gate
from function import take_input , move_ahead , shift_from_gate, normalise_coordinate, print_answer
from function import make_connections, horizonal_placement, divide_in_two, answer_calculation_of_path
from boxes import BoxxedBox, Box

with open('my_tc1.txt', 'r') as file:
    gates=[Gate]*0
    wire_delay = take_input(gates , file)
        
##################################
for gate in gates:
    gate.check()
    # print(gate)
##################################
try:
    paths = []
    for gate in gates:
        if gate.has_primary_input:
            move_ahead(current_gate = gate, current_path= [(gate.id, gate.primary_pin.pin_id)], paths=paths, gates= gates)
except:
    print("Loop found, plz clarify doubt")
    quit()
paths.sort(key=lambda a:len(a),reverse = True)
# for i in paths:
#     print(i,"\n")


connections = make_connections(paths)
dict_of_gates = {}
for gate in gates:
    dict_of_gates[gate.id] = gate

baseline = []
for keys in connections:
    baseline.append(keys)

boxxed_boxes = {}
for gate_id in connections:
    if connections[gate_id]:
        boxxed_boxes[gate_id] = []
        upper_list, lower_list = divide_in_two(connections[gate_id])
        # print("lower list", lower_list, "upper_list", upper_list)
        lower_list.sort(key=lambda a:len(a),reverse = True)
        upper_list.sort(key=lambda a:len(a),reverse = True)
        lower_boxxed_boxes = BoxxedBox()
        if lower_list:
            for listt in lower_list:
                box = Box(dict_of_gates,listt,False)
                lower_boxxed_boxes.insert(box)
            boxxed_boxes[gate_id].append(lower_boxxed_boxes)
        upper_boxed_box = BoxxedBox()
        if upper_list:
            for listt in upper_list:
                box = Box(dict_of_gates,listt,True)
                upper_boxed_box.insert(box)
            boxxed_boxes[gate_id].append(upper_boxed_box)
         
baseline_coord_dict = (horizonal_placement(baseline,dict_of_gates))

for gate_key in boxxed_boxes:
    shift = 0
    shift1 = 0
    shift2 = 0
    if boxxed_boxes[gate_key]:
        if boxxed_boxes[gate_key][0].width > dict_of_gates[gate_key].width:
            shift1 = boxxed_boxes[gate_key][0].width - dict_of_gates[gate_key].width
    if len(boxxed_boxes[gate_key])-1:
        if boxxed_boxes[gate_key][1].width > dict_of_gates[gate_key].width:
            shift2 = boxxed_boxes[gate_key][1].width - dict_of_gates[gate_key].width   
    shift=max(shift1,shift2)
    if shift:
            shift_from_gate (gate_key, baseline_coord_dict, (shift,0))   

coordinate_of_boxxed_boxes ={}
for gate_key in boxxed_boxes:
    if boxxed_boxes[gate_key]:
        coordinate_of_boxxed_boxes[boxxed_boxes[gate_key][0]] = (baseline_coord_dict[gate_key][0],baseline_coord_dict[gate_key][1])
        if len(boxxed_boxes[gate_key])-1:
            coordinate_of_boxxed_boxes[boxxed_boxes[gate_key][1]] = (baseline_coord_dict[gate_key][0],baseline_coord_dict[gate_key][1]+dict_of_gates[gate_key].height)

ans_dict = baseline_coord_dict.copy()
for boxxed_box in coordinate_of_boxxed_boxes:
    boxxed_box.shift_and_append(ans_dict,coordinate_of_boxxed_boxes[boxxed_box])

final_x_y = normalise_coordinate(ans_dict,dict_of_gates)
# print("BB of ",final_x_y)


# print('solution coord\n',ans_dict)
path_index, critical_path_delay =(answer_calculation_of_path(ans_dict,paths,dict_of_gates, wire_delay))
# print(paths[path_index], critical_path_delay)


print_answer(final_x_y, paths[path_index], critical_path_delay, ans_dict )





