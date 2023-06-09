import pandas as pd
import os
from datetime import datetime
from datetime import timedelta


filenames = []
takings = []
CommissionFee = []
Vat = []
Dates = []
for root, dirs, files in os.walk('CSV'):
    for f in files:
        filepath = f'{root}/{f}'
        filenames.append(filepath)

for i in filenames:
    date = i.split('_')[-2]
    date = datetime.strptime(date,'%Y%m%d') - timedelta(days=2)
    date = date.strftime('%d/%m/%Y')
    df = pd.read_csv(i, header = 1)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    Dates.append(date)
    takings.append(df['Order Value (£)'].sum())
    CommissionFee.append(df['Deliveroo Commission (£)'].sum() + df['Commission / Adjustment VAT (£)'].sum())
    Vat.append(df['Commission / Adjustment VAT (£)'].sum())

new_df = pd.DataFrame({'Date': Dates,
                       'TAKING': takings,
                       'COMM' : CommissionFee,
                       'VAT' : Vat})
new_df['COMM'] = new_df['COMM'] * -1 + 20
new_df['VAT'] = new_df['VAT'] * -1

new_df.to_excel('result.xlsx', index = False, header= True)