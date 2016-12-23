import hug
import re
import hashlib
from datetime import datetime
from mailchimp3 import MailChimp
import preorder.directives
import preorder.hug_types
from preorder.auth import http_basic_auth
from preorder.config import DATA, MAILCHIMP
from preorder.email import send_receipt
from preorder.env import tmpl_env
from preorder.gsheets import GoogleSheets


_gsheets = GoogleSheets(
    'kotakcon2016preorder', 'Kotakcon Pre-Order System',
    DATA['spreadsheet_id'])
if MAILCHIMP:
    _chimp = MailChimp(MAILCHIMP['user'], MAILCHIMP['api_key'])
else:
    _chimp = None
_RANGE_RE = re.compile(r'{}!A(?P<row>\d+)'.format(DATA['sheet_name']))


@hug.get('/', output=hug.output_format.html, requires=http_basic_auth)
def index():
    tmpl = tmpl_env.get_template('index.html')
    return tmpl.render()


@hug.post(
    input=[
        hug.input_format.json,
        hug.input_format.urlencoded],
    requires=http_basic_auth)
def preorder(
        user_name: hug.directives.user,
        ip_addr: preorder.directives.ip_addr,
        name: hug.types.text,
        email: preorder.hug_types.email,
        tier: hug.types.one_of([
            'kotakcon2016-moral',
            'kotakcon2016-paidfull']),
        facebook: hug.types.text = None,
        twitter: hug.types.text = None,
        phone: hug.types.text = None):
    if not ip_addr:
        client_ip = 'unknown'
    else:
        client_ip = ip_addr[0]

    transaction_id = hashlib.sha224(
        '{}purplehaze'.format(email).encode('utf-8')).hexdigest()
    transaction_time = datetime.utcnow().isoformat()

    # Write to our mastersheet
    if tier == 'kotakcon2016-paidfull':
        result = _gsheets.write_rows(
            DATA['sheet_name'], [
                [
                    name, email, tier, facebook, twitter, phone,
                    '{}Z'.format(transaction_time), transaction_id,
                    user_name, client_ip],
            ])
        backer_count = (
            int(_RANGE_RE.match(
                result['updates']['updatedRange']).group('row'))
            - 1)

        email_data = {
            'name': name,
            'email': email,
            'facebook': facebook,
            'twitter': twitter,
            'phone': phone,
            'transaction_id': transaction_id,
            'transaction_time': transaction_time,
            'backer_count': backer_count,
        }
        send_receipt(email_data)

    # Then we would want to sign people up to the newsletter
    if _chimp:
        name_components = name.split(' ')
        if len(name_components) == 3:
            last_name = name_components[0]
            first_name = ' '.join(name_components[1:])
        else:
            first_name = name_components[0]
            last_name = ' '.join(name_components[1:])

        _chimp.lists.members.create(MAILCHIMP['mailing_list_id'], {
            'email_address': email,
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': first_name,
                'LNAME': last_name,
            }
        })

    return {
        'success': True}


# DEBUG API endpoints
# @hug.get(output=hug.output_format.html)
def email(
        name: hug.types.text,
        email: preorder.hug_types.email,
        tier: hug.types.one_of([
            'kotakcon2016-moral',
            'kotakcon2016-paidfull']),
        facebook: hug.types.text = None,
        twitter: hug.types.text = None,
        phone: hug.types.text = None):
    tmpl = tmpl_env.get_template('email/receipt.html')

    transaction_id = hashlib.sha224(
        '{}purplehaze'.format(email).encode('utf-8')).hexdigest()
    transaction_time = datetime.utcnow().isoformat()
    return tmpl.render({
        'name': name,
        'email': email,
        'tier': tier,
        'facebook': facebook,
        'twitter': twitter,
        'phone': phone,
        'transaction_id': transaction_id,
        'transaction_time': transaction_time,
    })
