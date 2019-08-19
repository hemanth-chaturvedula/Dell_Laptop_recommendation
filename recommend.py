import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


class Recommend():
    
    
    def CountFrequency(self,my_list): 
  
        # Creating an empty dictionary  
        freq = {} 
        for item in my_list: 
            if (item in freq): 
                freq[item] += 1
            else: 
                freq[item] = 1
  
        return freq
        
    def train(self,train_df):
        df_tr = train_df

        #Cluster the data
        kmeans = KMeans(n_clusters=12, random_state=0).fit(df_tr)
        labels = kmeans.labels_

        #Glue back to originaal data
        df_tr['clusters'] = labels
        centroids = kmeans.cluster_centers_
        return kmeans,centroids,df_tr

    def predict(self,test,kmeans,df_tr,company,product):

        y_pred = kmeans.predict(test.values)
        freq = self.CountFrequency(y_pred)
        z = None
        for key,value in freq.items():
            if value == max(freq.values()):
                z = key
        df_tr['Company'] = company
        df_tr['Product'] = product
        filtered_data = df_tr.loc[df_tr['clusters'] == z]
        filtered_data = df_tr.loc[df_tr['Company'] == z]
        
        return filtered_data

    def run(self):

        df = pd.read_csv('cleaned_preprocessed_data_new2.csv')
        
        company = df['Company']
        product = df['Product']
        df.drop(['Product','Company'],axis=1,inplace=True)
        train_df , test_df = df.iloc[0:190],df.iloc[190:]
        kmeans,centroids,df_new = self.train(df)
        predicted_data = self.predict(test_df,kmeans,df_new,company,product)
        predicted_data.to_csv('predicted.csv')
        return predicted_data

    
##if __name__ == '__main__':
##    rec = Recommend()
##    pred = rec.run()
##    print('done')
