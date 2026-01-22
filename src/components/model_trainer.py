import os 
import sys
import pandas as pd
from dataclasses import dataclass
from xgboost import XGBRegressor
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier, 
    AdaBoostClassifier,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score


from src.logger import logging  
from src.exception import CustomException
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train= train_array[:,:-1], train_array[:,-1]
            X_test, y_test= test_array[:,:-1], test_array[:,-1]

            models={
                "XGBRegressor": XGBRegressor(),
                "Gradient Boosting Regressor": GradientBoostingClassifier(),
                "Random Forest Classifier": RandomForestClassifier(),
                "AdaBoost Classifier": AdaBoostClassifier(),
                "Linear Regression": LinearRegression(),
                "KNeighbors Regressor": KNeighborsRegressor(),
                "Decision Tree Regressor": DecisionTreeRegressor()
            }

            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models)

            best_model_name= list(model_report.keys())[list(model_report.values()).index(max(model_report.values()))]

            best_model= models[best_model_name]

            if max(model_report.values()) < 0.6:
                raise CustomException("No best model found")

            logging.info(f"Best model found on both training and testing dataset: {best_model_name}")

            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )

            predicted= best_model.predict(X_test)
            r2_square= r2_score(y_test, predicted)
            accuracy= r2_square * 100
            return [r2_square, accuracy]

        except Exception as e:
            logging.error("Error occurred in model trainer")
            raise CustomException(e, sys)
    
