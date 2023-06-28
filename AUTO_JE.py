import pandas as pd
import os
import pdfplumber
from pprint import pprint
from datetime import datetime as dt

takings = []
grosses = []
vats = []
dates1 = []
dates2 = []
filenames = []
months = {'Jan': '01',
          'Feb': '02',
          'Mar': '03',
          'Apr': '04',
          'May': '05',
          'Jun': '06',
          'Jul': '07',
          'Aug': '08',
          'Sep': '09',
          'Oct': '10',
          'Nov': '11',
          'Dec': '12',
          }


for root,dirs,files in os.walk('PDF'):
        for f in files:
            filepath = f'{root}/{f}'
            filenames.append(filepath)

for f in filenames:  
     try:
          with pdfplumber.open(f) as pdf:
               first_page = pdf.pages[0]
               second_page = pdf.pages[1]
               table1 = first_page.extract_tables()
               table2 = second_page.extract_text()
               day = table1[0][0][0].split('-')[1].split(' ')[1]
               if len(day) == 1:
                    day = f'0{day}'
               month = months[table1[0][0][0].split('-')[1].split(' ')[2]]
               year = table1[0][0][0].split('-')[1].split(' ')[3].split('0')[1]
               date = f'{day}/{month}/{year}'
               taking = float(table1[0][3][0].split('Total sales')[1].split('totalling')[1].split(' ')[1].split('£')[2].replace(',','').replace('£',''))
               admin_fee = float(table2.split('(VAT @ 20%) £')[1].split('\n')[0])
               total_vat = float(table2.split('Subtotal')[1].split('VAT £')[1].split('\n')[0])
               total_pay = float(table2.split('Subtotal')[1].split('VAT £')[2].split('\n')[0].replace(',',''))
               total_psa = admin_fee * 1.2
               vat_psa = admin_fee * 0.2
               total_comm = total_pay - total_psa
               vat_comm = total_vat - vat_psa
               takings.append(taking)
               grosses.append(total_psa)
               grosses.append(total_comm)
               vats.append(vat_psa)
               vats.append(vat_comm)
               dates1.append(date)
               dates1.append(date)
               dates2.append(date)
     except:
          dates1.append('')
          dates1.append('')
          dates2.append('')
          takings.append('')
          grosses.append('')
          grosses.append('')
          vats.append('')
          vats.append('')
          print(f)

df1 = pd.DataFrame({'Date': dates1,
                    'Gross': grosses,
                    'Vat' : vats})
df2 = pd.DataFrame({'Date': dates2,
                    'taking' : takings})

df1['Date'].astype('string')
df2['Date'].astype('string')

writer = pd.ExcelWriter('result.xlsx',engine='xlsxwriter')
df2.to_excel(writer, header=True, index=False, sheet_name='VAT2')
df1.to_excel(writer, header=True, index=False, sheet_name='VAT3')
writer.close()