import pandas as pd
import os
import pdfplumber
from pprint import pprint
from datetime import datetime as dt

takings = []
grosses = []
vats = []
issue_dates = []
period_dates = []
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
        table1 = first_page.extract_text()
        if len(pdf.pages) > 1:
            second_page = pdf.pages[1]
            table2 = second_page.extract_text()
            table = f'{table1} {table2}'
        else:
            table = table1
        gross = float(table.split('Invoice Total')[2].split(' ')[3])
        vat = float(table.split('Invoice Total')[2].split(' ')[2])
        try:
            taking = float(table.split('Gross amount (£)')[1].split('Total')[1].split(' ')[2]) + float(table.split('Gross amount (£)')[1].split('Total')[2].split(' ')[2])
        except:
            taking = float(table.split('Gross amount (£)')[1].split('Total')[1].split(' ')[2])
        day = table.split('Issue date: ')[1].split(' ')[1]
        month = months[table.split('Issue date: ')[1].split(' ')[2]]
        issue_date = f'{day}/{month}/23'
        day = table.split('Period covered: ')[1].split('-')[0].split(',')[1].split(' ')[0]
        month = months[table.split('Period covered: ')[1].split('-')[0].split(',')[1].split(' ')[1]]
        start_date =  f'{day}/{month}'
        day = table.split('Period covered: ')[1].split('-')[1].split(',')[1].split(' ')[0]
        month = months[table.split('Period covered: ')[1].split('-')[1].split(',')[1].split(' ')[1].split('\n')[0]]
        end_date =  f'{day}/{month}'
        period = f'{start_date}-{end_date}'
        print(issue_date)
        grosses.append(gross)
        vats.append(vat)
        takings.append(taking)
        issue_dates.append(issue_date)
        period_dates.append(period)

df = pd.DataFrame({
     'Invoice Date': issue_dates,
     'Invoice Period':period_dates,
     'Taking': takings,
     'Gross': grosses,
     'Vat' : vats
})
df['Invoice Date'].astype('string')
df.to_excel('result.xlsx', header=True,index=False)
        