from tkinter import *
from pymysql import *
import windows_control
import datetime

#连接数据库
db = connect(
    host = 'localhost' ,port = 3306 ,user = 'root' ,password = '123456' ,database = 'test'
)

#实例化数据库对象
cur = db.cursor()

#字典
#此刻正在操作的员工
opration = {
    'id':'',
    'name':'',
}


#列表
commodity = ['果汁','毛巾','烟']
room_type = ['单人','双人','大床','总统套房']
temp_commodity_list = []


#记录此时进行操作的员工到字典poration中
def working(staff_id ,title):
    if title == '员工':
        cur.execute('select sno,sname from tab_staff where sno={};'.format(staff_id))
    else:
        cur.execute('select sno,sname from tab_staff where sno=(select sno from tab_admin where id={});'.format(staff_id))
    (sno, sname) = cur.fetchone()
    opration['id'] = sno
    opration['name'] = sname


#操作人员账号登陆
def login(id ,password ,value ,textvar_id ,textvar_pass ,Tkinter):
    try:
        if value == 0:
            cur.execute('select sno from tab_staff where sno={} and spassword={};'.format(id ,password))
            title = '员工'
        else:
            cur.execute('select sno from tab_admin where id={} and password={};'.format(id,password))
            title = '管理员'
        sno = cur.fetchone()[0]
        if sno and title == '员工':
            working(id ,title)
            windows_control.staff_int_windows(Tkinter)
        elif sno and title == '管理员':
            working(id, title)
            windows_control.admin_int_windows(Tkinter)
    except:
        windows_control.popup('error_login')
        windows_control.input_clear(textvar_id ,textvar_pass)


#录入预约的客户
def order_register(name ,type ,number ,year ,month ,day):
    arrive_time = year + '-' + month + '-' + day
    try:
        cur.execute('select order_name,order_number from tab_order where order_name="{}" and order_number="{}";'.format(name ,number))
        if cur.fetchone():
            windows_control.popup('error_exist')
        else:
            cur.execute('select room from tab_room where rtype ="{}" and rstate = 0;'.format(type))
            try:
                room = cur.fetchone()[0]
                cur.execute('insert into tab_order(order_name,order_number,order_room,order_arrive_time) values("{}","{}","{}","{}");'
                    .format(name, number, room, arrive_time))
                cur.execute('update tab_room set rstate="1" where room="{}";'.format(room))
                cur.connection.commit()  # 一定要写这一句！！！！！不然不会保存的！！！
                windows_control.popup('ok')
            except:
                windows_control.popup('error_not_null')

    except:
        windows_control.popup('error_input')


#录入到店登记入住的客户
def direct_register(name ,room_type ,number ,sex ,ID):
    #已预约客户的登记
    try:
        cur.execute('select order_room from tab_order where order_name="{}" and order_number="{}";'.format(name ,number))
        room_number = cur.fetchone()[0]

        #如果第二次选择类型和预约时的不同
        cur.execute('select rtype from tab_room where room="{}";'.format(room_number))
        r_type = cur.fetchone()[0]
        if room_type == r_type:
            #删除预约表的信息
            cur.execute('delete from tab_order where order_name="{}" and order_number="{}";'.format(name ,number))
            cur.connection.commit()  # 一定要写这一句！！！！！不然不会保存的！！！
            register(name ,number ,sex ,ID ,room_number=room_number)
        else:
            windows_control.popup('与第一次选择的房间类型不同！')

    #未预约客户的登记
    except:
        register(name ,number ,sex ,ID ,room_type=room_type)


