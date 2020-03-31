import openpyxl as ox
import pandas as pd

file = ox.load_workbook("test.xlsx")
sheet = file['微博数据']
data = ['juju', '2020', 'asdusadhfisndhfniasdhfioushdnfiausdhnfi']
sheet.append(data)
data = ['kiki', '2019', 'asdasdr送到附近的四分四代机佛暗示#￥%……&']
sheet.append(data)
file.save("test.xlsx")