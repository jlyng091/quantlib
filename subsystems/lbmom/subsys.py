import json
import quantlib.indicators_calc as indicators_calc

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
        # need indicators of 'momentum'
        # let this be the moving avg crossover, such that if the fastMA crossovers the slowMA, it is a buy
        # a long-biased momentum strat is biased in the long direction. start with a 100/0 L/S strat
        # let's also use a filter to identify false positive signals. let's use the average directional index, or the adx
        for inst in instruments:
            # implement some calculator for moving average crossover
            historical_data['{} adx'.format(inst)] = indicators_calc.adx_series(
                high=historical_data[inst + ' high'],
                low=historical_data[inst + ' low'],
                close=historical_data[inst + ' close'],
                n=14
            )
        for pair in self.pairs:
            historical_data['{} ema{}'.format(inst, str(pair))] = indicators_calc.ema_series(
                series=historical_data[inst + ' close'],
                n = pair[0]
            ) - indicators_calc.ema_series(
                series=historical_data[inst + ' close'],
                n = pair[1]
            ) # fastMA - slowMA

        return historical_data
        # now historical data has ohlcvs and whether fastMA - slowMA for each pair
        # as well as ADX of closing prices to see if there's a 'trending' regime

    def run_simulation(self, historical_data):
        # init params
        instruments = self.instruments_config("instruments")

        # calculate/pre-process indicators
        historical_data = self.extend_historicals(instruments=instruments, historical_data=historical_data)

        # perform simulation
        portfolio_df = pd.DataFrame(index=historical_df[self.simulation_start:].index).reset_index()
        print(portfolio_df)

        # run diagnostics

        # return dataframe

        pass

    def get_subsys_pos(self):
        self.run_simulation(historical_data=self.historical_df)
    
# so main driver passes df into the LBMOM strat, so that LBMOM performs some calcs
# using the quantlib indicators calculator. after, we pass into the simulator to run simulations and backtests

# just establishing framework to ensure logic is sound and flexible, and unneeded calcs aren't run
# general calc happens in the driver, such as returns, volatility for all strats
# indicators specific to strat are done inside strat to save time

# each strat has a config file, to control some parameters
