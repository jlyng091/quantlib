import quantlib.data_utils as du
import quantlib.general_utils as gu

from subsystems.lbmom.subsys import Lbmom
from dateutil.relativedelta import relativedelta

# df, instruments = du.get_sp500_df()
# df = du.extend_dataframe(traded=instruments, df=df)

# gu.save_file('./data/historical_df.obj', (df, instruments))
# # saves us time re-downloading data from Yahoo Financecd ./

(df, instruments) = gu.load_file('./data/historical_df.obj')
# input(pbj)

# # import random

# # pairs = []
# # while len(pairs) <= 20:
# #     pair = random.sample(list(range(16, 300)), 2)
# #     if pair[0]==pair[1]:
# #         continue
# #     else:
# #         # each pair is a MA crossover pair
# #         pairs.append((min(pair[0], pair[1]), max(pair[0], pair[1])))

# # print(pairs)

# print(instruments)

# let's run the LBMOM strat thru the main driver
VOL_TARGET = 0.20   # we are targeting 20% annualised vol

print(df.index[-1]) # is today's date
sim_start = df.index[-1] - relativedelta(years=5)
print(sim_start)

# strat = Lbmom(instruments_config='./subsystems/lbmom/config.json', historical_df=df, simulation_start, vol_target=VOL_TARGET)