import pandas
import matplotlib.pyplot as plt


def import_data_from_csv_to_variable():
    path_to_data = 'dataset/tennis.csv'
    return pandas.read_csv(path_to_data, encoding='ISO-8859-1')


def top_5_overall(data, column_of_names):
    column_name = input('\nName column for data which will be generated (top 5 of what):\n')
    count_number_of_wins = pandas.DataFrame(data=0, index=set(data[column_of_names]), columns=[column_name])
    for name in data[column_of_names]:
        count_number_of_wins.loc[name] += 1
    count_number_of_wins.sort_values(by=[column_name], inplace=True, ascending=False)
    return count_number_of_wins.iloc[:5]


def plot_top_5_overall(data):
    x = list(data.index.values)
    y = list(data.iloc[:, 0])
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
    title_of_image = input('\nWhat is going to be name of image?\n')
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


def rearrange_data_multiple_indices(tennis_dataset):
    array_of_indices = [['Australian Open', 'U.S. Open', 'French Open', 'Wimbledon'],
                        ['Winner', 'Runner Up']]
    multiple_column_indices = pandas.MultiIndex.from_product(array_of_indices)
    table = pandas.DataFrame(index=set(tennis_dataset.YEAR),
                             columns=multiple_column_indices)
    for index, data in tennis_dataset.iterrows():
        if(data[1] == 'Australian Open (Dec)') | (data[1] == 'Australian Open (Jan)'):
            continue
        table[data[1], 'Winner'].loc[data[0]] = data[2]
        table[data[1], 'Runner Up'].loc[data[0]] = data[3]
    return table


def top_player_per_tournament_in_row(dataset):
    top_players = pandas.DataFrame(columns=['Tournament', 'Win/Lose', 'Player', 'In the row', 'First year', 'Last year'])
    starting_year = 1877
    interval = 0
    for index, column in enumerate(dataset.columns):
        temporary_player_statistics = [column[0], column[1], '', 0]
        best_player_statistics = [column[0], column[1], '', 0]
        off_set = 0
        for name in dataset[column]:
            if not pandas.isnull(name):
                if temporary_player_statistics[2] != name:
                    if best_player_statistics[3] < temporary_player_statistics[3]:
                        best_player_statistics = temporary_player_statistics.copy()
                        interval = off_set
                    temporary_player_statistics[2] = name
                    temporary_player_statistics[3] = 1
                else:
                    temporary_player_statistics[3] += 1
            off_set += 1
        best_player_statistics.append(starting_year + interval - best_player_statistics[3])
        best_player_statistics.append(starting_year + interval - 1)
        top_players.loc[index] = best_player_statistics
    return top_players


def plot_best_player_in_the_row(best_players):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Players with the most win/lose finales in the row', fontsize=16)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, hspace=0.4, wspace=0.3)
    for row in range(2):
        for column in range(2):
            axes[row, column].bar(best_players['Player'][:2], best_players['In the row'][:2], width=0.3, color='darkorange', zorder=2)
            axes[row, column].grid(axis='y', color='darkmagenta', zorder=0, linewidth=2)
            axes[row, column].set_title(best_players['Tournament'][0], fontsize=14)
            axes[row, column].set_ylim((0, 8))
            for place in range(2):
                axes[row, column].text(x=place,
                                       y=0.2,
                                       s=best_players['First year'][place],
                                       fontsize=12, horizontalalignment='center')
                axes[row, column].text(x=place,
                                       y=best_players['In the row'][place] - 0.5,
                                       s=best_players['Last year'][place],
                                       fontsize=12, horizontalalignment='center')
                axes[row, column].text(x=place,
                                       y=best_players['In the row'][place] / 2.2,
                                       s=best_players['Win/Lose'][place],
                                       fontsize=12, horizontalalignment='center')
            best_players.drop([0, 1], inplace=True)
            best_players.index = range(len(best_players.index))
    title_of_image = input('\nWhat is going to be name of image?\n')
    title_of_image += '.png'
    plt.savefig(title_of_image, dpi=600, format='png')
    plt.show()


def lucky_and_unlucky_players(data):
    set_of_winners = set(data.WINNER)
    set_of_runner_up = set(data['RUNNER UP'])
    only_win_if_in_final = set_of_winners - set_of_runner_up
    only_lose_if_in_final = set_of_runner_up - set_of_winners
    return pandas.DataFrame({'Only win': [len(only_win_if_in_final)], 'Only lose': [len(only_lose_if_in_final)]})


