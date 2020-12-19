from tkinter import *
import tkinter.messagebox
import tkinter.ttk
import database_control

title_hotel = 'xxx酒店'
title_admin = '管理员操作界面'
title_staff = '员工操作界面'


#消息提示窗
def popup(message):
    if message == 'ok':
        tkinter.messagebox.showinfo('提示' ,'操作成功！')
    elif message == 'error_exist':
        tkinter.messagebox.showwarning('警告','用户信息已经存在，请不要重复录入！')
    elif message == 'error_input':
        tkinter.messagebox.showerror('错误','输入数据有误！')
    elif message == 'error_login':
        tkinter.messagebox.showerror('错误', '账号或者密码有误！')
    elif message == 'error_not_null':
        tkinter.messagebox.showerror('错误', '抱歉！此类空闲房间暂无')
    elif message == 'error_not_oder':
        tkinter.messagebox.showerror('错误', '该客户未预约')
    elif message == 'error_no_person':
        tkinter.messagebox.showerror('错误', '查无此人！')
    else:
        tkinter.messagebox.showinfo('提示', message)


#统一界面风格
def int_windows(title ,header_title):
    int_windows = Tk()  # 初始化一个窗口实例
    int_windows.title(title)    # 标题命名
    int_windows.geometry('640x480+450+180')   # 窗口大小设置

    lb_header = Label(int_windows, text=header_title)      #页面标题
    lb_header.place(relx=0.4, rely=0, relwidth=0.2, relheight=0.1)

    lb_operator_no = Label(int_windows, text='编号：' + database_control.opration['id'])
    lb_operator_no.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    lb_operator = Label(int_windows ,text='员工：' + database_control.opration['name'])
    lb_operator.place(relx=0.15, rely=0.95, relwidth=0.1, relheight=0.05)

    return int_windows


#清空输入框数据
def input_clear(textvar_entry1 ,textvar_entry2):
    textvar_entry1.set('')
    textvar_entry2.set('')


#处理以后呈现元组中的元素在控件text中
def display(message_tuples ,control_text):
    #display（查询结果的元组，控件text）
    control_text.delete(1.0, END)  # 将先前信息清清除
    print(message_tuples)
    for message_tuple in message_tuples:
        for ele in message_tuple:
            control_text.insert('insert', ele)
            control_text.insert('insert' ,'\t\t ')
        control_text.insert('insert', '\n')


#直接呈现传入的消息在控件text中
def dir_display(message,control_text,if_clear=0):
    if if_clear == 0:
        control_text.delete(1.0, END)  # 将先前信息清清除
    control_text.insert('insert', message)


#初始化的登陆界面
def int_login_windows():
    login_interface = int_windows(title_hotel ,'欢迎回来')      #统一的界面风格

    textvar_id = StringVar()                        #用户名标签和输入框
    lb_id = Label(login_interface,text='用户名：',
                       bg='#f8f8ff',
                       fg='black',
                       relief=SUNKEN)
    lb_id.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.1)
    input_id = Entry(login_interface ,textvariable=textvar_id)
    input_id.place(relx=0.4, rely=0.2, relwidth=0.4, relheight=0.1)

    textvar_pass = StringVar()                       #密码标签和输入框
    lb_pass = Label(login_interface, text='密码：',
                        bg='#f8f8ff',
                        fg='black',
                        relief=SUNKEN)
    lb_pass.place(relx=0.2, rely=0.3, relwidth=0.2, relheight=0.1)
    input_pass = Entry(login_interface ,textvariable=textvar_pass ,show ='*')
    input_pass.place(relx=0.4, rely=0.3, relwidth=0.4, relheight=0.1)

    var = IntVar()                                         #单项选择器
    rd_staff = Radiobutton(login_interface, text="普通员工" ,variable=var ,value=0)
    rd_staff.place(relx=0.2, rely=0.5, relwidth=0.2, relheight=0.05)
    rd_admin = Radiobutton(login_interface, text="管理员" ,variable=var ,value=1)
    rd_admin.place(relx=0.4, rely=0.5, relwidth=0.4, relheight=0.05)

    btn_login = Button(login_interface, text='登录',             #登录按钮
                 command= lambda :database_control.login(
                     input_id.get() ,input_pass.get() ,var.get() ,textvar_id ,textvar_pass ,login_interface))
    btn_login.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

    login_interface.mainloop()  # 置于开启的状态直到用户关闭


