import datetime
import os
from base64 import b64encode

import boto3
from flask import Flask, render_template, request

try:
    import settings
    has_settings = True
except ImportError:
    has_settings = False


def get_config(key, default=None, cast=None):
    if has_settings:
        return getattr(settings, key, default)
    val = os.environ.get(key, default)
    if cast:
        val = cast(val)
    return val


AWS_KEY = get_config('AWS_KEY')
AWS_SECRET = get_config('AWS_SECRET')
AWS_BUCKET = get_config('AWS_BUCKET')

app = Flask(__name__)
app.config['DEBUG'] = get_config('DEBUG') == 'True'


@app.route("/")
def index():

    redirect = request.url_root

    s3 = boto3.client(
        's3', aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
    presigned = s3.generate_presigned_post(
        Bucket=AWS_BUCKET,
        Key='${filename}',
        Fields={
            "acl": "private",
            "success_action_redirect": redirect,
        },
        Conditions=[
            {"acl": "private"},
            {"success_action_redirect": redirect},
        ],
        ExpiresIn=3600
    )

    # create template context

    context = {
        'presigned': presigned,
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
