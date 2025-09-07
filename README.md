# 邮件发送说明

## 快速使用步骤

1. **配置邮箱信息**
   - 打开 `send_email.py` 文件
   - 修改 `sender_email` 为您的邮箱地址
   - 修改 `sender_password` 为您的邮箱授权码（不是登录密码）

2. **获取QQ邮箱授权码**
   - 登录QQ邮箱网页版 → 设置 → 账户
   - 开启"IMAP/SMTP服务"
   - 获取16位授权码

3. **运行脚本**
   ```bash
   python send_email.py
   ```

## 其他邮箱SMTP配置
- 163邮箱: smtp.163.com, 端口587
- Gmail: smtp.gmail.com, 端口587
- Outlook: smtp-mail.outlook.com, 端口587

## 注意事项
- 使用授权码，不是登录密码
- 确保5.html文件在同一目录
- 检查网络和防火墙设置