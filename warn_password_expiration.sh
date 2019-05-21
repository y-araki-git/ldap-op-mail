#!/usr/bin/bash

MailSubject='パスワード有効期限のお知らせ'                          # 送信メールの件名
MailFrom='xxx@xxx.com'                                              # 送信メールの送信元アドレス
MailTemplate=$(dirname $0)'/warn_password_expiration_mail.txt'      # 送信メール本文のテンプレートファイル
PY_LISTUP_EXSHORT=$(dirname $0)'/listup_password_expire_shortly.py' # パスワード期限切れが迫っているアカウントをリストアップするスクリプト
PY_SEND_MAIL=$(dirname $0)'/send_mail.py'                           # メールを送信するスクリプト


# メール送信処理部
function send_mail () {
  user_name="${1}"
  mail_to="${2}"
  user_until_exp_time="${3}"

  echo "${user_name}（${mail_to}）へメールを送信します."
  mail_text=$(sed -e 's#%UserName%#'"${user_name}"'#' -e 's#%untilExpirationTime%#'"${user_until_exp_time}"'#' ${MailTemplate})

  echo "${mail_text}" | ${PY_SEND_MAIL} "${MailFrom}" "${mail_to}" "${MailSubject}"
}


# アカウント管理者に順にメールを送信する
${PY_LISTUP_EXSHORT} | while read line
do
  user_name=$(echo "${line}" | cut -d';' -f1)
  user_mail=$(echo "${line}" | cut -d';' -f2)
  user_until_exp_time=$(echo "${line}" | cut -d';' -f3)
  send_mail "${user_name}" "${user_mail}" "${user_until_exp_time}"
done
