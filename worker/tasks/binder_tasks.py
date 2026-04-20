from worker.celery_app import celery_app

@celery_app.task(name="binder.test")
def binder_test():
    return "binder working"
