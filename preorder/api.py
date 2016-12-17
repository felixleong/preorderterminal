import hug
import preorder.hug_types
from preorder.env import tmpl_env


@hug.get('/', output=hug.output_format.html)
def index():
    tmpl = tmpl_env.get_template('index.html')
    return tmpl.render()


@hug.post(input=[
    hug.input_format.json,
    hug.input_format.urlencoded])
def preorder(
        name: hug.types.text,
        email: preorder.hug_types.email,
        tier: hug.types.one_of([
            'kotakcon2016-moral',
            'kotakcon2016-50paid',
            'kotakcon2016-paidfull']),
        facebook: hug.types.text = None,
        twitter: hug.types.text = None,
        phone: hug.types.text = None):
    return {
        'name': name,
        'email': email,
        'tier': tier,
        'facebook': facebook,
        'twitter': twitter,
        'phone': phone,
    }
