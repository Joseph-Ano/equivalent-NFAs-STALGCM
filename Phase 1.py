#[ [machine1, [state1, transition1, transition2, transitionN], [state2, transition1, transition2, transitionN]]
#  [machine2, [state1, transition1, transition2, transitionN], [state2, transition1, transition2, transitionN]] ]

def get_input(machines, final_states):
    state_dict= {}
    input_dict = {} 
    
    for i in range(2):
        #Get machine name and number of states
        machines.append([input()]) 
        num_states = int(input())

        #Get state names
        for j in range(num_states): 
            machines[i].append([input()])
            state_dict[machines[i][j+1][0]] = j+1 #fill state dictionary 

        #Get number of inputs
        num_inputs = int(input())

        #Adds an empty string to all transitions
        for j in range(1, num_states+1): 
            for k in range(num_inputs):
                machines[i][j].append("")

        #Fills input dictionary
        for j in range(num_inputs):
            temp = input()
            if(temp not in input_dict):
                input_dict[temp] = j+1

        #Gets number of transitions
        num_transitions = int(input())

        #Adds the transitions
        for j in range(num_transitions):
            temp = input().split(" ")
            if(machines[i][state_dict[temp[0]]][input_dict[temp[1]]] == ""):
                machines[i][state_dict[temp[0]]][input_dict[temp[1]]]+=temp[2]
            else:
                machines[i][state_dict[temp[0]]][input_dict[temp[1]]]+=" "+temp[2]

        #Place start state at the start and get number of final states
        start_state = input()
        machines[i][1], machines[i][state_dict[start_state]] = machines[i][state_dict[start_state]], machines[i][1]
        num_final = int(input())
        final_states.append([])

        #Add final states
        for j in range(num_final):
            final_states[i].append(input())

        #Buffer
        if(i == 0):
            input()

        state_dict.clear()

    return num_inputs

def convert_to_dfa(machine, start_state, num_inputs):
    state_dict = {}
    state_index = {}
    visited_states = set()
    dfa = []

    #Set the state indices and their respective code
    for i in range(1, len(machine)):
        state_dict[machine[i][0]] = 2**(i-1)
        state_index[machine[i][0]] = i
    
    #insert the start state
    dfa.append([start_state])
    visited_states.add(state_dict[start_state])

    #DFA algorithm
    for state in dfa:
        curr_state = state[0].split(" ")
        for j in range(1, num_inputs+1):
            sum = 0
            temp = ""
            for char in curr_state:
                if(char != ""):
                    curr_transition = machine[state_index[char]][j].split(" ")
                    for char in curr_transition:
                        if(curr_transition != ""):
                            if(char not in temp):
                                sum+=state_dict[char]
                                temp+=" "+char

            #Arranges the states alphabetically and adds the transition
            temp = temp.strip()
            temp = temp.split(" ")
            temp = " ".join(sorted(temp))
            state.append(temp)

            #dosent add exisiting states
            if(sum not in visited_states):
                visited_states.add(sum)
                dfa.append([temp])                                

    return dfa

def check_equivalence(machine1, machine2, dictionary, num_inputs):
    state_index = {}
    visited_states = set()
    dfa = []
    equivalent = 1

    #Set the state indices
    for i in range(len(machine1)):
        state_index[machine1[i][0]] = i
    for i in range(len(machine2)):
        state_index[machine2[i][0]] = i
    
    #insert the start state
    temp = machine1[0][0] + " " + machine2[0][0]
    dfa.append(temp)
    visited_states.add(temp)

    for state in dfa:
        curr_state = state.split(" ")
        for j in range(1, num_inputs+1):
            next_state1 = machine1[state_index[curr_state[0]]][j] 
            next_state2 = machine2[state_index[curr_state[1]]][j] 
            
            if(dictionary[next_state1] != dictionary[next_state2]):
                equivalent = 0
            temp = next_state1 + " " + next_state2

            #dosent add exisiting states
            if(temp not in visited_states):
                visited_states.add(temp)
                dfa.append(temp)
          
    return equivalent 

def main():
    nfa_machines = []
    dfa_machines = []
    final_states = []
    state_set = set()
    state_dict = {}
    final_dict = {}
    ctr = 0

    num_inputs = get_input(nfa_machines, final_states)

    #Converts nfa to dfa
    for machine in nfa_machines:
        dfa_machines.append(convert_to_dfa(machine, machine[1][0], num_inputs))

    #Gives each state in each machine a unique name
    for i in range(len(dfa_machines)):
        for j in range(len(dfa_machines[i])):
            for k in range(len(dfa_machines[i][j])):
                if dfa_machines[i][j][k] not in state_set:
                    state_set.add(dfa_machines[i][j][k])
                    state_dict[dfa_machines[i][j][k]] = str(ctr)
                    ctr+=1
                    if(dfa_machines[i][j][k] == ""):
                        final_dict[state_dict[dfa_machines[i][j][k]]] = 'n'
                    temp = dfa_machines[i][j][k].split(" ")
                    for char in temp:
                        if(char in final_states[i]):
                            final_dict[state_dict[dfa_machines[i][j][k]]] = 'f'
                            break
                        else:
                            final_dict[state_dict[dfa_machines[i][j][k]]] = 'n'
                dfa_machines[i][j][k] = state_dict[dfa_machines[i][j][k]]
        state_dict.clear()
        state_set.clear()

    answer = check_equivalence(dfa_machines[0], dfa_machines[1], final_dict, num_inputs)
    
    if(answer == 0):
        print("not equivalent")
    else:
        print("equivalent")

main()

