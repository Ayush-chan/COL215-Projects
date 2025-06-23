from function import verticle_down_placement,verticle_up_placement,normalise_coordinate

class Box:
     def __init__(self,dict_of_gates,list_of_gates_id,is_up) -> None:
            self.is_up = is_up
            if is_up:
                self.dict_of_coord = verticle_up_placement(list_of_gates_id, dict_of_gates )
            else:
                self.dict_of_coord = verticle_down_placement(list_of_gates_id,dict_of_gates)

            self.width , self.height = normalise_coordinate(self.dict_of_coord,dict_of_gates)
            self.x , self.y = (0,0)
    
     def shift_and_insert(self, ans_dict, shift):
          self.x, self.y = self.x + shift[0], self.y + shift[1]
          for gate_id in self.dict_of_coord:
               ans_dict[gate_id] = (self.dict_of_coord[gate_id][0]+self.x, self.dict_of_coord[gate_id][1]+self.y)

class BoxxedBox:
    def __init__(self) -> None:
          self.boxes = []
          self.width = 0
          self.height = 0
    def insert(self,box):
        self.boxes.append(box)
        if self.height <= self.width:
            if box.is_up:
                box.x , box.y = (0 , self.height)
            else:
                box.x , box.y = (0 , -self.height-box.height)
            self.height = self.height + box.height
            if box.width > self.width:
                self.width = box.width
                 
                 
        else:
            if box.is_up:
                box.x , box.y = ( self.width , 0)
            else:
                 box.x, box.y = (self.width, - box.height)
            self.width = self.width + box.width
            if box.height > self.height:
                  self.height = box.height

    def shift_and_append(self, ans_dic, shift):
         for box in self.boxes:
              box.shift_and_insert(ans_dic,shift)
    