#录入信息保存到住户表中，然后消息弹窗返回房间号
def register(name ,number ,sex ,ID ,room_type='default' ,room_number='default'):
    InTime = str(datetime.datetime.now().year) + '-' \
              + str(datetime.datetime.now().month) + '-' \
              + str(datetime.datetime.now().day)

    if name != '' and number != '' and sex != '' and ID != '':
        #有空闲房间时
        try:
            #对于到店客户
            if room_number == 'default':
                cur.execute('select room from tab_room where rtype ="{}" and rstate = 0;'.format(room_type))
                room_number = cur.fetchone()[0]

            #对于提前预约客户
            else:
                #将预约房间暂时归零
                cur.execute('update tab_room set rstate="0" where room="{}";'.format(room_number))
                cur.connection.commit()  # 一定要写这一句！！！！！不然不会保存的！！！

            #将信息添加到入住表中
            cur.execute('insert into tab_customers (cname ,csex ,cID ,cnumber ,cInTime ,cInStaff ,room)'
            'values("{}" ,"{}" ,"{}" ,"{}" ,"{}" ,"{}" ,"{}")'
            .format(name ,sex ,ID ,number ,InTime ,opration['id'] ,room_number))
            #房间状态归零
            cur.execute('update tab_room set rstate="1" where room="{}";'.format(room_number))
            #初始化房间对应的额外消费表
            cur.execute('insert into tab_extra_consume(room ,juice ,towel ,smoke)'
                        'values("{}" ,{} ,{} ,{})'
                        .format(room_number, 0, 0, 0))
            cur.connection.commit()  # 一定要写这一句！！！！！不然不会保存的！！！
            message = '登记成功！您的房间号为' + room_number
            windows_control.popup(message)

        # 无空余房间
        except:
            windows_control.popup('error_not_null')
    else:
        windows_control.popup('error_input')


#员工————按照名字或者电话查询客户信息
def cheak_customer_info(msg_text ,entry1 ,entry2,name='',number=''):
    try:
        if name == '':
            # 无输入--显示所有信息
            if number == '':
                cur.execute('select * from view_simple_customer_info order by room; ')
            #电话查找
            else:
                cur.execute('select * from view_simple_customer_info where cnumber like "%{}%" order by room; '.format(number))
        else:
            #名字、电话查找
            if number == 'default':
                cur.execute('select * from view_simple_customer_info where cnumber like "%{}%" and cname like "%{}%" order by room; '
                            .format(number ,name))
            #名字查找
            else:
                cur.execute('select * from view_simple_customer_info where cname like "%{}%" order by room; '.format(name))

        customers_tuple = cur.fetchall()
        if customers_tuple[0]:                      #确认存在信息以后执行
            windows_control.display(customers_tuple, msg_text)
            windows_control.input_clear(entry1, entry2)
    except:
        msg_text.delete(1.0, END)  # 将先前信息清清除
        windows_control.input_clear(entry1,entry2)
        windows_control.popup('error_no_person')


#员工————按照房间号查询客户消费清单
def cheak_customer_consume(textvar_entry ,control_text ,room_number=''):
    consume_sum = 0
    if room_number == '':
        windows_control.popup('error_input')
    else:
        try:
            #获取该房间的房价
            cur.execute('select rprice from tab_room where room = "{}"; '.format(room_number))
            consume_sum = cur.fetchone()[0]

            #该房间消费的物品数量
            cur.execute('select * from tab_extra_consume where room = "{}"; '.format(room_number))
            consume_tuple = cur.fetchone()

            #获取每个物品对应的价格的元组群
            cur.execute('select coname,coprice from tab_commodity order by cono; ')
            commodity_price_tuples = cur.fetchall()

            message = ''
            count = 0
            for commodity_price_tuple in commodity_price_tuples:
                count += 1
                goods_number = consume_tuple[count]
                goods_price = commodity_price_tuple[1]
                per_goods_sum = goods_price * goods_number
                message += commodity_price_tuple[0] + '\t\t\t\tX' + \
                           str(goods_number) + '\t\t\t' + str(goods_price) + '\t\t\t' + str(per_goods_sum) + \
                           '\n'
                consume_sum += per_goods_sum

            message += '\n\n\n\n\n\n\n\t\t\t\t\t\t\t\t\t合计：' + str(consume_sum)
            windows_control.dir_display(message,control_text)
        except:
            control_text.delete(1.0, END)  # 将先前信息清清除
            textvar_entry.set('')
            windows_control.popup('error_input')
        return consume_sum


