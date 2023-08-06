# simple-email
简易的发送邮件脚本,通过封装,可以发送带附件的邮件.

demo
```
import Simple_email
## 发送邮件
1.填写邮箱配置
    host = 'xx.xx.xx.xx'
    port = 110
    user = ''
    pass_ = ''
2.填写邮件配置
    title = ''
    body = ''
    attachment = ['']
    sender = ''
    to = ['']
    cc = []
3.发送邮件
    se = SenEmail(host=host,port=port,user=user,pass_=pass_)
    se.send_email(title=title, body=body, attachment=attachment, sender=sender, to=to, cc=cc)

## 接收邮件正文,附件,邮件头.
    se_server = SenEmail(host=host,port=port,user=user,pass_=pass_)
    class AB(GetEmail):
        def run():
            '重写run()方法'
        
```