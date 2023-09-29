import pandas as pd
df = pd.read_excel("./Data/ExternalData/dummy_uts.xlsx")
df['Gender'].replace('M','Male',inplace=True)
df['Gender'].replace('F','Female',inplace=True)
x = df.groupby(['Programme Name','Gender'])
out = x['Gender'].value_counts()
out = pd.DataFrame(out)
cols = list(set(df['Gender']))
ind = list(set(df['Programme Name']))
data = pd.DataFrame(data = out,columns = cols,index = ind)
for idx, row in out.iterrows():
    data.loc[idx] = row['count'] if row['count'] else "NAN"

for i in ind:
    data.loc[i,'Total'] = data.loc[i,:].sum()
print(data)
data.to_excel("report2.xlsx")
