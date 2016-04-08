import string
import inferParameter as param
import inferRule as Rule
import copy

def isFact(rule):
    if rule.type == param.RULE_TYPE['FACT']:
        return True
    return False

def length(goalList):
    return len(goalList)

def get_pred_object(pred_repr, ptype):
    print "-----In get Predicate obj-----"
    print 'pred_repr', pred_repr
    print 'ptype', ptype
    pobj = Rule.Predicate()
    pobj.type = ptype
    #storing name of predicate
    p_rule = pred_repr.strip()
    p_rule = p_rule.split('(')
    print 'p_rule',p_rule
    pobj.name = p_rule[0]
    print 'pobj',pobj.name
    #storing argument/argument list for the predicate
    args = p_rule[1].split(')')[0]
    print 'args',args
    argsList = args.split(',')
    print 'argsList',argsList
    #returning a list of all arguments to be stored
    pobj.argsList = map(lambda v : v.strip(), argsList)
    pobj.argsCount = len(pobj.argsList)
    print 'mapped argsList',pobj.argsList

    if (ptype == param.PREDICATE_TYPE['CLAUSE']) or (ptype == param.PREDICATE_TYPE['FACT']):
        IndexObj(pobj, ptype)
    
    
    return pobj

def IndexObj(pobj, ptype):
    idxObj = __builtins__['KB']
    print 'before idxObj',idxObj
    if not idxObj[ptype].get(pobj.name, None):
        idxObj[ptype][pobj.name] = [pobj]
    else:
        idxObj[ptype][pobj.name].append(pobj)
    print 'after idxObj',idxObj
    
#searching all matching predicates
def get_kb_list(ptype, name, argCount):
    print 'in get_kb_list ptype is ',ptype,'with name',name,'and argcount',argCount 
    flist = __builtins__['KB'][ptype]
    #print 'flist',flist
    item_list = []
    if flist.get(name, None):
        for obj in flist[name]:
            if obj.argsCount == argCount:
                print 'obj found with name ',obj.name
                item_list.append(obj)
        print '**********item_list***************',item_list
        return item_list
        
    return []

def pop_premise_objList(premise_repr, cobj):
    # we need to fill the list of premise in conclusion object: cobj.premiseObjs
    print "-----In pop premise_objList----"
    print "cobj.type",cobj.type
    print "premise_repr",premise_repr

    if cobj.type == param.PREDICATE_TYPE['CLAUSE'] and premise_repr:
        print "if is true"
        premise = premise_repr.strip()
        p_list = premise.split("&&")
        p_len = len(p_list)
        cobj.premiseCount = p_len
        p_type = param.PREDICATE_TYPE['PREDICATE']
        for i in range(p_len):
            print 'adding',p_list[i]
            cobj.premiseObjs.append(get_pred_object(p_list[i], p_type))
        
        print 'cobj.premiseObjs',cobj.premiseObjs

# def buildArgs(args):
#     base_str = param.ARGS_BASE_STR
#     vc = 0
#     cc = 0
#     arg_dict = {}
#     for i in range(len(args)):
#         arg_dict[base_str+str(i)] = args[i]
#         if args[i][0].isupper():
#             cc+=1
#         else:
#             vc+=1

#     return arg_dict, vc, cc

def get_new_name(name):
    i=1
    return name+str(i)

def Clone_pobj(pobj):
    newObj = Rule.Predicate()
    newObj.name = pobj.name
    newObj.pid = pobj.id
    newObj.type = pobj.type
    newObj.argsList = copy.deepcopy(pobj.argsList)#ReplaceArgs(pobj.argsList, replaceMap)
    newObj.argsCount = pobj.argsCount
    newObj.premiseCount = pobj.premiseCount
    for obj in pobj.premiseObjs:
        newObj.premiseObjs.append(Clone_pobj(obj))
    return newObj

def ReplaceArg(pobj, orig, new):
    if orig in pobj.argsList:
        idx = pobj.argsList.index(orig)
        pobj.argsList[idx] = new

