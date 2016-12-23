import hug
import re
import hashlib
from datetime import datetime
import preorder.directives
import preorder.hug_types
from preorder.auth import http_basic_auth
from preorder.config import DATA
from preorder.email import send_receipt, signup_newsletter
from preorder.env import tmpl_env
from preorder.gsheets import GoogleSheets


_gsheets = GoogleSheets(
    'kotakcon2016preorder', 'Kotakcon Pre-Order System',
    DATA['spreadsheet_id'])
_RANGE_RE = re.compile(r'{}!A(?P<row>\d+)'.format(DATA['sheet_name']))


@hug.get('/', output=hug.output_format.html, requires=http_basic_auth)
def index():
    tmpl = tmpl_env.get_template('index.html')
    return tmpl.render()


@hug.get(output=hug.output_format.html, requires=http_basic_auth)
def pages(name: hug.types.text):
    tmpl = tmpl_env.get_template('{}.html'.format(name))
    return tmpl.render({'page': name})


@hug.post(
    input=[
        hug.input_format.json,
        hug.input_format.urlencoded],
    requires=http_basic_auth)
def order(
        user_name: hug.directives.user,
        ip_addr: preorder.directives.ip_addr,
        name: hug.types.text,
        email: preorder.hug_types.email,
        facebook: hug.types.text = None,
        twitter: hug.types.text = None,
        phone: hug.types.text = None):
    if not ip_addr:
        client_ip = 'unknown'
    else:
        client_ip = ip_addr[0]

    transaction_time = datetime.utcnow().isoformat()
    transaction_id = hashlib.sha224('{}-{}-purplehaze'.format(
        email, transaction_time).encode('utf-8')).hexdigest()

    # Write to our mastersheet
    result = _gsheets.write_rows(
        DATA['sheet_name'], [
            [
                name, email, 'kotakcon2016-paidfull', facebook, twitter, phone,
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
    signup_newsletter(name, email)

    return {'success': True}


@hug.post(
    input=[
        hug.input_format.json,
        hug.input_format.urlencoded],
    requires=http_basic_auth)
def newsletter(
        name: hug.types.text,
        email: preorder.hug_types.email):
    signup_newsletter(name, email)

    return {'success': True}


# DEBUG API endpoints
# @hug.get(output=hug.output_format.html)
def email(
        name: hug.types.text,
        email: preorder.hug_types.email,
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
        'facebook': facebook,
        'twitter': twitter,
        'phone': phone,
        'transaction_id': transaction_id,
        'transaction_time': transaction_time,
    })
