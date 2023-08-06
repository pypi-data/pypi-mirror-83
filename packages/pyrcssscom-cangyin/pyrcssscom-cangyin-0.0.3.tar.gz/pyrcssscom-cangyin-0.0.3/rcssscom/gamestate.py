import re
from time import time
from coloredlog.color import * 

class GameState():
    state_atoms = [
        # Measurements and Rules
        "FieldLength",
        "FieldWidth",
        "FieldHeight",
        "GoalWidth",
        "GoalDepth",
        "GoalHeight",
        "FreeKickDistance",
        "WaitBeforeKickOff",
        "AgentRadius",
        "BallRadius",
        "BallMass",
        "RuleGoalPauseTime",
        "RuleKickInPauseTime",
        "RuleHalfTime",
        # Play State
        "play_modes",
        "team_left",
        "team_right",
        "score_left",
        "score_right",
        "play_mode",
        # Play Modes
        "BeforeKickOff",
        "KickOff_Left",
        "KickOff_Right",
        "PlayOn",
        "KickIn_Left",
        "KickIn_Right",
        "corner_kick_left",
        "corner_kick_right",
        "goal_kick_left",
        "goal_kick_right",
        "offside_left",
        "offside_right",
        "GameOver",
        "Goal_Left",
        "Goal_Right",
        "free_kick_left",
        "free_kick_right",
        "direct_free_kick_left",
        "direct_free_kick_right",
        "pass_left",
        "pass_right",
        # Time
        "time",
        "half",
        # Foul
        "foul",
    ]


    def __init__(self):
        self.time_last_sync = 0

        # Measurements and Rules
        self.FieldLength = 0
        self.FieldWidth = 0
        self.FieldHeight = 0
        self.GoalWidth = 0
        self.GoalDepth = 0
        self.GoalHeight = 0
        self.FreeKickDistance = 0
        self.WaitBeforeKickOff = 0
        self.AgentRadius = 0
        self.BallRadius = 0
        self.BallMass = 0
        self.RuleGoalPauseTime = 0
        self.RuleKickInPauseTime = 0
        self.RuleHalfTime = '0'
        # Play State
        self.play_modes = [''] * 12
        self.team_left = '<Left>'
        self.team_right = '<Right>'
        self.score_left = 0
        self.score_right = 0
        self.play_mode = 0
        # Play Modes
        self.BeforeKickOff = None
        self.KickOff_Left = None
        self.KickOff_Right = None
        self.PlayOn = None
        self.KickIn_Left = None
        self.KickIn_Right = None
        self.corner_kick_left = None
        self.corner_kick_right = None
        self.goal_kick_left = None
        self.goal_kick_right = None
        self.offside_left = None
        self.offside_right = None
        self.GameOver = None
        self.Goal_Left = None
        self.Goal_Right = None
        self.free_kick_left = None
        self.free_kick_right = None
        self.direct_free_kick_left = None
        self.direct_free_kick_right = None
        self.pass_left = None
        self.pass_right = None
        # Time
        self.time = '0'
        self.half = '0'
        # Foul
        self.foul = None
        # ball position
        self.ball = (0.0, 0.0, 0.0)


    def format_game_time(self): # specialized for use below.
        t = int(self.time)
        return '{:0>2}:{:0>2}'.format(int(t / 60), int(t % 60))

    def game_state_repr_decorated(self):
        """string representation of play state."""
        play_mode = self.play_modes[self.play_mode]
        game_time = self.format_game_time()

        s = deco(str(self.score_left) + ':' + str(self.score_right), bold=True) + reset()

        s = deco('{:>12}'.format(self.team_left), 0x001, bold=True) + reset() + \
            '  ' + s + '  ' + \
            deco('{:<12}'.format(self.team_right), 0x100, bold=True) + reset() + \
            deco('{:>8}'.format(game_time), bold=True) + reset() + '\n'
        
        s += '{:<25}'.format('Playmode: ' + play_mode) + '{:>8}'.format('Half: ' + str(self.half)) + '{:>12}'.format('Foul: ' + str(self.foul)) + '\n'
        s += 'Ball(' + '{:.3}, {:.3}, {:.3}'.format(*self.ball) + ')'
        return s

    def parse_state(self, state_str): # FieldLength FieldWidth time half score_left score_right play_mode ...s
        v = self._make_struct('(' + state_str + ')')

        # Measurements and Rules
        for t in v[0]:
            atom, values = t[0], t[1:]

            if atom == "FieldLength":
                self.FieldLength = float(values[0])
            elif atom == "FieldWidth":
                self.FieldWidth = float(values[0])
            elif atom == "FieldHeight":
                self.FieldHeight = float(values[0])
            elif atom == "GoalWidth":
                self.GoalWidth = float(values[0])
            elif atom == "GoalDepth":
                self.GoalDepth = float(values[0])
            elif atom == "GoalHeight":
                self.GoalHeight = float(values[0])
            elif atom == "FreeKickDistance":
                self.FreeKickDistance = float(values[0])
            elif atom == "WaitBeforeKickOff":
                self.WaitBeforeKickOff = float(values[0])
            elif atom == "AgentRadius":
                self.AgentRadius = float(values[0])
            elif atom == "BallRadius":
                self.BallRadius = float(values[0])
            elif atom == "BallMass":
                self.BallMass = float(values[0])
            elif atom == "RuleGoalPauseTime":
                self.RuleGoalPauseTime = float(values[0])
            elif atom == "RuleKickInPauseTime":
                self.RuleKickInPauseTime = float(values[0])
            elif atom == "RuleHalfTime":
                self.RuleHalfTime = float(values[0])
            # Play State
            elif atom == "play_modes":
                self.play_modes = values
            elif atom == "team_left":
                self.team_left = values[0]
            elif atom == "team_right":
                self.team_right = values[0]
            elif atom == "score_left":
                self.score_left = int(values[0])
            elif atom == "score_right":
                self.score_right = int(values[0])
            elif atom == "play_mode":
                self.play_mode = int(values[0])
            # Time
            elif atom == "time":
                self.time = float(values[0])
            elif atom == "half":
                self.half = values[0]
            # Foul
            elif atom == "foul":
                self.foul = values[0]

        if len(v[2][-1]) > 2:
            if v[2][-1][1][0] == 'SLT':
                self.ball = tuple(map(float, v[2][-1][1][-4:-1]))
            elif v[2][-1][2][0] == 'SLT': # full state
                self.ball = tuple(map(float, v[2][-1][2][-4:-1]))

        self.time_last_sync = time()


    def _make_struct(self, data):
        items = re.findall(r"\(|\)|[\w\.]+", data)

        def req(index):
            result = []
            item = items[index]
            while item != ")":
                if item == "(":
                    subtree, index = req(index + 1)
                    result.append(subtree)
                else:
                    result.append(item)
                index += 1
                item = items[index]
            return result, index

        return req(1)[0]
    
