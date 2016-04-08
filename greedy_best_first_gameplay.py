from optparse import OptionParser

enemy = []
nextstate=5*[5*[0]]
    
def getinput():

    linecount=1
    
    parser = OptionParser()
    parser.add_option("-i",action="store",type="string",dest="input", help="Specify input file")
    (options, args) = parser.parse_args()

    #print(options.input)
    filename = options.input
    
    fobj = open(filename,'r')
    
    option = fobj.readline()
    linecount+=1

    if option[0]=="4":
        exit(0)
        
    player = fobj.readline()
    linecount+=1

    depth = fobj.readline()
    linecount+=1

    points=5*[5*[0]]
    line1= fobj.readline()
    points[0]=line1.split()
    linecount+=1
    line1= fobj.readline()
    points[1]=line1.split()
    linecount+=1
    line1= fobj.readline()
    points[2]=line1.split()
    linecount+=1
    line1= fobj.readline()
    points[3]=line1.split()
    linecount+=1
    line1= fobj.readline()
    points[4]=line1.split()
    linecount+=1
    
    curstate=5*[5*[0]]
    curstate[0]= fobj.readline()
    linecount+=1
    curstate[1]= fobj.readline()
    linecount+=1
    curstate[2]= fobj.readline()
    linecount+=1
    curstate[3]= fobj.readline()
    linecount+=1
    curstate[4]= fobj.readline()
    linecount+=1


    print(option)
    print(player)
    print(depth)
    print(points[0])
    print(points[1])
    print(points[2])
    print(points[3])
    print(points[4])
    
    print(curstate[0])
    print(curstate[1])
    print(curstate[2])
    print(curstate[3])
    print(curstate[4])
    
    greedy(player,depth,points,curstate)

def greedy(player,depth,points,curstate):
    validraid = []
    
    print("Applying Greedy Best First Search.......")
    print(player)

    print len(player)
    #doesnt work
    player.strip('\n')

    player1 = player
    
    if player[0] == "X":
        player1 = "O"
        print("---Player X")
    elif player[0] == "O":
        player1 = "X"

    i=0
    j=-1
    score = 0
    validraid.append((0,[0,0]))

    for line in curstate:
        for pos in line:
            j+=1
            if pos == player[0]:
                print "validraid now column ",i,j,validraid
                #print(pos)
                print "open pos left",i,",",j-1
                if j-1>=0 and curstate[i][j-1] == "*":
                    score = int(points[i][j-1])
                    score+= checkenemy(player,player1,i,j-1,points,curstate)
                    print "below", score
                    print "left validraid",validraid
                    if score > int(validraid[0][0]):
                        print "new score added"
                        del validraid[:]
                        validraid.append((score,[i,j-1],enemy))
                        print "validraid1",validraid
                        
                print "open pos right",i,",",j+1 
                if j+1>=0 and j+1<5 and curstate[i][j+1] == "*":
                    score = int(points[i][j+1])
                    score+= checkenemy(player,player1,i,j+1,points,curstate)
                    print "below", score
                    print "right validraid",validraid
                    if score > int(validraid[0][0]):
                        print "new score added"
                        del validraid[:]
                        validraid.append((score,[i,j+1],enemy))
                        print "validraid2",validraid
                        
                print "open pos top",i-1,",",j
                if i-1>=0 and curstate[i-1][j] == "*":
                    score = int(points[i-1][j])
                    score+= checkenemy(player,player1,i-1,j,points,curstate)
                    print "below", score
                    print "top validraid",validraid
                    if score > int(validraid[0][0]):
                        print "new score added"
                        del validraid[:]
                        validraid.append((score,[i-1,j],enemy))
                        print "validraid3",validraid
                                           
                print "open pos below",i+1,",",j
                if i+1>=0 and i+1<5 and curstate[i+1][j] == "*":
                    score = int(points[i+1][j])
                    score+= checkenemy(player,player1,i+1,j,points,curstate)
                    print "below", score
                    print "before validraid",validraid
                    if score > int(validraid[0][0]):
                        print "new score added"
                        del validraid[:]
                        validraid.append((score,[i+1,j],enemy))
                        print "validraid4",validraid
                        
            #j+=1
            #print "validraid now column ",i,j-1,validraid
        
        print(line)
        j=0
        i+=1
        print "validraid",validraid

    print "validraid",validraid
    #print "raid max",max(validraid[0],key=int)

 

    i=0

    maxval=[]
    if curstate[0][0]=="*":
        maxval.append((points[0][0],[0,0]))
    elif curstate[0][1]=="*":
        maxval.append((points[0][1],[0,1]))

    print "maxval initial",maxval
    
    for line in curstate:
        j = 0
        for pos in line:
            if curstate[i][j]=="*":
                print "checking for pts at i,j",points[i][j],i,j
                if int(maxval[0][0])< int(points[i][j]):
                    del maxval[:]
                    maxval.append((points[i][j],[i,j]))
                    print "maxval updated",maxval
            j+=1
        i+=1

    print "maxval",maxval
    validsneak = maxval

    '''
    validsneak = []
    validsneak.append((max(points[0],key=int),[0,points[0].index(max(points[0],key=int))]))

    if max(points[1],key=int) > validsneak[0][0]:
        del validsneak[0]
        validsneak.append((max(points[1],key=int),[1,points[1].index(max(points[1],key=int))]))
    if max(points[2],key=int) > validsneak[0][0]:
        del validsneak[0]
        validsneak.append((max(points[2],key=int),[2,points[2].index(max(points[2],key=int))]))
    if max(points[3],key=int) > validsneak[0][0]:
        del validsneak[0]
        validsneak.append((max(points[3],key=int),[3,points[3].index(max(points[3],key=int))]))
    if max(points[4],key=int) > validsneak[0][0]:
        del validsneak[0]
        validsneak.append((max(points[4],key=int),[4,points[4].index(max(points[4],key=int))]))

    print "sneak max", validsneak
    '''

    for i in range(5):
        curstate[i]=curstate[i].strip('\r\n')

    print curstate

    nextstate=outputfile(player,player1,curstate,validsneak,validraid)
    print nextstate

        
    fileobj = open("next_state.txt",'w')

    i=0
    for line in nextstate:
        fileobj.write(str(nextstate[i]))
        fileobj.write("\n")
        i+=1
    
