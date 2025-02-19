import re
import csv

def extract_fsm_states_and_transitions(fsm_code):
    # Regular expressions to match states and transitions
    state_pattern = re.compile(r'\b(\w+):\s*begin')
    transition_pattern = re.compile(r'\bctrl_fsm_ns\s*=\s*(\w+);')
    if_pattern = re.compile(r'^\s*if\s*\(.*\)\s*begin')

    states = set()
    transitions = set()

    current_state = None
    state_transitions = {}

    for line in fsm_code.split('\n'):
        # Match states
        state_match = state_pattern.search(line)
        if state_match:
            if current_state and not state_transitions.get(current_state):
                # If no transition was defined for the current state, it transitions to itself
                transitions.add((current_state, current_state))
            
            current_state = state_match.group(1).upper()
            states.add(current_state)
            state_transitions[current_state] = False

        # Match transitions
        if current_state:
            transition_match = transition_pattern.search(line)
            if transition_match:
                next_state = transition_match.group(1).upper()
                if_block_match = if_pattern.search(line)
                # If the transition is inside an if block, it's conditional
                if if_block_match:
                    state_transitions[current_state] = True
                else:
                    state_transitions[current_state] = False
                transitions.add((current_state, next_state))

    # Check if the last state has an unconditional transition
    if current_state and not state_transitions.get(current_state):
        transitions.add((current_state, current_state))

    # If any state has the possibility to transition to itself, add an additional tuple entry
    for state in states:
        transitions.add((state, state))

    return states, transitions


# Read the FSM code from a file
with open('fsm_case.sv', 'r') as file:
    fsm_code = file.read()

# Extract states and transitions
states, transitions = extract_fsm_states_and_transitions(fsm_code)

# Write transitions to a CSV file
with open('fsm_transitions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['current_state', 'next_state'])
    for transition in transitions:
        current_state, next_state = transition
        writer.writerow([current_state, next_state])

print("Transitions have been saved to transitions.csv")
