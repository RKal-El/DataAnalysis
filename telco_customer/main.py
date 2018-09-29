import pandas
import matplotlib.pyplot as plt


def import_dataset():
    path = 'dataset/telco_customer.csv'
    return pandas.read_csv(path)


def count_female_and_male_customer(dataset):
    column_gender = dataset['gender']
    female = male = 0
    for gender in column_gender:
        if gender == 'Male':
            male += 1
        else:
            female += 1
    return female, male


def plot_female_and_male_customer(females, males):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.suptitle('Comparison of number males and females customers', fontsize=14)
    x = ['Females', 'Males']
    y = [females, males]
    plt.bar(x, y, width=0.35, color=['orchid', 'royalblue'])
    for gender in range(2):
        plt.text(x=gender, y=y[gender] / 2, s=y[gender],
                 fontsize=12, horizontalalignment='center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.savefig('Number of males and females customers.png', dpi=600)
    plt.show()


telco_customer_dataset = import_dataset()

number_of_females, number_of_males = count_female_and_male_customer(telco_customer_dataset)
plot_female_and_male_customer(number_of_females, number_of_males)
