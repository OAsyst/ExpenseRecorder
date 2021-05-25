# GUIBasic1.py

from tkinter import *
from tkinter import ttk, messagebox  # ttk is theme of TK
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย By Palmy')
GUI.geometry('500x625+500+50')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI


################################
# สร้าง MENU

menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)   #tearoff=0 คือไม่ต้องการให้ user ดึงเมนู ออกมา
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to GoogleSheet')
# Help
def Abount():
	messagebox.showinfo('Abount','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอ 1 BTC Address:	abc')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=Abount)
# Donate
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)


###############################




# เพิ่ม Tab
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

icon_t1 = PhotoImage(file='t1_expense.png')
icon_t2 = PhotoImage(file='t2_expenselist.png')

Tab.add(T1,text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2,text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')



#F1 = Frame(GUI)  # กรณีไม่มี Tab ก็จะสร้างเฟรมไว้บน GUI
F1 = Frame(T1)  #กรณี มีการเพิ่ม Tab จะทำการย้ายเฟรมที่อยู่บน GUI ไปไว้ใน Tab ที่ 1 แทน



#F1.place(x=100,y=50)
F1.pack()  #จัดเฟรมให้อยู่ตรงกลางบน GUI 

days = {'Mon':'จันทร์','Tue':'อังคาร','Wed':'พุธ','Thu':'พฤหัสบดี','Fri':'ศุกร์','Sat':'เสาร์','Sun':'อาทิตย์'}

def Save(event=None):
		expense = v_expense.get()  # .get() คือดึงค่ามาจาก v_expense = StringVar()
		price = v_price.get()
		amount = v_amount.get()

		if expense == '':
			print('No Data')
			messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
			return
		elif price == '':
			messagebox.showerror('Error','กรุณากรอกราคา')
			return
		elif amount == '':
			messagebox.showerror('Error','กรุณากรอกจำนวน')
			return

		try:
				total = int(price)*int(amount)        
				
				# clear ข้อมูลเก่า
				v_expense.set('')
				v_price.set('')
				v_amount.set('')

				today = datetime.now().strftime('%a')   # days['Mon'] ='จันทร์'
				dt = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
				dt = days[today] + '-' + dt
				print('วันที่ {}'.format(dt))
				print('รายการสินค้า: {} ราคาต่อหน่วย: {} จำนวน: {} รวมเป็นเงินทั้งหมด {} บาท'.format(expense,price,amount,total))
				
				text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
				text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(amount,total)
				v_result.set(text)  # เคลียร์ข้อมูลเก่า

				# บันทึกข้อมูลลง CSV อย่าลืม import csv ด้วย
				with open('Order.csv','a', encoding = 'utf-8',newline='') as f:
						# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
						# 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
						# newline ='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
						fw = csv.writer(f)  # สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
						data = (dt,expense,price,amount,total)
						fw.writerow(data)

				# ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
				E1.focus()
				update_table()										
		except Exception as e:
				print('ERROR: ',e)
				messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
				#messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
				#messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
				v_expense.set('')
				v_price.set('')
				v_amount.set('')


# ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,20)  # None อาจจะเปลี่ยนเป็น 'Angsana New'

#-------Image---------

main_icon = PhotoImage(file='icon_money.png')
mainicon=Label(F1,image=main_icon)
mainicon.pack()



#-------text1---------
L = ttk.Label(F1,text='รายการสินค้า',font=FONT1).pack()

v_expense = StringVar()  # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#---------------------

#-------text2---------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()

v_price = StringVar()  # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#---------------------

#-------text3---------
L = ttk.Label(F1,text='จำนวน (หน่วย)',font=FONT1).pack()

v_amount = StringVar()  # StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_amount,font=FONT1)
E3.pack()
#---------------------

icon_b1 = PhotoImage(file='b_save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=20,ipady=15,pady=20)


v_result = StringVar()
v_result.set('-------ผลลัพธ์-------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground= 'green')
# result = label(F1,textvariable=v_result,font=Font1,fg='green')
result.pack(pady=20)


####################################################
# Tabที่2


def read_csv():     
	with open('Order.csv',newline='',encoding='utf-8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data


##################################################
# Show String In Tab2(T2)

#def update_record():
#	getdata = read_csv()
#	v_allrecord.set('')
#	text = ''
#	for d in getdata:
#		text =text + '{}\n'.format(d)
		
#	v_allrecord.set(text)


#v_allrecord = StringVar()
#v_allrecord.set('-----All Record-----')
#allrecord = ttk.Label(T2,textvariable=v_allrecord,font=(None,10),foreground= 'green')
#allrecord.pack()
###################################################


#Table & TreeView

L = ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)
header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()



# for i in range(len(header)):
# 	resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

hearderwidth = [150,170,80,80,80]

for h,w in zip(header,hearderwidth):
	resulttable.column(h,width=w)


#ค่าวันจันทร์จะอยู่บนสุด
#resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150])  # การใส่ค่าแบบ Manual
#resulttable.insert('','end',value=['อังคาร,'น้ำดื่ม',30,5,150])  # การใส่ค่าแบบ Manual

#ค่าวันอังคารจะอยู่บนสุด
#resulttable.insert('',0,value=['จันทร์','น้ำดื่ม',30,5,150])  # การใส่ค่าแบบ Manual
#resulttable.insert('',0,value=['อังคาร,'น้ำดื่ม',30,5,150])  # การใส่ค่าแบบ Manual


def update_table():
	resulttable.delete(*resulttable.get_children())  # ตัว * เป็นการแสดง for loop
	data = read_csv()
	for d in data:
		resulttable.insert('',0,value=d)    # ค่า 0 หมายถึง คอลัมน์แรกสุดหรือบนสุด


update_table()

GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
