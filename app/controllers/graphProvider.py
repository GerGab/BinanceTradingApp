import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import io
import base64

def graph(qty = 100,noise = 1,A = 0.5,B = 2,C = 2):
    x = 6* np.random.rand(qty,noise) -3
    y = A * x**2 + B*x+C + np.random.randn(qty,noise)
    x = [value[0] for value in x.tolist()]
    y = [value[0] for value in y.tolist()]
    df = pd.DataFrame({'x':x,'y':y})
    
    with io.BytesIO() as img:
        fig = sns.scatterplot(data = df,x='x',y='y').get_figure()
        fig.savefig(img,format='png')
        plt.clf()
        img.seek(0)
        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

