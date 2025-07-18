from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import tkinter as tk
from tkinter.messagebox import *
from tkinter import messagebox
from tkinter.scrolledtext import *
import json, os, re, random
import datetime as dt
import smtplib, ssl, base64, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import ImageTk, Image

my_font = ('Helvetica', 20)
my_font2 = ('Helvetica', 18)
my_font3 = ('Helvetica', 22)
my_font4 = ('Helvetica', 10)
my_font5 = ('Helvetica', 7)

a,b,d,e,f,g,k,c=0,0,0,0,0,0,0,-1

class FitPeriod(tk.Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("800x620+-10+0")
        self.iconbitmap("assets/vector/favicon.ico")
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        def switch_frame2(self,frame_class):
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()
        if frame_class==SendNow:
            dtime=dt.datetime.now()
            file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
            if os.path.isfile(file_name):
                switch_frame2(self,frame_class)
            else:
                showerror(title="Error",message="No arrangement generated today!")
        elif frame_class==ContactDetails or frame_class==NewTT:
            if os.path.isfile("data/stt_data.json"):
                switch_frame2(self,frame_class)
            else:
                showerror(title="Error",message="Add teachers before continue!")
        elif frame_class==NewArng:
            if os.path.isfile("data/tt_data.json"):
                switch_frame2(self,frame_class)
            else:
                showerror(title="Error",message="No time table found!")
        else:
            switch_frame2(self,frame_class)
        
    def menubar(self):
        self.mainmenu = Menu(self)
        
        self.filemenu = Menu(self.mainmenu, tearoff=0,font=("Helvetica",10))

        self.mainmenu.add_cascade(label="Home", command=lambda: self.switch_frame(HomePage))

        self.filemenu.add_command(label="Set New", command=lambda: self.switch_frame(NewArng))
        self.filemenu.add_command(label="Older", command=lambda: self.switch_frame(OlderArng))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=lambda: self.quit())
        self.mainmenu.add_cascade(label="Arrangement", menu=self.filemenu)
        
        self.ttmenu = Menu(self.mainmenu, tearoff=0,font=("Helvetica",10))
        self.ttmenu.add_command(label="Time Table", command=lambda: self.switch_frame(NewTT))
        self.ttmenu.add_command(label="Teachers", command=lambda: self.switch_frame(Teachers))
        self.mainmenu.add_cascade(label="TimeTable", menu=self.ttmenu)
        
        self.notifmenu = Menu(self.mainmenu, tearoff=0,font=("Helvetica",10))
        self.notifmenu.add_command(label="Send now", command=lambda: self.switch_frame(SendNow))
        self.notifmenu.add_command(label="Contact Details", command=lambda: self.switch_frame(ContactDetails))	
        self.mainmenu.add_cascade(label="Notifications", menu=self.notifmenu)

        self.mainmenu.add_cascade(label="About", command=lambda: self.switch_frame(About))

        self.config(menu=self.mainmenu)

    def loading_bar(self,val):
        from time import sleep
        lb=Toplevel()
        lb.geometry("190x60+300+300")
        lb.maxsize(190,60)
        lb.minsize(190,60)
        lb.resizable(0,0)
        lb.config(bg="#000000")
        lb.title("Please wait...")
        lb.iconbitmap("assets/vector/favicon.ico")
        def play_animation(self,val):
            for a in range(val):
                for b in range(8):
                    tk.Label(self,bg="#33daff",width=2,height=1).place(x=(b+0.4)*22,y=25)
                    sleep(0.06)
                    self.update_idletasks()
                    tk.Label(self,bg="#ffffff",width=2,height=1).place(x=(b+0.4)*22,y=25)
            else:
                self.destroy()
        tk.Label(lb,bg="#000000",fg="#ffffff",text="Loading...",font=("Helvetica",11)).place(x=4,y=1)
        for i in range(8):

            tk.Label(lb,bg="#ffffff",width=2,height=1).place(x=(i+0.4)*22,y=25)
        lb.update()
        play_animation(lb,val)

    def lbg(self,fname,alist):
        from threading import Thread


                
        
class HomePage(tk.Frame,FitPeriod):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("FitPeriod - Set Arrangements")
        master.maxsize(800,620)
        master.minsize(800,620)
        master.config(bg="#000000")
        self.config(bg="#000000")
        lg1=Image.open("assets/vector/full_logo.png")
        lg1=lg1.resize((600, 150), Image.ANTIALIAS)
        lg1=ImageTk.PhotoImage(lg1)
        img1=Image.open("assets/vector/click.png")
        img1=img1.resize((80, 80), Image.ANTIALIAS)
        img1=ImageTk.PhotoImage(img1)
        mainlbl=tk.Label(self,image=lg1,relief=tk.FLAT,bg="#000000",activebackground="#000000",fg="#000000",bd=0)
        mainlbl.image=lg1
        mainlbl.pack(pady=(30,0))
        main_btn=tk.Button(self, image=img1,relief=tk.FLAT,bg="#000000",activebackground="#000000",fg="#000000",bd=0, font=('Helvectiva', 19), command=lambda: master.switch_frame(NewArng))
        main_btn.image=img1
        main_btn.pack(anchor=CENTER,pady=(120,0))

