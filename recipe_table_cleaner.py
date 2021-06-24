import pandas as pd
from string import digits
from check_similarity import is_similar
import re
import nltk
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

df = pd.read_csv('Recipe_ingredients.csv')

user_ingredients = ['salt','red pepper', 'ground allspice','white wine','white miso','Kosher','Chicken']

# Removing digits
df["Ingredients"] = df["Ingredients"].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

# Removing Vulgar Functions
df["Ingredients"] = df["Ingredients"].apply(lambda x: ''.join([re.sub("[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞↉]+", "",i) for i in x]))

#print(df["Ingredients"][0][1:-1].replace(",","").replace(".","").replace("'","").split())
for i in range(len(df["Ingredients"])):
    print(i)
    test = df["Ingredients"][i][1:-1].replace(",","").replace(".","").replace("'","")
    test = nltk.word_tokenize(test)
    test = [word for word in test if word.isalnum()]
    lemma = WordNetLemmatizer()
    test = list(map(lambda x: lemma.lemmatize(x), test))
    words_to_remove = ["lb", "Tbsp", "tbsp", "cup", "cups", "medium", "small", "large", "tsp", "Tbsp" "tsp.", "pint", "oz", "gallon", "kg", "liters", " ml ", "mL", "whole","round","stock", "room", "teperature", "total", "ground", "torn", "piece", "pinch", "freshly"]
    test = list(filter(lambda x: x.lower() not in list(map(lambda x: x.lower(), words_to_remove)), test))
    inter = nltk.pos_tag(test)
    test = [w[0] for w in inter if w[1] in ["NN", "NNP"]]
    df["Ingredients"].iloc[i] = ' '.join(test)


df.to_csv("Final_Recipes_v2.csv")

# Edited = nltk.pos_tag(["Hello", "that's", "a", "fat","cat"])

#print(df["Ingredients"][0])
# meets_threshold = is_similar(user_string, recipe_ingredients_list[0])
