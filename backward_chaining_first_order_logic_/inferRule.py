import inferParameter as param
import inferfunc as util
import copy

FIRSTTIME=0

class Predicate:
    id=1
    def __init__(self):
        self.name = ''
        self.pid = Predicate.id
        Predicate.id = Predicate.id+1
        self.type = None
        self.argsList = None
        self.argsCount = None
        self.premiseObjs = []
        self.premiseCount = 0

    def printPredicate(self):
        i = 1
        pre_str = ''
        for pobj in self.premiseObjs:
            pre_str = pre_str + pobj.printPredicate()
        if self.type == param.PREDICATE_TYPE['CLAUSE']:
            pre_str += '=>' 
        pre_str+= self.name+'(' + str(self.argsList) + ')'
        return pre_str
      
    def printdashes(self):
        i = 1
        pre_str = ''
        for pobj in self.premiseObjs:
            pre_str = pre_str + pobj.printdashes()
        if self.type == param.PREDICATE_TYPE['CLAUSE']:
            pre_str += '=>' 
        new_args=copy.deepcopy(self.argsList)
        i=0
        for each in new_args:
            if new_args[i].islower():
                new_args[i]='_'
            i+=1
        pre_str+= self.name+'(' + str(new_args) + ')'
        return pre_str

class Query:
    def __init__(self, rule):
        self.pobj = util.get_pred_object(rule, param.PREDICATE_TYPE['QUERY'])

    def infer(self):
        
        
        theta = {}
        print 'infer called with pobj.name is',self.pobj.name
        theta['_status'] = param.VALID_RULE
        print 'theta',theta
        print '\n\ninfer calls OR\n'

        theta_list = logic_OR(self.pobj, theta, {})
        print '\nOR returns to infer\n\n'
        
        print 'theta list:',theta_list
        result = param.INVALID_RULE
        for t in theta_list:
            if t['_status']==param.VALID_RULE:
                return 'True\n'
        return 'False\n'

