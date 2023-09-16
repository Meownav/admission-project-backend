import pandas as pd
df = pd.read_excel("./Data/ExternalData/dummy_uts.xlsx")
x = df.groupby(['Programme Name','Paper Type'])
out = x['Paper Type'].value_counts()
out.to_excel("report_output.xlsx")