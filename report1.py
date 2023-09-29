import pandas as pd
df = pd.read_excel("./Data/ExternalData/dummy_uts.xlsx")
x = df.groupby(['Programme Name','Paper Type'])
out = x['Paper Type'].value_counts()
out = pd.DataFrame(out)
cols = list(set(df['Paper Type']))
ind = list(set(df['Programme Name']))
data = pd.DataFrame(data = out,columns=cols,index=ind)
for idx, row in out.iterrows():
    data.loc[idx] = row['count'] if row['count'] else "NAN"

for i in cols:
    data.loc['Total',[i]] = data.loc[:,[i]].sum()
print(data)
data.to_excel("report1.xlsx")
