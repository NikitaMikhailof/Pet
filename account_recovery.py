import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(recipient, **context):
    login = 'mikhailoffnikita2016@yandex.ru'
    password = 'maduhqztwlfxcrep'
    message = f'Используйте логин: {context['login']} и временный пароль: {context['password']} для входа в свою учетную запись!'
    msg = MIMEText(f'{message}', 'plain', 'utf-8' )
    msg['Subject'] = Header('Восстановление учётной записи', 'utf-8')
    msg['From'] = login
    msg['To'] = recipient
    server = smtplib.SMTP('smtp.yandex.ru', 587)

    try:
        server.starttls()
        server.login(login, password)
        server.sendmail(msg['From'], recipient, msg.as_string()) 
    except Exception as _ex:
        print(f'{_ex}\nПроверьте адрес почты получателя пожалуйста!') 
    finally:
        server.quit()  


def main():
    send_email(recipient='nikitamikhailov2392@gmail.com')

if __name__ == '__main__':
    main()
