import configparser
import re
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()

options.add_experimental_option("prefs",
                                {'credentials_enable_service': False, 'profile.password_manager_enabled': False})
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/124.0.0.0 Safari/537.36')
options.add_experimental_option("detach", True)

s = Service(r'..\.venv\Scripts\chromedriver.exe')  # 填写浏览器驱动程序路径
driver = webdriver.Chrome(options=options, service=s)

driver.get('https://kyfw.12306.cn/otn/resources/login.html')
driver.maximize_window()

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

person = config.get('train_info', 'person')
fromstation = config.get('train_info', 'fromstation')
destination = config.get('train_info', 'destination')
train_date = config.get('train_info', 'train_date')
# 检测日期格式是否正确
date_str = train_date
pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
if not bool(re.match(pattern, date_str)):
    print(f"填写的车票日期：{train_date} 不是有效的日期格式")
    input("请重新输入正确的日期格式，然后按任意键继续...")
    exit()

train_number = config.get('train_info', 'train_number')
zw = config.get('train_info', 'zw')  # 定义座位类型： 1为硬座 3为硬卧 4 为软卧

student_ = config.get('train_info', 'student_')  # 是否学生票： 0为否，1为是
wuzuo = config.get('train_info', 'wuzuo')  # 是否接受无座：0为接受，1为不接受

# 扫码登录
locate = (By.XPATH, '//*[@id="toolbar_Div"]/div[2]/div[2]/ul/li[2]/a')
saoma = WebDriverWait(driver, 120, 0.5).until(EC.presence_of_element_located(locate))
saoma.click()

# 账号密码登录
# locate = (By.XPATH, '//*[@id="toolbar_Div"]/div[2]/div[2]/ul/li[1]/a')
# login_btn = WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locate))
# login_btn.click()
#
# locate = (By.ID, 'J-userName')
# login_user = WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locate))
# login_user.send_keys('')
#
# driver.find_element(By.ID,'J-password').send_keys('')
#
# driver.find_element(By.ID,'J-login').click()
#
# locate = (By.ID, 'id_card')
# login_pass = WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located(locate))
# login_pass.send_keys('')
#
# driver.find_element(By.ID,'verification_code').click()
#
# driver.find_element(By.ID,'code').send_keys(input('请输入手机验证码：'))
#
# driver.find_element(By.ID,'sureClick').click() #登录

# 等待时间
# start_time = time.time()
# count_time = 1
# while True:
#     if time.time() - start_time >= 60:
#         start_time = time.time()
#         driver.refresh()
#         print(f'刷新网页(第{count_time}次)')
#         count_time += 1
#     now = datetime.now()
#     print("当前时间：", now.strftime("%Y-%m-%d %H:%M:%S"))
#     if now.minute >= 59:
#         break
#     print("将在售票前1分钟开始操作...")
#     time.sleep(10)

# 点击订票
locate = (By.ID, 'link_for_ticket')
WebDriverWait(driver, 600, 0.5).until(EC.visibility_of_element_located(locate)).click()

locate = (By.ID, 'fromStationText')
from_input = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(locate))
from_input.click()
from_input.clear()
from_input.send_keys(fromstation)
time.sleep(0.5)

locate2 = (By.ID, 'panel_cities')
from_input2 = WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located(locate2))

fromstation_select = from_input2.find_elements(By.XPATH, './div')

for idx in fromstation_select:
    i = idx.find_element(By.XPATH, './span[1]')
    if i.text == fromstation:
        i.click()
        break

locate = (By.ID, 'toStationText')
to_input = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(locate))
to_input.click()
to_input.clear()
to_input.send_keys(destination)
time.sleep(0.5)

locate2 = (By.ID, 'panel_cities')
from_input2 = WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located(locate2))

destination_select = from_input2.find_elements(By.XPATH, './div')
for idx in destination_select:
    i = idx.find_element(By.XPATH, './span[1]')
    if i.text == destination:
        i.click()
        break

locate = (By.ID, 'train_date')
bt_date = WebDriverWait(driver, 10, 0.2).until(EC.presence_of_element_located(locate))
bt_date.click()
bt_date.clear()
bt_date.send_keys(train_date)
bt_date.send_keys(Keys.ENTER)

