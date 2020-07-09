import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from ml_data import mldata_add
from data_dict import ml_data_url, test_ml_data_url

train_feats = ['num_feat1', 'num_feat2', 'num_feat3', 'cat_feat1', 'cat_feat2', 'cat_feat3']
target_feat = ['Result']


def ml_rf_acc(rf=None):
    train_df = pd.read_csv(ml_data_url)
    X_train, y_train = train_df[train_feats], train_df[target_feat].values.flatten()

    test_df = pd.read_csv(test_ml_data_url)
    X_test, y_test = test_df[train_feats], test_df[target_feat].values.flatten()
    if rf is None:
        rf = RandomForestClassifier(n_estimators=100, min_samples_leaf=2, random_state=42)
    rf.fit(X_train, y_train)
    return rf.score(X_test, y_test)


def ml_rf_pred(ctx):
    test_df = mldata_add(pd.DataFrame([ctx]))
    tmp_df = pd.read_csv(ml_data_url)
    train_df, target = tmp_df[train_feats], tmp_df[target_feat].values.flatten()
    rf = RandomForestClassifier(n_estimators=100, min_samples_leaf=2, random_state=42)
    rf.fit(train_df, target)
    prob = rf.predict_proba(test_df).max()
    pred = rf.predict(test_df)[0]
    return prob, pred


def simple_model_tune():
    n_est = [75, 100, 128, 256]
    min_s_l = [1, 2, 0.5]
    max_d = [None, 1]

    for n in n_est:
        for m_l in min_s_l:
            for d in max_d:
                rf = RandomForestClassifier(n_estimators=n, min_samples_leaf=m_l, max_depth=d, random_state=42)
                sc = ml_rf_acc(rf)
                print('Score: {}, n_est: {}, min_sl: {}, max_d: {}'.format(sc, n, m_l, d))


if __name__ == '__main__':
    print('Testing..')
    simple_model_tune()
    # print(ml_rf_acc())