@echo off
echo Running email script...
python send_email_enhanced.py > email_output.txt 2>&1
echo Script completed. Check email_output.txt for results.
type email_output.txt