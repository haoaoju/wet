import requests
from bs4 import BeautifulSoup
from smtplib import SMTP_SSL                    # SSL加密的   传输协议
from email.mime.text import MIMEText            # 构建邮件文本
from email.mime.multipart import MIMEMultipart  # 构建邮件体
from email.header import Header                 # 发送内容
import schedule
import time


urls = "http://wsjkw.shandong.gov.cn/ztzl/rdzt/qlzhxxgzbdfyyqfkgz/tzgg/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 HBPC/12.0.0.303'}

def get_url():
    req = requests.get(urls,headers=headers)
    req.encoding='utf-8'
    html = BeautifulSoup(req.text, 'html.parser')
    url = html.find_all(class_ = "newsfld")
    title = url[0].find("a")["title"]
    url = urls + url[0].find("a")["href"]
    return url,title

def get_text():
    url,_ = get_url()
    req = requests.get(url,headers=headers)
    req.encoding = 'utf-8'
    html = BeautifulSoup(req.text, 'html.parser')
    text = html.find(class_="view TRS_UEDITOR trs_paper_default trs_web")
    #texts = text.text.split(";")
    texts = text.text
    return texts

def mail_message():
    _,title = get_url()
    text = get_text()
    host_server = 'smtp.qq.com'         # QQ邮箱smtp服务器
    pwd = 'tgyrukxvwgskjbfh'            # 授权码
    from_qq_mail = '1778856647@qq.com'          # 发件人
    #to_qq_mail = '757049583@qq.com'            # 收件人
    to_qq_mail = '1778856647@qq.com'
    msg = MIMEMultipart()               # 创建一封带附件的邮件

    msg['Subject'] = Header(title, 'UTF-8')    # 消息主题
    msg['From'] = from_qq_mail                       # 发件人
    msg['To'] = Header("YH", 'UTF-8')                # 收件人
    msg.attach(MIMEText(text, 'html', 'UTF-8'))    # 添加邮件文本信息

    smtp = SMTP_SSL(host_server)           # 链接服务器
    smtp .login(from_qq_mail, pwd)         # 登录邮箱
    smtp.sendmail(from_qq_mail, to_qq_mail, msg.as_string())  # 发送邮箱
    smtp.quit()     # 退出

def main():
    mail_message()
main()
