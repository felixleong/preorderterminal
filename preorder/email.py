from marrow.mailer import Message
from preorder.config import RECEIPT, MAILCHIMP
from preorder.env import tmpl_env, mailer, mailchimp
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


def signup_newsletter(name, email):
    if not mailchimp:
        _logger.info('Mailchimp instance not configured, no new signup added')
        return

    # Parse the name
    name_components = name.split(' ')
    if len(name_components) == 3:
        last_name = name_components[0]
        first_name = ' '.join(name_components[1:])
    else:
        first_name = name_components[0]
        last_name = ' '.join(name_components[1:])

    mailchimp.lists.members.create(MAILCHIMP['mailing_list_id'], {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': first_name,
            'LNAME': last_name,
        }
    })
