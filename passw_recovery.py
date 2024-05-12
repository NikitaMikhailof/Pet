import smtplib
from email.mime.text import MIMEText
from email.header import Header
import secrets

def send_email(recipient):
    login = 'expresspizza914@gmail.com'
    password = 'lamuwojaikkpqvir'
    temporary_password = secrets.token_hex(5)

    message = f'Используйте временный пароль: {temporary_password} для входа в свою учетную запись. ' \
              'Для входа в свой личный кабинет перейдите по ссылке https://chester1991.pythonanywhere.com/login/ .' \
              'С уважением пиццерия Modernissimo. '

    msg = MIMEText(f'{message}', 'plain', 'utf-8' )
    msg['Subject'] = Header('Восстановление пароля', 'utf-8')
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
        return temporary_password


if __name__ == '__main__':
    send_email()