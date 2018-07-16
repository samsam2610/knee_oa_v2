
class Gait_Cycle():
    def __init__(self):
        self.cycle_start = bool
        self.cycle_end = bool
        self.swing_phase_duration = float
        self.stance_phase_duration = float
        self.gait_event = []

    def add_imu(self, Gait_Event):

        if Gait_Event.toeoff_time != -1:
            self.gait_event.append([Gait_Event.toeoff_time, 'toe off'])
        if Gait_Event.heelstrike_time != -1:
            self.gait_event.append([Gait_Event.heelstrike_time, 'heel strike'])
        if Gait_Event.hamstring_time != -1:
            self.gait_event.append([Gait_Event.hamstring_time, 'hamstring'])
        if Gait_Event.quadtricep_time != -1:
            self.gait_event.append([Gait_Event.quadtricep_time, 'quadriceps'])


