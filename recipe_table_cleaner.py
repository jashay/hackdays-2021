import pandas as pd 
from string import digits
from check_similarity import is_similar
import re
import nltk
from nltk import word_tokenize

df = pd.read_csv('Recipe_ingredients.csv')

user_ingredients = ['salt','red pepper', 'ground allspice','white wine','white miso','Kosher','Chicken']
#user_ingredients2 = ['Chicken','salt','red pepper', 'white wine','white miso','Kosher','ground allspice']


# Removing digits
df["Ingredients"] = df["Ingredients"].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

# Removing Vulgar Functions
df["Ingredients"] = df["Ingredients"].apply(lambda x: ''.join([re.sub("[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞↉]+", "",i) for i in x]))

recipe_ingredients_list = df["Ingredients"]
test_list = df["Ingredients"][0]


remove_words = ["lb.", "Tbsp", "tbsp", "cup", "cups", "medium", "small", "large",
 "tsp", "Tbsp." "tsp.", "pint", "oz.", "gallon", "kg", "liters", " ml ", " mL ", " whole ","round"," s ","stock"]

# Remove weird shit
for i in range(len(df["Ingredients"])):
    print(i)
    for word in remove_words:
        df["Ingredients"].iloc[i] = df["Ingredients"][i].replace(word,"")
    df["Ingredients"].iloc[i] = df["Ingredients"][i].replace("'","").replace(",","").replace("[","").replace("]","").replace(".","")
    x = word_tokenize(df["Ingredients"].iloc[i])
    y = nltk.pos_tag(x)
    Result = [t[0] for t in y if t[1] == "NN" ]
    Result = list(filter(lambda x: x not in remove_words, Result))
    df["Ingredients"].iloc[i] = ' '.join(Result)

user_string = ''

for ingredient in user_ingredients:
    user_string += ' ' + ingredient

df.to_csv("Final_Recipes.csv")

# Edited = nltk.pos_tag(["Hello", "that's", "a", "fat","cat"])

print(recipe_ingredients_list[0])
# meets_threshold = is_similar(user_string, recipe_ingredients_list[0])
