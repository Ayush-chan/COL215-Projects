class Pin:
    def __init__(self,pin,x,y) -> None:
        self.pin = pin
        self.x = x
        self.y = y
        self.is_left = not x

class Gates:
    def __init__(self,line1,line2) :    
        str=line1.split(" ")
        self.gate=int(str[0][1:])
        self.width=int(str[1])
        self.height=int(str[2])
        self.pins=[]
        self.left_count = 0

        p=line2.split(" ")
        for i in range(1,(len(p)//2)):
            self.pins.append(Pin(i,int(p[2*i]),int(p[2*i+1])))
            self.left_count += 1 if not int(p[2*i]) else 0

        self.right_count = len(self.pins)- self.left_count

    def print_gate(self):
        print("gate",self.gate)
        print("height",self.height, "width", self.width)
        print("left", self.left_count," right  ", self.right_count)
        print()
        for pin in self.pins:
            print(pin.pin,"x", pin.x, "y", pin.y,"is_left", pin.is_left)
        print()
        print()

class Connections:
     def __init__(self) -> None:
         self.l=[]

     def new_connection(self,line):
         added = False
         l=line.split()
         p1 = l[1].split(".")
         p2 = l[2].split(".")
         pin1=(int(p1[0][1:]),int(p1[1][1:]))
         pin2=(int(p2[0][1:]),int(p2[1][1:]))
         for i in self.l:
            for pin in i:
                if (pin2==pin):
                    i.append(pin1)
                    added = True
                    break
                if (pin1==pin):
                    i.append(pin2)
                    added = True
                    break
         if not added:
             self.l.append([pin1,pin2])

     def print_connections(self):
         print(self.l)

     def cal_len_overall(self, dict, gates):
        length=0
        for connected_pins in self.l:
            min_x = gates[connected_pins[0][0]-1].pins[connected_pins[0][1]-1].x + dict[gates[connected_pins[0][0]-1].gate][0]
            min_y = gates[connected_pins[0][0]-1].pins[connected_pins[0][1]-1].y + dict[gates[connected_pins[0][0]-1].gate][1]
            max_x = min_x
            max_y = min_y
            
            for pin in connected_pins:
                x = gates[pin[0]-1].pins[pin[1]-1].x + dict[gates[pin[0]-1].gate][0]
                y = gates[pin[0]-1].pins[pin[1]-1].y + dict[gates[pin[0]-1].gate][1]
                min_x = min(min_x,x)
                max_x = max(max_x,x)
                min_y = min(min_y,y)
                max_y = max(max_y,y)
            length += (max_y - min_y) + (max_x - min_x)
        # print("wire_length",length)

        return length
class Clubed_gates:
    def __init__(self,width,height,dictionary,i) -> None:
        self.clubed_coordinates=dictionary
        self.width=width
        self.height=height
        self.gate=i
    
    def print_info(self):
        print("width",self.width, "height", self.height,"clubed_coordinates",self.clubed_coordinates, "gate",self.gate)
    

