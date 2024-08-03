import plotly.express as px
import pandas as pd

df = px.data.gapminder()

# Remove old data
df = df[df.year >= 2007]

df = df.rename(columns = {'lifeExp':'Life Expectancy',
                          'pop':'Population',
                          'gdpPercap':'GDP Per Capita'})
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

df['iso_alpha'] = df['iso_alpha'].astype('string')
print(df.info())
print(df)