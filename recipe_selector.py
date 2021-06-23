import pandas as pd 
from string import digits
from check_similarity import is_similar
import re

df = pd.read_csv('Recipe_ingredients.csv')

user_ingredients = ['salt','red pepper', 'ground allspice','white wine','white miso','Kosher','Chicken']
user_ingredients2 = ['Chicken','salt','red pepper', 'white wine','white miso','Kosher','ground allspice']
recipe_ingredints = df["Ingredients"]

# Removing digits
df["Ingredients"] = df["Ingredients"].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

# Removing Vulgar Functions
df["Ingredients"] = df["Ingredients"].apply(lambda x: ''.join([re.sub("[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞↉]+", "",i) for i in x]))
        
#str = str.replaceAll("(([\\xbc-\\xbe])?)", "")

test_list = recipe_ingredints[2]


remove_words = ["lb.", "Tbsp", "tbsp", "cup", "cups", "medium", "small", "large",
 "tsp", "Tbsp." "tsp.", "pint", "oz.", "gallon", "kg", "liters", "ml", "mL", "whole"]

df["Ingredients"] = df["Ingredients"].apply(lambda x: 'i'.join([word for word in df["Ingredients"] if word not in remove_words])

user_string = ''
recipe_string = ''

for ingredient in user_ingredients:
    user_string += ' ' + ingredient

for ingredient in user_ingredients2:
    recipe_string += ' ' + ingredient

print(user_string, recipe_string)
meets_threshold = is_similar(user_string, recipe_string)
print(meets_threshold)
print(test_list)