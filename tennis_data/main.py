import pandas
import matplotlib.pyplot as plt
from collections import Counter


def import_data_from_csv_to_variable():
    path_to_data = 'dataset/tennis.csv'
    return pandas.read_csv(path_to_data, encoding='ISO-8859-1')


def top_5_winners_overall(data):
    count_number_of_wins = {}
    for name in data.WINNER:
        if name in count_number_of_wins:
            count_number_of_wins[name] += 1
        else:
            count_number_of_wins[name] = 1
    return dict(Counter(count_number_of_wins).most_common(5))


def plot_5_winners_overall(winners):
    plt.bar(range(len(winners)), list(winners.values()), tick_label=list(winners.keys()))
    plt.show()


tennis_data = import_data_from_csv_to_variable()


top_5_winners = top_5_winners_overall(tennis_data)
plot_5_winners_overall(top_5_winners)
