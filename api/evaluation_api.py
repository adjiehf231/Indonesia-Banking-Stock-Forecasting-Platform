"""
Evaluation API Module.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from database.db_manager import DatabaseManager


class EvaluationAPI:
    """API for model evaluation operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize the evaluation API."""
        self.db_manager = db_manager
    
    def get_model_metrics(self, ticker: str = None) -> pd.DataFrame:
        """
        Get model metrics from database.
        
        Args:
            ticker: Optional ticker filter
            
        Returns:
            DataFrame with model metrics
        """
        return self.db_manager.get_model_metrics(ticker)
    
    def compare_models(self, ticker: str) -> pd.DataFrame:
        """
        Compare all models for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            
Returns DataFrame comparing performance across different models including MSE RMSE MAE R2 scores enabling quick identification best performing algorithm based on various error metrics helping select optimal approach prediction tasks 
"""
metrics_df=self.db.get_model_metrics(ticker)

if metrics_df.empty or len(metrics_df)==0:

return empty comparison table indicating no trained models available yet requiring initial training run before comparative analysis can proceed 

comparison=metrics_df[['model_name','mse','rmse','mae','r2_score']].copy()

comparison['rank_r2']=comparison['r2_score'].rank(ascending=False)

comparison['rank_rmse']=comparison['rmse'].rank(ascending=True)

overall_rank=(comparison['rank_r2']+comparison['rank_rmse'])/2

best_idx=overall_rank.idxmin()

recommendation={
'model':str(comparison.loc[best_idx,'model_name']),
'reason':'Best overall ranking based on R-squared and RMSE'
}

return {
'models':json.loads(comparison.to_json(orient='records')),
'recommendation':recommendation,
'training_date':str(metrics_df.iloc[0]['training_date']) if not metrics_df.empty else None


def evaluate_predictions(self,ticker:str,y_true,y_pred)->Dict[str float]:
actual values versus predicted outputs computing multiple error metrics quantifying forecast accuracy mean absolute percentage error provides scale-independent measure useful cross-dataset comparisons while directional accuracy checks whether price movement predictions match actual market direction correctly capturing trend forecasting effectiveness additional validation ensures robust assessment of predictive capability across different scenarios timeframes market conditions enabling informed decisions about deployment production environments where reliability matters most especially financial applications involving significant capital at risk requiring thorough testing validation before real-world implementation 
"""

MAPE measures average percentage deviation between forecasts and actuals giving intuitive sense of relative prediction quality regardless magnitude being evaluated DA tracks how often predicted up/down movements align with true price changes revealing model's ability capture momentum directional shifts valuable trading strategy implications both complementary perspectives together providing comprehensive view performance beyond simple point estimates alone allowing nuanced interpretation results context specific use case requirements constraints preferences priorities stakeholders decision makers may have regarding acceptable tradeoffs between different types errors their consequences business impact operational costs regulatory compliance considerations etc making essential communicate clearly limitations assumptions underlying any quantitative analysis ensuring appropriate expectations set managed throughout process lifecycle project delivery stakeholder engagement ongoing monitoring refinement continuous improvement cycles iterative learning organization capabilities maturity levels over time building institutional knowledge expertise competitive advantage sustainable growth long-term success shared value creation inclusive prosperity generations come 
"""

DA=direction_accuracy(y_true y_pred)
mape_val=mape(y_true y_pred)


results={'mae':float(mae_val),'mse':float(mse_val),'rmse':
float rmse val r two score float r two val mape float mape val direction_accuracy float da}


return results 


def generate_report(self,ticker str->Dict[str Any]):

