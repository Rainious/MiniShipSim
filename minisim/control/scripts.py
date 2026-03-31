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