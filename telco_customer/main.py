import pandas
import matplotlib.pyplot as plt


def import_dataset():
    path = 'dataset/telco_customer.csv'
    return pandas.read_csv(path)


def data_distribution_plot(dataset):
    fig, axes = plt.subplots(1, 3, figsize=(16, 9))
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, hspace=0.2, wspace=0.3)
    total_charges = convert_to_float(dataset['TotalCharges'])
    seaborn.distplot(dataset['MonthlyCharges'], ax=axes[0])
    seaborn.distplot(total_charges['TotalCharges'], ax=axes[1])
    seaborn.distplot(dataset['tenure'], ax=axes[2])
    names_of_columns = list(dataset.columns)
    for subplot in range(3):
        axes[subplot].grid()
        axes[subplot].set_title(names_of_columns[subplot])
        axes[subplot].set_ylabel('Amount of customers')
        axes[subplot].set_xlabel('Bill')
    plt.savefig('Data distribution.png', dpi=1200)
    plt.show()


def convert_to_float(dataset):
    dataset_with_numbers = pandas.DataFrame()
    for _, data in enumerate(dataset):
        if not (data and (data.isspace())):
            dataset_with_numbers = dataset_with_numbers.append({'TotalCharges': float(data)}, ignore_index=True)
    return dataset_with_numbers.copy()


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
    fig.suptitle('Number of males and females customers', fontsize=14)
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
    plt.savefig('Number of males and females customers.png', dpi=1200)
    plt.show()


def gender_age_customer_division(dataset):
    gender_age_dataset = dataset[['gender', 'SeniorCitizen']].copy()
    '''
    Data representation of customer division: numpy.array
        [[female_senior, female_junior], [male_senior, male_junior]]
    '''
    customers_gender_age = numpy.array([[0, 0], [0, 0]])
    for _, row in gender_age_dataset.iterrows():
        if (row[0] == 'Female') & (row[1] == 1):
            customers_gender_age[0][0] += 1
        elif (row[0] == 'Female') & (row[1] == 0):
            customers_gender_age[0][1] += 1
        elif (row[0] == 'Male') & (row[1] == 1):
            customers_gender_age[1][0] += 1
        else:
            customers_gender_age[1][1] += 1
    return customers_gender_age


def plot_gender_age_customer_division(number_of_customers):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('dimgray')
    fig.suptitle('Representation of customers by gender and senior/junior status', fontsize=16, color='w')
    plt.subplots_adjust(top=0.95, right=0.95, bottom=0.05, left=0.05)
    size = 0.35
    color_map = plt.get_cmap('tab20c')
    outer_colors = color_map(numpy.array([0, 4]))
    inner_colors = color_map(numpy.array([1, 2, 5, 6]))
    labels = ['Females', 'Males', 'Senior females', 'Junior females', 'Senior males', 'Junior males']
    ax.pie(number_of_customers.sum(axis=1), radius=1, colors=outer_colors,
           autopct='%1.1f%%', pctdistance=0.8,
           wedgeprops=dict(width=size, edgecolor='w'))
    ax.pie(number_of_customers.flatten(), radius=1 - size, colors=inner_colors,
           autopct='%1.1f%%', pctdistance=0.75,
           wedgeprops=dict(width=size, edgecolor='w'))
    plt.legend(labels, loc='best')
    plt.savefig("Representation of customers by gender and senior(junior) status.png", dpi=1200, facecolor=fig.get_facecolor())
    plt.show()


def charge_extraction(dataset, dependecies):
    '''
    :parameter dataset: a full dataset of telco customers
    :parameter dependecies: list [gender, SeniorCitizen, Partner, MonthlyCharges(TotalCharges)]
    '''
    dataset_with_dependencies = dataset[dependecies]
    '''
    :variable dataset_set_dependencies: DataFrame: columns: [Dependencies, MonthlyCharges(TotalCharges)]
        values for Dependencies: Senior_Female_with_Partner, Young_Female_with_Partner, Senior_Female_without_Partner, Young_Female_without_Partner,
                                 Senior_Male_with_Partner, Young_Male_with_Partner, Senior_Male_without_Partner, Young_Male_without_Partner
    '''
    dataset_set_dependencies = pandas.DataFrame()

    for index, data in dataset_with_dependencies.iterrows():
        if (data[0] == 'Female') & (data[1] == 1) & (data[2] == 'Yes'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Senior_Female_with_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        elif (data[0] == 'Female') & (data[1] == 0) & (data[2] == 'Yes'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Young_Female_with_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        elif (data[0] == 'Female') & (data[1] == 1) & (data[2] == 'No'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Senior_Female_without_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        elif (data[0] == 'Female') & (data[1] == 0) & (data[2] == 'No'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Young_Female_without_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        elif (data[0] == 'Male') & (data[1] == 1) & (data[2] == 'Yes'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Senior_Male_with_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        elif (data[0] == 'Male') & (data[1] == 0) & (data[2] == 'Yes'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Young_Male_with_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        elif (data[0] == 'Male') & (data[1] == 1) & (data[2] == 'No'):
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Senior_Male_without_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)
        else:
            dataset_set_dependencies = dataset_set_dependencies.append({'Dependencies': 'Young_Male_without_Partner', dependecies[3]: data[3]},
                                                                       ignore_index=True)

    return dataset_set_dependencies


def is_float_is_not_nan(dataset, column):
    if dataset.dtypes[1] != numpy.float:
        dataset[column] = pandas.to_numeric(dataset[column], errors='coerce')
        dataset.dropna(subset=[column], inplace=True)
        dataset_without_nan = dataset.reset_index(drop=True)
        return dataset_without_nan
    else:
        return dataset


def plot_charge(dataset, type_of_charge):
    plt.figure(figsize=(14, 9))
    seaborn.boxplot(x='Dependencies', y=dataset.columns.values[1], data=dataset, showfliers=False)
    plt.subplots_adjust(top=0.95, right=0.95, bottom=0.1, left=0.05)
    plt.xticks(rotation=10)
    image_name = type_of_charge + " charges for females and males with or without partner.png"
    plt.savefig(image_name, dpi=1200)
    plt.show()


telco_customer_dataset = import_dataset()

number_of_females, number_of_males = count_female_and_male_customer(telco_customer_dataset)
plot_female_and_male_customer(number_of_females, number_of_males)

gender_age_customers = gender_age_customer_division(telco_customer_dataset)
plot_gender_age_customer_division(gender_age_customers)

sy_fm_wpwop_monthly_charges = monthly_charges_extraction(telco_customer_dataset, ['gender', 'SeniorCitizen', 'Partner', 'MonthlyCharges'])
sy_fm_wpwop_monthly_charges_without_nan = is_float_is_not_nan(sy_fm_wpwop_monthly_charges, 'MonthlyCharges')
plot_monthly_charges(sy_fm_wpwop_monthly_charges_without_nan, 'Monthly')

sy_fm_wpwop_total_charges = charge_extraction(telco_customer_dataset, ['gender', 'SeniorCitizen', 'Partner', 'TotalCharges'])
sy_fm_wpwop_total_charges_without_nan = is_float_is_not_nan(sy_fm_wpwop_total_charges, 'TotalCharges')
plot_charge(sy_fm_wpwop_total_charges_without_nan, 'Total')
