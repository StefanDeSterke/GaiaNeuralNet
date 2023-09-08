import pandas as pd

originalDataframe = pd.read_csv('C:\\Users\\hml-7455\\Desktop\\Programming\\Python\\Gaia interpreter\\gaia-1 medium.csv', header=0, sep=r'\s*,\s*', engine='python', comment='#')
filteredDataframe = originalDataframe[["teff_gspphot", "lum_flame"]]
filteredDataframe.dropna(axis=0, how="any",inplace=True)
filteredDataframe.to_csv("gaia-1 medium filtered.csv", index=False)