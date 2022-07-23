import mysql.connector
from datetime import datetime as d
import re 
from selenium import webdriver

class scrape(object):
  def __init__(self):    
    browser = webdriver.Chrome(executable_path='C:/Users/localhost/Downloads/chromedriver.exe')
    browser.implicitly_wait(15)
    browser.get("https://www.covid19india.org/")
    self.h1text=browser.find_element_by_xpath('/html/body/div/div/div/div[3]/div[1]/div[2]/div[1]/h1').get_attribute('innerHTML')
    browser.quit()

class mydbdata(scrape):
    l=[]
    def __init__(self,oj):
      mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="%unknown%123",
        database="coronadb"
      )
      mycursor = mydb.cursor()
      mycursor.execute("SELECT * FROM coronastats")
      mycursor.fetchall()
      row_count = mycursor.rowcount
      if row_count ==0:
        table_insert="INSERT INTO coronastats(ccount,cdate,ctime) VALUES(%s,%s,%s)"
        count_date=d.now().strftime('%y-%m-%d')
        count_time=d.now().strftime('%H:%M:%S')
        val=[oj.h1text,count_date,count_time]
        mycursor.execute(table_insert,val)
        mydb.commit()
      else:
        s=[d.now().strftime('%y-%m-%d')]
        id_check=mycursor.execute("SELECT id FROM coronastats WHERE cdate=%s",s)
        res=mycursor.fetchone()
        print(res)
        if id_check==None:
          table_insert="INSERT INTO coronastats(ccount,cdate,ctime) VALUES(%s,%s,%s)"
          count_date=d.now().strftime('%y-%m-%d')
          count_time=d.now().strftime('%H:%M:%S')
          val=[oj.h1text,count_date,count_time]
          mycursor.execute(table_insert,val)
          mydb.commit() 
        else:
            update_table="UPDATE coronastats SET ctime= %s,ccount=%s WHERE id=%s"
            count_time=d.now().strftime('%H:%M:%S')
            val=[count_time,oj.h1text,res]
            mycursor.execute(update_table,val)
            mydb.commit() 
      strTable = "<html><body><title>'COVID-19 INDIA STATS '</title></body><style>table, th, td {border: 1px solid black;}</style><table style= 'width:60%' ><tr><th>IndiaCount</th><th>Date</th><th>Time</th></tr>"
      strRW="<tr>"
      mycursor.execute("SELECT ccount,cdate,ctime FROM coronastats")
      result=mycursor.fetchall()
      for x in result:
        print(x)
        for i in range(0,len(x)):
          strRW+="<td>"+str(x[i])+"</td>"
        strRW+="</tr>"
      strTable+=strRW
      strTable = strTable+"</table></html>"
      hs = open(r"C:\Users\localhost\Desktop\HTMLTable.html", 'w')
      hs.write(strTable)
 
            
obj1=scrape()
obj2=mydbdata(obj1)


    
    
