import pandas as pd

from data_dict import cf2_list, cf3_list, data_url, ml_data_url
from ml_data import mldata_add
import seaborn as sns
import matplotlib.pyplot as plt


def data_add(ctx):
    new_str = pd.DataFrame([ctx])
    new_str.to_csv(data_url, mode='a', index=False, header=False)
    mldata_add(new_str).to_csv(ml_data_url, mode='a', index=False, header=False)


def data_size():
    return str(len(pd.read_csv(data_url).index))


def data_show_stat():
    tmp = pd.read_csv(data_url)
    wins = tmp['Result'].sum()*100/tmp['Result'].count()
    nf4_mean = tmp['num_feat4'].mean()
    ratio_nf5 = tmp['num_feat5'] / tmp['num_feat1']
    m_r = ratio_nf5.mean()
    return wins, nf4_mean, m_r


def data_show_stat_ext(target):
    tmp = pd.read_csv(data_url)
    tmp['mean_value'] = tmp['num_feat5'] / tmp['num_feat1']
    try:
        stat_df = pd.DataFrame(tmp.groupby(target)["Result"].mean())
        stat_df['num_feat4'] = tmp.groupby(target)["num_feat4"].mean()
        stat_df['mean_value'] = tmp.groupby(target)["mean_value"].mean()
        stat_df['count'] = tmp.groupby(target)["Result"].count()

        stat_df.sort_values('count', inplace=True, ascending=False)
        return stat_df
    except KeyError:
        print('Wrong target')


def rank_handler(ctx):
    num_feat1 = int(ctx[0])
    try:
        ranks, ctx = ctx[1:num_feat1+1], ctx[num_feat1+1:]
        ranks = [int(item) for item in ranks]
        num_feat2, num_feat3, = pd.Series(ranks).mean(), pd.Series(ranks).max() - pd.Series(ranks).min()
        if ctx[0] is 'm':
            cat_feat1 = 1
            ctx = ctx[1:]
        else:
            cat_feat1 = 0
        return 'ok', (num_feat1, num_feat2, num_feat3, cat_feat1, ctx)
    except ValueError:
        return 'len', []


def content_handler(ctx):
    res, tmp = rank_handler(ctx)
    if res is 'len':
        return 'len', []

    num_feat1, num_feat2, num_feat3, cat_feat1, ctx = tmp

    if len(ctx) != 4:
        return 'len', []

    try:
        num_feat4, num_feat5 = int(ctx[2]), int(ctx[3])
        wins = int(num_feat5/num_feat1 >= 0.50)
    except ValueError:
        return 'err', []

    cat_feat2, cat_feat3 = ctx[0], ctx[1]
    if cat_feat2 not in list(cf2_list.keys()):
        return 'cf2', []

    if cat_feat3 not in list(cf3_list.keys()):
        return 'cf3', []

    return 'ok', [num_feat1, num_feat2, num_feat3, cat_feat1, cat_feat2, cat_feat3, num_feat4, num_feat5, wins]


def content_handler_ai(ctx):
    res, tmp = rank_handler(ctx)
    if res is 'len':
        return 'len', []

    num_feat1, num_feat2, num_feat3, cat_feat1, ctx = tmp

    if len(ctx) != 2:
        return 'len', []

    cat_feat2, cat_feat3 = ctx[0], ctx[1]
    if cat_feat2 not in list(cf2_list.keys()):
        return 'cf2', []
    if cat_feat3 not in list(cf3_list.keys()):
        return 'cf3', []
    return 'ok', [num_feat1, num_feat2, num_feat3, cat_feat1, cat_feat2, cat_feat3]


def content_check(ctx, mode):
    if mode is 'a':
        fl, ctx_list = content_handler(ctx)
        if fl is not 'ok':
            return fl
        return ctx_list

    elif mode is 'p':
        fl, ctx_list = content_handler_ai(ctx)
        if fl is not 'ok':
            return fl
        return ctx_list
    else:
        print('Wrong mode.')


def get_dist(feat_name, url_plot, url_data=data_url):
    train = pd.read_csv(url_data)
    fig, ax = plt.subplots()
    sns.countplot(train[feat_name], order=train[feat_name].value_counts().index, palette='Set3', ax=ax)
    fig.savefig(url_plot)


def get_prop_plot(feat_name, url_plot, url_data=data_url, target='Result'):
    train = pd.read_csv(url_data)
    fig, ax = plt.subplots()
    prop_plot = train.groupby(feat_name)[target].value_counts(normalize=True).unstack()
    prop_plot = prop_plot.sort_values(by=1, ascending=False)
    prop_plot.plot(kind='bar', stacked='True', color=["#3f3e6fd1", "#85c6a9"], ax=ax)
    plt.legend(('Lose', 'Win'))
    plt.title('Proportion of Win/Lose by cat_feat2', fontsize=12)
    fig.savefig(url_plot)


if __name__ == '__main__':
    print("Testing...")

