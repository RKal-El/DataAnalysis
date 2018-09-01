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


def top_3_per_tournament(data, column_of_names):
    table_player_tournament = pandas.DataFrame(0, index=set(data[column_of_names]), columns=set(data.TOURNAMENT))
    table_player_tournament.drop(columns=['Australian Open (Jan)', 'Australian Open (Dec)'], inplace=True)
    for index, row in data.iterrows():
        tournament, player = row['TOURNAMENT'], row[column_of_names]
        if (tournament != 'Australian Open (Jan)') & (tournament != 'Australian Open (Dec)'):
            table_player_tournament[tournament].loc[player] += 1

    us_open = table_player_tournament['U.S. Open'].copy()
    australian_open = table_player_tournament['Australian Open'].copy()
    french_open = table_player_tournament['French Open'].copy()
    wimbledon = table_player_tournament['Wimbledon'].copy()

    us_open.sort_values(inplace=True, ascending=False)
    australian_open.sort_values(inplace=True, ascending=False)
    french_open.sort_values(inplace=True, ascending=False)
    wimbledon.sort_values(inplace=True, ascending=False)

    return us_open[:3], australian_open[:3], french_open[:3], wimbledon[:3]


def plot_top_3_per_tournament(add_to_the_title, *arg):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Top 3 ' + add_to_the_title + ' per tournament', fontsize=16)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, hspace=0.4, wspace=0.3)
    for x_axis in range(2):
        for y_axis in range(2):
            if(x_axis == 0) & (y_axis == 0):
                argument = 0
            elif(x_axis == 0) & (y_axis == 1):
                argument = 1
            elif (x_axis == 1) & (y_axis == 0):
                argument = 2
            else:
                argument = 3
            x_values = list(arg[argument].index.values)
            y_values = list(arg[argument].iloc[:])
            axes[x_axis, y_axis].bar(x_values, y_values, width=0.25)
            axes[x_axis, y_axis].set_title(arg[argument].name, fontsize=14)
            for index in range(len(x_values)):
                axes[x_axis, y_axis].text(x=index,
                                          y=y_values[index] / 2,
                                          s=y_values[index],
                                          fontsize=12, horizontalalignment='center')
    title_of_image = input('\nWhat is going to be name of image?\n')
    title_of_image += '.png'
    plt.savefig(title_of_image, dpi=600, format='png')
    plt.show()


tennis_data = import_data_from_csv_to_variable()
top_5_victorious_players = top_5(tennis_data, 'WINNER')
plot_5(top_5_victorious_players)
top_5_runner_up_players = top_5(tennis_data, 'RUNNER UP')
plot_5(top_5_runner_up_players)

top_3_us_win, top_3_aus_win, top_3_fra_win, top_3_wim_win = top_3_per_tournament(tennis_data, 'WINNER')
plot_top_3_per_tournament('winners', top_3_us_win, top_3_aus_win, top_3_fra_win, top_3_wim_win)
top_3_us_run, top_3_aus_run, top_3_fra_run, top_3_wim_run = top_3_per_tournament(tennis_data, 'RUNNER UP')
plot_top_3_per_tournament('runner up', top_3_us_run, top_3_aus_run, top_3_fra_run, top_3_wim_run)
