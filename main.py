import quantlib.data_utils as du
import quantlib.general_utils as gu

# df, instruments = du.get_sp500_df()
# df = du.extend_dataframe(traded=instruments, df=df)

# gu.save_file('./data/historical_df.obj', (df, instruments))
# # saves us time re-downloading data from Yahoo Financecd ./

(df, instruments) = gu.load_file('./data/historical_df.obj')
# input(pbj)