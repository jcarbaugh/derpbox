from base64 import b64encode
import datetime
import hashlib
import hmac
import os

from flask import Flask, render_template, request

try:
    import settings
    has_settings = True
except ImportError:
    has_settings = False

def get_config(key, default=None):
    if has_settings:
        return getattr(settings, key, default)
    return os.environ.get(key, default)

AWS_KEY = get_config('AWS_KEY')
AWS_SECRET = get_config('AWS_SECRET')
AWS_BUCKET = get_config('AWS_BUCKET')

app = Flask(__name__)

@app.route("/")
def index():

    policy = {
        "conditions": [
            {"bucket": AWS_BUCKET},
            {"acl": "private"},
            ['starts-with', '$key', ''],
        ]
    }

    # add expiration and redirect fields

    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(minutes=10)
    policy['expiration'] = then.isoformat() + 'Z'

    redirect = request.url_root
    policy['conditions'].append({"success_action_redirect": redirect})

    # encode and sign policy

    b64_policy = b64encode(str(policy))
    signature = b64encode(
        hmac.new(AWS_SECRET, b64_policy, hashlib.sha1).digest())

    # create template context

    context = {
        'key': AWS_KEY,
        'bucket': AWS_BUCKET,
        'policy': b64_policy,
        'signature': signature,
        'redirect': redirect,
    }

    if 'key' in request.args:
        context['success'] = {'filename': request.args['key']}

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(
        debug=get_config('DEBUG') is not None,
        host=get_config('HOST', '0.0.0.0'),
        port=get_config('PORT', 8000),
    )