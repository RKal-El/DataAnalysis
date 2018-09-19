import pandas


def import_dataset():
    path = 'dataset/telco_customer.csv'
    return pandas.read_csv(path)


telco_customer_dataset = import_dataset()
