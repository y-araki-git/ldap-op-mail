#!/usr/bin/python
# -*- encoding=utf8 -*-

import sys, smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

argvs = sys.argv
argc = len(argvs)

if (argc != 4):
    print 'Usage: # %s from to subject' % argvs[0]
    quit()

# メールの文字コード、アドレス、件名の設定
charset = 'cp932'
from_address = argvs[1]
to_address   = argvs[2]
subject = unicode(argvs[3], 'utf-8')

# 標準入力からメール本文を取得
text = ''
for line in sys.stdin:
    text = text + line
text = unicode(text, 'utf-8')

# 送信メールの作成
msg = MIMEText(text.encode(charset), 'plain', charset)
msg['Subject'] = Header(subject, charset)
msg['From'] = from_address
msg['To'] = to_address
msg['Date'] = formatdate(localtime=True)

# メールの送信
smtp = smtplib.SMTP('localhost')
smtp.sendmail(from_address, to_address, msg.as_string())
smtp.close()