def outputfile(player,player1,curstate,validsneak,validraid):


    #print validsneak[0][1][0]
    if int(validsneak[0][0]) > validraid[0][0]:
        x=validsneak[0][1][0]
        y=validsneak[0][1][1]
        print "Sneak x,y",x,y
        count=0
        temp=[]
        for each_string in curstate:
            ls=list(each_string)
            if count==x:
                ls[y]=player[0]
                each_string=''.join(ls)
            temp.append(each_string)    
            count=count+1
        print temp    
    
    else:
        print "validraid",validraid
        print "len of validraid",len(validraid[0][2])
        print "len of validraid[0][2][0]",validraid[0]
        temp=[]

        x=validraid[0][1][0]
        y=validraid[0][1][1]

        if len(validraid[0][2])>=0:
            count=0
            temp=[]
            for each_string in curstate:
                ls=list(each_string)
                if count==x:
                    ls[y]=player[0]
                    each_string=''.join(ls)
                temp.append(each_string)    
                count=count+1
            print "tmep",temp
        
        if len(validraid[0][2])>=1:
            x=validraid[0][2][0][0]
            y=validraid[0][2][0][1]
            count=0
            temp1=[]
            for each_string in temp:
                ls=list(each_string)
                if count==x:
                    ls[y]=player[0]
                    each_string=''.join(ls)
                temp1.append(each_string)    
                count=count+1
            print temp1
            temp=temp1
        
        
    return temp       

    '''for i in range(5):
        for j in range(5):
            nextstate[i][j]=curstate[i][j]
            if i==x and j==y:
                nextstate[x][y]="X"
                
            print nextstate[i][j]
        print
        print nextstate[i]
    print

    print len(curstate)
    print len(nextstate)
    print nextstate
    '''
def checkenemy(player,player1,i,j,points,curstate):
    #print "i",i,"j",j
    pts=0
    del enemy[:] 
    if j-1>=0 and curstate[i][j-1] == player1[0]:
        pts+=int(points[i][j-1])
        enemy.append([i,j-1])
    if j+1>=0 and j+1<5 and curstate[i][j+1] == player1[0]:
        pts+=int(points[i][j+1])
        enemy.append([i,j+1])
    if i-1>=0 and curstate[i-1][j] == player1[0]:
        pts+=int(points[i-1][j])
        enemy.append([i-1,j])
    if i+1>=0 and i+1<5 and curstate[i+1][j] == player1[0]:
        pts+=int(points[i+1][j])
        enemy.append([i+1,j])
    
    print "check enemy around ",i,j,enemy
    print "points to be conquered",pts
    return pts
    #print "enemy conquered at",i,j

            
if __name__ == '__main__':
    getinput()

