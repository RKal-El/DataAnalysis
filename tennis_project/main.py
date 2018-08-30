import pandas
import matplotlib.pyplot as plt


def import_data_from_csv_to_variable():
    path_to_data = 'dataset/tennis.csv'
    return pandas.read_csv(path_to_data, encoding='ISO-8859-1')


def top_5(data, column_of_names):
    column_name = input('\nName column for data which will be generated (top 5 of what):\n')
    count_number_of_wins = pandas.DataFrame(data=0, index=set(data[column_of_names]), columns=[column_name])
    for name in data[column_of_names]:
        count_number_of_wins.loc[name] += 1
    count_number_of_wins.sort_values(by=[column_name], inplace=True, ascending=False)
    return count_number_of_wins.iloc[:5]


def plot_5(winners):
    x = list(winners.index.values)
    y = list(winners.iloc[:, 0])
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, width=0.25)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
    for index in range(5):
        plt.text(x=index,
                 y=y[index] / 2,
                 s=y[index],
                 fontsize=15,
                 horizontalalignment='center')
    title_of_plot = input('\nWhat is the title of plot?\n')
    plt.title(title_of_plot)
    title_of_image = input('\nWhat is going to be name of image for plot?\n')
    title_of_image += '.png'
    plt.savefig(title_of_image, dpi=600, format='png')
    plt.show()


tennis_data = import_data_from_csv_to_variable()
top_5_victorious_players = top_5(tennis_data, 'WINNER')
plot_5(top_5_victorious_players)
top_5_runner_up_players = top_5(tennis_data, 'RUNNER UP')
plot_5(top_5_runner_up_players)
