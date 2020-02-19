__version__ = '0.1.0'

flask.Flask(__name__)

@app.context_processor
def example():
    try:
        return dict(job_status=Job.fetch(session.get("interval_id"), connection=conn))
    except:
        pass