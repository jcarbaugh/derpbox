# derpbox

derpbox uploads files directly to a private Amazon S3 bucket under your control.

![a beautiful screenshot](http://assets.carbauja.com.s3.amazonaws.com/derpbox/screenshot.png)

Want to receive notifications when someone uploads a file? [Amazon has you covered](http://docs.amazonwebservices.com/AmazonS3/latest/dev/NotificationHowTo.html?r=9985).

## Running on Heroku

derpbox is Heroku ready. Rather than creating a `settings.py` file, set the following config variables on your app:

    heroku config:add AWS_KEY=<your key>
    heroku config:add AWS_SECRET=<your secret>
    heroku config:add AWS_BUCKET=<your bucket>

Follow this [handy guide](http://blog.heroku.com/archives/2011/9/28/python_and_django/) for instructions on running Flask apps on Heroku.

## Running locally or elsewhere

1. `pip install -r requirements.txt`
2.  Copy `settings.example.py` to `settings.py` and fill in the variables accordingly
3. `python derp.py` or use your favorite application server