#员工————确定支付此次入住的费用
def customer_payment(textvar_entry ,control_text ,room_number=''):
    #获取总消费额
    consume_sum = cheak_customer_consume(textvar_entry ,control_text ,room_number)
    #如果房间未住人(跳过）
    if consume_sum == 0 or consume_sum == None:
        pass
    else:
        #获取客户身份证
        cur.execute('select cID from tab_customers where room="{}"'.format(room_number))
        customer_ID = cur.fetchone()[0]

        #获取退房时间
        OutTime = str(datetime.datetime.now().year) + '-' \
                 + str(datetime.datetime.now().month) + '-' \
                 + str(datetime.datetime.now().day)

        #收入表的更新
        cur.execute('insert into tab_income(past_ID,past_Out_Time,past_consume) values("{}","{}","{}");'
                        .format(customer_ID, OutTime, consume_sum))
        #住户表更新(多项信息修改）
        cur.execute('update tab_customers set room=null ,cOutTime="{}" ,cOutStaff="{}" where room="{}";'
                    .format(OutTime,opration['id'],room_number))

        #消费表清空
        cur.execute('delete from tab_extra_consume where room="{}";'.format(room_number))

        #房间表归零
        cur.execute('update tab_room set rstate="0" where room="{}";'.format(room_number))

        #信息保存
        cur.connection.commit()  # 一定要写这一句！！！！！不然不会保存的！！！

        windows_control.popup('ok')

        # 将界面信息清清除
        control_text.delete(1.0, END)
        textvar_entry.set('')


#员工————完成添加商品操作并显示在文本框中
def add_commodity(room ,textvar_room ,name ,number ,textvar_number ,control_text):
    #检查房间号是否存在
    try:
        cur.execute('select * from tab_extra_consume where room="{}";'.format(room))
        response = cur.fetchone()
        print(response)
        #缓存列表添加元素
        temp_commodity_list.append([room ,name ,number])
        #添加框内容清空
        windows_control.input_clear(textvar_room ,textvar_number)
        #将添加的商品逐一显示在文本框中
        message = str(room) + '\t\t' + name + '\t\tX' + str(number) + '\n'
        windows_control.dir_display(message ,control_text ,1)
    except:
        windows_control.input_clear(textvar_room, textvar_number)
        windows_control.popup('error_input')
    print(temp_commodity_list)



#员工————完成将添加的商品提交并且记录到数据库中
def save_add_commodity(control_text):
    #将商品一一记录到额外消费表中
    for sub_temp_commodity_list in temp_commodity_list:
        print(sub_temp_commodity_list)
        if sub_temp_commodity_list[1] == '果汁':
            #获取原先的数值
            cur.execute('select juice from tab_extra_consume where room = "{}"; '.format(sub_temp_commodity_list[0]))
            past_number = cur.fetchone()[0]
            print(past_number)
            cur.execute('update tab_extra_consume set juice="{}" where room={};'
                        .format(past_number + int(sub_temp_commodity_list[2]) ,sub_temp_commodity_list[0]))
        elif sub_temp_commodity_list[1] == '烟':
            cur.execute('select smoke from tab_extra_consume where room = "{}"; '.format(sub_temp_commodity_list[0]))
            past_number = cur.fetchone()[0]
            cur.execute('update tab_extra_consume set smoke="{}" where room={};'
                        .format(past_number + int(sub_temp_commodity_list[2]) , sub_temp_commodity_list[0]))
        elif sub_temp_commodity_list[1] == '毛巾':
            cur.execute('select towel from tab_extra_consume where room = "{}"; '.format(sub_temp_commodity_list[0]))
            past_number = cur.fetchone()[0]
            cur.execute('update tab_extra_consume set towel="{}" where room={};'
                        .format(past_number + int(sub_temp_commodity_list[2]) , sub_temp_commodity_list[0]))
        #信息保存
        cur.connection.commit()  # 一定要写这一句！！！！！不然不会保存的！！！

    #缓存列表清空
    temp_commodity_list.clear()

    #清空text框
    message = ''
    windows_control.dir_display(message, control_text)

    #弹窗
    windows_control.popup('ok')
