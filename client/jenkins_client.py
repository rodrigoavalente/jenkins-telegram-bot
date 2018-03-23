import re
import requests

from viewmodels.jenkins_view_model import JobViewModel, BuildViewModel, LastBuildViewModel


class JenkinsClient(object):
    username = None
    password = None
    jenkins_url = None

    def __init__(self, **kwargs):
        try:
            self.username = kwargs.pop('username')
        except KeyError:
            raise 'Jenkins username not provided. Username must be defined before proceding.'
        try:
            self.password = kwargs.pop('password')
        except KeyError:
            raise 'Jenkins password not provided. Password must be defined before proceding.'
        try:
            temp_jenkins_url = kwargs.pop('jenkins_url')
            does_match = re.match(
                r'(http:\/\/)|(https:\/\/)(www)?', temp_jenkins_url)
            if does_match:
                self.jenkins_url = re.sub(r'(http:\/\/)|(https:\/\/)(www)?', r'\1%s:%s@' % (
                    self.username, self.password), temp_jenkins_url)
            else:
                self.jenkins_url = 'http://%s:%s@%s' % (
                    self.username, self.password, temp_jenkins_url)
        except KeyError:
            raise 'Jenkins url not provided. Password must be defined before proceding.'

    def list_jobs(self, params=['name', 'color', 'url']):
        response = requests.get(
            '%s/api/json?tree=jobs[%s]' % (self.jenkins_url, ','.join(params)))
        if response.status_code == requests.codes.get('ok'):
            jobs = response.json().pop('jobs', None)
            return [JobViewModel(**job) for job in jobs]
        response.raise_for_status()

    def list_builds(self, job_name, params=['number', 'status', 'timestamp', 'id', 'result']):
        if not job_name:
            raise 'The Jenkins job name is required. Please provide one to proced.'
        response = requests.get(
            '%s/job/%s/api/json?tree=builds[%s]' % (self.jenkins_url, job_name, ','.join(params)))
        if response.status_code == requests.codes.get('ok'):
            builds = response.json().pop('builds', None)
            return [BuildViewModel(job_name=job_name, **build) for build in builds]
        response.raise_for_status()

    def get_last_build(self, job_name, params=['displayName', 'building', 'duration', 'estimatedDuration', 'id', 'result']):
        if not job_name:
            raise 'The Jenkins job name is required. Please provide one to proced.'
        response = requests.get(
            '%s/job/%s/lastBuild/api/json?tree=%s' % (self.jenkins_url, job_name, ','.join(params)))
        if response.status_code == requests.codes.get('ok'):
            last_build = response.json()
            return LastBuildViewModel(job_name=job_name, **last_build)
        response.raise_for_status()
