import json

'''
https://hangukquant.substack.com/p/volatility-targeting-the-asset-level
https://hangukquant.substack.com/p/volatility-targeting-the-strategy
'''
class Lbmom():

    def __init__(self, instruments_config, historical_df, simulation_start, vol_target):
        self.pairs = [(69, 108), (231, 268), (27, 287), (207, 267), (22, 103), (112, 277), (112, 207), (185, 204), (83, 298), (98, 207), (86, 246), (18, 109), (49, 284), (151, 196), (114, 137), (30, 136), (23, 25), (210, 256), (130, 195), (67, 175), (59, 165)]
        self.historical_df = historical_df
        self.simulation_start = simulation_start
        self.vol_target = vol_target                # for more info on vol-targeting, refer the posts linked
        with open(instruments_config) as f:
            self.instruments_config = json.load(f)
        self.sysname = 'LBMOM'

# let's implement a few methods
# 1. method to get indicators specific to this strat
# 2. method to run a backtest/get positions from this strat

def extend_historicals(self, instruments, historical_data):
    pass

def run_simulation(self, historical_data):
    pass

def get_subsys_pos(self):
    pass