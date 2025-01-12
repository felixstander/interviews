# coding: utf-8
import json
import pickle
from pathlib import Path

import lightgbm as lgb
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

print("Loading data...")
# load or create your dataset
binary_example_dir = Path(__file__).absolute().parent
df = pd.read_csv(binary_example_dir / "data/high_diamond_ranked_10min.csv")


y = df['blueWins']
X = df.drop(['gameId',"blueWins"],axis=1)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=2025)

def main():

# create dataset for lightgbm
# if you want to re-use data, remember to set free_raw_data=False
    lgb_train = lgb.Dataset(
        X_train, y_train,  free_raw_data=False
    )
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train, free_raw_data=False)


# specify your configurations as a dict
    params = {
        "boosting_type": "gbdt",
        "objective": "binary",
        "metric": "binary_logloss",
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "verbose": 1,
    }

    print("Starting training...")
# feature_name and categorical_feature
    gbm = lgb.train(
        params,
        lgb_train,
        num_boost_round=50,
        valid_sets=lgb_train,  # eval training data
    )

    print("Finished first 10 rounds...")
# check feature name
    print(f"7th feature name is: {lgb_train.feature_name[6]}")

    print("Saving model...")
# save model to file
    gbm.save_model("model.txt")

    print("Dumping model to JSON...")
# dump model to JSON (and save to file)
    model_json = gbm.dump_model()

    with open("model.json", "w+") as f:
        json.dump(model_json, f, indent=4)

# feature names
    print(f"Feature names: {gbm.feature_name()}")

# feature importances
    print(f"Feature importances: {list(gbm.feature_importance())}")

    print("Loading model to predict...")
# load model to predict
    bst = lgb.Booster(model_file="model.txt")
# can only predict with the best iteration (or the saving iteration)
    y_pred = bst.predict(X_test)
# eval with loaded model
    auc_loaded_model = roc_auc_score(y_test, y_pred)
    print(f"The ROC AUC of loaded model's prediction is: {auc_loaded_model}")

    print("Dumping and loading model with pickle...")
# dump model with pickle
    with open("model.pkl", "wb") as fout:
        pickle.dump(gbm, fout)
# load model with pickle to predict
    with open("model.pkl", "rb") as fin:
        pkl_bst = pickle.load(fin)
# can predict with any iteration when loaded in pickle way
    y_pred = pkl_bst.predict(X_test, num_iteration=7)
# eval with loaded model
    auc_pickled_model = roc_auc_score(y_test, y_pred)
    print(f"The ROC AUC of pickled model's prediction is: {auc_pickled_model}")

if __name__ == "__main__":
    main()
