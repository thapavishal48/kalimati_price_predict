import pandas as pd
import numpy as np
import pickle


class TrainingTesting:

    def __init__(self, data_processing):
        self.data_processing = data_processing

        pickle_off = open("/home/lenevo/kalimati_price_predict/home/data/final_W.pickle", 'rb')
        final_W = pickle.load(pickle_off)

        pickle_off_X_test = open("/home/lenevo/kalimati_price_predict/home/data/X_test.pickle", 'rb')
        X_test = pickle.load(pickle_off_X_test)

        pickle_off_y_test = open("/home/lenevo/kalimati_price_predict/home/data/y_test.pickle", 'rb')
        y_test = pickle.load(pickle_off_y_test)

        y_ = X_test.dot(final_W)

        y1 = pd.DataFrame(y_test)
        y1.columns = ['Date', 'Items', 'Real Price']
        y2 = pd.DataFrame(y_)
        y2.columns = ['Estimated Price']
        y3 = pd.concat([y1, y2], axis=1)

        self.df0 = self.denormalize('Real Price', 'Average', self.data_processing.data1, y3)
        self.df1 = self.denormalize('Estimated Price', 'Average', self.data_processing.data1, self.df0)

        self.df1['Date'] = pd.to_datetime(self.df1['Date'])
        self.df1.set_index('Date', inplace=True)

    def denormalize(self, columns_name, min_max_column, dataframe1, dataframe2):
        newnormalized_df = []
        cols = [columns_name]
        unique_veglist = np.unique(self.data_processing.data1['Items'].to_numpy())
        for i in unique_veglist:
            max_value = dataframe1[dataframe1.Items == i][min_max_column].max()
            min_value = dataframe1[dataframe1.Items == i][min_max_column].min()

            item_df = dataframe2[dataframe2.Items == i]

            item_df[cols] = ((item_df[cols]) * (max_value - min_value)) + (min_value)

            newnormalized_df.append(item_df)

        newnormalized_df = pd.concat(newnormalized_df)
        return newnormalized_df
