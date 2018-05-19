import os

from celery import Celery

from tinyblog import create_app

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """
        Integrate app context to celery.Task
        """
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    
    # Make other extensions could be called normally
    celery.Task = ContextTask
    return celery


env = os.environ.get('BLOG_ENG', 'dev')
flask_app = create_app('tinyblog.config.{}Config'.format(env.capitalize()))
# Each celery process needs to create an instance of flask app, register the celery object to the app object.
celery = make_celery(flask_app)