#按键返回登陆界面
def exit(Tkinter):
    database_control.opration['id'] = ''
    database_control.opration['name'] = ''
    Tkinter.destroy()
    int_login_windows()


#普通员工————一、登记入住；二、客户查找；三、酒水订购；四、退房
def staff_int_windows(Tkinter):
    Tkinter.destroy()
    int_staff_interface = int_windows(title_staff ,'员工操作菜单')           #统一的界面风格

    btn_register = Button(int_staff_interface,text='登记入住',
                          command=lambda :staff_register_windows(int_staff_interface))   #实现新客户的登记
    btn_register.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.2)

    btn_register = Button(int_staff_interface,text='客户查找',
                          command=lambda :cheak_customer_info(int_staff_interface))                       #实现查找客户的信息
    btn_register.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.2)

    btn_out = Button(int_staff_interface, text='酒水服务',
                     command=lambda :commodity_server_windows())
    btn_out.place(relx=0.05, rely=0.5, relwidth=0.4, relheight=0.2)

    btn_out = Button(int_staff_interface,text='退房',
                     command=lambda :customer_check_out(int_staff_interface))                               #实现入住用户的退房管理
    btn_out.place(relx=0.55, rely=0.5, relwidth=0.4, relheight=0.2)

    btn_logout = Button(int_staff_interface,text='注销', command=lambda: exit(int_staff_interface))  #返回到登陆界面
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


#普通员工————一1、预约登记；2、到店登记
def staff_register_windows(Tkinter):
    Tkinter.destroy()
    register_staff_windows = int_windows(title_staff ,'客户信息登记')

    btn_register = Button(register_staff_windows ,text='预约登记' ,          #实现新客户的预约登记
                          command=lambda :order_register_windows(register_staff_windows))
    btn_register.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.2)

    btn_register = Button(register_staff_windows ,text='到店登记' ,                 #实现客户的到店登记
                          command=lambda :arrive_register_windows(register_staff_windows))
    btn_register.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.2)

    btn_logout = Button(register_staff_windows ,text='返回上一级' ,        #返回到登陆界面
                        command=lambda :staff_int_windows(register_staff_windows))
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


#普通员工————一1、预约登记
def order_register_windows(Tkinter):
    Tkinter.destroy()
    order_windows = int_windows(title_staff ,'预约客户信息录入')

    lb_name = Label(order_windows, text='名字：')             #输入客户名字标签、按钮
    lb_name.place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.05)
    input_name = Entry(order_windows)
    input_name.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.05)

    lb_room = Label(order_windows, text='房间类型：')  # 输入房间类型
    lb_room.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.05)
    comb_room = tkinter.ttk.Combobox(order_windows,values=database_control.room_type)
    comb_room.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.05)

    lb_number = Label(order_windows, text='电话号码：')          #输入客户电话号码标签、按钮
    lb_number.place(relx=0.1, rely=0.4, relwidth=0.1, relheight=0.05)
    input_number = Entry(order_windows)
    input_number.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.05)

    lb_time = Label(order_windows, text='预计到店时间：')           #输入客户估计到达时间标签、按钮
    lb_time.place(relx=0.1, rely=0.6, relwidth=0.2, relheight=0.05)
    input_year = Entry(order_windows)
    input_year.place(relx=0.3, rely=0.6, relwidth=0.1, relheight=0.05)
    lb_1 = Label(order_windows, text='年-')
    lb_1.place(relx=0.4, rely=0.6, relwidth=0.1, relheight=0.05)
    input_month = Entry(order_windows)
    input_month.place(relx=0.5, rely=0.6, relwidth=0.1, relheight=0.05)
    lb_2 = Label(order_windows, text='月-')
    lb_2.place(relx=0.6, rely=0.6, relwidth=0.1, relheight=0.05)
    input_day = Entry(order_windows)
    input_day.place(relx=0.7, rely=0.6, relwidth=0.1, relheight=0.05)

    btn_submit = Button(order_windows, text='提交',                  #提交数据
                        command=lambda :database_control.order_register(
                            input_name.get() ,comb_room.get(),input_number.get() ,input_year.get() ,input_month.get() ,input_day.get()))
    btn_submit.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

    btn_logout = Button(order_windows, text='返回上一级',            #返回上一级
                        command=lambda :staff_register_windows(order_windows))
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


