import pandas as pd

# Load the original dataset
df = pd.read_csv('original_data.csv')
df = df.drop(['No', 'NRSC','GSI','New','Building_I','Road_impac','Impact_Agr','Length', 'Width', 'Area', 'Specific_r','%increase', 'Remarks','RASTERVALU','Reclass_Sl'], axis=1)

# Define a mapping of districts to numerical values
district_mapping = {
    'Ernakulam': 0,
    'Idukki': 1,
    'Kannur': 2,
    'Kasaragod': 3,
        'Kollam': 4,
        'Kottayam': 5,
        'Kozhikode': 6,
        'Malappuram': 7,
        'Palakkad': 8,
        'Pathanamthitta': 9,
        'Thiruvananthapuram': 10,
        'Thrissur': 11,
        'Wayanad': 12   
}
# Define a mapping of land use to numerical values
land_use_mapping = {
    'BRF':1,
    'BRG':2,
    'BRO':3,
    'BRS':4,
    'BSF':5,
    'BSG':6,
    'BSL':7,
    'BSO':8,
    'BSS':9,
    'BUI':10,
    'CSB':11,
    'CSV':12,
    'FCP':13,
    'FDN':14,
    'FMP':15,
    'FNO':16,
    'GMC':17,
    'GNA':18,
    'QUA':19,
    'QUU':20,
    'ROA':21,
    'RUB':22,
    'SNA':23,
    'SPL':24,
    'TEA':25,
}
type_of_slide = {
    'DF':1,
    'RF':2,
    'SS':3
}

# Map the 'Land Use' column to numerical values using the mapping
df['LU_2010'] = df['LU_2010'].map(land_use_mapping)
df['LU_2018'] = df['LU_2018'].map(land_use_mapping)
df['Type_of_sl']=df['Type_of_sl'].map(type_of_slide)

# Map the 'District' column to numerical values using the mapping
df['District'] = df['District'].map(district_mapping)

# Save the modified dataset
df.to_csv('encoded_data.csv', index=False)
