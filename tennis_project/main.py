import pandas
import matplotlib.pyplot as plt


def import_data_from_csv_to_variable():
    path_to_data = 'dataset/tennis.csv'
    return pandas.read_csv(path_to_data, encoding='ISO-8859-1')


def top_5_winners_overall(data):
    count_number_of_wins = pandas.DataFrame(data=0, index=set(data.WINNER), columns=['victories'])
    for name in data.WINNER:
        count_number_of_wins.loc[name] += 1
    count_number_of_wins.sort_values(by=['victories'], inplace=True, ascending=False)
    return count_number_of_wins.iloc[:5]


def plot_5_winners_overall(winners):
    winners.reset_index(inplace=True)
    winners.rename(columns={'index': 'players'}, inplace=True)
    x = list(winners['players'])
    y = list(winners['victories'])

    plt.figure(figsize=(10, 5))
    plt.bar(x, y, width=0.25)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
    for index in range(len(winners)):
        plt.text(x=index,
                 y=winners['victories'].iloc[index] / 2,
                 s=winners['victories'].iloc[index],
                 fontsize=15,
                 horizontalalignment='center')
    plt.title('Top 5 players with the most victories')
    plt.show()


tennis_data = import_data_from_csv_to_variable()

top_5_winners = top_5_winners_overall(tennis_data)
plot_5_winners_overall(top_5_winners)
