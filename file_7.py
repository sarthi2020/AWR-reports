from bs4 import BeautifulSoup
import xlwt 
from xlwt import Workbook 
import os


folder_path="/Users/ishaan/Desktop/Ubuntu/Exe"
#folder_path=input("Enter Folder Path: ")

report=[]

for entry in os.listdir(folder_path):
	if os.path.isfile(os.path.join(folder_path, entry)):
		if(entry.endswith(".html")):
			print(entry)
			report.append(folder_path+'/'+entry)

#print(report)

class Database:
	def __init__(self):
		self.wb=Workbook()
		self.worksheet=self.wb.add_sheet("New Sheet") 
		self.row=0
		self.col=0
		self.space=5

	def Open(self,filename,identification,identification2,num=0):
		self.f=open(filename,"r")
		self.soup=BeautifulSoup(self.f.read(),"lxml")
		self.tables=self.soup.find_all('table')     #finding all table
		#print(self.tables)
		if(identification==""):
			self.table_no=num
		else:
			for tb in range(len(self.tables)):     #finding elapsed time table 
				if(self.tables[tb].attrs['summary']==identification or self.tables[tb].attrs['summary']==identification2):
					self.table_no=tb
		self.output_rows = []       #extracting data from table and writing in list
		for table_row in self.tables[self.table_no].findAll('tr'):   #data from each cell
			self.columns = table_row.findAll('td')
			self.output_row = []
			#print(columns)
			for column in self.columns:
				self.output_row.append(column.text)
			self.output_rows.append(self.output_row)
		self.header_list=[]
		for header in self.tables[self.table_no].findAll('th'):   #extracting header
			self.header_list.append(header.text)
		self.output_rows[0]=self.header_list
		#print(self.output_rows)
		
	def del_line(self):
		for i in range(len(self.output_rows)):
			for j in range(len(self.output_rows[i])):
				self.output_rows[i][j]=self.output_rows[i][j].strip()
	
	def filtering(self,time,string):
		self.index=self.output_rows[0].index(string)
		for r in range(len(self.output_rows)-1,0,-1):   #applying filter time on output list
			self.output_rows[r][self.index]=self.output_rows[r][self.index].replace(',','')
			#print(self.output_rows[r][self.index])
			if(float(self.output_rows[r][self.index])<time):
				self.output_rows.pop(r)
		
	def main(self,time,identification,identification2,string,excelname):
		for rpt in range(len(report)):
			self.Open(report[rpt],identification,identification2)
			self.del_line()
			#print(self.output_rows)
			if(time!=0):
				self.filtering(float(time),string)
			self.writing(report[rpt],excelname)

	def snap(self,num):
		for rpt in range(len(report)):
			self.Open(report[rpt],"","",num)
			self.writing(report[rpt],'Awr_Snap.xls')
			self.Open(report[rpt],"Top 5 Timed Foreground Events","This table displays top 10 wait events by total wait time")
			self.filtering(0,"% DB time")
			self.writing(report[rpt],'Awr_Snap.xls')
	
	def writing(self,filename,excelname):
		self.worksheet.write(self.row,self.col,filename)           #writing in excel sheet
		for i in range(self.row,self.row+len(self.output_rows)):
			for j in range(len(self.output_rows[i-self.row])):
				self.worksheet.write(i+1,j+1,self.output_rows[i-self.row][j])
			if(i+1==self.row+len(self.output_rows)):
				self.row=i+self.space
		self.wb.save(excelname)

ET=Database()
get=Database()
sn=Database()

ET.main(input("Enter filter for ET(in secs): "),"This table displays top SQL by elapsed time","","Elapsed Time per Exec (s)",'Awr_ET.xls')
#ET.main(5,"This table displays top SQL by elapsed time","","Elapsed Time per Exec (s)",'Awr_ET.xls')
get.main(input("Enter filter for Gets Per Execution: "),"This table displays top SQL by buffer gets","","Gets     per Exec",'Awr_GETS.xls')
#get.main(1000,"This table displays top SQL by buffer gets","","Gets     per Exec",'Awr_GETS.xls')
sn.snap(2)	



