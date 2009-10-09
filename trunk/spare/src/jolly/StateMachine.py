# -*- coding:utf-8 -*-
"""
Created on 2009-10-4

@author: summit

StatueMachine is the surrogate. This base class is derived along with the class
or classes that provide the actual implementation
"""

class State:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name
    
# Inputs to a state machine
class Input: 
    def __init__(self, name): self.name = name
    def __str__(self): return self.name

# Condition function object for state machine
class Condition:
    def condition(self, statemachine, input):
        assert 1, "condition() not implemented"

# Transition function object for state machine
class Transition:
    def transition(self, statemachine, input):
        assert 1, "transition() not implemented"

# A table-driven state machine
class StateMachine:
    def __init__(self, initialState, tranTable):
        self.state = initialState
        self.transitionTable = tranTable
    
    def nextState(self, input):
        tran = self.transitionTable.get((self.state,input))
        
        if tran <> None:    
            if (tran[0] <> None):
                c = tran[0]
                if not c.condition(self, input):
                    pass    # Failed test
            if (tran[1] <> None):
                tran[1].transition(self, input)
            self.state = tran[2]
            return
        raise RuntimeError, "Input not supported for current state"

if __name__ == "__main__":
    State.hello_jolly = State("Hello jolly!")
    State.hello_summit = State("Hello summit!")
    State.end = State("Salutation has finished")
    
    Input.hello = Input("Hello")
    Input.noattension = Input("Jolly pay no attension!")
    
    class HelloStateMachine(StateMachine):
        def __init__(self):
            StateMachine.__init__(self,State.hello_jolly, {
            # Current state, input
            (State.hello_jolly, Input.hello) :
            # test, transition, next state:
            (None, None, State.hello_summit),
            (State.hello_jolly, Input.noattension) :
            (None, None, State.end),
            (State.hello_summit, Input.hello) :
            (None, None, State.end)
            })
    hsm = HelloStateMachine()   
    for input in [Input.hello, Input.hello]:
        
        print hsm.state, ":", input
        hsm.nextState(input)