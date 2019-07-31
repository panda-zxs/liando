from wisdom_brain.taskapp.celery_app import app


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
