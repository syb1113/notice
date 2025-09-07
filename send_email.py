import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_html_email():
    # 邮件配置 - 请根据您的邮箱服务商修改
    smtp_server = "smtp.qq.com"  # QQ邮箱SMTP服务器
    smtp_port = 587
    sender_email = "3130492454@qq.com"  # 您的邮箱
    sender_password = "msxnfzikzhbkdfhb"  # 您的邮箱授权码（不是登录密码）
    
    # 收件人
    recipient_email = "3068894619@qq.com"
    
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "君莲会验证码邮件模板"
    
    # 读取HTML文件内容
    try:
        with open('5.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # 添加HTML内容到邮件正文
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 同时作为附件发送
        with open('5.html', 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename= "5.html"'
        )
        msg.attach(part)
        
        # 发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("邮件发送成功！")
        
    except FileNotFoundError:
        print("错误：找不到5.html文件")
    except Exception as e:
        print(f"发送邮件时出错：{str(e)}")

if __name__ == "__main__":
    print("邮件发送脚本")
    print("请先配置您的邮箱信息：")
    print("1. 修改 sender_email 为您的邮箱地址")
    print("2. 修改 sender_password 为您的邮箱授权码")
    print("3. 如果不是QQ邮箱，请修改 smtp_server 和 smtp_port")
    print("\n运行脚本发送邮件...")
    
    send_html_email()