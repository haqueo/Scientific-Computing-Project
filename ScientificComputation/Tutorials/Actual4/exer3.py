import pandas as pd
import numpy as np
from CRR import CoxRossRubinstein
if __name__ == '__main__':

	# read S&P 500 prices from file
	df    = pd.read_csv('AIG06-07.csv')
	AdjC  = df['AdjClose']
	Price = np.array(AdjC[::-1])

	




