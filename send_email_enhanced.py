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
    # recipient_email = "lw616458279@qq.com"

    print(f"发件人: {sender_email}")
    print(f"收件人: {recipient_email}")
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    
    # 查找所有HTML文件
    all_html_files = glob.glob('*.html')
    if not all_html_files:
        print("错误：当前目录下没有找到HTML文件")
        return False
    
    all_html_files.sort()  # 按文件名排序
    print(f"找到HTML文件: {all_html_files}")
    
    # 让用户选择要发送的文件
    print("请选择要发送的文件：")
    print("1. 直接按回车 - 发送所有HTML文件")
    print("2. 输入文件名 - 发送指定文件（多个文件用逗号分隔）")
    print("3. 输入文件序号 - 发送指定序号的文件（多个序号用逗号分隔）")
    
    # 显示文件列表供用户参考
    print("可用的HTML文件：")
    for i, file in enumerate(all_html_files, 1):
        print(f"  {i}. {file}")
    
    user_input = input("请输入您的选择（直接回车发送全部）: ").strip()
    
    # 确定要发送的文件列表
    html_files = []
    
    if not user_input:  # 用户直接按回车，发送所有文件
        html_files = all_html_files
        print(f"将发送所有 {len(html_files)} 个HTML文件")
    else:
        # 解析用户输入
        inputs = [item.strip() for item in user_input.split(',')]
        
        for item in inputs:
            if item.isdigit():  # 如果是数字，按序号选择
                index = int(item) - 1
                if 0 <= index < len(all_html_files):
                    if all_html_files[index] not in html_files:
                        html_files.append(all_html_files[index])
                else:
                    print(f"警告：序号 {item} 超出范围，已忽略")
            else:  # 如果是文件名
                # 检查是否是完整文件名
                if item in all_html_files:
                    if item not in html_files:
                        html_files.append(item)
                # 检查是否是部分文件名匹配
                else:
                    matched_files = [f for f in all_html_files if item.lower() in f.lower()]
                    if matched_files:
                        for matched_file in matched_files:
                            if matched_file not in html_files:
                                html_files.append(matched_file)
                        print(f"根据 '{item}' 匹配到文件: {matched_files}")
                    else:
                        print(f"警告：未找到包含 '{item}' 的文件，已忽略")
        
        if not html_files:
            print("错误：没有选择任何有效的文件")
            return False
        
        print(f"将发送以下 {len(html_files)} 个文件: {html_files}")
    
    success_count = 0
    failed_files = []
    
    # 逐个发送每个HTML文件
    for i, html_file in enumerate(html_files, 1):
        print(f"=== 发送第 {i}/{len(html_files)} 个文件 ===")
        
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