#普通员工————一2、到店登记
def arrive_register_windows(Tkinter):
    Tkinter.destroy()
    register_windows = int_windows(title_staff, '客户信息录入')

    lb_name = Label(register_windows, text='名字：')  # 输入客户名字标签、按钮
    lb_name.place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.05)
    input_name = Entry(register_windows)
    input_name.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.05)

    lb_room = Label(register_windows, text='房间类型：')  # 输入房间类型
    lb_room.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.05)
    comb_room = tkinter.ttk.Combobox(register_windows, values=['单人', '双人', '大床', '总统套房', ])
    comb_room.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.05)

    lb_number = Label(register_windows, text='电话号码：')  # 输入客户电话号码标签、按钮
    lb_number.place(relx=0.1, rely=0.4, relwidth=0.1, relheight=0.05)
    input_number = Entry(register_windows)
    input_number.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.05)

    lb_sex = Label(register_windows, text='性别：')  # 输入性别
    lb_sex.place(relx=0.5, rely=0.4, relwidth=0.1, relheight=0.05)
    comb_sex = tkinter.ttk.Combobox(register_windows, values=['男' ,'女',])
    comb_sex.place(relx=0.6, rely=0.4, relwidth=0.2, relheight=0.05)

    lb_ID = Label(register_windows, text='身份证号：')  # 输入客户身份证号标签、按钮
    lb_ID.place(relx=0.2, rely=0.6, relwidth=0.1, relheight=0.05)
    input_ID = Entry(register_windows)
    input_ID.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.05)

    btn_submit = Button(register_windows, text='提交',
                        command=lambda: database_control.direct_register(
                            input_name.get(), comb_room.get(), input_number.get(), comb_sex.get(), input_number.get()))
    btn_submit.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

    btn_logout = Button(register_windows, text='返回上一级',  # 返回到登陆界面
                        command=lambda: staff_int_windows(register_windows))
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


#普通员工————二、客户查找
def cheak_customer_info(Tkinter):
    Tkinter.destroy()
    cheak_windows = int_windows(title_staff, '')

    lb_name = Label(cheak_windows, text='名字：')  # 输入客户名字标签、按钮
    lb_name.place(relx=0, rely=0.05, relwidth=0.1, relheight=0.05)
    textvar_name = StringVar()
    input_name = Entry(cheak_windows ,textvariable=textvar_name)
    input_name.place(relx=0.1, rely=0.05, relwidth=0.25, relheight=0.05)

    lb_number = Label(cheak_windows, text='电话号码：')  # 输入客户电话号码标签、按钮
    lb_number.place(relx=0.4, rely=0.05, relwidth=0.1, relheight=0.05)
    textvar_number = StringVar()
    input_number = Entry(cheak_windows ,textvariable=textvar_number)
    input_number.place(relx=0.5, rely=0.05, relwidth=0.35, relheight=0.05)

    btn_submit = Button(cheak_windows, text='查询',relief='solid',
                        command=lambda :database_control.cheak_customer_info(
                            name=input_name.get(),number=input_number.get() ,
                            msg_text=text_customer_message ,entry1=textvar_name ,entry2=textvar_number))
    btn_submit.place(relx=0.9, rely=0.05, relwidth=0.1, relheight=0.05)

    #显示标签
    lb_customer_message = Label(cheak_windows,
                             text='姓名                   '
                                  '性别                '
                                  '房间号                '
                                  '电话号码                                                                       ')
    lb_customer_message.place(relx=0, rely=0.15, relwidth=1, relheight=0.05)

    text_customer_message = Text(cheak_windows)
    text_customer_message.place(relx=0, rely=0.2, relwidth=1, relheight=0.75)

    btn_logout = Button(cheak_windows, text='返回上一级',  # 返回到登陆界面
                        command=lambda: staff_int_windows(cheak_windows))
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


