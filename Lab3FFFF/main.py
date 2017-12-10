 
import copy

exp = []
var_test = []
rules_input = []
stack = []
var = []
final= []

class Rule:
    def __init__(self , variable , productions):
        self.variable   = variable
        self.productions = [productions]

def read_rules(): #Read rules from 'rules.cfg' into a list called rules_input
    rules_file = open("rules.cfg", "rt")
    data = rules_file.read()
    lines = data.split("\n")
    for line in lines:
        rules_input.append(line)
        print(line)

def read_exp():  #Expression is read from 'expression.cfg' into list exp in reverse order, removing whitespace.
    i = 0
    global exp
    exp_file = open("expression.cfg", "rt")
    data = exp_file.read()
    chars = data.split(" ")
    chars = [w.replace('\n', '') for w in chars]
    for char in chars[::-1]:
        i = i + 1
        exp.append(char)
    return i

def divide_rules():  # split productions into the rules class by variable
    results = []
    for rule in rules_input:
        found = False
        var = rule.split(" -> ")
        for result in results:
            if result.variable == var[0]:
                result.productions.append(var[1])
                found = True
        if not found:
            results.append(Rule(var[0] , var[1]))
    for result in results:
        splt_res = result.productions[0].split('|')
        if(len(splt_res)>0):
            result.productions = []
            for s in splt_res:
                result.productions.append(s.strip())
    
    return results



def print_reject():  #Prints Reject and exits program.
    print("\n\n")
    print("************************************")
    print("*             REJECT               *")
    print("************************************")
    exit()

def get_rule(symbol):
    global rules
    for rule in rules:
        if rule.variable == symbol:
            return rule
    return False

def operation(stack, exp):  #Performs the operations of a PDA.  Recursive.
    print("STACK:\n"+  str(stack))
    print("EXP:\n"+  str(exp))
    if len(stack) > len(exp) or (len(stack) == 0 and len(exp) > 0):
        return
    current_symbol = stack.pop()
    if current_symbol == exp[-1]:
        exp.pop()
        test(stack , exp)
        operation(copy.deepcopy(stack) , copy.deepcopy(exp))
    rule = get_rule(current_symbol)
    if rule == False:
        return
    for production in rule.productions:
        new_stack = copy.deepcopy(stack)
        for s in production.split(" ")[::-1]:
            new_stack.append(s)
        operation(new_stack, copy.deepcopy(exp))

def test(stack, exp):
    if len(stack) == 0 and len(exp) == 0:
        print("\n\n")
        print("************************************")
        print("*             ACCEPT               *")
        print("************************************")
        exit()
    else:
        return False

def main():
    global length
    global rules
    global var_test
    print("\nRules:")
    read_rules()
    global exp
    print("\nP:")
    read_exp()
    print(set(exp))
    rules = divide_rules()
    for rule in rules:
        var_test.append(rule.variable)
    print("\nZ:")
    print(set(var_test + exp))
    stack = []
    stack.append(rules[0].variable)
    operation(stack, exp)
    print_reject()




main()

