def rudder_step_script(step_index):
    if step_index < 10:
        return 0.1
    else:
        return 0.5
        
def speed_step_script(step_index):
    if step_index < 10:
        return 1.0
    else:
        return 2.0
        
def rudder_pulse_script(step_index):
    if step_index < 10:
        return 0.0
    elif step_index < 20:
        return 0.5
    else: 
        return 0.0
        
def rudder_s_turn_script(step_index):
    if step_index < 10:
        return 0.0
    elif step_index < 20:
        return 0.5
    elif step_index < 30:
        return -0.5
    else:
        return 0.0
        
def speed_ramp_script(step_index):
    value = 0.5 + 0.05 * step_index
    if value > 2.5:
        value = 2.5
    return value
            
def speed_hold_then_drop(step_index):
    if step_index < 15:
        return 2.0
    elif step_index < 25:
        return 1.0
    else:
        return 0.5
            