#普通员工，为指定房间增加酒水的用品信息
def commodity_server_windows():
    commodity_windows = Tk()
    commodity_windows.geometry('480x360+550+250')
    commodity_windows.title('酒水服务')

    textvar_room = StringVar()
    lb_room = Label(commodity_windows, text='房间号：')       #输入房号
    lb_room.place(relx=0.05, rely=0, relwidth=0.1, relheight=0.05)
    input_room = Entry(commodity_windows ,textvariable=textvar_room)
    input_room.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.05)

    lb_commodity = Label(commodity_windows, text='商品名：')  # 选择商品名称
    lb_commodity.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.05)
    comb_commodity = tkinter.ttk.Combobox(commodity_windows, values=database_control.commodity)
    comb_commodity.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.05)

    lb_x = Label(commodity_windows, text='X')  # 选择商品名称
    lb_x.place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.05)

    textvar_number = StringVar()
    lb_number = Label(commodity_windows, text='数量：')          #输入数量
    lb_number.place(relx=0.4, rely=0.15, relwidth=0.1, relheight=0.05)
    input_number = Entry(commodity_windows ,textvariable=textvar_number)
    input_number.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.05)

    btn_add = Button(commodity_windows, text='添加',
                     command=lambda :database_control.add_commodity(input_room.get() ,textvar_room ,comb_commodity.get()
                                                                    ,input_number.get() ,textvar_number ,
                                                                    text_customer_message))
    btn_add.place(relx=0.75, rely=0.05, relwidth=0.2, relheight=0.2)

    text_customer_message = Text(commodity_windows)        #文本框显示
    text_customer_message.place(relx=0, rely=0.3, relwidth=1, relheight=0.5)

    btn_add = Button(commodity_windows, text='提交',
                     command=lambda :database_control.save_add_commodity(text_customer_message))
    btn_add.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

    btn_logout = Button(commodity_windows, text='取消',
                        command=commodity_windows.destroy)
    btn_logout.place(relx=0.8, rely=0.9, relwidth=0.2, relheight=0.1)


#普通员工————四、退房操作
def customer_check_out(Tkinter):
    Tkinter.destroy()
    check_out_windows = int_windows(title_staff, '')

    lb_room = Label(check_out_windows, text='房间号：')  # 输入客户房间号标签、按钮
    lb_room.place(relx=0.3, rely=0.05, relwidth=0.1, relheight=0.05)
    textvar_room = StringVar()
    input_number = Entry(check_out_windows ,textvariable=textvar_room)
    input_number.place(relx=0.4, rely=0.05, relwidth=0.2, relheight=0.05)

    btn_cheak = Button(check_out_windows, text='查询',relief='solid',
                        command=lambda :database_control.cheak_customer_consume(
                            textvar_room ,text_customer_message ,input_number.get()))
    btn_cheak.place(relx=0.8, rely=0.05, relwidth=0.2, relheight=0.05)

    # 显示标签
    lb_list = Label(check_out_windows,text='消费物品\t\t\t\t数量\t\t\t单价\t\t\t总价')
    lb_list.place(relx=0, rely=0.15, relwidth=1, relheight=0.05)

    text_customer_message = Text(check_out_windows)
    text_customer_message.place(relx=0, rely=0.2, relwidth=1, relheight=0.65)

    btn_submit = Button(check_out_windows, text='支付',
                        command=lambda :database_control.customer_payment(
                            textvar_room, text_customer_message, input_number.get()))
    btn_submit.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    btn_logout = Button(check_out_windows, text='返回上一级',  # 返回到登陆界面
                        command=lambda: staff_int_windows(check_out_windows))
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


#管理员————操作主界面(未完成）
def admin_int_windows(Tkinter):
    Tkinter.destroy()
    int_admin_interface = int_windows(title_admin ,'管理员操作主菜单')          #统一的界面风格








    btn_logout = Button(text ='注销' ,command = lambda :exit(int_admin_interface))   #返回到登陆界面
    btn_logout.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)


