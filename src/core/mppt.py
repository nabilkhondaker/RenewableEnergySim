class MPPTController:
    def __init__(self, step_size: float = 0.5):
        self.step_size = step_size
        self.v_ref = 24.0 # Initial voltage reference
        self.prev_p = 0.0
        self.prev_v = 0.0

    def optimize(self, v_current: float, i_current: float) -> float:
        """
        Perturb and Observe (P&O) MPPT algorithm.
        Adjusts the reference voltage to find the peak of the P-V curve.
        """
        p_current = v_current * i_current
        
        delta_p = p_current - self.prev_p
        delta_v = v_current - self.prev_v
        
        if delta_p != 0:
            if delta_p > 0:
                if delta_v > 0:
                    self.v_ref += self.step_size
                else:
                    self.v_ref -= self.step_size
            else:
                if delta_v > 0:
                    self.v_ref -= self.step_size
                else:
                    self.v_ref += self.step_size
                    
        self.prev_p = p_current
        self.prev_v = v_current
        return self.v_ref
