import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(recipient, **context):
    login = 'expresspizza914@gmail.com'
    password = 'lamuwojaikkpqvir'
    message = f'Используйте логин: {context["login"]} и временный пароль: {context["password"]} для входа в свою учетную запись. ' \
               'Для завершения восстановления учетной записи перейдите по ссылке https://chester1991.pythonanywhere.com/login/ .' \
               'С уважением пиццерия Modernissimo. '
    msg = MIMEText(f'{message}', 'plain', 'utf-8' )
    msg['Subject'] = Header('Восстановление учётной записи', 'utf-8')
    msg['From'] = login
    msg['To'] = recipient
    server = smtplib.SMTP('smtp.gmail.com', 587)

    try:
        server.starttls()
        server.login(login, password)
        server.sendmail(msg['From'], recipient, msg.as_string())
    except Exception as _ex:
        print(f'{_ex}\nПроверьте адрес почты получателя пожалуйста!')
    finally:
        server.quit()


if __name__ == '__main__':
    send_email()
