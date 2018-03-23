import datetime


class JobViewModel(object):
    url = None
    name = None
    color = None

    def __init__(self, **kwargs):
        self.url = kwargs.pop('url', None)
        self.name = kwargs.pop('name', None)
        self.color = kwargs.pop('color', None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class BuildViewModel(object):
    number = None
    result = None
    build_id = None
    job_name = None
    timestamp = None

    def __init__(self, job_name='Not Informed', **kwargs):
        self.job_name = job_name
        self.number = kwargs.pop('number', None)
        self.result = kwargs.pop('result', None)
        self.build_id = kwargs.pop('id', None)
        self.timestamp = kwargs.pop('timestamp', None)

    def __str__(self):
        return 'Job: %s | Build: %s - Result: %s' % (self.job_name, self.number, self.result)

    def __repr__(self):
        return str(self)


class LastBuildViewModel(object):
    result = None
    building = None
    job_name = None
    duration = None
    display_name = None
    estimated_duration = None

    def __init__(self, job_name='Not Informed', **kwargs):
        self.job_name = job_name
        self.result = kwargs.pop('result', None)
        self.building = kwargs.pop('building', None)
        self.duration = kwargs.pop('duration', None)
        self.display_name = kwargs.pop('displayName', None)
        self.estimated_duration = kwargs.pop('estimatedDuration')

    def __str__(self):
        return 'Job: %s | Building: %s - Duration: %s | Result: %s' % (self.job_name, self.building, self.human_duration, self.result)

    @property
    def human_duration(self):
        return datetime.timedelta(milliseconds=self.duration)

    @property
    def human_estimated_duration(self):
        return datetime.timedelta(milliseconds=self.estimated_duration)
