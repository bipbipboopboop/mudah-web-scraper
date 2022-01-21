import requests
from bs4 import BeautifulSoup
import xlsxwriter
import os

workbook = xlsxwriter.Workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)),"result.xlsx"))
worksheet = workbook.add_worksheet()
row = 0
col = 0
states = ["Kelantan", "Johor", "Kedah", "Kuala-Lumpur", "Labuan", "Melaka", "Negeri-Sembilan" , "Pahang", "Penang", "Perak", "Perlis", "Putrajaya", "Selangor", "Sabah", "Sarawak", "Terrenganu"]  

def detailed_area_list(state):
    new_url = "https://www.mudah.my/{}/Services-available-7040?sa=".format(state)
    new_text = requests.get(new_url)
    new_soup = BeautifulSoup(new_text.text, "html.parser")
    lis3 = list(new_soup.find(attrs={"id": "searcharea_detailed"}))[3:]
    lis3.pop()
    dic = {}
    for i in lis3:
        dic[str(i["value"])] = str(i.text)
    return(dic)
    
def find_total(state, area, name):
    search_url = "https://www.mudah.my/{}/Services-available-7040?sa={}".format(state, area)
    searched_text = requests.get(search_url)
    searched_soup = BeautifulSoup(searched_text.text, "html.parser")
    searched_list = searched_soup.find(attrs={"class":"list-total"})
    if searched_list:
        for i in searched_list:
            return(int(i))
    else:
        return(0)

for s in states:
    worksheet.write(row, col, s)
    row+=1
    sum = 0
    state_list = detailed_area_list(s)
    for k , v in state_list.items():
        num = find_total(s, k, v)
        sum+=num
        worksheet.write(row, col, num)
        worksheet.write(row, col + 1, v)
        row+=1
    row+=1

workbook.close()
