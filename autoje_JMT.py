import pandas as pd
import os
import pdfplumber
from pprint import pprint
from datetime import datetime as dt

takings = []
grosses = []
vats = []
dates = []
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
        dates.append(date)
        taking = float(table1[0][3][0].split('\n')[11].split(' ')[0].replace(',','').replace('£',''))
        total_vat = float(table2.split('Subtotal')[1].split('VAT £')[1].split('\n')[0])
        total_pay = float(table2.split('Subtotal')[1].split('VAT £')[2].split('\n')[0].replace(',',''))
        takings.append(taking)
        grosses.append(total_pay)
        vats.append(total_vat)
df = pd.DataFrame({
     'Date': dates,
     'taking' : takings,
     'Gross': grosses,
     'Vat' : vats
})

df['Date'].astype('string')

df.to_excel('result_JMT.xlsx', header=True,index=False)