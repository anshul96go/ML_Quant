### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    nMarkets=VOL.shape[1]
    #print(nMarkets)
    periodLonger=100
    periodShorter=5

    
    # Calculate Simple Moving Average (SMA)
    #smaLongerPeriod=numpy.nansum(CLOSE[-periodLonger:,:],axis=0)/periodLonger
    #smaShorterPeriod=numpy.nansum(CLOSE[-periodShorter:,:],axis=0)/periodShorter

    #ADV20
    adv20 = np.nansum(VOL[-20:,:],axis=0)/20
    adv40 = np.nansum(VOL[-40:,:],axis=0)/40

    #print(adv20.shape)

    #alpha = np.divide(VOL[0,:],adv20)
    longEquity= (adv20-adv40)/adv20 > 0.1
    shortEquity= ~longEquity
    #print(longEquity.shape)

    pos=np.zeros(nMarkets)
    pos[longEquity]=1
    pos[shortEquity]=-1

    weights = np.divide(pos,np.nansum(abs(pos)))

    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings= {}

    # S&P 100 stocks
    # settings['markets']=['CASH','AAPL','ABBV','ABT','ACN','AEP','AIG','ALL',
    # 'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C',
    # 'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW',
    # 'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE',
    # 'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM',
    # 'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON',
    # 'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM',
    # 'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP',
    # 'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']

    # Futures Contracts

    settings['markets']  = ['CASH','F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CC', 'F_CD',
    'F_CL', 'F_CT', 'F_DX', 'F_EC', 'F_ED', 'F_ES', 'F_FC','F_FV', 'F_GC',
    'F_HG', 'F_HO', 'F_JY', 'F_KC', 'F_LB', 'F_LC', 'F_LN', 'F_MD', 'F_MP',
    'F_NG', 'F_NQ', 'F_NR', 'F_O', 'F_OJ', 'F_PA', 'F_PL', 'F_RB', 'F_RU',
    'F_S','F_SB', 'F_SF', 'F_SI', 'F_SM', 'F_TU', 'F_TY', 'F_US','F_W', 'F_XX',
    'F_YM']
    # settings['beginInSample'] = '20120506'
    # settings['endInSample'] = '20150506'
    settings['lookback']= 504
    settings['budget']= 10**6
    settings['slippage']= 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    #returnDict = quantiacsToolbox.runts('/Path/to/your/TradingSystem.py')
    results = quantiacsToolbox.runts(__file__)
    