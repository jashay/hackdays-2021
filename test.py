import pandas as pd 


df = pd.read_csv('Recipe_ingredients.csv')

df = df.drop(['Ingredients','Image_Name'],axis = 1)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.rename(columns = {"Cleaned_Ingredients": "Ingredients"})

df.to_csv('Recipes.csv')

print(df.head())
