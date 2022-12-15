import xgboost as xgb
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier



def CreateXgboostModel(X, Y):
    xgbc = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, gamma=0, subsample=0.5,colsample_bytree=1, max_depth=8)
    xgbc.fit(X,Y)
    return xgbc


def keepLearning(model_old, X_new, y_new):
  model_new = XGBClassifier().fit(X_new, y_new, xgb_model=model_old)
  return model_new