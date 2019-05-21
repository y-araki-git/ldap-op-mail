#!/usr/bin/python
# -*- encoding=utf8 -*-

import os, sys, datetime, codecs, ldap
from datetime import datetime as dt
sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)

# LDAP接続情報
expireDay = 90
shortlyDay = 7
ldap_uri = u'ldap://LDAPサーバIP'
base_dn = u'dc=test,dc=org'

# 関数：アカウントのパスワード有効期限が迫っている場合に、残りの時間を返す
def password_expire_shortly ( dn,entry,expireDay,shortlyDay ):
    nowTime = dt.now() - datetime.timedelta(hours=9)
    pwdChangedTimeStr = entry['pwdChangedTime'][0]
    pwdChangedTime = dt.strptime(pwdChangedTimeStr, '%Y%m%d%H%M%SZ')
    pwdExpireTime  = pwdChangedTime + datetime.timedelta(days=expireDay)
    # パスワードの有効期限が迫っているかをチェック（すでに有効期限切れは含まない）
    untilExpirationTime   = pwdExpireTime - nowTime
    if ( datetime.timedelta(days=0) < untilExpirationTime
         and untilExpirationTime < datetime.timedelta(days=shortlyDay)):
        return untilExpirationTime
    else:
        return None

# パスワードが設定されているLDAPアカウントを検索
lo = ldap.initialize(ldap_uri)
lo.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
lo.simple_bind_s()
filterstr = u'(&(objectClass=posixAccount)(pwdChangedTime=*))'
attrlist  = ['+', '*']
result    = lo.search_s(base_dn, ldap.SCOPE_SUBTREE, filterstr, attrlist, )

# パスワードの有効期限が迫っている利用者情報を表示
for dn,entry in result:
    untilExpirationTime = password_expire_shortly ( dn,entry,expireDay,shortlyDay )
    if untilExpirationTime is not None:
        sn        = entry.get ('sn',[''])[0]
        givenName = entry.get ('givenName',[''])[0]
        mail      = entry.get ('mail',[''])[0]
        print u'%s %s;%s;%s' % (unicode(sn,'utf-8'), unicode(givenName,'utf-8'), mail, untilExpirationTime)
