import pandas as pd
import plotly.express as px

# Load dataset
url = "https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/married_data_on_Climate_Smart_Agriculture.csv"
df = pd.read_csv(url)

# 1. Bar - Level of education
fig1 = px.bar(df['Level of education'].value_counts().reset_index(),
              x='index', y='Level of education',
              title="Distribution of Level of Education among Married Household Heads",
              labels={'index': 'Level of Education', 'Level of education': 'Count'},
              color='index',
              color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.show()

# 2. Histogram - Age
fig2 = px.histogram(df, x='Age',
                    nbins=20, title="Distribution of Age among Married Household Heads",
                    color_discrete_sequence=['skyblue'])
fig2.update_layout(xaxis_title="Age", yaxis_title="Frequency")
fig2.show()

# 3. Bar - Access to training
fig3 = px.bar(df['Access to training'].value_counts().reset_index(),
              x='index', y='Access to training',
              title="Access to Training among Married Households",
              labels={'index': 'Access to Training', 'Access to training': 'Count'},
              color='index',
              color_discrete_sequence=px.colors.qualitative.Set2)
fig3.show()

# 4. Box - Age by Level of education
fig4 = px.box(df, x='Level of education', y='Age',
              title="Age Distribution by Level of Education",
              color='Level of education',
              color_discrete_sequence=px.colors.qualitative.Prism)
fig4.update_layout(xaxis_title="Level of Education", yaxis_title="Age")
fig4.show()