class NewArng(FitPeriod, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Set New Arrangements - FitPeriod")
        master.config(bg="#000000")
        self.config(bg="#000000")
        class_no = ["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
        
        def check_per(teach_list, class_no, sday, am):
            period_dict = {}
            tmp_list = []
            tmp_class = ""
            for b in range(len(teach_list)):
                period_dict[teach_list[b]] = []
            for i in range(len(teach_list)):
                for a in range(8):
                    tmp_list.clear()
                    for k in class_no:
                        if type(am[k][sday][a]) is list:
                            if teach_list[i] in am[k][sday][a]:
                                tmp_list.append("yes")
                                tmp_class = k
                            else:
                                tmp_list.append("no")
                        else:
                            if teach_list[i] == am[k][sday][a]:
                                tmp_list.append("yes")
                                tmp_class = k
                            else:
                                tmp_list.append("no")
                    if "yes" not in tmp_list:
                        period_dict[teach_list[i]].append("nil")
                    else:
                        period_dict[teach_list[i]].append(tmp_class)
            return period_dict
        
        def check_day(file,day):
            cls_dict={}
            for a in file:
                cls_dict[a]=file[a][day]
            return cls_dict
            
        def check_arng(t_dict):
            prd_list=[0,0,0,0,0,0,0,0]
            prd_list2=[[],[],[],[],[],[],[],[]]
            prd_list3=[[],[],[],[],[],[],[],[]]
            for a in t_dict:
                for b in range(8):
                    if t_dict[a][b] != "nil":
                        prd_list2[b].append(t_dict[a][b]+" ("+a+")")
                        prd_list3[b].append(t_dict[a][b])
                        prd_list[b]+=1
            for b in range(8):
                if len(prd_list2[b]) == 0:
                    prd_list2[b].append("nil")
                    prd_list3[b].append("nil")
            return prd_list, prd_list2, prd_list3
            
        def make_arng(dict1, list1):
            tchrs_arng_list=[[],[],[],[],[],[],[],[]]
            for a in range(len(list1)):
                if list1[a] != 0:
                    for b in dict1:
                        if dict1[b][a] == "nil":
                            tchrs_arng_list[a].append(b)
                else:
                    tchrs_arng_list[a].append("not needed")
            return tchrs_arng_list
            
        def get_teachers(file1, file2, day_list):
            raw_dict={}
            for e in file2:
                raw_dict[e]=[]
            for a in file1:
                for b in day_list:
                    for c in range(8):
                        if type(file1[a][b][c]) is list:
                            file1[a][b].extend(file1[a][b][c])
                            del file1[a][b][c]
                    for d in file2:
                        if d in file1[a][b]:
                            if a not in raw_dict[d]:
                                raw_dict[d].append(a)
            return raw_dict
            
        def set_arng(list1, list2, list3, dict1, list4):
            raw_dict,raw_dict2,raw_dict3={},[{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{}]
            cls_list=["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
            subs = "PRINCIPAL"
            for a in cls_list:
                raw_dict[a]=[]
                for b in dict1:
                    if a in dict1[b]:
                        raw_dict[a].append(b)
            for c in range(len(list3)):
                for d in list3[c]:
                    if d != "nil":
                        raw_dict2[c][d]=raw_dict[d]
            for e in raw_dict2:
                if len(e) != 0:
                    for f in list(e.keys()):
                        res=[i for i in e[f] if subs in i]
                        for g in res:
                            e[f].remove(g)
            raw_wlist=[]
            for h in range(len(raw_dict2)):
                if len(raw_dict2[h]):
                    for i in raw_dict2[h]:
                        random.shuffle(raw_dict2[h][i])
                        for j in raw_dict2[h][i]:
                            if (j not in raw_wlist and j not in list4):
                                raw_dict3[h][i]=j
                                raw_wlist.append(j)
                                break
                        else:
                            raw_dict3[h][i]=random.choice(raw_dict2[h][i])
            return raw_dict2,raw_dict3
        na_scroll=ttk.Scrollbar(self)
        na_scroll.pack(side=RIGHT,fill=Y,anchor=E)
        na_canvas=Canvas(self,height=2000,yscrollcommand=na_scroll.set,width=800,bg="#000000",highlightthickness=0)
        na_canvas.pack(fill='both',expand='true',padx=100)
        na_frame=tk.Frame(na_canvas,bg="#000000",bd=-2)
        na_frame.pack(fill='both',expand='true')
        na_canvas.create_window(0,0,anchor=NW,window=na_frame)
        na_canvas.update_idletasks()
        
        na_canvas.configure(scrollregion=na_canvas.bbox('all'))
        na_scroll.config(command=na_canvas.yview)
        with open("data/stt_data.json", "r") as st_data0:
            teachers0 = json.load(st_data0)
            teachers = ["Select Teacher"] + teachers0
        
        tk.Label(na_frame, text="SELECT DAY", font=my_font3, fg="#ffffff",bg="#000000").pack(pady=(20,10),ipadx=201)
        tn_frame=tk.Frame(na_frame,bg="#000000",bd=-2)
        tn_frame.pack(fill='both',expand='true',pady=(0,20))
        
        days = ["Select", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        
        day = tk.StringVar(self)
        day.set(days[0])
        
        select_day = ttk.OptionMenu(tn_frame, day, *days)
        select_day.pack(side=LEFT,padx=(229,10))
        def for_ret(widget, widget2, widget3, widget4, var, widget5):
            if var.get() != "Select":
                widget.pack(pady=5)
                widget2.pack(pady=5,padx=(170,10),side=LEFT)
                widget3.pack(pady=5,padx=(0,10),side=LEFT)
                widget4.pack(pady=5,side=LEFT)
                widget5.pack(fill='both',expand='true',pady=(0,20))
                
            if var.get() == "Select":
                showwarning(title="Select day", message="Please select the day first!")

        
        img2=Image.open("assets/vector/next.png")
        img2=img2.resize((50, 24), Image.ANTIALIAS)
        img2=ImageTk.PhotoImage(img2)
        day_btn = tk.Button(tn_frame,image=img2,relief=tk.FLAT,bg="#000000",activebackground="#000000",fg="#000000",bd=0,command=lambda: for_ret(add_label, add_btn, remove_btn, confirm_btn, day, tn1_frame))
        day_btn.image=img2
        day_btn.pack(side=LEFT)
        
        add_label = tk.Label(na_frame, text="ADD TEACHERS", font=my_font3, fg="#ffffff",bg="#000000")
        
        global teachers_entry_list
        global teachers_entry_list2
        
        teachers_entry_list = []
        teachers_entry_list2 = []
        
        add_var0 = StringVar()
        add_var1 = StringVar()
        add_var2 = StringVar()
        add_var3 = StringVar()
        add_var4 = StringVar()
        add_var5 = StringVar()
        add_var6 = StringVar()
        add_var7 = StringVar()
        add_var8 = StringVar()
        add_var9 = StringVar()
        add_var10 = StringVar()
        add_var11 = StringVar()
        add_var12 = StringVar()
        add_var13 = StringVar()
        add_var14 = StringVar()
        
        om0 = ttk.Combobox(self, textvariable=add_var0, values=teachers, state="readonly")
        om1 = ttk.Combobox(self, textvariable=add_var1, values=teachers, state="readonly")
        om2 = ttk.Combobox(self, textvariable=add_var2, values=teachers, state="readonly")
        om3 = ttk.Combobox(self, textvariable=add_var3, values=teachers, state="readonly")
        om4 = ttk.Combobox(self, textvariable=add_var4, values=teachers, state="readonly")
        om5 = ttk.Combobox(self, textvariable=add_var5, values=teachers, state="readonly")
        om6 = ttk.Combobox(self, textvariable=add_var6, values=teachers, state="readonly")
        om7 = ttk.Combobox(self, textvariable=add_var7, values=teachers, state="readonly")
        om8 = ttk.Combobox(self, textvariable=add_var8, values=teachers, state="readonly")
        om9 = ttk.Combobox(self, textvariable=add_var9, values=teachers, state="readonly")
        om10 = ttk.Combobox(self, textvariable=add_var10, values=teachers, state="readonly")
        om11 = ttk.Combobox(self, textvariable=add_var11, values=teachers, state="readonly")
        om12 = ttk.Combobox(self, textvariable=add_var12, values=teachers, state="readonly")
        om13 = ttk.Combobox(self, textvariable=add_var13, values=teachers, state="readonly")
        om14 = ttk.Combobox(self, textvariable=add_var14, values=teachers, state="readonly")
        
        global add_var_list
        global no_e
        
        no_e = [add_var0, add_var1, add_var2, add_var3, add_var4, add_var5, add_var6, add_var7, add_var8, add_var9, add_var10, add_var11, add_var12, add_var13, add_var14]
        
        add_var_list = [om0, om1, om2, om3, om4, om5, om6, om7, om8, om9, om10, om11, om12, om13, om14]
        
        def add_entry_func(self,canvas):
            canvas.config(scrollregion=na_canvas.bbox('all'))
            global a
            global b
            global add_var_list
            global no_e
            if a<15:
                try:
                    add_var_list[a] = ttk.Combobox(na_frame, textvariable=no_e[a], values=teachers, state="readonly", width=50)
                    add_var_list[a].pack(pady=3)
                    add_var_list[a].current(0)
                except:
                    pass
                try:
                    add_var_list[a].pack(pady=3)
                    add_var_list[a].current(0)
                    a = a +1
                    b = a
                except:
                    pass
            else:
                showwarning(title="Warning", message="Only 15 teachers can be added")                   
                
        def remove_entry_func(self,canvas):
            canvas.config(scrollregion=na_canvas.bbox('all'))
            global a
            global b
            global add_var_list
            if (b-1) >= 0:
                try:
                    add_var_list[b-1].destroy()
                    b = b - 1
                    if a>=1:
                        a = a - 1
                except:
                    pass
            else:
                showwarning(title="Warning", message="Please add at least one teacher")
        
        def confirm_arng(self):
            global teachers_entry_list
            global teachers_entry_list2
            if (b-1) >= 0:
                for entry_var in range(a):
                    teachers_entry_list.append(no_e[entry_var].get())
                if "Select Teacher" in teachers_entry_list:
                    showwarning(title="Warning", message="Field cannot be empty")
                    teachers_entry_list.clear()
                else:
                    try:
                        with open("data/tt_data.json", "r") as tt_file:
                            am=json.load(tt_file)
                            tt_file.close()
                    except:
                        showerror(title="Error", message="No time table found")
                    try:
                        with open("data/stt_data.json", "r") as stt_file:
                            all_tea_list=json.load(stt_file)
                            stt_file.close()
                    except:
                        showerror(title="Error", message="Unexpected error encountered")
                    per_dict=check_per(teachers_entry_list, class_no, day.get(), am)
                    day_list=check_day(am, day.get())
                    arng_list=check_arng(per_dict)
                    all_prd_dict=check_per(all_tea_list, class_no, day.get(), am)
                    tchrs_list=make_arng(all_prd_dict, arng_list[0])
                    tchrs_prd_list=get_teachers(am, all_tea_list, days[1:])
                    # Final output
                    global final_result
                    final_result=set_arng(list1=arng_list[1],list2=tchrs_list,list3=arng_list[2],dict1=tchrs_prd_list, list4=teachers_entry_list)
                    self.openNewWindow(final_result,teachers_entry_list,arng_list[1])
                    teachers_entry_list.clear()
            else:
                showwarning(title="Warning", message="Please add at least one teacher to set the arrangement")

        tn1_frame=tk.Frame(na_frame,bg="#000000",bd=-2)

        img3=Image.open("assets/vector/add.png")
        img3=img3.resize((45, 28), Image.ANTIALIAS)
        img3=ImageTk.PhotoImage(img3)
        add_btn = tk.Button(tn1_frame, image=img3,relief=tk.FLAT,bg="#000000",bd=0,fg="#000000",activebackground="#000000", font=('Helvectiva', 10), command=lambda:add_entry_func(self,na_canvas))
        add_btn.image=img3
        
        img4=Image.open("assets/vector/remove.png")
        img4=img4.resize((85, 28), Image.ANTIALIAS)
        img4=ImageTk.PhotoImage(img4)
        remove_btn = tk.Button(tn1_frame,image=img4,relief=tk.FLAT,bg="#000000",bd=0,activebackground="#000000",fg="#000000", font=('Helvectiva', 10), command=lambda:remove_entry_func(self,na_canvas))
        remove_btn.image=img4
        
        img5=Image.open("assets/vector/setnow.png")
        img5=img5.resize((90, 28), Image.ANTIALIAS)
        img5=ImageTk.PhotoImage(img5)
        confirm_btn = tk.Button(tn1_frame,image=img5, relief=tk.FLAT,bg="#000000",bd=0,activebackground="#000000",fg="#000000", font=('Helvectiva', 10), command=lambda:confirm_arng(self))
        confirm_btn.image=img5

    def openNewWindow(self,tuple1,list1,list2):
        second_teacher_var ={}
        second_teacher_var_list=[]
        for a in range(16):
            for b in range(9):
                second_teacher_var[(a,b)]=StringVar()
                second_teacher_var_list.append((a,b))

        color_list=('#0000FF', '#FF1493', '#4B0082', '#008000', '#FF0000', '#00FFFF', '#DAA520', '#191970', '#A52A2A', '#FFA07A', '#808000', '#808080', '#FFA500', '#FFFF00', '#00FF00')
        period_list = ["Per/Class","Period I", "Period II",  "Period III", "Period IV", "Period V", "Period VI", "Period VII", "Period VIII"]
        class_list = ["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
        final1_raw_list=[]
        final2_raw_list=list(class_list)
        final3_raw_list=[]
        final4_raw_dict={}
        my_font2 = ('Helvetica', 9)
        my_font1 = ('Helvetica', 11)
        my_font3 = ('Helvetica', 15)
        my_font4 = ('Helvetica', 7)
        
        newWindow = Toplevel(self)
        newWindow.geometry("1114x437+100+20")
        newWindow.maxsize(1114,437)
        newWindow.minsize(1114,437)
        newWindow.resizable(0,0)
        newWindow.config(bg="#000000")
        newWindow.title("Generated Arrangement")
        raw_dict=[{},{},{},{},{},{},{},{}]
        list1_value=[]
        def get_val(tuple1,var1,list1,list2):
            save_notif(tuple1,var1,list2)
            import xlsxwriter as xr
            dtime=dt.datetime.now()
            file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
            xlsx_name=f"{dtime.day}-{dtime.month}-{dtime.year}"
            day=f"{dtime.strftime('%A')}"
            if os.path.isfile(file_name):
                with xr.Workbook(os.path.join(os.path.join(os.environ['USERPROFILE'],f'Desktop\\{xlsx_name}.xlsx'))) as xf:
                    xw=xf.add_worksheet()
                    format0=xf.add_format({
                        'bold': 1,
                        'border': 1,
                        'align': 'center',
                        'valign': 'vcenter'})
                    format0.set_text_wrap()
                    format0.set_font_size(14)
                    format1=xf.add_format({
                        'bold': 1,
                        'border': 1,
                        'align': 'center',
                        'valign': 'vcenter'})
                    format3=xf.add_format({
                        'border': 1,
                        'align': 'center',
                        'valign': 'vcenter'})
                    format2=xf.add_format({
                        'bold': 1,
                        'border': 1,
                        'align': 'center'})
                    format4=xf.add_format({
                        'bold': 1,
                        'border': 1,
                        'align': 'center',
                        'valign': 'vcenter'})
                    format4.set_font_size(10)
                    xw.set_column('C:C', 15)
                    xw.set_column('E:E', 15)
                    xw.set_row(0,40)
                    xw.merge_range('A1:E1', f"JAWAHAR NAVODAYA VIDYALAYA, HARIDWAR\nARRANGEMENT, {xlsx_name}, {day}", format0)
                    tol=""
                    for a in range(1,len(list1)+1):
                        if a%3==0:
                            tol=tol+f"{a}. "+list1[a-1]+"\n"
                        else:
                            tol=tol+f"{a}. "+list1[a-1]+"   "
                    xw.merge_range('A2:E2', f"Teachers On Leave:\n{tol}", format4)
                    if len(list1)%3!=0 and len(list1)!=1:
                        xw.set_row(1,15+15*(len(list1)//2))
                    elif len(list1)%3==0:
                        xw.set_row(1,15+15*(len(list1)//3))
                    elif len(list1)==1:
                        xw.set_row(1,30)
                    
                    with open(file_name,"r") as csvfile:
                        reader = csv.reader(csvfile)
                        row1=next(reader)
                        for b in range(len(row1)):
                            if b==0:
                                xw.write(2,b,f"Teacher Name",format1)
                            else:
                                xw.write(2,b,f"{row1[b]}",format1)
                        xw.write(2,4,f"Signature",format1)
                        llist=[]
                        for line0 in reader:
                            if len(line0)!=0:
                                llist.append(line0)
                        ccb=0
                        for cc0 in llist:
                            if len(cc0[1])>ccb:
                                ccb=len(cc0[1])
                        xw.set_column('B:B', ccb+8)
                        cca=0
                        for cc1 in llist:
                            if len(cc1[0])>cca:
                                cca=len(cc1[0])
                        xw.set_column('A:A', cca+8)
                        ccd=0
                        for cc2 in llist:
                            if len(cc2[3])>ccd:
                                ccd=len(cc2[3])
                        xw.set_column('D:D', ccd+8)
                        ccc=0
                        for cc3 in llist:
                            if len(cc3[2])>ccc:
                                ccc=len(cc3[2])
                        xw.set_column('C:C', ccc+8)
                        for line1 in range(len(llist)):
                            for line2 in range(len(llist[line1])+1):
                                if line2!=len(llist[line1]):
                                    xw.write(line1+3,line2,f"{llist[line1][line2]}",format3)
                                else:
                                    xw.write(line1+3,line2,f"",format3)
                        space=""
                        for spc in range(170):
                            space+=" "
                        space2=""
                        for spc1 in range(160):
                            space2+=" "
                        xw.merge_range(f"A{len(llist)+4}:E{len(llist)+4}", f"(Signature){space}(Signature)\n    PRINCIPAL{space2}      VICE PRINCIPAL", format2)
                        xw.set_row(len(llist)+3,70)
                    showinfo(title="Success",message="Printable file saved on desktop")

            else:
                showerror(title="Failed",message="Save before print!")

                    
        def make_row(file):
            try:
                with open(file,"r") as file2:
                    reader = csv.reader(file2)
                    next(reader)
                    html_string=""""""
                    for tcpn in reader:
                        if len(tcpn)!=0:
                            Teacher=tcpn[0]
                            Class=tcpn[1]
                            Period=tcpn[2]
                            Email=tcpn[3]
                            html_string2="""
                                              <tr>
                                                <td class="item-col item">
                                                  <table cellspacing="0" cellpadding="0" width="100%">
                                                    <tr>
                                                      <td class="product">
                                                        <span style="color: #4d4d4d; font-weight:bold;">{Name_t}</span> <br />
                                                        {Email_t}
                                                      </td>
                                                    </tr>
                                                  </table>
                                                </td>
                                                <td class="item-col quantity">
                                                  {Class_t}
                                                </td>
                                                <td class="item-col">
                                                  {Period_t}
                                                </td>
                                              </tr>
                                              
                                              
                                              
                            """
                            html_string3=html_string2.format(Name_t=Teacher,Class_t=Class,Period_t=Period,Email_t=Email)
                            html_string+=html_string3
                return html_string
            except:
                showwarning(title="Error",message="File not found")

        def save_notif(list1,dict1,list2):
            list3=list(list1)
            list4=[]
            list5=[]
            for rl0 in dict1:
                if dict1[rl0].get()!="Suggestion" and dict1[rl0].get()!="":
                    list3[rl0[1]-1][list2[rl0[0]]]=dict1[rl0].get()
            for rl1 in range(1,len(list3)+1):
                for rl2 in list3[rl1-1]:
                    dict2={}
                    dict2["Teacher"]=list3[rl1-1][rl2]
                    dict2["Class"]=rl2
                    dict2["Period"]=str(rl1)
                    list4.append(dict2)
            for rl3 in list4:
                for rl4 in list5:
                    if rl4["Teacher"]==rl3["Teacher"]:
                        rl4["Class"]=rl4["Class"]+","+rl3["Class"]
                        rl4["Period"]=rl4["Period"]+","+rl3["Period"]
                        break
                else:
                    list5.append(rl3)

            if os.path.isfile("data/cd_data.json"):
                with open("data/cd_data.json","r") as noti_file:
                    notif_email=json.load(noti_file)
                for rl5 in list5:
                    rl5["Email"]=notif_email[rl5["Teacher"]]
                dtime=dt.datetime.now()
                file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
                with open(file_name,"w",newline="") as notif_csv_file:
                    field_names = ['Teacher','Class','Period','Email']
                    writer = csv.DictWriter(notif_csv_file, fieldnames=field_names)
                    writer.writeheader()
                    for rl6 in list5:
                        writer.writerow(rl6)
                showinfo(title="Success",message="Arrangement saved successfully")
            else:
                showwarning(title="Error",message="Unable to save\nPlease submit contact details!")
            
                    
        def send_notif(list1,dict1,list2):
            list3=list(list1)
            list4=[]
            list5=[]
            for rl0 in dict1:
                if dict1[rl0].get()!="Suggestion" and dict1[rl0].get()!="":
                    list3[rl0[1]-1][list2[rl0[0]]]=dict1[rl0].get()
            for rl1 in range(1,len(list3)+1):
                for rl2 in list3[rl1-1]:
                    dict2={}
                    dict2["Teacher"]=list3[rl1-1][rl2]
                    dict2["Class"]=rl2
                    dict2["Period"]=str(rl1)
                    list4.append(dict2)
            for rl3 in list4:
                for rl4 in list5:
                    if rl4["Teacher"]==rl3["Teacher"]:
                        rl4["Class"]=rl4["Class"]+","+rl3["Class"]
                        rl4["Period"]=rl4["Period"]+","+rl3["Period"]
                        break
                else:
                    list5.append(rl3)

            if os.path.isfile("data/cd_data.json"):
                with open("data/cd_data.json","r") as noti_file:
                    notif_email=json.load(noti_file)
                for rl5 in list5:
                    rl5["Email"]=notif_email[rl5["Teacher"]]
                dtime=dt.datetime.now()
                file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
                with open(file_name,"w",newline="") as notif_csv_file:
                    field_names = ['Teacher','Class','Period','Email']
                    writer = csv.DictWriter(notif_csv_file, fieldnames=field_names)
                    writer.writeheader()
                    for rl6 in list5:
                        writer.writerow(rl6)
                dtime=dt.datetime.now()
                file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
                
                pass_key='QW1hbmFtYW5AMTIzNCRhcyM='
                pass_key=base64.b64decode(pass_key)
                pass_key=pass_key.decode("ascii")
                sender_email = "arrangementsystem@gmail.com"
                mon_list=("January","February","March","April","May","June","July","August","September","October","November","December")
                dtime=dt.datetime.now()
                Date=f"{dtime.day} {mon_list[dtime.month]} {dtime.year}"
                Day=f"{dtime.strftime('%A')}"
                
                message = MIMEMultipart("alternative")
                message["From"] = "FitPeriod"
                message["To"] = "Teacher"
                text = """\
                Dear Teacher,
                This Is Your Arrangement Details"""
                from email_template import get_html
                raw_html=get_html()
                html=raw_html[0]
                html2=raw_html[1]
                html4=make_row(file_name)
                part1 = MIMEText(text, "plain")
                message.attach(part1)
                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, pass_key)
                        with open(file_name,"r") as file:
                            reader = csv.reader(file)
                            next(reader)
                            for tcpn in reader:
                                if len(tcpn)!=0:
                                    Teacher=tcpn[0]
                                    Class=tcpn[1]
                                    Period=tcpn[2]
                                    Email=tcpn[3]
                                    try:
                                        message["Subject"] = f"Arrangement in Class {Class} in Period {Period}"
                                        html3=html2.format(Class=Class,Period=Period,Name=Teacher,Email=Email,Day=Day,Date=Date,Name2=Teacher[:Teacher.find("(")-1],Table_Contents=html4)
                                        part2 = MIMEText(html+html3, "html")
                                        message.attach(part2)
                                        server.sendmail(
                                        sender_email, Email, message.as_string()
                                        )
                                    except:
                                        showerror(title="Failed",message=f"Contact details for {Teacher} not found!")
                            showinfo(title="Success",message="All notifications sent successfully\nat valid contact details.")
                except:
                    showerror(title="Error",message="An unexpected error occurred")
            else:
                showwarning(title="Error",message="Please submit contact details to continue!")

            
                                
        for unq in list1:
            if unq not in final3_raw_list:
                final3_raw_list.append(unq)
        for b in tuple1[1]:
            for c in b:
                if c not in final1_raw_list:
                    final1_raw_list.append(c)
        for m in range(len(list2)):
            for n in list2[m]:
                if n!='nil':
                    raw_dict[m][n[0:n.find("(")-1]]=n[n.find('(')+1:-1]
        for h in final2_raw_list:
            if h not in final1_raw_list:
                i=final2_raw_list.index(h)
                del final2_raw_list[i]
                
        main_canvas0=tk.Frame(newWindow,bg="#000000")
        main_canvas0.grid(row=1,columnspan=9)
        scroll0=ttk.Scrollbar(main_canvas0,orient="vertical")
        scroll0.pack(fill=Y, side='right')
        canvas0=tk.Canvas(main_canvas0,width=1098,height=60,bg="#000000",bd=0,relief=FLAT,highlightthickness=0)
        frame0=tk.Frame(canvas0,bg="#000000")
        frame0.pack()
        frame3=tk.Frame(canvas0,bg='#000000')
        frame3.pack()
        dtime=dt.datetime.now()
        tk.Label(main_canvas0,text=f"Generated Arrangement {dtime.day}/{dtime.month}/{dtime.year} {dtime.strftime('%A')}",font=('Helvetica', 18),fg="#ffffff",bg="#000000").pack(ipadx=10)
        canvas0.create_window(350,10,anchor=NW,window=frame0)
        canvas0.create_window(410,5,anchor=NW,window=frame3)
        canvas0.config(scrollregion=(0,0,1000,320),yscrollcommand=scroll0.set)
        canvas0.update_idletasks()
        canvas0.pack(fill='both',expand='true')
        scroll0.config(command=canvas0.yview)
        
        nwframe=tk.Frame(newWindow)
        nwframe.grid(row=2,column=0,sticky=W)
        nwframe1=tk.Frame(newWindow)
        nwframe1.grid(row=3,column=0)
        nwcanvas=tk.Canvas(nwframe1,width=1098,height=250,bg='#000000',relief=FLAT,highlightthickness=0)
        nwcanvas.grid(row=0,column=0)
        nwframe2=tk.Frame(nwcanvas)
        nwframe2.pack(fill='both',expand='true')
        nwcanvas.create_window(0,0,anchor=NW,window=nwframe2)
        nwscroll=ttk.Scrollbar(nwframe1,orient="vertical")
        nwscroll.grid(row=0,column=1,sticky=NS)
        nwscroll.config(command=nwcanvas.yview)
        nwcanvas.config(scrollregion=nwcanvas.bbox(ALL),yscrollcommand=nwscroll.set)
        for j in range(1,len(final3_raw_list)+1):
            tk.Label(frame3,text='⚫',fg=color_list[j-1],bg='#000000',font=('Helvetica', 11)).grid(row=j-1,column=0)
            tk.Label(frame3,text=final3_raw_list[j-1],bg='#000000',font=('Helvetica', 11),fg=color_list[j-1]).grid(row=j-1,column=1)
            canvas0.configure(scrollregion=(0,0,2730,j*30),yscrollcommand=scroll0.set)
        for f in range(9):
            canvas1=tk.Canvas(nwframe,width=120,height=30,bg='#000000',relief=FLAT,highlightthickness=1)
            frame1=tk.Frame(canvas1,bg="#000000")
            frame1.pack()
            canvas1.create_window(60,19,anchor=CENTER,window=frame1)
            canvas1.grid(row=1,column=f,padx=0)
            tk.Label(frame1,text=period_list[f],font=('Helvetica', 11),bg='#000000',fg='#ffffff').pack()
        for g in range(len(final1_raw_list)):
            nwcanvas.config(scrollregion=(0,0,1200,(g+1)*62),yscrollcommand=nwscroll.set)
            canvas3=tk.Canvas(nwframe2,width=120,height=60,bg='#000000',relief=FLAT,highlightthickness=1)
            frame2=tk.Frame(canvas3)
            frame2.pack()
            canvas3.create_window(60,30,anchor=CENTER,window=frame2)
            canvas3.grid(row=g+2,column=0)
            tk.Label(frame2,text=final1_raw_list[g],bg='#000000',fg='#ffffff',font=my_font3).pack()
        for d in range(len(final1_raw_list)):
            for e in range(1,9):
                canvas2=tk.Canvas(nwframe2,width=120,height=60,bg='#a3e4d7',relief=FLAT,highlightthickness=1)
                frame4=tk.Frame(canvas2)
                frame4.pack(fill='both',expand='true')
                frame5=tk.Frame(canvas2)
                frame5.pack(fill='both',expand='true')
                frame6=tk.Frame(canvas2)
                frame6.pack(fill='both',expand='true')
                canvas2.create_window(60,40,anchor=CENTER,window=frame4)
                canvas2.create_window(3,2,anchor=NW,window=frame5)
                canvas2.create_window(21,2,anchor=NW,window=frame6)
                canvas2.grid(row=d+2,column=e,sticky=NSEW)
                for k in tuple1[1][e-1]:
                    if final1_raw_list[d] == k:
                        st_var=second_teacher_var[(d,e)]
                        combo_box0=ttk.Combobox(frame6,textvariable=st_var,values=['Suggestion']+tuple1[0][e-1][k],state='readonly',width=10)
                        final4_raw_dict[(d,e)]=tuple1[0][e-1][k]
                        combo_box0.pack()
                        combo_box0.current(0)
                        color_index=list1.index(raw_dict[e-1][k])
                        tk.Label(frame5,text='⚫',fg=color_list[color_index],bg='#a3e4d7',font=my_font2).grid(row=0,column=0,sticky=W)
                        tk.Label(frame4,text=f"{tuple1[1][e-1][k][:tuple1[1][e-1][k].find('(')-1]}\n{tuple1[1][e-1][k][tuple1[1][e-1][k].find('('):]}",font=('Helvetica', 8),bg='#a3e4d7').grid(row=1,column=0)
        row_var=len(final1_raw_list)+4
        end_frame=tk.Frame(newWindow,bg="#000000")
        end_frame.grid(row=row_var,columnspan=9)
        internal_end_frame0=tk.Frame(end_frame,bg="#000000")
        internal_end_frame0.grid(row=0)
        internal_end_frame1=tk.Frame(end_frame,bg="#000000")
        internal_end_frame1.grid(row=1)
        img16=Image.open("assets/vector/print.png")
        img16=img16.resize((70, 28), Image.ANTIALIAS)
        img16=ImageTk.PhotoImage(img16)
        prbtn=tk.Button(internal_end_frame1,image=img16,relief=tk.FLAT,bg="#000000",fg="#000000",activebackground="#000000",bd=0, font=('Helvectiva', 11),command=lambda:get_val(tuple1[1],second_teacher_var,final3_raw_list,final1_raw_list))
        prbtn.image=img16
        prbtn.pack(side=RIGHT,padx=2,pady=10,ipadx=5)
        img17=Image.open("assets/vector/send.png")
        img17=img17.resize((60, 28), Image.ANTIALIAS)
        img17=ImageTk.PhotoImage(img17)
        sebtn=tk.Button(internal_end_frame1,image=img17,relief=tk.FLAT,bg="#000000",fg="#000000",activebackground="#000000",bd=0, font=('Helvectiva', 11),command=lambda:send_notif(tuple1[1],second_teacher_var,final1_raw_list))
        sebtn.image=img17
        sebtn.pack(side=RIGHT,padx=2,pady=10,ipadx=5)
        img18=Image.open("assets/vector/save.png")
        img18=img18.resize((60, 28), Image.ANTIALIAS)
        img18=ImageTk.PhotoImage(img18)
        sabtn=tk.Button(internal_end_frame1,image=img18,relief=tk.FLAT,bg="#000000",fg="#000000",activebackground="#000000",bd=0, font=('Helvectiva', 11),command=lambda:save_notif(tuple1[1],second_teacher_var,final1_raw_list))
        sabtn.image=img18
        sabtn.pack(side=RIGHT,padx=2,pady=10,ipadx=5)

class OlderArng(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("Older Arrangements - FitPeriod")
        from tkcalendar import Calendar, DateEntry
        from datetime import date, timedelta, datetime

        def all_children(window) :
            _list = window.winfo_children()
            for item in _list :
                if item.winfo_children() :
                    _list.extend(item.winfo_children())
            return _list

        def print_csv(csv_name,canvas,frame):
            if os.path.isfile(f"arrangements/{csv_name}"):
                with open(f"arrangements/{csv_name}","r") as csvfile:
                    widget_list1 = all_children(frame)
                    for item in widget_list1:
                        item.destroy()
                    col=0
                    reader=csv.reader(csvfile)
                    row1 = next(reader)
                    for label in row1:
                        tk.Label(frame,text=label.upper(),fg='#ffffff',bg='#000000',font=('Helvetica', 15)).grid(row=0,column=col,sticky=W,padx=10,pady=(0,10))
                        col+=1
                    row1=1
                    for row in reader:
                        if len(row)!=0:
                            col=0
                            for label2 in row:
                                tk.Label(frame,text=label2,fg='#ffffff',bg='#000000',font=('Helvetica', 10)).grid(row=row1,column=col,sticky=W,padx=10)
                                col+=1
                            canvas.configure(scrollregion=(0,0,1000,1500))
                            row1+=1 

            else:
                showwarning(title="Error",message="Arrangement not found")

        def make_csv2(canvas,d1,frame):
            sdate = d1.get_date()
            abc=datetime.strptime(str(sdate),'%Y-%m-%d')
            csv_name=f"{abc.strftime('X%d-X%m-%Y').replace('X0','X').replace('X','')}.csv"
            print_csv(csv_name,canvas,frame)
        
        ar_frame0=tk.Frame(self,bg='#000000')
        ar_frame0.pack(fill='both',expand='true')
        tk.Label(ar_frame0,text='OLDER ARRANGEMENTS',fg='#ffffff',bg='#000000',font=my_font3).pack(pady=10)
        ar_frame2=tk.Frame(ar_frame0,bg='#000000')
        ar_frame2.pack(fill='both',expand='true')
        ar_scroll=ttk.Scrollbar(ar_frame0)
        ar_scroll.pack(side=RIGHT,fill=Y,anchor=E,pady=(50,0))
        ar_canvas=tk.Canvas(ar_frame0,width=1114,height=2000,yscrollcommand=ar_scroll.set,bg='#000000',highlightthickness=0)
        ar_canvas.pack(fill='both',expand='true',pady=(50,0))
        tk.Label(ar_frame2,text='Enter Date',fg='#ffffff',bg='#000000',font=('Helvetica', 15)).pack(pady=10,side=LEFT,padx=(250,0))
        de1=DateEntry(ar_frame2,state="readonly",width=10)
        de1.pack(side=LEFT,padx=(10,10))
        csv_frame0=tk.Frame(ar_canvas,bg='#000000')
        csv_frame0.pack(fill='both',expand='true')
        ar_canvas.create_window(250,0,anchor=NW,window=csv_frame0)
        img13=Image.open("assets/vector/apply.png")
        img13=img13.resize((60, 22), Image.ANTIALIAS)
        img13=ImageTk.PhotoImage(img13)
        appbtn=tk.Button(ar_frame2,image=img13,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 8),command=lambda:make_csv2(ar_canvas,de1,csv_frame0))
        appbtn.image=img13
        appbtn.pack(padx=(5,0),ipadx=8,side=LEFT)

        ar_canvas.configure(scrollregion=ar_canvas.bbox('all'))
        ar_scroll.config(command=ar_canvas.yview)

class NewTT(Frame):
    def __init__(self, master):
        window.update()
        Frame.__init__(self, master)
        master.title("New Time Table - FitPeriod")
        self.newttexel()
        
    def validate_day(self,day_str):
        fstr=""
        vlist=[1,2,3,4,5,6]
        if len(day_str)!=0:
            for a in day_str:
                if int(a) in vlist and a not in fstr:
                    fstr+=a
                else:
                    return "error"
                    break
            else:
                return fstr
        else:
            return "empty"

    def readsheet(self):
        import xlrd
        errortxt="no"
        fpath=self.saveas_file("open")
        wb=xlrd.open_workbook(fpath)
        sheet=wb.sheet_by_index(0)
        dl_2=["MON", "TUE", "WED", "THU", "FRI", "SAT"]
        pl_3=["PERIOD 1","PERIOD 2","PERIOD 3","PERIOD 4","PERIOD 5","PERIOD 6","PERIOD 7","PERIOD 8"]
        pl_2=["p1","p2","p3","p4","p5","p6","p7","p8"]
        cl_2=["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
        with open("data/stt_data.json","r") as sdj:
            vfile=json.load(sdj)
        pc0={}
        pc={}
        fres_data={}
        for f in range(14):
            pc0[cl_2[f]]=[]
        for g in range(8):
            pc[pl_2[g]]=pc0
        with open("data/stt_data.json","r") as std:
            sttd=json.load(std)
            for e in sttd:
                fres_data[e]=pc
            with open("assets/blank_day_data.json","w") as bdd1:
                    json.dump(fres_data,bdd1)
        with open("assets/blank_day_data.json","r") as bdd2:
                fres=json.load(bdd2)
                
        for a in range(1,len(vfile)*16,16):
            bn=0
            for b in range(2,17,2):
                cn=0
                for c in range(a,a+14):
                    vfg=sheet.cell_value(c+1,b+1)
                    if type(vfg)!=str:
                        vfg=int(vfg)
                        vfg=str(vfg)
                    alist=self.validate_day(vfg)
                    if alist=="empty":
                        pass
                    elif alist=="error":
                        showerror(title="Error",message=f"Error while reading\n{sheet.cell_value(a,1)}>{pl_3[bn]}>{pl_2[bn]}")
                        errortxt="yes"
                    elif type(alist)==str:
                        for d in alist:
                            fres[sheet.cell_value(a,1)][pl_2[bn]][cl_2[cn]].append(int(d))
                    cn+=1
                bn+=1
        
        if errortxt=="no":
            ttdict2={}
            ttdict3={}
            for e in cl_2:
                ttdict2[e]={}
                for f in dl_2:
                    ttdict2[e][f]=[]
                    for k in range(8):
                        ttdict2[e][f].append([])
            for g in fres:
                for h in pl_2:
                    for i in cl_2:
                        for j in fres[g][h][i]:
                            ttdict2[i][dl_2[j-1]][pl_2.index(h)].append(g)
            for l in cl_2:
                ttdict3[l]={}
                for m in dl_2:
                    ttdict3[l][m]=[]
                    for n in ttdict2[l][m]:
                        if len(n)==1:
                            ttdict3[l][m].append(n[0])
                        else:
                            ttdict3[l][m].append(n)
            with open("data/tt_data.json","w") as final_file:
                json.dump(ttdict3,final_file)
                showinfo(title="Success",message="Time table successfully submitted")
        elif errortxt=="yes":
            showerror(title="Error",message=f"Please re-submit the file after fixing the errors")
                        
    def saveas_file(self,argt):
        files=[('Exel Files', '*.xlsx')]
        if argt=="save":
            from tkinter.filedialog import asksaveasfile
            file=asksaveasfile(filetypes=files,defaultextension=files)
        elif argt=="open":
            from tkinter.filedialog import askopenfile
            file=askopenfile(filetypes=files,defaultextension=files)
        dr=str(file)
        dr1=dr[dr.find("name='")+6:]
        dr2=dr1[:dr1.find("'")]
        return dr2

    def blanksheet(self):
        if os.path.isfile("data/stt_data.json"):
            import xlsxwriter as xr
            drname=self.saveas_file("save")
            with xr.Workbook(drname) as xtt:
                with open("data/stt_data.json") as namelist:
                    namelist1=json.load(namelist)
                xtts=xtt.add_worksheet()
                xtts.protect()
                f0=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'})
                f1=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'locked':TRUE})
                f2=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'locked':TRUE})
                f5=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'})
                f3=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'top',
                    'locked':TRUE})
                f4=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'left',
                    'valign': 'top',
                    'locked':TRUE})
                f6=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'locked':FALSE})
                xtts.data_validation(0,0,len(namelist1)*16,17,{'validate':'integer','criteria':'between','minimum':1,'maximum':123456,'input_title':'Enter days:','input_message':'From 1 to 6','show_input':TRUE,'error_title':'Error: Follow the points:','error_message':'1.Value should be an integer\n2.Do not repeat same day\n3.Days should be in accending order','error_type':'stop'})
                xtts.merge_range('A1:R1', f"TIME TABLE FILE", f0)
                xtts.set_row(0,30)
                xtts.set_column('B:B',40)
                f0.set_font_size(15)
                f1.set_font_size(13)
                f2.set_font_size(11)
                f5.set_font_size(11)
                f6.set_font_size(11)
                f3.set_font_size(13)
                f4.set_font_size(13)
                alist=['C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R']
                clist=["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
                srn=1
                for d in range(2,len(namelist1)*16,16):
                    xtts.merge_range(f"B{d}:B{d+14}", namelist1[srn-1], f4)
                    xtts.merge_range(f"A{d}:A{d+14}", f"{srn}.", f3)
                    srn+=1
                    pv=1
                    for a in range(0,15,2):
                        xtts.merge_range(f"{alist[a]}{d}:{alist[a+1]}{d}", f"PERIOD {pv}", f1)
                        pv+=1
                    for c in range(2,17,2):
                        cl=0
                        for b in range(d,d+14):
                            xtts.write(b,c,clist[cl],f2)
                            xtts.write(b,c+1,"",f6)
                            cl+=1
        else:
            showerror(title="Error",message="Teachers data not found!")

    def updatefile(self):
        if os.path.isfile("data/tt_data.json"):
            import xlsxwriter as xr
            drname=self.saveas_file("save")
            with open("data/tt_data.json","r") as ttfile:
                ttdict=json.load(ttfile)
                fres_data={}
                cl=["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
                pl=["p1","p2","p3","p4","p5","p6","p7","p8"]
                dl=["MON", "TUE", "WED", "THU", "FRI", "SAT"]
                pc0={}
                pc={}
                for f in range(14):
                    pc0[cl[f]]=[]
                for g in range(8):
                    pc[pl[g]]=pc0
                with open("data/stt_data.json","r") as std:
                    sttd=json.load(std)
                    for e in sttd:
                        fres_data[e]=pc
                    with open("assets/blank_day_data.json","w") as bdd:
                        json.dump(fres_data,bdd)
                with open("assets/blank_day_data.json","r") as bddj:
                    fres=json.load(bddj)
                    
                for ab in cl:
                    for bc in dl:
                        for cd in range(len(ttdict[ab][bc])):
                            if type(ttdict[ab][bc][cd])!=list:
                                fres[ttdict[ab][bc][cd]][pl[cd]][ab].append(dl.index(bc)+1)
                            else:
                                for de in ttdict[ab][bc][cd]:
                                    fres[de][pl[cd]][ab].append(dl.index(bc)+1)
            tnamelist=list(fres.keys())

            with xr.Workbook(drname) as xtt:
                xtts=xtt.add_worksheet()
                xtts.protect()
                f0=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'})
                f1=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'locked':TRUE})
                f2=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'locked':TRUE})
                f5=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'})
                f3=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'top',
                    'locked':TRUE})
                f4=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'left',
                    'valign': 'top',
                    'locked':TRUE})
                f6=xtt.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'locked':FALSE})
                xtts.data_validation(0,0,len(tnamelist)*16,17,{'validate':'integer','criteria':'between','minimum':1,'maximum':123456,'input_title':'Enter days:','input_message':'From 1 to 6','show_input':TRUE,'error_title':'Error: Follow the points:','error_message':'1.Value should be an integer, 2.Do not repeat same day, 3.Days should be in accending order','error_type':'stop'})
                xtts.merge_range('A1:R1', f"TIME TABLE FILE", f0)
                xtts.set_row(0,30)
                xtts.set_column('B:B',40)
                f0.set_font_size(15)
                f1.set_font_size(13)
                f2.set_font_size(11)
                f5.set_font_size(11)
                f6.set_font_size(11)
                f3.set_font_size(13)
                f4.set_font_size(13)
                alist=['C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R']
                clist=["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
                cl_1=["VIA", "VIB", "VIIA", "VIIB", "VIIIA", "VIIIB", "IXA", "IXB", "XA", "XB", "XIA", "XIB", "XIIA", "XIIB"]
                pl_1=["p1","p2","p3","p4","p5","p6","p7","p8"]
                srn=1
                for d in range(2,len(tnamelist)*16,16):
                    xtts.merge_range(f"B{d}:B{d+14}", tnamelist[srn-1], f4)
                    xtts.merge_range(f"A{d}:A{d+14}", f"{srn}.", f3)
                    pv=1
                    pn=0
                    for c in range(2,17,2):
                        xtts.merge_range(f"{alist[c-2]}{d}:{alist[c-1]}{d}", f"PERIOD {pv}", f1)
                        pv+=1
                        cl=0
                        cn=0
                        for b in range(d,d+14):
                            drsn=""
                            for mn in fres[tnamelist[srn-1]][pl_1[pn]][cl_1[cn]]:
                                drsn+=str(mn)
                            xtts.write(b,c,clist[cl],f2)
                            xtts.write(b,c+1,drsn,f6)
                            cl+=1
                            cn+=1
                        pn+=1
                    srn+=1
                        
        else:
            showerror(title="Error",message="Time table not found!")

    def newttexel(self):
        fr0=tk.Frame(self,bg="#000000")
        fr0.pack(fill=BOTH,expand=TRUE)
        tk.Label(fr0,text="TIME TABLE DATA",font=my_font2,fg="#ffffff",bg="#000000").pack(pady=10,fill=Y)
        tk.Label(fr0,text="Time table data can be submitted in EXEL(.xlsx) files.\nSave file from below for update data or submit new data.",font=('Helvetica',15),fg="#ffffff",bg="#000000").pack(pady=10)
        tk.Label(fr0,text="Note: Data can be submitted through the .xlsx file saved from here",font=('Helvetica',10),fg="#ffffff",bg="#000000").pack()
        fr2=tk.Frame(self,bg="#000000")
        fr2.pack(fill=BOTH,expand=TRUE)
        fr1=tk.Frame(fr2,bg="#000000")
        fr1.pack(fill=BOTH,expand=TRUE,pady=(30,0))

        img6=Image.open("assets/vector/update.png")
        img6=img6.resize((80, 28), Image.ANTIALIAS)
        img6=ImageTk.PhotoImage(img6)
        upbtn=tk.Button(fr1,image=img6,command=lambda:self.updatefile(),text='Update Data',relief=tk.FLAT,activebackground="#000000",bg="#000000",fg="#000000", font=('Helvectiva', 10))
        upbtn.pack(padx=(80,20),side=LEFT)
        upbtn.image=img6
        
        img7=Image.open("assets/vector/blanksheet.png")
        img7=img7.resize((130, 28), Image.ANTIALIAS)
        img7=ImageTk.PhotoImage(img7)
        dnbtn=tk.Button(fr1,image=img7,command=lambda:self.blanksheet(),text='Download New File',relief=tk.FLAT,activebackground="#000000",bg="#000000",fg="#000000", font=('Helvectiva', 10))
        dnbtn.pack(side=LEFT,padx=(0,20))
        dnbtn.image=img7
        
        img8=Image.open("assets/vector/import.png")
        img8=img8.resize((80, 28), Image.ANTIALIAS)
        img8=ImageTk.PhotoImage(img8)
        imbtn=tk.Button(fr1,image=img8,command=lambda:self.readsheet(),text='Import File',relief=tk.FLAT,activebackground="#000000",bg="#000000",fg="#000000", font=('Helvectiva', 10))
        imbtn.pack(side=LEFT)
        imbtn.image=img8

class Teachers(Frame,FitPeriod):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("Teachers - FitPeriod")
        self.make_fields(master)
    def make_fields(self,master):
        selfframe=tk.Frame(self,bg="#000000")
        selfframe.pack(fill=BOTH,expand=TRUE)
        teacher_var_tuple={}
        teacher_var_tuple_list=[]
        for var_n in range(1,51):
            for var_n1 in range(1,5):
                teacher_var_tuple[(var_n,var_n1)]=StringVar()
        for var_n2 in range(1,51):
            for var_n3 in range(1,5):
                teacher_var_tuple_list.append((var_n2,var_n3))
        fields_num=0
        def fill_fields(self,value,vardict={}):
            clist0,elist0=[],[]
            clist1,elist1,clist2,elist2=[],[],[],[]
            fflist=window.winfo_children()
            for item in fflist:
                if item.winfo_children():
                    fflist.extend(item.winfo_children())
            for item1 in fflist:
                if type(item1)==tk.ttk.Combobox:
                    clist0.append(item1)
                elif type(item1)==tk.Entry:
                    elist0.append(item1)
            cl=1
            for item2 in clist0:
                if cl%2==0:
                    clist1.append(item2)
                else:
                    clist2.append(item2)
                cl+=1
            el=1
            for item3 in elist0:
                if el%2==0:
                    elist1.append(item3)
                else:
                    elist2.append(item3)
                el+=1
            vardict=vardict[0:int(value)]
            for item4 in range(len(elist1)):
                if len(elist1[item4].get())==0:
                    if item4<=len(vardict)-1:
                        if vardict[item4][:vardict[item4].index(" ")] in ['SH','SMT','MISS']:
                            elist1[item4].insert(0,vardict[item4][vardict[item4].index(" ")+1:vardict[item4].index("(")-1])
                        else:
                            elist1[item4].insert(0,vardict[item4][:vardict[item4].index("(")-1])
            elist2.pop(0)
            cvalue2=[]
            for item5 in range(len(elist2)):
                if len(elist2[item5].get())==0:
                    if item5<=len(vardict)-1:
                        chvar=0
                        for val in ['TGT','PGT','PRINCIPAL','VICEPRINCIPAL']:
                            if val in vardict[item5]:
                                chvar=vardict[item5].rfind(val)+len(val)+1
                        if chvar!=0:
                            elist2[item5].insert(0,vardict[item5][chvar:-1])
                        else:
                            elist2[item5].insert(0,vardict[item5][vardict[item5].index("(")+1:-1])
            chlist=['Select','TGT','PGT','PRINCIPAL','VICEPRINCIPAL','Unspecified']
            chlist2=['Select','SH','SMT','MISS','Unspecified']

            if (clist2[0]).get()=="Select":
                cn1=0
                for item7 in vardict:
                    try:
                        sn1=item7[:item7.index(" ")]
                        clist2[cn1].current(chlist2.index(sn1))
                    except:
                        sn3=item7[:item7.index("(")-1]
                        if sn3 in ['SH','SMT','MISS']:
                            clist2[cn1].current(chlist2.index(sn3))
                        else:
                            clist2[cn1].current(chlist2.index('Unspecified'))
                    cn1+=1    
            if (clist1[0]).get()=="Select":
                cn=0
                for item6 in vardict:
                    try:
                        sn=item6[item6.index("(")+1:][0:item6[item6.index("(")+1:].index(" ")]
                        clist1[cn].current(chlist.index(sn))
                    except:
                        sn=item6[item6.index("(")+1:-1]
                        if sn in ['PRINCIPAL','VICEPRINCIPAL']:
                            clist1[cn].current(chlist.index(sn))
                        else:
                            clist1[cn].current(chlist.index('Unspecified'))
                    cn+=1


        def clear_fields(self):
            res=messagebox.askquestion('Clear Fields', 'Do you want to clear all fields?')
            if res == 'yes' :
                flist=window.winfo_children()
                for item in flist:
                    if item.winfo_children():
                        flist.extend(item.winfo_children())
                flist.pop(14)
                for item1 in flist:
                    if type(item1)==tk.Entry:
                        item1.delete(0,END)
                    elif type(item1)==tk.ttk.Combobox:
                        item1.current(0)
        def all_children(window):
            _list=window.winfo_children()
            for item in _list:
                if item.winfo_children():
                    _list.extend(item.winfo_children())
            return _list
        def disable_w0(val):
            for var_n4 in range(1,val+1):
                teacher_var_tuple[teacher_var_tuple_list[teacher_var_tuple_list.index((var_n4,3))]].trace("w",disable_w)
        def get_value(num,wid):
            all_teachers_entry=[]
            validate_num=0
            validate_num1=0
            for value0 in range(1,num+1):
                main_str=""
                for value1 in range(1,5):
                    var_value0=teacher_var_tuple[teacher_var_tuple_list[teacher_var_tuple_list.index((value0,value1))]].get()
                    if len(var_value0)!=0 and var_value0!="Select":
                        if var_value0!="Unspecified":
                            if value1==1 or value1==2:
                                main_str+=var_value0.upper()+" "
                            elif value1==3:
                                main_str+="("+var_value0.upper()+" "
                            else:
                                main_str+=var_value0.upper()+")"
                        else:
                            if value1==3:
                                main_str+="("
                    else:
                        validate_num+=1
                        
                all_teachers_entry.append(main_str)
            if validate_num!=0:
                showerror(title="Error", message="Field cannot be empty")
            else:
                for _val in all_teachers_entry:
                    if len(_val)==0:
                        validate_num1+=1
                if validate_num1==0:
                    if os.path.isfile("data/cd_data.json"):
                        res=messagebox.askquestion('Send Notification', 'By continue present data will be overwrite!\nDo you want to continue?')
                        if res == 'yes' :
                            with open("data/stt_data.json","w") as main_tdata:
                                json.dump(all_teachers_entry,main_tdata)
                    else:
                        with open("data/stt_data.json","w") as main_tdata:
                            json.dump(all_teachers_entry,main_tdata)
                    showinfo(title='Success',message='Teachers submitted successfully')
                    
        def lbg(self,fname,alist):
            def aman():
                print("aman")
            import multiprocessing
            p1 = multiprocessing.Process(target=self.loading_bar, args=(2, )) 
            p2 = multiprocessing.Process(target=aman) 
            
            # starting process 1 
            p1.start() 
            # starting process 2 
            p2.start() 
            
            # wait until process 1 is finished 
            p1.join() 
            # wait until process 2 is finished 
            p2.join() 

        def create_fields(master,self,value,canvas,scroll,selfframe,vardict={}):
            global btval
            sname=('Select','SH','SMT','MISS','Unspecified')
            status=('Select','TGT','PGT','PRINCIPAL','VICEPRINCIPAL','Unspecified')
            dict1={}
            try:
                value=int(value)
            except:
                showwarning(title="Error", message="Please enter valid no of teachers")
            if type(value)==int and value<=50:
                widget_list = all_children(self)
                for item in widget_list:
                    item.destroy()
                tk.Label(self,text="Sr. ",font=my_font2,fg="#ffffff",bg="#000000").grid(row=1,column=0,padx=5)
                tk.Label(self,text="Sh/Smt",font=my_font2,fg="#ffffff",bg="#000000").grid(row=1,column=1,padx=5)
                tk.Label(self,text="Full Name",font=my_font2,fg="#ffffff",bg="#000000").grid(row=1,column=2,padx=5)
                tk.Label(self,text="T/P",font=my_font2,fg="#ffffff",bg="#000000").grid(row=1,column=3,padx=5)
                tk.Label(self,text="Subject",font=my_font2,fg="#ffffff",bg="#000000").grid(row=1,column=4,padx=5)
                for field in range(1,value+1):
                    cbox0=ttk.Combobox(self,width=7,state='readonly',values=sname,textvariable=teacher_var_tuple[(field,1)])
                    cbox0.grid(row=field+1,column=1,padx=0,pady=10)
                    cbox0.current(0)
                    tk.Label(self,text=f"{field}.",font=my_font2,bg="#000000",fg="#ffffff").grid(row=field+1,column=0,padx=0,pady=10)
                    ebox0=tk.Entry(self,width=30,textvariable=teacher_var_tuple[(field,2)],bg="#ffffff",fg="#000000",relief=FLAT,font=('Helvetica', 11))
                    ebox0.grid(row=field+1,column=2,padx=10,pady=10)
                    cbox1=ttk.Combobox(self,width=11,state='readonly',values=status,textvariable=teacher_var_tuple[(field,3)])
                    cbox1.grid(row=field+1,column=3,padx=5,pady=10)
                    cbox1.current(0)
                    ebox1=tk.Entry(self,width=25,textvariable=teacher_var_tuple[(field,4)],bg="#ffffff",fg="#000000",relief=FLAT,font=('Helvetica', 11))
                    ebox1.grid(row=field+1,column=4,padx=10,pady=10)
                    
                    canvas.config(scrollregion=(0,0,700,field*58+30),yscrollcommand=scroll.set)
                    fields_num=value

                disable_w0(value)
                img12=Image.open("assets/vector/submit.png")
                img12=img12.resize((80, 28), Image.ANTIALIAS)
                img12=ImageTk.PhotoImage(img12)
                sbubtn=tk.Button(selfframe,command=lambda:get_value(value,ebox1),image=img12,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 10))
                sbubtn.image=img12
                sbubtn.grid(row=3,columnspan=9,pady=(20,0))
                
                if len(vardict)!=0:
                    fill_fields(self,value,vardict)

            elif type(value)==int:
                showwarning(title="Error", message="Max 50 teachers allowed")
            
        no_var=StringVar()
        t_frame0=tk.Frame(selfframe,bg="#000000",highlightthickness=0)
        t_frame0.grid(row=2,columnspan=9)
        t_scroll0=ttk.Scrollbar(t_frame0,orient="vertical")
        t_scroll0.pack(fill=Y, side='right')
        
        tk.Label(selfframe,text='SUBJECT TEACHERS DATA',font=my_font,fg="#ffffff",bg="#000000").grid(row=0,columnspan=9,pady=(15,5))
        
        t_frame1=tk.Frame(selfframe,bg="#000000")
        t_frame1.grid(row=1,pady=(0,10),columnspan=9)
        
        tk.Label(t_frame1,text='  No of teachers: ',font=my_font2,fg="#ffffff",bg="#000000").grid(row=0,column=0)
        tk.Entry(t_frame1,width=10,textvariable=no_var,bg="#ffffff",fg="#000000",relief=FLAT).grid(row=0,column=1)
        if os.path.isfile("data/stt_data.json"):
            with open("data/stt_data.json","r") as varfile:
                vardict=json.load(varfile)
                no_var.set(len(vardict))
        else:
            no_var.set(5)
        
        t_canvas0=tk.Canvas(t_frame0,width=782.7,height=450,bg="#000000",highlightthickness=0)
        t_canvas0.config(scrollregion=t_canvas0.bbox(ALL),yscrollcommand=t_scroll0.set)
        t_canvas0.update_idletasks()
        t_canvas0.pack(fill='both',expand='true')
        t_scroll0.config(command=t_canvas0.yview)
        
        t_frame2=tk.Frame(t_canvas0,bg="#000000")
        t_frame2.pack(fill='both',expand='true')

        try:
            cv=vardict[-1]
            img9=Image.open("assets/vector/apply.png")
            img9=img9.resize((50, 22), Image.ANTIALIAS)
            img9=ImageTk.PhotoImage(img9)
            apbtn=tk.Button(t_frame1,image=img9,activebackground="#000000",bd=0,command=lambda:create_fields(t_canvas0,t_frame2,no_var.get(),t_canvas0,t_scroll0,selfframe,vardict),relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 10))
            #apbtn=tk.Button(t_frame1,image=img9,activebackground="#000000",bd=0,command=lambda:lbg(master,"aman",[1,2]),relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 10))
            
            apbtn.image=img9
            apbtn.grid(row=0,column=2,padx=(10,10))
        except:
            img9=Image.open("assets/vector/apply.png")
            img9=img9.resize((50, 22), Image.ANTIALIAS)
            img9=ImageTk.PhotoImage(img9)
            apbtn=tk.Button(t_frame1,image=img9,activebackground="#000000",bd=0,command=lambda:create_fields(t_canvas0,t_frame2,no_var.get(),t_canvas0,t_scroll0,selfframe,vardict={}),relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 10))
            apbtn.image=img9
            apbtn.grid(row=0,column=2,padx=(10,10))

        img10=Image.open("assets/vector/clearall.png")
        img10=img10.resize((80, 22), Image.ANTIALIAS)
        img10=ImageTk.PhotoImage(img10)
        clbtn=tk.Button(t_frame1,image=img10,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000",command=lambda:clear_fields(self),font=('Helvectiva', 10))
        clbtn.image=img10
        clbtn.grid(row=0,column=3,pady=5)

        t_canvas0.create_window(25,0,anchor=NW,window=t_frame2)
        def disable_w(a,b,c):
            value=31
            teacher_var_tuple1=dict(teacher_var_tuple)
            for var_n6 in range(1,value+1):
                for var_n7 in range(1,5):
                    if var_n7!=3:
                        del teacher_var_tuple1[(var_n6,var_n7)]
            try:
                for var_n5 in teacher_var_tuple1:
                    if teacher_var_tuple[var_n5].get() in ['PRINCIPAL','VICEPRINCIPAL']:
                        all_children(t_frame2)[5+5*var_n5[0]].config(state='disabled')
                        teacher_var_tuple[(var_n5[0],var_n5[1]+1)].set("DISABLED")
                    else:
                        try:
                            if all_children(t_frame2)[5+5*var_n5[0]].cget('state')=='disabled':
                                all_children(t_frame2)[5+5*var_n5[0]].config(state='normal')
                                teacher_var_tuple[(var_n5[0],var_n5[1]+1)].set("")
                        except:
                            pass
            except:
                pass
        try:
            cv1=vardict[-1]
            create_fields(t_canvas0,t_frame2,no_var.get(),t_canvas0,t_scroll0,selfframe,vardict)
        except:
            create_fields(t_canvas0,t_frame2,no_var.get(),t_canvas0,t_scroll0,selfframe)

class SendNow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("Send Notifications - FitPeriod")
        self.send_now()

    def make_row(self,file):
            try:
                with open(file,"r") as file2:
                    reader = csv.reader(file2)
                    next(reader)
                    html_string=""""""
                    for tcpn in reader:
                        if len(tcpn)!=0:
                            Teacher=tcpn[0]
                            Class=tcpn[1]
                            Period=tcpn[2]
                            Email=tcpn[3]
                            html_string2="""
                                              <tr>
                                                <td class="item-col item">
                                                  <table cellspacing="0" cellpadding="0" width="100%">
                                                    <tr>
                                                      <td class="product">
                                                        <span style="color: #4d4d4d; font-weight:bold;">{Name_t}</span> <br />
                                                        {Email_t}
                                                      </td>
                                                    </tr>
                                                  </table>
                                                </td>
                                                <td class="item-col quantity">
                                                  {Class_t}
                                                </td>
                                                <td class="item-col">
                                                  {Period_t}
                                                </td>
                                              </tr>
                                              
                                              
                                              
                            """
                            html_string3=html_string2.format(Name_t=Teacher,Class_t=Class,Period_t=Period,Email_t=Email)
                            html_string+=html_string3
                return html_string
            except:
                showwarning(title="Error",message="File not found")

    def send_single_notif(self,tdict1,lb):
        def fdes():
            dtime=dt.datetime.now()
            file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
            pass_key='QW1hbmFtYW5AMTIzNCRhcyM='
            pass_key=base64.b64decode(pass_key)
            pass_key=pass_key.decode("ascii")
            sender_email = "arrangementsystem@gmail.com"
            mon_list=("January","February","March","April","May","June","July","August","September","October","November","December")
            dtime=dt.datetime.now()
            Date=f"{dtime.day} {mon_list[dtime.month]} {dtime.year}"
            Day=f"{dtime.strftime('%A')}"
            message = MIMEMultipart("alternative")
            message["From"] = "FitPeriod"
            message["To"] = "Teacher"
            text = """\
            Dear Teacher,
            This Is Your Arrangement Details"""
            from email_template import get_html
            raw_html=get_html()
            html=raw_html[0]
            html2=raw_html[1]
            html4=self.make_row(file_name)
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, pass_key)
                    with open(file_name,"r") as file:
                        reader = csv.reader(file)
                        next(reader)
                        for tcpn in reader:
                            if len(tcpn)!=0:
                                Teacher=tcpn[0]
                                Class=tcpn[1]
                                Period=tcpn[2]
                                Email=tcpn[3]
                                if Teacher in list(tdict2.keys()):
                                    try:
                                        message["Subject"] = f"Arrangement in Class {Class} in Period {Period}"
                                        html3=html2.format(Class=Class,Period=Period,Name=Teacher,Email=Email,Day=Day,Date=Date,Name2=Teacher[:Teacher.find("(")-1],Table_Contents=html4)
                                        part2 = MIMEText(html+html3, "html")
                                        message.attach(part2)
                                        server.sendmail(
                                        sender_email, Email, message.as_string()
                                        )
                                    except:
                                        showerror(title="Failed",message=f"Contact details for {Teacher} not found!")
                        showinfo(title="Success",message="Notifications sent successfully\nat valid email address.")
            except:
                showerror(title="Error",message="An unexpected error occurred")
        if os.path.isfile("data/cd_data.json"):
            tdict2={}
            if type(lb)!=tuple:
                tindex=lb.curselection()
                for tchr1 in tindex:
                    tdict2[list(tdict1.keys())[tchr1]]=list(tdict1.values())[tchr1]
            else:
                for tchr1 in range(len(tdict1)):
                    tdict2[list(tdict1.keys())[tchr1]]=list(tdict1.values())[tchr1]
            if len(tdict2)!=0:
                res=messagebox.askquestion('Send Notification', 'Do you want to send notifications\nto selected teachers?')
                if res == 'yes' :
                    fdes()
            else:
                showerror(title="Error",message="Please select at least one teacher!")
        else:
            showerror(title="Error",message="Contact details not found!")
            
        

    def send_now(self):
        dtime=dt.datetime.now()
        file_name=f"arrangements/{dtime.day}-{dtime.month}-{dtime.year}.csv"
        tk.Label(self,text='SEND NOTIFICATION',fg='#ffffff',bg='#000000',font=my_font3).pack(ipady=10,ipadx=100)
        t_frame0=tk.Frame(self,highlightthickness=0,bg="#000000")
        t_frame0.pack(expand=True,fill=BOTH)
        tk.Label(t_frame0,text=f"Select One Or Multiple Teachers",fg='#ffffff',bg='#000000',font=('Helvetica', 15)).pack(ipady=5)
        tlist={}
        tvar=StringVar()
        with open(file_name,"r") as tfile:
            reader = csv.reader(tfile)
            next(reader)
            for row in reader:
                if len(row)!=0:
                    tlist[row[0]]=row[3]

        
        t_list=Listbox(t_frame0,state="normal",bg="#000000",fg="#ffffff",width=40,bd=10,relief=FLAT,selectmode="multiple",height=10,selectbackground="#ffffff",selectforeground="#000000",font=('Helvetica', 10),highlightcolor="#ffffff")
        ins=0
        for item in list(tlist.keys()):
            t_list.insert(ins, item)
            ins+=1
        t_list.pack(side=LEFT, fill=BOTH, expand=1)
        ylscroll=ttk.Scrollbar(t_frame0,orient=VERTICAL)
        ylscroll.pack(side=RIGHT,fill=Y)
        t_list.config(yscrollcommand=ylscroll.set)
        ylscroll.config(command=t_list.yview)
        t_frame1=tk.Frame(self,highlightthickness=0,bg="#000000")
        t_frame1.pack(expand=True,fill=BOTH)
        img14=Image.open("assets/vector/send.png")
        img14=img14.resize((55, 25), Image.ANTIALIAS)
        img14=ImageTk.PhotoImage(img14)
        snbtn=tk.Button(t_frame1,command=lambda:self.send_single_notif(tlist,t_list),image=img14,relief=tk.FLAT,activebackground="#000000",bd=0,bg="#000000",fg="#000000", font=('Helvectiva', 10))
        snbtn.image=img14
        snbtn.pack(side=LEFT,pady=10,padx=(175,0))
        img15=Image.open("assets/vector/sendall.png")
        img15=img15.resize((80, 25), Image.ANTIALIAS)
        img15=ImageTk.PhotoImage(img15)
        sabtn=tk.Button(t_frame1,command=lambda:self.send_single_notif(tlist,(0,)),image=img15,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 10))
        sabtn.image=img15
        sabtn.pack(side=LEFT,pady=10,padx=10)
        
