# from visualize_gates import draw_gate_packing
"""
Create dictionary for the gate dimensions (gate_dimensions) and
gates coordinates (gates)
"""

def read_gate_dimensions (list_of_gates):
        gate_dimensions = {}
        for class_gate in list_of_gates:
            gate_dimensions[class_gate.gate]= (class_gate.width,class_gate.height)
        
        gates_list=list(gate_dimensions.items())
        widthlist = sorted(gates_list, key=lambda x: x[1][0], reverse=True)  # Returns a new sorted list
        max_width=widthlist[0][1][0]

        lengthlist = sorted(gates_list, key=lambda x: x[1][1], reverse=True)  # Returns a new sorted list
        max_length=lengthlist[0][1][1]

        widthSame_list=[]
        i=0
        j=-1
        width=[]
        while i<(len(widthlist)-1):
            check=0
            while widthlist[i][1][0]==widthlist[i+1][1][0]:
                if check==0:
                    widthSame_list.append([])
                    width.append(widthlist[i][1][0])
                    j+=1
                    widthSame_list[j].append(widthlist[i])
                check=1
                widthSame_list[j].append(widthlist[i+1])
                i+=1
                if (i>=(len(widthlist)-1)):
                    break
            i+=1
        i=0
        while i<len(widthlist):
            if widthlist[i][1][0] in width:
                widthlist.remove(widthlist[i])
                i-=1
            i+=1
        lengthlist = sorted(widthlist, key=lambda x: x[1][1], reverse=True)  # Returns a new sorted list
        lengthSame_list=[]
        i=0
        j=-1
        length=[]
        while i<(len(lengthlist)-1):
            check=0
            while lengthlist[i][1][1]==lengthlist[i+1][1][1]:
                if check==0:
                    lengthSame_list.append([])
                    length.append(lengthlist[i][1][1])
                    j+=1
                    lengthSame_list[j].append(lengthlist[i])
                check=1
                lengthSame_list[j].append(lengthlist[i+1])
                i+=1
                if (i>=(len(lengthlist)-1)):
                    break
            i+=1
        i=0
        while i<len(lengthlist):
            if lengthlist[i][1][1] in length:
                lengthlist.remove(lengthlist[i])
                i-=1
            i+=1
    
        m = 0
        while m < len(widthSame_list):
            
            subLength_sum = 0
            n = 0
            subWidth_sum = widthSame_list[m][0][1][0]  
            
            while n < len(widthSame_list[m]):
               
               gate=widthSame_list[m][n][0]
               subLength_sum = 0
               l=["Yadd"]

               while subLength_sum <=max_length  and n < len(widthSame_list[m]):
                 
                 l.append([widthSame_list[m][n][0],widthSame_list[m][n][1][1]])
                 subLength_sum += widthSame_list[m][n][1][1]
                 if subLength_sum > max_length:
                    subLength_sum-= widthSame_list[m][n][1][1]
                    l.pop()
                    # print(l)
                    break
                 n += 1
               widthlist.append((gate,(subWidth_sum, subLength_sum),l))
            m += 1
        
        m = 0
        while m < len(lengthSame_list):
            
            subWidth_sum = 0
            n = 0
            subLength_sum = lengthSame_list[m][0][1][1]  
            
            while n < len(lengthSame_list[m]):
               
               gate=lengthSame_list[m][n][0]
               subWidth_sum = 0
               l=["Xadd"]

               while subWidth_sum <=max_width  and n < len(lengthSame_list[m]):
                 
                 l.append([lengthSame_list[m][n][0],lengthSame_list[m][n][1][0]])
                 subWidth_sum += lengthSame_list[m][n][1][0]
                 if subWidth_sum > max_width:
                    subWidth_sum-= lengthSame_list[m][n][1][0]
                    l.pop()
                    break
                 n += 1
               lengthlist.append((gate,(subWidth_sum, subLength_sum),l))
            m += 1
        

        for index_of_i,i in enumerate(lengthSame_list):
            for index_of_j,j in enumerate(lengthSame_list[index_of_i]):
                if lengthSame_list[index_of_i][index_of_j] in widthlist:
                    widthlist.remove(lengthSame_list[index_of_i][index_of_j])

        for index,i in enumerate(lengthlist):
            widthlist.append(lengthlist[index])
        
        lengthlist = sorted(widthlist, key=lambda x: x[1][1], reverse=True)

        widthlist = sorted(widthlist, key=lambda x: x[1][0], reverse=True)
        i=0
        unique_widthlist = []
        for item in widthlist:
          if item not in unique_widthlist:
            unique_widthlist.append(item)
        widthlist=unique_widthlist
        
        lengthlist = sorted(widthlist, key=lambda x: x[1][1], reverse=True)
        
        Final_Widthlist = sorted(widthlist, key=lambda x: x[1][0], reverse=True)
        Final_Lengthlist = sorted(lengthlist, key=lambda x: x[1][1], reverse=True)

        x,y=0,0
        l=int(len(Final_Lengthlist))
        BoundX=0
        BoundY=0
        listt=[]
        for i in range(l):
            if int(Final_Widthlist[0][1][0])<int(Final_Lengthlist[0][1][1]):
                
                rightMost=x+Final_Lengthlist[0][1][0]
                topMost=y+Final_Lengthlist[0][1][1]
                if rightMost>BoundX:
                    BoundX=rightMost
                if topMost>BoundY:
                    BoundY=topMost
                a=f"{Final_Lengthlist[0][0]} {x} {y}"
                listt.append(a)
               
                if len(Final_Lengthlist[0])>2:
                    
                    x1=x
                    y1=y
                    for i in range(1,(len(Final_Lengthlist[0][2])-1)):
                        if Final_Lengthlist[0][2][0]=="Xadd":
                          x1=x1+Final_Lengthlist[0][2][i][1]
                        elif Final_Lengthlist[0][2][0]=="Yadd":
                          y1=y1+Final_Lengthlist[0][2][i][1]
                        b=f"{Final_Lengthlist[0][2][i+1][0]} {x1} {y1}"
                        listt.append(b)
                x+=int(Final_Lengthlist[0][1][0])
                Final_Widthlist.remove(Final_Lengthlist[0])
                Final_Lengthlist.remove(Final_Lengthlist[0])
               

            else :
               
                rightMost=x+Final_Widthlist[0][1][0]
                topMost=y+Final_Widthlist[0][1][1]
                if rightMost>BoundX:
                    BoundX=rightMost
                if topMost>BoundY:
                    BoundY=topMost
                c=f"{Final_Widthlist[0][0]} {x} {y}"
                listt.append(c)
                
                if len(Final_Widthlist[0])>2:
                 
                 x1=x
                 y1=y
                 for i in range(1,(len(Final_Widthlist[0][2])-1)):
                        if Final_Widthlist[0][2][0]=="Xadd":
                          x1=x1+Final_Widthlist[0][2][i][1]
                        elif Final_Widthlist[0][2][0]=="Yadd":
                          y1=y1+Final_Widthlist[0][2][i][1]
                        d=f"{Final_Widthlist[0][2][i+1][0]} {x1} {y1}"
                        listt.append(d)
                y+=int(Final_Widthlist[0][1][1])
                Final_Lengthlist.remove(Final_Widthlist[0])
                Final_Widthlist.remove(Final_Widthlist[0])
                
        # print("bounding_box",BoundX,BoundY)
        dictionary={}
        for items in listt:
            item = [int(i) for i in items.split()]
            dictionary[item[0]] = (item[1], item[2])
        # print(dictionary)
        return BoundX,BoundY,dictionary



#Invoke the GUI for visualization
# read_gate_dimensions("dimensions_file.txt")
#root = draw_gate_packing(gate_dimensions, gates, (20,20))
#root.mainloop()