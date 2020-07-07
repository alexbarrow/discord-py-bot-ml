import pandas as pd
import pickle

from sklearn.preprocessing import LabelEncoder

from data_dict import cf2_list, cf3_list, data_url, ml_data_url


def dprep_train_set():
    train = pd.read_csv(data_url)

    lbl_cf2, lbl_cf3 = LabelEncoder(), LabelEncoder()

    lbl_cf2.fit(list(cf2_list.keys()))
    lbl_cf3.fit(list(cf3_list.keys()))

    train['cat_feat2'] = lbl_cf2.transform(train['cat_feat2'])
    train['cat_feat3'] = lbl_cf3.transform(train['cat_feat3'])

    train.to_csv(ml_data_url, index=False)
    with open('ml_data/le_cf2.pickle', "wb") as pickle_out:
        pickle.dump(lbl_cf2, pickle_out)
    with open('ml_data/le_cf3.pickle', "wb") as pickle_out:
        pickle.dump(lbl_cf3, pickle_out)
    print('Done!')


def mldata_add(ctx):
    tmp = ctx.copy()
    with open('ml_data/le_cf2.pickle', "rb") as pickle_in:
        lbl_cf2 = pickle.load(pickle_in)
    with open('ml_data/le_cf3.pickle', "rb") as pickle_in:
        lbl_cf3 = pickle.load(pickle_in)

    tmp[4] = lbl_cf2.transform(tmp[4])
    tmp[5] = lbl_cf3.transform(tmp[5])
    return tmp


if __name__ == '__main__':
    print('Testing..')
    dprep_train_set()
