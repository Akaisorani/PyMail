#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

mail_host="smtp.126.com"
mail_user="mail address"
mail_pass="password"
mail_from="username<%s>"%mail_user

def send_mail(to_list,subject,text=None,image=None,attachment=None):
	"""to_list=list/str   subject=str   text=list/str/None   image=list/str/None   attachment=list/str/None"""
	if not isinstance(to_list,(list,tuple)):to_list=[to_list]
	
	msg=MIMEMultipart('mixed')
	msg["Subject"]=subject
	msg["From"]=mail_from
	msg["To"]=";".join(to_list)
	
	try:
		msgRelated=MIMEMultipart('related')
		msg.attach(msgRelated)
		msgAlternative=MIMEMultipart('alternative')
		msgRelated.attach(msgAlternative)
		
		if text!=None:				#添加文字
			msgAlternative.attach(MIMEText(text,"html","utf-8"))
		
		if image!=None:				#添加图片
			img_list=image if isinstance(image,(list,tuple)) else [image]
			for filename in img_list:
				img_html="<p><img src='cid:image%d'></p>"%img_list.index(filename)
				msgAlternative.attach(MIMEText(img_html,"html","utf-8"))

				msgImage=MIMEImage(open(filename,'rb').read())
				msgImage["Content-ID"]="<image%d>"%img_list.index(filename)
				msgRelated.attach(msgImage)
				
		if attachment!=None:		#添加附件
			att_list=attachment if isinstance(attachment,(list,tuple)) else [attachment]
			for filename in att_list:
				msgAtt=MIMEText(open(filename,'rb').read(),'base64','utf-8')
				msgAtt["Content-Type"]="application/octet-stream"
				msgAtt["Content-Disposition"]="attachment; filename="+filename
				msg.attach(msgAtt)

		#连接服务器，发送邮件
		server=smtplib.SMTP_SSL(mail_host,465)
		server.login(mail_user,mail_pass)
		server.sendmail(mail_user,to_list,msg.as_string())
		server.quit()
		return True
	except Exception as e:
		print(e)
		return False
		
if __name__=="__main__":
	test_to_list="mail_address"
	if send_mail(test_to_list,"测试邮件","Mail test"):
		print("发送成功")
	else:
		print("发送失败")