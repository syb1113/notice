import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_html_email():
    print("=== 邮件发送脚本开始运行 ===")
    
    # 邮件配置 - 请根据您的邮箱服务商修改
    smtp_server = "smtp.qq.com"  # QQ邮箱SMTP服务器
    smtp_port = 587
    sender_email = "your_email@qq.com"  # 您的邮箱
    sender_password = "your_app_password"  # 您的邮箱授权码（不是登录密码）
    
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    print(f"发件人: {sender_email}")
    
    # 收件人
    recipient_email = "3068894619@qq.com"
    print(f"收件人: {recipient_email}")
    
    # 检查配置
    if sender_email == "your_email@qq.com" or sender_password == "your_app_password":
        print("\n❌ 错误：请先配置您的邮箱信息！")
        print("请编辑脚本文件，修改以下内容：")
        print("1. sender_email = '您的真实邮箱地址'")
        print("2. sender_password = '您的邮箱授权码'")
        return
    
    # 检查HTML文件
    if not os.path.exists('5.html'):
        print("\n❌ 错误：找不到5.html文件")
        return
    
    print("\n✅ 配置检查通过，开始发送邮件...")
    
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "君莲会验证码邮件模板"
    
    # 读取HTML文件内容
    try:
        print("📖 正在读取HTML文件...")
        with open('5.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        print(f"✅ HTML文件读取成功，内容长度: {len(html_content)} 字符")
        
        # 添加HTML内容到邮件正文
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        print("✅ HTML内容已添加到邮件正文")
        
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
        print("✅ HTML文件已添加为附件")
        
        # 发送邮件
        print("🔗 正在连接SMTP服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        print("🔐 TLS加密已启用")
        
        print("🔑 正在进行身份验证...")
        server.login(sender_email, sender_password)
        print("✅ 身份验证成功")
        
        print("📧 正在发送邮件...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("🎉 邮件发送成功！")
        
    except FileNotFoundError:
        print("❌ 错误：找不到5.html文件")
    except smtplib.SMTPAuthenticationError:
        print("❌ 错误：邮箱认证失败，请检查邮箱地址和授权码")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP错误：{str(e)}")
    except Exception as e:
        print(f"❌ 发送邮件时出错：{str(e)}")

if __name__ == "__main__":
    print("📧 君莲会验证码邮件发送工具")
    print("=" * 50)
    print("⚠️  使用前请确保已配置邮箱信息：")
    print("1. 修改 sender_email 为您的邮箱地址")
    print("2. 修改 sender_password 为您的邮箱授权码")
    print("3. 如果不是QQ邮箱，请修改 smtp_server 和 smtp_port")
    print("=" * 50)
    
    send_html_email()