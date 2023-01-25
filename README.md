# msbk57
#production_countries
df=pd.read_json('data/production_countries.json', lines=True)
df.fillna("",inplace=True)

df = df.values.tolist()
df = pd.DataFrame(df)
print(df)
prod_country = pd.DataFrame()
for (columnName, columnData) in df.items():
    prod_country[str(columnName) + '_prod_country_id_name'] = pd.DataFrame(df[columnName].values.tolist(),columns = ['iso_3166_1'])
    prod_country[str(columnName) + '_prod_country_name'] = pd.DataFrame(df[columnName].values.tolist(),columns = ['name'])
    
country_list =  pd.DataFrame()
country_list['0_prod_country_name'] = copy.deepcopy(prod_country.iloc[:,1])

country_list = country_list.drop_duplicates()
country_list["prod_country_id"] = np.arange(len(country_list)) + 1
db.store(country_list, "country_list")

prod_country = prod_country.iloc[:,:2]
prod_country = pd.merge(prod_country, country_list, on="0_prod_country_name")

df=pd.read_csv('data/un_codes.csv',on_bad_lines='skip',sep=';')  
df.fillna("",inplace=True)
prod_country = pd.merge(prod_country, df, on="0_prod_country_id_name")

db.store(prod_country, "prod_country")