def plot_lucky_and_unlucky_players(dictionary_data):
    x = list(dictionary_data.columns)
    y = list(dictionary_data.loc[0])
    plt.figure(figsize=(10, 7))
    plt.bar(x, y, width=0.4)
    for index in range(2):
        plt.text(x=index,
                 y=y[index] / 2,
                 s=y[index],
                 fontsize=15,
                 horizontalalignment='center')
    plt.title('Number of player who came to the final and only had won (lucky ones) or only had lost (unlucky ones)')
    plt.savefig('Number of lucky players vs number of unlucky players.png', dpi=600, format='png')
    plt.show()


def top_5_finalists(dataset):
    top_5 = pandas.DataFrame(columns=['Overall', 'Win', 'Percent_win', 'Lose', 'Percent_lose'], index=set(dataset['WINNER']).union(set(dataset['RUNNER UP'])))
    list_of_winners = list(dataset['WINNER'])
    list_of_losers = list(dataset['RUNNER UP'])
    for name in top_5.index:
        top_5['Win'].loc[name] = list_of_winners.count(name)
        top_5['Lose'].loc[name] = list_of_losers.count(name)
        top_5['Overall'].loc[name] = top_5['Win'].loc[name] + top_5['Lose'].loc[name]
        top_5['Percent_win'].loc[name] = round(top_5['Win'].loc[name] / top_5['Overall'].loc[name], 2)
        top_5['Percent_lose'].loc[name] = round(1 - top_5['Percent_win'].loc[name], 2)
    top_5.sort_values(by=['Overall'], inplace=True, ascending=False)
    return top_5.iloc[:5]


def plot_top_5_finalists(data):
    data.sort_values(by=['Percent_win'], inplace=True, ascending=False)
    ratio_win_lose = plt.figure(figsize=(12, 5))
    subplot_111 = ratio_win_lose.add_subplot(111)
    bar_width = 0.3
    x = list(data.index.values)
    y_win = list(data['Percent_win'])
    y_lose = list(data['Percent_lose'])
    y_win_number = list(data['Win'])
    y_lose_number = list(data['Lose'])
    bar_win = subplot_111.bar(x, y_win, bar_width, color='seagreen')
    bar_lose = subplot_111.bar(x, y_lose, bar_width, color='orangered', bottom=y_win)
    subplot_111.set_title('Ratio of won and lost finales among 5 players with most finales', fontsize=14)
    for index in range(5):
        plt.text(x=x[index],
                 y=y_win[index] / 2,
                 s=y_win_number[index],
                 fontsize=13,
                 horizontalalignment='center')
        plt.text(x=x[index],
                 y=y_lose[index] / 2 + y_win[index],
                 s=y_lose_number[index],
                 fontsize=13,
                 horizontalalignment='center')
    plt.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9)
    plt.legend((bar_win, bar_lose), ('Victories', 'Defeats'), loc=(1.02, 0.45), fontsize=12)
    plt.savefig('Ratio between victories and defeats among top 5 finalists', dpi=600)
    plt.show()


tennis_data = import_data_from_csv_to_variable()

top_5_winner_players_overall = top_5_overall(tennis_data, 'WINNER')
plot_top_5_overall(top_5_winner_players_overall)

top_5_runner_up_players_overall = top_5_overall(tennis_data, 'RUNNER UP')
plot_top_5_overall(top_5_runner_up_players_overall)

top_3_us_win, top_3_aus_win, top_3_fra_win, top_3_wim_win = top_3_per_tournament(tennis_data, 'WINNER')
plot_top_3_per_tournament('winners', top_3_us_win, top_3_aus_win, top_3_fra_win, top_3_wim_win)

top_3_us_run, top_3_aus_run, top_3_fra_run, top_3_wim_run = top_3_per_tournament(tennis_data, 'RUNNER UP')
plot_top_3_per_tournament('runner up', top_3_us_run, top_3_aus_run, top_3_fra_run, top_3_wim_run)

index_year_column_tournament_winner_loser = rearrange_data_multiple_indices(tennis_data)
best_player_in_the_row = top_player_per_tournament_in_row(index_year_column_tournament_winner_loser)
plot_best_player_in_the_row(best_player_in_the_row)

only_win_lose_finalists = lucky_and_unlucky_players(tennis_data)
plot_lucky_and_unlucky_players(only_win_lose_finalists)

players_with_the_most_finales = top_5_finalists(tennis_data)
plot_top_5_finalists(players_with_the_most_finales)
