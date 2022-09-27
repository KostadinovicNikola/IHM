


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
import numpy as np

if __name__=="__main__":
    #Load csv
    df = pd.read_csv("./logs/data.csv" , delimiter=";")
    # Display the data with seaborn
    #sns.lineplot(...) sns.barplot(...) etc.
    x ,y  = [],[]
    for j in [16, 25, 36]:
        x.append([i for i in range(df.shape[0]) if df.iloc[i,6] == j and df.iloc[i,2] == df.iloc[i,3]])
        y.append(sum(df.iloc[x[len(x)-1],4])/ len(x[len(x)-1]))

    sns.barplot( x="mat_size", y="time_taken", data = df,estimator = np.median , hue="condition")
    plt.show()
       # ANOVA test
   # the parameters are data=, dv=, wihtin=, subject=
   #res = pg.rm_anova( ... )
   #print(res)

   # Posthoc test (if necessary)
   # the parameters are data=, dv=, wihtin=, subject=
   #posthocs = pg.pairwise_ttests(dv='Temps_space', within=['Type', 'Nb_obj'], subject='Participant', data=df)
   #pg.print_table(posthocs)
