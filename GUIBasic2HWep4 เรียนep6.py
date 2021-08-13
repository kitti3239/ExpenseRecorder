

from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย')
GUI.geometry('600x600+500+20')

#สร้าง menu ใหม่
################MENU###############
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
# Help menu

def About(): # สร้าง function command
	messagebox.showinfo('About','โปรแกรมบันทึกข้อมูล \n สนใจบริจาค เลขบัญชี\n ขอ 1BTC')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

# Donate Menu
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)

#################################

Tab = ttk.Notebook(GUI) # Notebook คือสร้าง Tab
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill= BOTH, expand =1)

icon_t1 = PhotoImage(file='T1_expense.png')
icon_t2 = PhotoImage(file='T2_expenselist.png')

Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top') # f-string ปรับ Style ของ Tab  กว้าง 30 เคาะ อยู่ตรงกลาง ...
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top') # ...ใส่รูป icon t1 และ t2 ให้อยู่ด้านบน

# สร้าง Button แปะใน frame แล้วเอา Frame ไปแปะ ใน GUI
F1 = Frame(T1) # สร้าง Frame
#F1.place(x=100,y=50) # วาง Frame
F1.pack()

# F2 = Frame(T2)
# F2.pack()

# Dictionary
days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัส',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

# สร้าง Function
def Save(event=None):
	expense = v_expense.get() # ดึงมาจาก v_expense = StringVar()
	price = v_price.get()
	quantity = v_quan.get()

	if expense == '' :
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return 
	elif price == '':
			messagebox.showwarning('Error','กรุณากรอกข้อมูลราคา')
			return
	elif quantity == '':
			messagebox.showwarning('Error','กรุณากรอกจำนวน')
			return


	try:
		total = float(price) * int(quantity)

		today = datetime.now().strftime('%a') # weekday แบบ ย่อ

		dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
		dt = days[today]+'-'+dt

		print('รายการ: {} ราคา: {} บาท '.format(expense, price))
		print('จำนวน: {} ชิ้น รวมราคา: {} บาท'.format(quantity, total))
		print('บันทึกเมื่อ: {}'.format(dt))

		# แสดง Result (text) บน จอ Program สำหรับ Lable (v_result)
		text = 'รายการ: {} ราคา: {} บาท\n'.format(expense, price)
		text = text + 'จำนวน: {} ชิ้น รวมราคา: {} บาท'.format(quantity, total)
		v_result.set(text)
	   
	   # Clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quan.set('')

		# บันทึกข้อมูล ลง csv
		with open('savedata1.csv','a',encoding='utf-8', newline = '')as f:
			#with คือสั่งเปิด ไฟล์ แล้วปิดอัตโนมัติ
			#'a' การบันทึกเรื่อยๆเพิ่มข้อมูลจากข้อมูลเก่า
			# newline = '' ทำให้ไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้าง function สำหรับเขียนข้อมูล
			data = [dt, expense, price, quantity, total]
			fw.writerow(data)

		# ทำให้ Cursor กลับไปตำแหน่ง ช่องกรอก E1
		E1.focus()
		update_table() # Run update table

	except Exception as e:
		print('ERROR', e)
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
 # Clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quan.set('')

# ทำให้กด enter ได้
GUI.bind('<Return>',Save)# ต้องเพิ่มใน Def Save(event=None) ด้วย

FONT1 = (None,20) # None เปลี่ยนเป็น Angsana New ได้ อันนี้ (None) เปลี่ยนแค่ Font Size

#-------Image-------------

main_icon = PhotoImage(file='IconMoney.png')
Mainicon = Label(F1,image=main_icon)
Mainicon.pack()



#-------Text1-------------

L = ttk.Label(F1, text='รายการค่าใช้จ่าย', font = FONT1).pack()
v_expense = StringVar() # StringVar เป็นตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1, textvariable = v_expense, font = FONT1)# สร้างกล่องรับค่า
E1.pack()
#--------------------------
#------Text2---------------
L = ttk.Label(F1, text='ราคา (บาท)', font = FONT1).pack()# L ไม่ต้องเปลี่ยน
v_price = StringVar() # StringVar เป็นตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1, textvariable = v_price, font = FONT1)# สร้างกล่องรับค่า
E2.pack()
#--------------------------
#------Text3---------------
L = ttk.Label(F1, text='จำนวน', font = FONT1).pack()# L ไม่ต้องเปลี่ยน
v_quan = StringVar() # StringVar เป็นตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1, textvariable = v_quan, font = FONT1)# สร้างกล่องรับค่า
E3.pack()
#--------------------------

icon_b1 = PhotoImage(file='B_Save.png')

# ตัวแปร v_result สำหรับแสดง Label (text) บน จอ Program
v_result = StringVar()
v_result.set('----------RESULT----------')
result = ttk.Label(F1, textvariable=v_result, font=FONT1, foreground='green')
result.pack(pady=20)

B = ttk.Button(F1,text='Save',command=Save,image=icon_b1,compound='left') 
B.pack(ipadx=20,ipady=10,pady=20) # ipad --> internal pad, pad ---> external pad

############TAB2##############

def read_csv():
#	global rs # ให้ rs เป็น Global variable (สามารถเอาไปใช้นอก function ได้) มิฉะนั้น จะเป็น Local variable ใช้เฉพาะใน Function
	with open('savedata1.csv',newline='',encoding='utf-8') as f:  # เปิด file savedata1 ในชื่อเล่น f
		fr = csv.reader(f) # อ่าน ไฟล์ f
		data = list(fr) # ปรับข้อมูลให้เป็น List ถ้าไม่ทำอ่านไม่ออก
		return data # ต้องการข้อมูลที่ read ไปใช้งานต่อ

		#nest list (list ใน List)
		# print(data)
		# print(data[0][0]) # list field แรก ใน list แรก
		# for a in data
		#	print(a[4])

		# for a,b,c,d,e in data: # ให้ ผลเหมือนกัน 
		# 	print(e)

# rs = read_csv()
# print(rs)

# Table

L = ttk.Label(T2, text='ตารางแสดงผลทั้งหมด', font = FONT1).pack(pady=20)

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10) # height คือ จำนวน บรรทัด
resulttable.pack()

# เขียน header วิธีแรก
# for i in range(len(header)):
# 	resulttable.heading(header[i],text=header[i])

for h in header: # list เอามา run ได้เลย
	resulttable.heading(h,text=h)
	
#ปรับความกว้าง column
headerwidth = [150,170,80,80,80]
resulttable.column(header[0],width=headerwidth[0])

# รวม 2 list ใช้ zip
for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)
 
#insert data in table manually
# resulttable.insert('','end',value=['mon','tea',3,5,15]) # insert last in table
# resulttable.insert('','0',value=['sun','toast',3,5,15]) # insert to first list in table


def update_table():
	resulttable.delete(*resulttable.get_children()) # delete ข้อมูล ก่อน update table (ลบทั้ั้บรรทัด)
	# for c in resulttable.get_children(): # *resulttable ---> แทน for loop แสดงผล บรรทัดเดียวได้
	# 	resulttable.delete(c)
	data = read_csv()
	for d in data:
		resulttable.insert('',0,value=d)



update_table()

GUI.mainloop()