def logic_OR(pobj, theta, ruleids):
    
    print "\n\n----- start FOL_BC_OR-----\n"
    #1 Get the rule list
    ruleList = Search_Rule(pobj.name, pobj.argsCount)

    returnList = []
    i=1
    for rule in ruleList:
        print '\nNEXT ITERATION\n'
        i+=1
        global FIRSTTIME
        '''
        if i > 2 and lastval=='FALSE':
            strword1=rule.printPredicate()
            strword1=strword1.split("=>")
            strword1=strword1[len(strword1)-1]
            origrhs=strword1

            strword1="Ask1: "+strword1+"\n"
            strword1=strword1.replace("[","")
            strword1=strword1.replace("]","")
            strword1=strword1.replace("'","")
                        

            fptr=open('output.txt','a')
            fptr.write(strword1)
            fptr.close()

            lastval='TRUE'
        '''

        print '\ni',i
        print 'rule',rule.printPredicate()
        print 'theta',theta
        inner_theta = copy.deepcopy(theta)
        inner_ruleids = copy.deepcopy(ruleids)
        arg_goal = str(pobj.argsList)
        if rule.pid in inner_ruleids:
            if arg_goal in inner_ruleids[rule.pid]:
                print 'Loop Detected'
                exit(0)
                continue
            else:
                inner_ruleids[rule.pid].append(arg_goal)    
        else:
            inner_ruleids[rule.pid] = [arg_goal]
        #standardize theta
        print 'inner-ruleids',inner_ruleids
        print 'inner-theta before std:', inner_theta
        rule, inner_theta = Standardize(rule, inner_theta)
        print 'inner-theta after std:', inner_theta
        print 'rule.argsList',rule.argsList
        print 'pobj.argsList',pobj.argsList
        print 'returnList',returnList


        if FIRSTTIME==0:
            fptr=open('output.txt','a')
            if rule.argsList == pobj.argsList:
                strword1=pobj.printdashes()
            else:
                strword1=pobj.printPredicate()    
            
            strword1=strword1.replace("[","")
            strword1=strword1.replace("]","")
            strword1=strword1.replace("'","")
            fptr.write("Ask: "+strword1+"\n")
            fptr.close()
            FIRSTTIME=1
        
        #print 'Rule after std:',rule.printPredicate()
        #unify will modify inner_theta
        print '\n\n************* internal call from OR to AND ***********\n'
        
        returnList.extend(logic_AND(rule.premiseObjs, Unify(rule.argsList, pobj.argsList, inner_theta), inner_ruleids))

        print '\n********* return internal call from AND to OR **********\n\n'
        
        print 'inner-theta after std:', inner_theta
        print 'rule.argsList',rule.argsList
        print 'pobj.argsList',pobj.argsList
        print 'inner_ruleids',inner_ruleids
        print 'returnList',returnList


        #strword1="True: "+rule.printPredicate()+"\n"
        

        strword1=rule.printPredicate()
        #keep only R.h.s.

        if len(returnList) is 1:
            strword1=rule.printPredicate()
            rule2 = Substitute(rule,returnList[0])
            rule2 = Substitute(rule2,returnList[0])
            strword1=rule2.printPredicate()
            strword1=strword1.split("=>")
            strword1=strword1[len(strword1)-1]
            origrhs=strword1

            strword1="True: "+strword1+"\n"
            strword1=strword1.replace("[","")
            strword1=strword1.replace("]","")
            strword1=strword1.replace("'","")
                        

            fptr=open('output.txt','a')
            fptr.write(strword1)
            fptr.close()

            global lastval
            lastval='TRUE'
            print '\n\n\n##### True statement to file #####with i',i,'\n',strword1

        elif inner_theta['_status']==param.INVALID_RULE:
            strword1=rule.printPredicate()
            strword1=strword1.split("(")
            strword1=strword1[0]  
            strword1=strword1+"("+str(pobj.argsList)+")"
            #printing KB
            facts = __builtins__['KB'][param.PREDICATE_TYPE['FACT']]
            cc = __builtins__['KB'][param.PREDICATE_TYPE['CLAUSE']]
            print 'Fact List-->'
            for key in facts:
                flist = facts[key]
                for fobj in flist:
                    print fobj.printPredicate()

            print 'Inference Rule -->'
            for key in cc:
                flist = cc[key]
                for fobj in flist:
                    print fobj.printPredicate()

            #checking if fact is innknowledge base already
            facts = __builtins__['KB'][param.PREDICATE_TYPE['FACT']]
            #print 'Fact List-->'
            exists='FALSE'
            for key in facts:
                flist = facts[key]
                for fobj in flist:
                    if(strword1) == fobj.printPredicate():
                        exists='TRUE'
                        print 'strword1',strword1
                        print '\n\nexists' ,fobj.printPredicate()
            
            if exists is 'FALSE':
                strword1=strword1.split("=>")
                strword1=strword1[len(strword1)-1]
                origrhs=strword1

                #strword1=strword1.split("(")
                #strword1=strword1[0]  
                #"("+str(pobj.argsList)+")"+
                strword1="False: "+strword1+"\n"
                strword1=strword1.replace("[","")
                strword1=strword1.replace("]","")
                strword1=strword1.replace("'","")
                        

                fptr=open('output.txt','a')
                fptr.write(strword1)
                fptr.close()

                global lastval
                lastval='FALSE'
                print '\n\n\n##### False statement to file ##### with i',i,'\n',strword1

        #rule2 = Substitute(rule,returnList[0])
        #rule2 = Substitute(rule2,returnList[0])


        #print '\n\n rule2 ',rule2.printPredicate()
        '''
        strword1=rule.printPredicate()
        strword1=strword1.split("=>")
        strword1=strword1[len(strword1)-1]
        origrhs=strword1

        strword1="True: "+strword1+"\n"
        '''
        #replace any variables 
        #variable=strword1.replace("("," ")
        #variable=variable.replace(")"," ")
        '''
        word2=variable.split()
        word2=word2[len(word2)-1]
        word2=word2.replace("[","")
        word2=word2.replace("]","")
        word2=word2.replace("'","")
        '''
        #strword1="True: "+word2+"\n"
        '''
        for x in returnList:
            print '\n\nx\n',x
            for y in x:
                print '\n\n y ',y
                if word2 == y:
                    print '\n\nTrue\n'
                    subs=y
                    strword1="\nChange: "+subs+"\n"
        '''

        #stripping all unnecesary chars
        
        print 'inner_theta',inner_theta
        print 'Return list after selecting rule:', rule.printPredicate(), ' List: ',returnList
        #if inner_theta['_status'] == param.VALID_RULE:
        #   break

    print 'returnList',returnList
    print "\n-----FOL_BC_OR end-----\n\n"
    return returnList

