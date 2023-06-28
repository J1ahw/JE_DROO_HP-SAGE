import pandas as pd
import os
import pdfplumber
from pprint import pprint
from datetime import datetime as dt

dates = []
filenames = []
grosses = []
payes = []
ernis = []
eenis = []
erps = []
eeps = []
sls = []


for root,dirs,files in os.walk('WAGE'):
        for f in files:
            filepath = f'{root}/{f}'
            filenames.append(filepath)

for f in filenames:
    with pdfplumber.open(f) as pdf:
         for page in pdf.pages:
              table = page.extract_text()
              n = len(table.split('Process Date:'))
              m = 1
              list1 = []
              while m < n:
                   list1.append(m)
                   m+=1
              for m in list1:
                   date = table.split('Process Date:')[m].split(' ')[1]
                   gross = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[1].replace(',','')
                   paye = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[4]
                   eeni = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[5]
                   erni = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[6]
                   eep = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[7]
                   erp = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[8]
                   sl = table.split('Process Date:')[m].split('Process Date Total')[1].split(' ')[9]
                   dates.append(date)
                   grosses.append(gross)
                   payes.append(paye)
                   eenis.append(eeni)
                   ernis.append(erni)
                   eeps.append(eep)
                   erps.append(erp)
                   sls.append(sl)
                   
df = pd.DataFrame({
                    'DATE': dates,
                    'GROSS': grosses,
                    'PAYE': payes,
                    'NI\'EE': eenis,
                    'EMPLOYEE PENSIONS': eeps,
                    'NI\'ER': ernis,
                    'EMPLOYER PENSIONS': erps,
                    'STUDENT LOAN': sls})

for col in df:
     if col != 'DATE':
          df[col] = pd.to_numeric(df[col])
     else:
          df[col].astype('string')

df['NET'] = df['GROSS']-df['PAYE']-df['NI\'EE']-df['EMPLOYEE PENSIONS']
df['EMPLOYMENT ALLOWENCE'] = - df['NI\'ER']
if df['STUDENT LOAN'].sum() != 0:
     print('STUDENT LOAN!!!!!!!!!!!!')

final_df = df[['DATE','GROSS','PAYE','NI\'EE','EMPLOYEE PENSIONS','NET','NI\'ER','EMPLOYMENT ALLOWENCE','EMPLOYER PENSIONS','STUDENT LOAN']]
final_df.to_excel('result.xlsx', header=True, index= False)