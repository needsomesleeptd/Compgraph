

class StateSaver:
    def __init__(self,max_state_cnt = 5):
        self.states = []
        self.max_states = max_state_cnt

    def push_state(self,state:list):
        if (len(self.states) < self.max_states):
            self.states.append(state)
        else:
            for i in range(1,len(self.states)):
                self.states[i-1] = self.states[i]
            self.states[-1] = state

    def pop_state(self):
        state = None
        if (len(self.states) > 0):
            state = self.states[-1]
            del self.states[-1]
        return  state

