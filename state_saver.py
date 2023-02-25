

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
        print("last_state", self.states[-1])
        print("last_state_vizited", self.states[-2])

    def pop_state(self):
        state = None
        if (len(self.states) > 1):
            state = self.states[-2]
            del self.states[-1]
        return  state

