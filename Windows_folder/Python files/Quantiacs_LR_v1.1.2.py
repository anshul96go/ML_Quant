
# coding: utf-8

# In[ ]:


import quantiacsToolbox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


class myStrategy(object):

    def myTradingSystem(self, DATE, OPEN, HIGH, LOW, CLOSE, VOL, OI, P, R, RINFO, exposure, equity, settings):
        """ This system uses linear regression to allocate capital into the desired equities"""

        # Get parameters from setting
        nMarkets = len(settings['markets'])
        lookback = settings['lookback']
        dimension = settings['dimension']
        threshold = settings['threshold']

        pos = np.zeros(nMarkets, dtype=np.float)

        poly = PolynomialFeatures(degree=dimension)
        for market in range(nMarkets):
            reg = linear_model.LinearRegression()
            try:
                #predicting volume
                reg.fit(poly.fit_transform(np.arange(lookback).reshape(-1,1)), VOL[:,market])
                vol_predict = reg.predict(poly.fit_transform(np.array([[lookback]])))
                #predicting open price
                reg.fit(poly.fit_transform(np.arange(lookback).reshape(-1,1)), OPEN[:,market])
                open_predict = reg.predict(poly.fit_transform(np.array([[lookback]])))
                #predicting close price
                X = np.append(VOL[:,market], OPEN[:,market], axis=1)
                reg.fit(X,CLOSE[:,market])
                x = np.append(vol_predict,open_predict,axis=1)
                close_predict = reg.predict(x)
                
                trend = (close_predict - CLOSE[-1, market]) / CLOSE[-1, market]

                if abs(trend[0]) < threshold:
                    trend[0] = 0

                pos[market] = np.sign(trend)

            # for NaN data set position to 0
            except ValueError:
                pos[market] = .0

        return pos, settings


    def mySettings(self):
        """ Define your trading system settings here """

        settings = {}

        Futures Contracts
        settings['markets'] = ['AAPL', 'MMM', 'ABT', 'ABBV', 'ACN', 'ALL', 'MO', 'AMZN', 'AEP', 'AXP', 'AIG', 'AMGN', 'APC', 'APA', 'AAPL', 'T', 'BAC', 'BK', 'BAX', 'BRK.B', 'BA', 'BMY', 'COF', 'CAT', 'CVX', 'CSCO', 'C', 'KO', 'CL', 'CMCSA', 'COP', 'COST', 'CVS', 'DVN', 'DOW', 'DD', 'EBAY', 'EMC', 'EMR', 'EXC', 'XOM', 'FB', 'FDX', 'F', 'FCX', 'GD', 'GE', 'GM', 'GILD', 'GS', 'GOOG', 'GOOGL', 'HAL', 'HPQ', 'HD', 'HON', 'INTC', 'IBM', 'JNJ', 'JPM', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDT', 'MRK', 'MET', 'MSFT', 'MDLZ', 'MON', 'MS', 'NOV', 'NKE', 'NSC', 'OXY', 'ORCL', 'PEP', 'PFE', 'PM', 'PG', 'QCOM', 'RTN', 'SLB', 'SPG', 'SO', 'SBUX', 'TGT', 'TXN', 'TWX', 'FOXA', 'USB', 'UNP', 'UPS', 'UTX', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'WFC', 'A', 'AA', 'ABC', 'ACE', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'ADT', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIV', 'AIZ', 'AKAM', 'ALLE', 'ALTR', 'ALXN', 'AMAT', 'AME', 'AMG', 'AMP', 'AMT', 'AN', 'AON', 'APD', 'APH', 'ARG', 'ATI', 'AVB', 'AVGO', 'AVP', 'AVY', 'AZO', 'BBBY', 'BBT', 'BBY', 'BCR', 'BDX', 'BEN', 'BF.B', 'BHI', 'BLK', 'BLL', 'BMS', 'BRCM', 'BSX', 'BWA', 'BXP', 'CA', 'CAG', 'CAH', 'CAM', 'CB', 'CBG', 'CBS', 'CCE', 'CCI', 'CCL', 'CELG', 'CERN', 'CF', 'CHK', 'CHRW', 'CI', 'CINF', 'CLX', 'CMA', 'CME', 'CMG', 'CMI', 'CMS', 'CNP', 'CNX', 'COG', 'COH', 'COL', 'CPB', 'CRM', 'CSC', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVC', 'D', 'DAL', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DISCA', 'DISCK', 'DLPH', 'DLTR', 'DNB', 'DNR', 'DO', 'DOV', 'DPS', 'DRI', 'DTE', 'DUK', 'DVA', 'EA', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EOG', 'EQR', 'EQT', 'ESRX', 'ESS', 'ESV', 'ETFC', 'ETN', 'ETR', 'EW', 'EXPD', 'EXPE', 'FAST', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLIR', 'FLR', 'FLS', 'FMC', 'FOSL', 'FSLR', 'FTI', 'FTR', 'GAS', 'GCI', 'GGP', 'GIS', 'GLW', 'GMCR', 'GME', 'GNW', 'GPC', 'GPS', 'GRMN', 'GT', 'GWW', 'HAR', 'HAS', 'HBAN', 'HCBK', 'HCN', 'HCP', 'HES', 'HIG', 'HOG', 'HOT', 'HP', 'HRB', 'HRL', 'HRS', 'HST', 'HSY', 'HUM', 'ICE', 'IFF', 'INTU', 'IP', 'IPG', 'IR', 'IRM', 'ISRG', 'ITW', 'IVZ', 'JCI', 'JEC', 'JNPR', 'JOY', 'JWN', 'K', 'KEY', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KORS', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LLL', 'LLTC', 'LM', 'LNC', 'LRCX', 'LUK', 'LUV', 'LVLT', 'LYB', 'M', 'MAC', 'MAR', 'MAS', 'MAT', 'MCHP', 'MCK', 'MCO', 'MHFI', 'MHK', 'MJN', 'MKC', 'MLM', 'MMC', 'MNK', 'MNST', 'MOS', 'MPC', 'MRO', 'MSI', 'MTB', 'MU', 'MUR', 'MYL', 'NAVI', 'NBL', 'NBR', 'NDAQ', 'NE', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NLSN', 'NOC', 'NRG', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWSA', 'OI', 'OKE', 'OMC', 'ORLY', 'PAYX', 'PBCT', 'PBI', 'PCAR', 'PCG', 'PCL', 'PCLN', 'PCP', 'PDCO', 'PEG', 'PFG', 'PGR', 'PH', 'PHM', 'PKI', 'PLD', 'PNC', 'PNR', 'PNW', 'POM', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'QEP', 'R', 'RAI', 'REGN', 'RF', 'RHI', 'RHT', 'RIG', 'RL', 'ROK', 'ROP', 'ROST', 'RRC', 'RSG', 'SCG', 'SCHW', 'SE', 'SEE', 'SHW', 'SJM', 'SNA', 'SNDK', 'SNI', 'SPLS', 'SRCL', 'SRE', 'STI', 'STJ', 'STT', 'STX', 'STZ', 'SWK', 'SWN', 'SYK', 'SYMC', 'SYY', 'TAP', 'TDC', 'TE', 'TEL', 'THC', 'TIF', 'TJX', 'TMK', 'TMO', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSO', 'TSS', 'TWC', 'TXT', 'TYC', 'UA', 'UHS', 'UNM', 'URBN', 'URI', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSN', 'VRTX', 'VTR', 'WAT', 'WDC', 'WEC', 'WFM', 'WHR', 'WIN', 'WM', 'WMB', 'WU', 'WY', 'WYN', 'WYNN', 'XEC', 'XEL', 'XL', 'XLNX', 'XRAY', 'XRX', 'XYL', 'YHOO', 'YUM', 'ZION', 'ZTS' ]
        #settings['markets'] = ['CASH', 'F_S', 'F_AD']
        settings['lookback'] = 252
        settings['budget'] = 10 ** 6
        settings['slippage'] = 0.05

        settings['threshold'] = 0.05
        settings['dimension'] = 3

        return settings


# In[ ]:


result = quantiacsToolbox.runts(myStrategy)