flag = False
cnt = 1
start_time = time.time()
cs_cnt = 1
print("等待1秒")
time.sleep(1)
while True:
    if time.time() - start_time >= 100:
        start_time = time.time()
        driver.refresh()
        print('刷新网页')
    # 点击查询车票信息
    # driver.find_element(By.ID, 'query_ticket').click()
    locate = (By.ID, 'query_ticket')
    query_btn = WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable(locate))
    while query_btn.get_attribute('class') != 'btn92s':
        time.sleep(0.1)
    # time.sleep(1)
    query_btn.click()

    try:
        # 获取当日车次信息
        locate = (By.ID, 'queryLeftTable')
        tbody = WebDriverWait(driver, 0.8, 0.2).until(EC.visibility_of_element_located(locate))
    except TimeoutException:
        print(f'超时重试...(第{cs_cnt}次)')
        cs_cnt += 1
        continue
    trs = tbody.find_elements(By.XPATH, './tr')
    for i in range(0, len(trs), 2):
        tr = trs[i].find_element(By.XPATH, './td/div/div/div/a')
        if tr.text == train_number:
            tr_main = trs[i].find_elements(By.XPATH, './td')
            sta = tr_main[-4].text
            sta_wuzuo = tr_main[-3].text  # 如果有无座的票，则直接购买
            # if (sta == '候补' or sta == '--' or sta == '无') and sta_wuzuo == '无':
            if sta == '候补' or sta == '--' or sta == '无':
                if (wuzuo == '1') or (wuzuo == '0' and sta_wuzuo == '无'):  # 判断是否选择了无座票
                    print(f'当前车次暂无余票，再次尝试中(第{cnt}次)')
                    cnt = cnt + 1
                    break
            if sta == '*':
                print(f'当前车次还未开售(第{cnt}次)')
                cnt = cnt + 1
                break
            flag = True
            tr_main[-1].click()
            break
    if flag:
        break

# 获取账号已保存的乘车人信息
locate = (By.ID, 'normal_passenger_id')

max_attempts = 2  # 尝试的最大次数
attempt = 0
while attempt < max_attempts:
    try:
        persons = WebDriverWait(driver, 5, 0.2).until(EC.visibility_of_element_located(locate))
        break  # 如果元素可见，则跳出循环
    except TimeoutException:
        driver.refresh()
        attempt += 1
# persons = WebDriverWait(driver, 10, 0.2).until(EC.visibility_of_element_located(locate))
persons = persons.find_elements(By.XPATH, './li')
# 选中乘车人
for i in persons:
    # if i.text == person:
    if i.text.startswith(person):
        i.find_element(By.XPATH, './input').click()
        # 是否购买学生票
        # 如果没有选择学生票，但是账号信息中是学生身份，则选择取消学生票类别
        if (student_ == '0') and i.text.endswith('(学生)'):
            locate = (By.ID, 'dialog_xsertcj_cancel')
            conf_xue = WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable(locate))
            conf_xue.click()
        # 如果有选择学生票，并且账号信息中是学生身份，则选择学生票类别
        if student_ == '1' and i.text.endswith('(学生)'):
            locate = (By.ID, 'dialog_xsertcj_ok')
            conf_xue = WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable(locate))
            conf_xue.click()
        # 如果有选择学生票，但是账号信息中不是学生身份，则选择成人票类别
        elif student_ == '1' and (not i.text.endswith('(学生)')):
            print('配置文件中选择了学生票，但乘车人身份信息不是学生！本次将按照成人票购票！')
        break

# 选择座位类型
select = Select(driver.find_element(By.ID, 'seatType_1'))
select.select_by_value(zw)

# 提交订单
sub = driver.find_element(By.ID, 'submitOrder_id')
actions = ActionChains(driver)
actions.move_to_element(sub)
actions.click()
actions.perform()

# 检查是否有空余座位
locate = (By.ID, 'check_ticketInfo_id')
zw_info = WebDriverWait(driver, 10, 0.2).until(EC.visibility_of_element_located(locate))
if zw_info == '无座':
    print('当前所选车次没有空余座位了，只有无座！！！')

# 确认提交订单
locate = (By.ID, 'qr_submit_id')
confirm = WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable(locate))
# 等待元素变成点击有效状态
while confirm.get_attribute('class') != 'btn92s':
    time.sleep(0.1)
confirm.click()

print('购买成功！！！请10分钟之内在待支付页面支付。')

# 无座票确认框：id：qd_closeDefaultWarningWindowDialog_id
try:
    locate = (By.ID, 'qd_closeDefaultWarningWindowDialog_id')
    confirm = WebDriverWait(driver, 60, 0.2).until(EC.element_to_be_clickable(locate))
    confirm.click()
    print('当前购买车票为无座票！！！')
except:
    print('当前非无座票车次！')

input('按任意键退出...')
