from flask import Flask, redirect

from config import DevConfig
import forms

app = Flask(__name__)
app.config.from_object(DevConfig)
from views import *

views = __import__('views')


if __name__ == '__main__':
    # Entry the application
    app.register_blueprint(blog_blueprint)
    app.run()