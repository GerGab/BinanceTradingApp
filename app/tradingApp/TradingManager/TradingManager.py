from .Trader import MACDStragety

class TradingManager:

    def __init__(self):
        pass

    def applyStrategy(self,**dfs):
        results = {'buy':[],'sell':[]}
        for key,df in dfs.items():
            response = MACDStragety(df)
            if response.get('result',False):
                results[response['result']].append(key)
            
                
        return results

    
        
        
        
        
        
        
