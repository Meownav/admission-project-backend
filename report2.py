import pandas as pd
df = pd.read_excel("./Data/ExternalData/dummy_uts.xlsx")
x = df.groupby('Programme Name')
out = x['Gender'].value_counts()
out = pd.DataFrame(out)
cols = list(set(df['Gender']))
ind = list(set(df['Programme Name']))
data = pd.DataFrame(data = out,columns=cols,index=ind)
data['Male']+=data['M']
data['Female']+=data['F']
data.drop(['M','F'],axis='columns',inplace=True)
for idx, row in out.iterrows():
    if idx[1] in ['Male','Female']:
        data.loc[idx] = row['count'] if row['count'] else "NAN"
data.to_excel("report2.xlsx")
print(data)
