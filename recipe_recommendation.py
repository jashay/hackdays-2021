from queue import PriorityQueue
import pandas as pd
from check_similarity import is_similar


def make_queue(list_ing_recipe):
    df = pd.read_csv("Final_Recipes_v2.csv")
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

    def get_missing(lst1, lst2):
        for w in lst1:
            if w not in lst2:
                yield w

    for pair in lst:
        index = pair[1]
        d["title"] = df["Title"].iloc[index]
        d["ingredients"] = df["Ingredients"].iloc[index]
        d["recipe"] = df["Recipe"].iloc[index]
        d["missing"] = list(get_missing(list_ing_recipe, df["Ingredients"].iloc[index].split()))
    return d

    #return [q.get() for _ in range(5)]


print(make_queue(['allspice','white wine','white miso','Kosher','Chicken']))
