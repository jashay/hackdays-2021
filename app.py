from flask import Flask, render_template, request
#from recipe_recommendation import make_queue
from queue import PriorityQueue
import pandas as pd
from check_similarity import is_similar
from collections import defaultdict
from multiprocessing import Pool
from object_detection import *
import numpy as np


#lst_in = []

print("reading pandas")
df = pd.read_csv("Final_Recipes_v2.csv")
print("READ")
q = PriorityQueue()

def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def modded_make_queue(df):
    for i in range(len(df["Ingredients"])):
        print(df["Ingredients"].iloc[i])
        score = is_similar(df["Ingredients"].iloc[i], ' '.join(lst_in))
        print(score)
        q.put((-score, i))
    return df


def make_queue(list_ing_recipe):
    #global q
    #global lst_in
    #lst_in = list_ing_recipe
    print("making queue")

    q = PriorityQueue()

    for i in range(len(df["Ingredients"].dropna())):
        try:
            score = is_similar(df["Ingredients"].iloc[i], ' '.join(list_ing_recipe))
            print(score)
            q.put((-score, i))
        except:
            continue

    #parallelize_dataframe(df, modded_make_queue)

    lst = [q.get() for _ in range(5)]
    q = PriorityQueue()
    print(lst)
    res = []


    def get_missing(lst1, lst2):
        for w in lst1:
            if w.lower() not in list(map(lambda x: x.lower,lst2)):
                yield w

    for pair in lst:
        index = pair[1]
        d = {}
        d["title"]=df["Title"].iloc[index]
        d["ingredients"]=df["Ingredients"].iloc[index]
        d["recipe"]=df["Instructions"].iloc[index]
        d["missing"]=list(get_missing(df["Ingredients"].iloc[index].split(), list_ing_recipe))
        res.append(d)
    return res

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route('/', methods=['post', 'get'])
def home():
    message = ''
    success=False
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        inp = get_labels(file1.read())
        print("fn call")
        x = make_queue(inp)
        print("done")
        message = x
        success=True

    return render_template('index.html', success=success, resp=message)

if __name__ == "__main__":
    app.run(debug=True)
