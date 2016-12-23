from marrow.mailer import Message
from preorder.config import RECEIPT
from preorder.env import tmpl_env, mailer
import logging
import html2text

_logger = logging.getLogger('preorder.email')


def send_receipt(data):
    if not mailer:
        _logger.info('Email server not configured, email receipt not sent')
        return

    tmpl = tmpl_env.get_template('email/receipt.html')
    content = tmpl.render(data)

    print('Sender: {} <{}>'.format(RECEIPT['sender_name'], RECEIPT['email']))
    print('Receive: {} <{}>'.format(data['name'], data['email']))
    message = Message(
        author='{} <{}>'.format(RECEIPT['sender_name'], RECEIPT['email']),
        to='{} <{}>'.format(data['name'], data['email']))
    message.subject = RECEIPT['subject']
    message.plain = html2text.html2text(content)
    message.rich = content
    mailer.send(message)