class ContactDetails(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("Manage Contact Details - FitPeriod")
        self.cd_fields()
        master.config(bg="#000000")
    def cd_fields(self):
        tk.Label(self,text='CONTACT DETAILS',font=my_font,bg="#000000",fg="#ffffff").pack(ipadx=300,ipady=15)
        t_frame0=tk.Frame(self,bg="#000000")
        t_frame0.pack(expand=True,fill=BOTH)
        t_scroll0=ttk.Scrollbar(t_frame0,orient="vertical")
        t_scroll0.pack(fill=Y, side='right')
        t_canvas0=tk.Canvas(t_frame0,width=800,height=487,bg="#000000",highlightthickness=0)
        t_canvas0.config(scrollregion=t_canvas0.bbox('all'),yscrollcommand=t_scroll0.set)
        t_canvas0.update_idletasks()
        t_canvas0.pack(fill=BOTH,expand=True)
        t_scroll0.config(command=t_canvas0.yview)
        t_frame2=tk.Frame(t_canvas0,bg="#000000")
        t_frame2.pack(fill='both',expand='true')
        t_frame3=tk.Frame(t_frame0,bg="#000000")
        t_frame3.pack(fill='both',expand='true')
        t_canvas0.create_window(110,0,anchor=NW,window=t_frame2)
        with open("data/stt_data.json","r") as cd_data_file:
            cd_data=json.load(cd_data_file)
            cd_data_file.close()
        tk.Label(t_frame2,text="Sr.",font=('Helvetica', 18),bg="#000000",fg="#ffffff").grid(row=0,column=0,padx=5)
        tk.Label(t_frame2,text="Name",font=('Helvetica',18),bg="#000000",fg="#ffffff").grid(row=0,column=1,padx=20,sticky=W)
        tk.Label(t_frame2,text="Email",font=('Helvetica', 18),bg="#000000",fg="#ffffff").grid(row=0,column=2,padx=5)
        cd_var_dict={}
        for cd_var0 in range(len(cd_data)):
            cd_var_dict[(cd_var0,)]=StringVar()
        for cdval in range(len(cd_data)):    
            tk.Label(t_frame2,text=f"{cdval+1}.",font=('Helvetica', 12),bg="#000000",fg="#ffffff").grid(row=cdval+1,column=0,pady=5)
            tk.Label(t_frame2,text=cd_data[cdval][:cd_data[cdval].find("(")-1],font=('Helvetica', 12),bg="#000000",fg="#ffffff").grid(row=cdval+1,column=1,sticky=W,padx=20)
            ttk.Entry(t_frame2,textvariable=cd_var_dict[(cdval,)],width=30,font=('Helvetica', 12)).grid(row=cdval+1,column=2,sticky=W,padx=20)
            t_canvas0.config(scrollregion=(0,0,1000,len(cd_data)*40),yscrollcommand=t_scroll0.set)

        def all_children(window) :
            _list = window.winfo_children()
            for item in _list :
                if item.winfo_children() :
                    _list.extend(item.winfo_children())
            
            return _list






        if os.path.isfile("data/cd_data.json"):
            with open("data/stt_data.json","r") as gdata1:
                gdict1=json.load(gdata1)
            with open("data/cd_data.json","r") as gdata:
                gdict=json.load(gdata)
                glist=list(gdict.values())
                glist1=list(gdict.keys())
            gmaill=[]
            for c in gdict1:
                try:
                    gmaill.append(gdict[c])
                except:
                    gmaill.append("")
            a=all_children(t_frame2)
            var1=0
            for b in a:
                if type(b)==tk.ttk.Entry:
                    b.insert(0,gmaill[var1])
                    var1+=1

        def is_email(email):
            import re
            regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
            if(re.search(regex,email)):
                return True
            else:  
                return False
        
        def get_cd_value():
            res=messagebox.askquestion('Save Details', 'By continue allb data will be overwrite!\nDo you want to continue?')
            if res == 'yes' :
                cd_value_dict={}
                for cd_value in range(len(cd_data)):
                    if len(cd_var_dict[(cd_value,)].get())!=0:
                        if is_email(cd_var_dict[(cd_value,)].get()):
                                cd_value_dict[cd_data[cd_value]]=cd_var_dict[(cd_value,)].get()
                        else:
                            showwarning(title="Error",message=f"Please enter a valid gmail  address \n for {cd_data[cd_value]}")
                            break
                    else:
                        showwarning(title="Error",message=f"Field cannot be empty")
                        break
                    
                if len(cd_value_dict)==len(cd_data):
                    with open("data/cd_data.json","w") as final_cd_file:
                        json.dump(cd_value_dict,final_cd_file)
                        final_cd_file.close()
                        showinfo(title="Success",message=f"Contact details submitted successfully")
                
        img11=Image.open("assets/vector/submit.png")
        img11=img11.resize((80, 30), Image.ANTIALIAS)
        img11=ImageTk.PhotoImage(img11)
        subbtn=tk.Button(t_frame3,image=img11,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000", font=('Helvectiva', 10),command=lambda:get_cd_value())
        subbtn.image=img11
        subbtn.pack(pady=20)
        

class About(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("About - FitPeriod")
        self.about_text()

    def about_text(self):
        l0=tk.Frame(self,bg="#000000")
        l0.pack(expand=TRUE,fill=BOTH)
        lg2=Image.open("assets/vector/logo.png")
        lg2=lg2.resize((250, 120), Image.ANTIALIAS)
        lg2=ImageTk.PhotoImage(lg2)
        l1=tk.Label(l0,image=lg2,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000")
        l1.image=lg2
        l1.pack(ipady=20)
        l2=tk.Label(l0,text="FitPeriod",bd=0,bg="#000000",fg="#ffffff",font=("Helvetica",25))
        l2.pack(ipadx=60)
        l3=tk.Label(l0,text="Developed by Jawahar Navodaya Vidyalaya Haridwar",bd=0,bg="#000000",fg="#ffffff",font=("Helvetica",15))
        l3.pack(ipadx=60,pady=(50,0))
        l4=tk.Label(l0,text="Developer: Aman Choudhary",bd=0,bg="#000000",fg="#ffffff",font=("Helvetica",15))
        l4.pack(ipadx=60,pady=(0,0))
        tk.Label(l0,text="@fitpriod/@fitperiod.setarrangements",bd=0,bg="#000000",fg="#ffffff",font=("Helvetica",10)).pack(pady=(20,0))
        l5=tk.Frame(l0,bg="#000000")
        l5.pack(expand=TRUE,fill=BOTH,pady=(0,0))

        sl1=Image.open("assets/vector/instagram.png")
        sl1=sl1.resize((60, 60), Image.ANTIALIAS)
        sl1=ImageTk.PhotoImage(sl1)
        s1=tk.Label(l5,image=sl1,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000")
        s1.image=sl1
        s1.pack(pady=(10,5),side=LEFT,padx=(157,5))
        sl2=Image.open("assets/vector/facebook.png")
        sl2=sl2.resize((60, 60), Image.ANTIALIAS)
        sl2=ImageTk.PhotoImage(sl2)
        s2=tk.Label(l5,image=sl2,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000")
        s2.image=sl2
        s2.pack(pady=(10,5),side=LEFT,padx=5)
        sl3=Image.open("assets/vector/twitter.png")
        sl3=sl3.resize((60, 60), Image.ANTIALIAS)
        sl3=ImageTk.PhotoImage(sl3)
        s3=tk.Label(l5,image=sl3,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000")
        s3.image=sl3
        s3.pack(pady=(10,5),side=LEFT,padx=5)
        sl4=Image.open("assets/vector/linkedin.png")
        sl4=sl4.resize((60, 60), Image.ANTIALIAS)
        sl4=ImageTk.PhotoImage(sl4)
        s4=tk.Label(l5,image=sl4,activebackground="#000000",bd=0,relief=tk.FLAT,bg="#000000",fg="#000000")
        s4.image=sl4
        s4.pack(pady=(10,5),side=LEFT,padx=5)

        tk.Label(l0,text="Copyroght (c) 2020 FitPeriod - All Rights Reserved",bd=0,bg="#000000",fg="#ffffff",font=("Helvetica",10)).pack(pady=(165,0))
        tk.Label(l0,text="Version 1.0.0",bd=0,bg="#000000",fg="#ffffff",font=("Helvetica",10)).pack()


        
if __name__ == "__main__":
    window = FitPeriod()
    window.menubar()
    window.mainloop()