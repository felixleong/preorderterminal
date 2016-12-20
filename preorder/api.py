import hug
from datetime import datetime
import preorder.directives
import preorder.hug_types
from preorder.auth import http_basic_auth
from preorder.env import tmpl_env
from preorder.gsheets import GoogleSheets


_gsheets = GoogleSheets(
    'kotakcon2016preorder', 'Kotakcon Pre-Order System',
    '1E-zZproC0CZ1vWV3Lv5aGvEUbYGLiwm_Ph4Npccd88c')
_SHEET_NAME = 'DevTest'


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
            'kotakcon2016-50paid',
            'kotakcon2016-paidfull']),
        facebook: hug.types.text = None,
        twitter: hug.types.text = None,
        phone: hug.types.text = None):
    if not ip_addr:
        client_ip = 'unknown'
    else:
        client_ip = ip_addr[0]

    result = _gsheets.write_rows(
        _SHEET_NAME, [
            [
                name, email, tier, facebook, twitter, phone,
                '{}Z'.format(datetime.utcnow().isoformat()),
                user_name, client_ip],
        ])
    return result
