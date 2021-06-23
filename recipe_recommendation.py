from queue import PriorityQueue
import pandas as pd
from check_similarity import is_similar

df = pd.read_csv("Final_Recipes.csv")

def make_queue(list_ing_recipe):
    q = PriorityQueue()
    for i in range(len(df["Ingredients"])):
        try:
            score = is_similar(df["Ingredients"].iloc[i], ' '.join(list_ing_recipe))
            q.put((-score, i))
        except:
            #print(df["Ingredients"].iloc[i], ' '.join(list_ing_recipe))
            continue

    lst = [q.get() for _ in range(5)]
    d = {}

    return [(df["Title"].iloc[i[1]],df["Ingredients"].iloc[i[1]]) for i in lst]
    #return [q.get() for _ in range(5)]


print(make_queue(['ground allspice','white wine','white miso','Kosher','Chicken']))

