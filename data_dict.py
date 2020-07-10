data_url = 'data/data_all.csv'
ml_data_url = 'ml_data/data_train.csv'
test_ml_data_url = 'ml_data/X_test.csv'

fplot_url = 'img/fplot'
pr_plot_url = 'img/pr_plot'

cf2_list = {
    'x1': 'cf2 value 1',
    'x2': 'cf2 value 2',
    'x3': 'cf2 value 3',
    'x4': 'cf2 value 4',
    'x5': 'cf2 value 5',
    'x6': 'cf2 value 6',
    'x7': 'cf2 value 7',
    'x8': 'cf2 value 8',
    'x9': 'cf2 value 9',
    'x10': 'cf2 value 10',
    'x11': 'cf2 value 11',
    'x12': 'cf2 value 12',
    'x13': 'cf2 value 13'
}

cf3_list = {
    'y1': 'cf3 value 1',
    'y2': 'cf3 value 2',
    'y3': 'cf3 value 3',
    'y4': 'cf3 value 4',
    'y5': 'cf3 value 5',
    'y6': 'cf3 value 6',
    'y7': 'cf3 value 7',
    'y8': 'cf3 value 8',
    'y9': 'cf3 value 9',
    'y10': 'cf3 value 10',
}


def get_str_from_dict(dic):
    s = ''
    for x, y in dic.items():
        s += x + ':    ' + y + '\n'
    return s


if __name__ == '__main__':
    print('Testing is coming...')
