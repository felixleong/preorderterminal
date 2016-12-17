import hug
from marshmallow import fields


@hug.get('/', output=hug.output_format.html)
def index():
    return open('preorder/templates/index.html').read()


@hug.post(input=[
    hug.input_format.json,
    hug.input_format.urlencoded])
def preorder(
        name: hug.types.text,
        email: fields.Email(),
        tier: hug.types.one_of([
            'kotakcon2016-moral',
            'kotakcon2016-50paid',
            'kotakcon2016-paidfull']),
        facebook=None,
        twitter=None):
    return {
        'name': name,
        'email': email,
        'tier': tier
    }
