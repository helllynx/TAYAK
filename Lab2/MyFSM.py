
from itertools import chain


class Node:
    def __init__(self, num, terminate, trans):
        self.state_num = num
        self.transitions = trans
        self.terminate = terminate

    def addTransition(self, c, ref):
        self.transitions.append([c, ref])

    def __str__(self):
        if(self.terminate):
            return str(self.state_num) +  "#" + str(self.transitions) + " * "
        else:
            return str(self.state_num) +  "#" + str(self.transitions)



class MyStateMachine:
    def __init__(self, nodes, start_state):
        self.state = start_state
        self.nodes = nodes
        self.terminate = nodes[0].terminate

    def get_state(self, c):
        for t in self.nodes[self.state].transitions:
            if(t[0] == c):
                return t[1]
        return -1


    def getRemovedNodeTrans(self, c, trans):
        new_trans = []
        nodes = []

        for t in trans:
            if(t[0]==c):
                nodes.append(t[1])
        print(nodes)
        for node in nodes:
            new_trans.append(self.nodes[node].transitions)
        new_trans = list(chain.from_iterable(new_trans))
        print(new_trans)

        s_state = int("".join(str(x) for x in nodes))
        self.nodes[s_state] = Node(s_state, False, new_trans)

        self.checkEdge(nodes, s_state)
        self.removeNodes(nodes)

    def removeNodes(self, nodes):
        for node in nodes:
            del self.nodes[node]

    def checkEdge(self, n_list, new_state):
        print("CHECK EDGE")
        for node in self.nodes:
            for i in range(0, len(self.nodes[node].transitions):
                if(n_list.__contains__()):
                    print(t)
                    self.nodes[node].transitions[]



    def check_nfa_cast_to_dfa(self):
        k=0
        nodes_copy = self.nodes.copy()
        for n in nodes_copy:
            f = nodes_copy[n].transitions[0][0]
            # print(f)
            for t in nodes_copy[n].transitions:
                if(t[0]==f): k+=1
            if (k > 1):
                self.getRemovedNodeTrans(f, nodes_copy[n].transitions)


            k = 0

    def printNodes(self):
        print("==========================")
        for n in self.nodes:
            print(self.nodes[n])
        print("==========================")

    def start(self, string):
        self.printNodes()
        self.check_nfa_cast_to_dfa()
        self.printNodes()

        for c in string:
            state = self.get_state(c)
            if(state!=-1):
                print("From " + str(self.state) + " to " + str(state) + "  char: " + c)
                self.state = state
                self.terminate = self.nodes[state].terminate


        if(self.terminate == True and len(string)>0):
            print("Success!")
        else:
            print("ERROR! Stop in non-final state or an empty string.")

