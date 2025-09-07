import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
import glob
import time

def send_single_html_email(html_file, smtp_server, smtp_port, sender_email, sender_password, recipient_email):
    """发送单个HTML文件的邮件"""
    try:
        print(f"正在发送 {html_file} ---")
        
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"君莲会验证码邮件模板 - {html_file}"
        
        print(f"正在读取HTML文件内容: {html_file}")
        
        # 读取HTML文件内容
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        print(f"HTML文件大小: {len(html_content)} 字符")
        
        # 添加HTML内容到邮件正文
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        print("HTML内容已添加到邮件正文")
        
        # 同时作为附件发送
        with open(html_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= "{html_file}"'
        )
        msg.attach(part)
        print("HTML文件已添加为附件")
        
        # 连接SMTP服务器
        print("正在连接SMTP服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print("启用TLS加密...")
        server.starttls()  # 启用TLS加密
        
        print("正在登录邮箱...")
        server.login(sender_email, sender_password)
        
        print("正在发送邮件...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ {html_file} 发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 发送 {html_file} 时出错：{str(e)}")
        return False

def send_html_email():
    print("=== 邮件发送脚本开始执行 ===")
    
    # 邮件配置 - 请根据您的邮箱服务商修改
    smtp_server = "smtp.qq.com"  # QQ邮箱SMTP服务器
    smtp_port = 587
    sender_email = "3130492454@qq.com"  # 您的邮箱
    sender_password = "msxnfzikzhbkdfhb"  # 您的邮箱授权码（不是登录密码）
    
    # 收件人
    recipient_email = "3068894619@qq.com"
    
    print(f"发件人: {sender_email}")
    print(f"收件人: {recipient_email}")
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    
    # 查找所有HTML文件
    html_files = glob.glob('*.html')
    if not html_files:
        print("错误：当前目录下没有找到HTML文件")
        return False
    
    html_files.sort()  # 按文件名排序
    print(f"找到HTML文件: {html_files}")
    print(f"将逐个发送 {len(html_files)} 个HTML文件")
    
    success_count = 0
    failed_files = []
    
    # 逐个发送每个HTML文件
    for i, html_file in enumerate(html_files, 1):
        print(f" {i}/{len(html_files)} ===")
        
        if send_single_html_email(html_file, smtp_server, smtp_port, sender_email, sender_password, recipient_email):
            success_count += 1
        else:
            failed_files.append(html_file)
        
        # 在发送之间稍作延迟，避免被邮件服务器限制
        if i < len(html_files):
            print("等待2秒后发送下一个文件...")
            time.sleep(2)
    
    # 显示发送结果统计
    print(f"=== 发送完成统计 ===")
    print(f"成功发送: {success_count}/{len(html_files)} 个文件")
    
    if failed_files:
        print(f"发送失败的文件: {failed_files}")
        return False
    else:
        print("✅ 所有文件发送成功！")
        return True


if __name__ == "__main__":
    print("=== 君莲会验证码邮件发送工具 ===")
    print("配置信息：")
    print("- 发件邮箱: 3130492454@qq.com")
    print("- 收件邮箱: 3068894619@qq.com")
    print("- 邮件内容: 当前目录下所有HTML文件")
    print()
    
    success = send_html_email()
    
    if success:
        print("\n🎉 任务完成！请检查收件箱。")
    else:
        print("\n💥 任务失败！请检查错误信息。")
    
    print("=== 脚本执行结束 ===")