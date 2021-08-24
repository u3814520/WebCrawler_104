import  requests
from bs4 import BeautifulSoup
import json
import os



if not os.path.exists('./job104'):
    os.mkdir('./job104')
if not os.path.exists('./job104/tool'):
    os.mkdir('./job104/tool')
if not os.path.exists('./job104/toolall'):
    os.mkdir('./job104/toolall')


page=1

allworklist = []   #所有擅長工具  #全部公司用
toolall={}   #所有擅長工具出現次數

for i in range(0, 2):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E5%89%AA%E6%8E%A5%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&page={}'.format(page)
    userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'


    headers={'User-Agent':userAgent}
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    titles = soup.select('div[id="js-job-content"]')


    for n in range(0, 20):
        for titleSoup in titles:
            job = titleSoup.select('article')[n]['data-job-name']
            cust = titleSoup.select('article')[n]['data-cust-name']
            titleurl = 'https:'+ titleSoup.select('a[class="js-job-link"]')[n]['href']
            # 取職缺內容
            urlid = titleurl.split('job/')[1].split('?')[0]
            newUrl='https://www.104.com.tw/job/ajax/content/{}'.format(urlid)
            newheaders={'Referer': 'https://www.104.com.tw/job/{}'.format(urlid)}
            newres = requests.get(url=newUrl, headers=newheaders)
            jsonData = json.loads(newres.text)
            jsondatas = jsonData['data']
            jobDetails = jsondatas['jobDetail']
            # 職缺內容
            jobDescriptions = jobDetails['jobDescription']
            # 擅長工具
            jobDetails = jsondatas['condition']
            specialtys = jobDetails['specialty']
            wlen = len(specialtys)
            work = list()
            allwork = []

            if wlen == 0:
                work.append('None')
            for w in range(0, wlen):
                specialtys = jobDetails['specialty'][w]
                works = specialtys["description"]
                work.append(works)
                allworklist.append(works)

            #全部工具次數
            for i in range(0,len(allworklist)):
                n= allworklist.count(allworklist[i])
                toolall[allworklist[i]]=n
            # print(toolall)
            frequency=[]
            for k, v in toolall.items():
                fre = str(k) + ':' + str(v)
                frequency.append(fre)

            with open('./job104/toolall/frequency.doc', 'w', encoding='utf-8') as f:
                f.write(str(frequency))

            with open('./job104/{}.txt'.format(cust), 'w', encoding='utf-8') as f:
               f.write( str(cust) + '---split---' + str(job) + '---split---' + str(jobDescriptions) + "---split---" + str(work)+'---split---'+'https://www.104.com.tw/job/'+str(urlid)+'---split---'+'end')
            with open('./job104/tool/{}.txt'.format(cust), 'w', encoding='utf-8') as f:
                f.write(str(allwork))

    page+=1


