def logic_AND(goals, theta, ruleids):
    '''
    '''
    print "\n\n----- start FOL_BC_AND-----\n"
    print 'In FOL_BC_AND with theta:',theta,'Goals', goals,'ruleids',ruleids

    if theta['_status']==param.INVALID_RULE:
        print '\n\n!!!!!! False:Invalid Rule'
        return []
    elif len(goals)==0:
        print 'len goals 0'
        return [theta]
    first, rest = goals[0], goals[1:]
    print 'first object before substitution',first.printPredicate()
    
    #replace=copy.deepcopy(first)

    '''
    replace = Substitute(first,theta)
    

    if replace is first:
        print 'replace object after substitution is the same',replace.printPredicate()
        change=1
    else:
        change=2
'''
    first = Substitute(first, theta)
    #printing to the file
    #print "````````````````````````````````````````````fileptr",Driver.fpptr
    #if (first.argsList[0]).islower():
     #   print 'replace object to file',first.printPredicate()
    strword="Ask: "+first.printdashes()+"\n"
    #else:
     #   strword="Ask: "+first.printPredicate()+"\n"


    strword=strword.replace("[","")
    strword=strword.replace("]","")
    strword=strword.replace("'","")


    fptr=open('output.txt','a')
    fptr.write(strword)
    fptr.close()

    print '\n\n\n##### Ask: statment to file #####\n',strword

    print 'first object after substitution',first.printPredicate()


    print '\n\n************ internal call from AND to OR ************\n'
    theta_d = logic_OR(first, theta, ruleids)
    print '\n************ return internal call from OR to AND  returns ************\n\n'
    print 'theta d',theta_d
    print 'theta',theta
    print 'ruleids',ruleids    

    '''
    if(len(theta_d)) is 0:

        fptr2=open('output.txt','r')
        
        #with open('output.txt,'r') as fptr2:
            
        while True:
            lastwrite=fptr2.readline()
            if not lastwrite: break
            #checking if line already exists in file
            strword="False: "+first.printPredicate()+"\n"
    
            strword=strword.replace("[","")
            strword=strword.replace("]","")
            strword=strword.replace("'","")

            if(lastwrite) == 
            print 'lastwrite is ',lastwrite

        
        #lastwrite=fptr2.readline()
        #print 'lastwrite is ',lastwrite
        cfptr2.close()

        strword="Ask1: "+first.printPredicate()+"\n"
    
        strword=strword.replace("[","")
        strword=strword.replace("]","")
        strword=strword.replace("'","")


        fptr=open('output.txt','a')
        fptr.write(strword)
        fptr.close()

        print '\n\n\n##### Ask1: statment to file #####\n',strword
    '''
    resultList = []
    for t in theta_d:
        print 't',t
        resultList.extend(logic_AND(rest, t, ruleids))

    print "\n----- FOL_BC_AND end-----\n\n"
    return resultList


def Substitute(pobj, theta):
    pobj_c = util.Clone_pobj(pobj)
    for i in range(len(pobj_c.argsList)):
        if pobj_c.argsList[i][0].islower() and theta[pobj_c.argsList[i]]:
            pobj_c.argsList[i] = theta[pobj_c.argsList[i]]
    return pobj_c

def Unify(rhs, goal, theta):
    print 'rhs:',rhs
    print 'goal',goal
    print 'theta', theta
    
    if theta['_status']==param.INVALID_RULE:
        print '\n\n.... UNify Fails... with '
        print 'rhs:',rhs
        print 'goal',goal
        print 'theta', theta
        return theta
    elif len(goal)==1:
        #print 'length 1 '
        if rhs[0]==goal[0]:
            return theta
        elif rhs[0][0].islower():  #rhs[0] is variable case 1
            return Unify_Var(rhs[0], goal[0], theta)
        elif goal[0][0].islower(): #goal[0] is variable and rhs[0] is constant case 2
            return Unify_Var(goal[0], rhs[0], theta)
        else:
            theta['_status'] = param.INVALID_RULE

            print '\n\n.... UNify Fails... with '
            print 'rhs:',rhs
            print 'goal',goal
            print 'theta', theta
            return theta
    else:
        t = Unify([rhs[0]], [goal[0]], theta)
        #print 'before unify list recursion rhs',rhs[1:],' - goal:',goal[1:]
        return Unify(rhs[1:], goal[1:], t)

def Unify_Var(var, prob_const, theta):
    
    if (var in theta.keys()) and theta[var]:

        return Unify([theta[var]], [prob_const], theta)
    elif (prob_const in theta.keys()) and theta[prob_const]:
        return Unify([var], [theta[prob_const]], theta)
    else:
        theta[var] = prob_const
        return theta


def Standardize(pobj, theta):
    
    if pobj.type==param.PREDICATE_TYPE['FACT']:
        return pobj, theta
    else:
        replaceMap = {}
        addMap = []
        pobj_c = util.Clone_pobj(pobj)
        chkList = [pobj_c]
        for elem in pobj_c.premiseObjs:
            chkList.append(elem)
        for elem in chkList:
            for i in range(elem.argsCount):
                if elem.argsList[i][0].isupper():
                    continue
                origvar = elem.argsList[i]
                var = origvar
                if origvar in theta:
                    unique = False
                    while not unique:
                        var = util.get_new_name(var)
                        if(len(var) > 26):
                            exit(0)
                        unique = var not in theta

                    elem.argsList[i] = var
                    if not var in addMap:
                        addMap.append(var)

                else:
                    addMap.append(origvar)

        for newv in addMap:
            theta[newv] = None
        return pobj_c, theta

def Search_Rule(name, argCount):
    ruleList = []
    print 'Searching rule with name:',name
    ruleList.extend(util.get_kb_list(param.PREDICATE_TYPE['FACT'], name, argCount))
    ruleList.extend(util.get_kb_list(param.PREDICATE_TYPE['CLAUSE'], name, argCount))
    print 'Searched Rules ruleList',ruleList
    return ruleList