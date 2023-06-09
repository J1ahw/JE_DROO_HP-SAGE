import aspose.words as aw
import os
filenames = []
for root,dirs,files in os.walk('C:/Users/vc-user12-guest/Downloads/je'):
        for f in files:
            filepath = f'{root}/{f}'
            filenames.append(filepath)
i = 0            
for m in filenames:
    doc = aw.Document(m)
    doc.save(f"V:/Hanwen J1a/personal document/AUTO JE/PDF/{i+100}.pdf")
    i += 1
