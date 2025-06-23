

class Pin:
        def __init__(self,pin,x,y) -> None:
            self.pin_id = pin
            self.x = x
            self.y = y
            self.is_left = not x


class Gate:
    def __init__(self,line1,line2):
        str=line1.split(" ")
        self.id=int(str[0][1:])
        self.width=int(str[1])
        self.height=int(str[2])
        self.delay= int(str[3])
        self.pins=[]
        self.has_primary_input = True
        self.input_pins = [] #has all pin ids which takes input
        self.out = []  #has elements(pin id,(other gate id, other gate pin id))

        p=line2.split(" ")
        for i in range(1,(len(p)//2)):
            self.pins.append(Pin(i,int(p[2*i]),int(p[2*i+1])))
    
    def __str__(self):
        print("gate id",self.id)
        print("gate delay",self.delay)
        print("height",self.height, "width", self.width)
        for pin in self.pins:
            print(pin.pin_id,"x", pin.x, "y", pin.y,"is_left", pin.is_left)
        print("outputs are:", self.out)
        print("has primary input?",self.has_primary_input)
        print("gives output?",self.is_last_gate)
        print()
        return ""
    

    def check(self):
         #initiates is_last_gate and if primary, primary_pin
         self.is_last_gate = not len(self.out)
         if len(self.input_pins):
              self.has_primary_input == False
         if self.is_last_gate or self.has_primary_input:
            temp = self.input_pins
            for data in self.out:
                temp.append(data[0])
            for pin in self.pins:
                   if pin.pin_id not in temp:
                        self.primary_pin = pin
                        break


        

    
     

                      
     

