import re
import typing
import jenkins
import os
import requests
from common.logger import log_wrapper
from jenkins_job import JenkinsJobList, JenkinsJob
from jenkins_logs_parser import JobLogParserFactory
from common.polling import condition_polling

os.environ["PYTHONHTTPSVERIFY"] = "0"
JENKINS_URL = 'https://chief'
JENKINS_USERNAME = 'automation'
JENKINS_PASSWORD = 'tuyunmhv2018!'
logger = log_wrapper.logger()


class JenkinsHandler:  # TODO jenkins refactor: split this file to multiple files
    def __init__(self, server: jenkins.Jenkins):
        self.server = server

    def get_all_builds_results(self, jobs_folder_path, additional_paths=()) -> JenkinsJobList:
        try:
            all_jenkins_jobs = self._get_job_objects(folder_path=jobs_folder_path, additional_paths=additional_paths)
            jobs_results = self._convert_jenkins_objects_to_results(all_jenkins_jobs)
            return JenkinsJobList(jobs=jobs_results)

        except requests.exceptions.ConnectionError as e:
            if 'HTTPSConnectionPool' in str(e):
                raise ConnectionError('Could not reach jenkions server - make sure you are connected with VPN')

    def _convert_jenkins_objects_to_results(self, all_jenkins_jobs):
        jobs = [
            JenkinsJob(url=job['url'], name=job['name'], last_build=job['lastBuild']['number'],
                       last_result=job['color'], folder=os.path.dirname(job['fullName']))
            for job in all_jenkins_jobs]

        return self._update_failed_builds_exceptions(jobs)

    def _update_failed_builds_exceptions(self, jobs):
        for job in jobs:
            if job.last_result == 'red':
                job.log_parser = JobLogParserFactory().get_job_log_parser(
                    console_output=self._get_last_console_output(job))
                job.traceback = job.log_parser.exception_traceback
                job.last_exception = job.log_parser.exception_to_show
        return jobs

    def _get_last_console_output(self, job):
        return self.server.get_build_console_output(name=f'{job.folder}/{job.name}',
                                                    number=job.last_build)

    def _get_job_objects(self, folder_path: str, additional_paths: typing.Tuple = ()):
        jobs_paths = self._get_jobs_paths(folder_path=folder_path)
        jobs_paths.extend(additional_paths)
        all_jenkins_jobs = [self.server.get_job_info(path) for path in jobs_paths]
        return all_jenkins_jobs

    def _get_jobs_paths(self, folder_path: str) -> typing.List[str]:
        jobs_names = [job['name'] for job in self.server.get_job_info(name=folder_path)['jobs']]
        jobs_paths = [f'{folder_path}/{name}' for name in jobs_names]
        return jobs_paths

    def _get_build_result(self, project_path, build_number):
        return self.server.get_build_info(name=project_path, number=build_number)['result']

    def was_build_successful(self, project_path, build_number):
        logger.debug(f'checking if dev build #{build_number} was successful')
        try:
            result = self._get_build_result(project_path=project_path, build_number=build_number)
        except Exception as e:
            logger.warning(f'got exception while trying to get build info: {e}')
            return False
        if result is not None:
            return 'SUCCESS' in result

    def get_build_name(self, project_path, build_number):
        logger.debug('getting build name')
        return self.server.get_build_info(name=project_path, number=build_number)['displayName']

    def get_console_output(self, project_path, build_number):
        logger.debug(f'getting console output, project path: <{project_path}>, build number: <{build_number}>')
        return self.server.get_build_console_output(project_path, build_number)

    def get_all_build_numbers(self, project_path) -> typing.List:
        logger.debug(f'getting all builds from job {project_path}')
        builds = self.server.get_job_info(project_path)['builds']
        return list(map(lambda build: build['number'], builds))

    def _get_last_build_number(self, project_path: str):
        return self.server.get_job_info(project_path)['lastBuild']['number']

    def wait_for_build_to_finish(self, build_number, job_path):
        logger.debug(f'wait for build number: {build_number} to finish')
        condition_polling.poll(
            func=lambda: self._get_build_result(project_path=job_path, build_number=build_number) == 'SUCCESS',
            sleep_time_sec=10, timeout_in_sec=660)

    def wait_for_build_to_start(self, build_number, job_path):
        logger.debug(f'wait for build number: {build_number} to start')
        condition_polling.poll(
            func=lambda: self._get_last_build_number(project_path=job_path) == build_number, timeout_in_sec=660)


def get_jenkins_handler(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD) -> 'JenkinsHandler':
    logger.debug('getting jenkins_wrapper handler object')
    try:
        server = jenkins.Jenkins(url=url, username=username,
                                 password=password)
    except ConnectionError:
        logger.exception('Could not connect to jenkins_wrapper server')
        return None

    return JenkinsHandler(server=server)


class ManagementJenkinsHandler:
    _jenkins_handler: 'JenkinsHandler'
    _project_path: str

    def __init__(self, jenkins_handler, project_path='Management/Management-CI'):
        self._jenkins_handler = jenkins_handler
        self._project_path = project_path

    def get_rpm_url(self, version):
        logger.debug(f'getting rpm url from management jenkins job - {self._jenkins_handler}')
        latest_successful_build = self._get_latest_successful_build_number(version=version)
        console_output = self._jenkins_handler.get_console_output(self._project_path,
                                                                  build_number=latest_successful_build)
        return self._get_rpm_url_from_output(console_output)

    def _get_latest_successful_build_number(self, version) -> int:
        logger.debug('getting latest successful build from branch dev')
        builds = self._jenkins_handler.get_all_build_numbers(self._project_path)
        for build in builds:
            if self._is_build_from_branch(build=build, version=version) and self._jenkins_handler.was_build_successful(
                    project_path=self._project_path, build_number=build):
                logger.info(f'latest successful build from branch dev is - {build}')
                return build
        raise LookupError(f'Could not find successful build for branch {version}')

    def _is_build_from_branch(self, build, version):
        logger.debug(f'checking if build is {version}')
        build_name = self._jenkins_handler.get_build_name(project_path=self._project_path, build_number=build)
        return (f'dev - develop_{version}' in build_name) or (f'master_{version} - develop_{version}' in build_name)

    @staticmethod
    def _get_rpm_url_from_output(console_output: str):
        logger.debug('extracting rpm url from build console output')
        # dev local rpm url is \ test local rpm url is:
        dhub_repo = 'dev'
        # if VCenterData.is_gve(): # TODO: resolve this weird coupling
        #     dhub_repo = 'test'
        return re.search(f'{dhub_repo} local rpm url is: (https://.*\\.rpm)', console_output).group(1)


class AgentJenkinsHandler(JenkinsHandler):

    def __init__(self, server, branch):
        super().__init__(server)
        self.path = f'Windows/WindowsAgent/{branch}'
        self.branch = branch

    def get_installer_url_for_latest_build(self):
        logger.info(f'fetching latest successful job under {self.path}')
        last_successful_build = self.get_last_successful_build()
        installer_name = 'InstallerManaged_deep'
        return f'{last_successful_build["url"]}artifact/bin/Release/Win32/{installer_name}.exe'

    def get_last_successful_build(self):
        builds = self.server.get_job_info(name=self.path)['builds']
        for build in builds:
            if self.was_build_successful(project_path=self.path, build_number=build['number']):
                logger.info(f'Found successful build #{build["number"]}: {build["url"]}')
                return build

        raise LookupError('Could not find Successful build')


class ApplianceK8sJenkinsHandler(JenkinsHandler):
    def __init__(self, server):
        super().__init__(server)
        self.create_path = 'Management/K8s/Development-QA/Create appliance in K8S - DEV QA'
        self.delete_path = 'Management/K8s/Development-QA/Delete appliance in K8S - DEV QA'

    def create_appliance(self, image_tag: str = 'latest', msp_option: bool = False, max_replicas: int = 5) -> str:
        next_build_number = self.server.get_job_info(self.create_path)['nextBuildNumber']
        logger.debug(f'going to run create appliance job path: {self.create_path} build number: {next_build_number}')
        self.server.build_job(self.create_path,
                              parameters={'TAG': image_tag, 'MSP_OPTION': msp_option,
                                          'MAX_REPLICAS': max_replicas})
        self.wait_for_build_to_start(build_number=next_build_number, job_path=self.create_path)
        self.wait_for_build_to_finish(build_number=next_build_number, job_path=self.create_path)
        console_output = self.server.get_build_console_output(self.create_path, next_build_number)
        return self._get_appliance_name_from_output(console_output=console_output)

    def delete_appliance(self, namespace: str):
        logger.debug(f'going to run delete appliance with namespace: {namespace}')
        next_build_number = self.server.get_job_info(self.delete_path)['nextBuildNumber']
        self.server.build_job(self.delete_path, parameters={'NAMESPACE': namespace})
        self.wait_for_build_to_start(build_number=next_build_number, job_path=self.delete_path)
        self.wait_for_build_to_finish(build_number=next_build_number, job_path=self.delete_path)

    @staticmethod
    def _get_appliance_name_from_output(console_output: str):
        logger.debug('extracting appliance name from build console output')
        pattern = r'automation-[0-9]*-.*testing.deepinstinctweb.com'
        return re.search(pattern=pattern, string=console_output).group(0)


class LocustK8sScalingJenkinsHandler(JenkinsHandler):

    def __init__(self, server):
        super().__init__(server)
        self.path = 'DevOps/update locust server'

    def deploy_code_to_locust_worker(self, locust_ip: str, branch: str):
        next_build_number = self.server.get_job_info(self.path)['nextBuildNumber']
        logger.debug(
            f'going to deploy branch: {branch} to locust server: {locust_ip} build number: {next_build_number}')
        self.server.build_job(self.path,
                              parameters={'MASTER_IP': locust_ip, 'GIT_BRANCH': branch})
        self.wait_for_build_to_start(build_number=next_build_number, job_path=self.path)
        self.wait_for_build_to_finish(build_number=next_build_number, job_path=self.path)


def get_management_jenkins_handler() -> ManagementJenkinsHandler:
    logger.debug('getting management jenkins handler object')
    server = jenkins.Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    jenkins_handler = JenkinsHandler(server=server)
    return ManagementJenkinsHandler(jenkins_handler)


def get_agent_jenkins_handler(branch: str = 'develop') -> AgentJenkinsHandler:
    server = jenkins.Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    return AgentJenkinsHandler(server=server, branch=branch)


def get_appliance_k8s_jenkins_handler() -> ApplianceK8sJenkinsHandler:
    server = jenkins.Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    return ApplianceK8sJenkinsHandler(server=server)


def get_locust_jenkins_handler() -> LocustK8sScalingJenkinsHandler:
    server = jenkins.Jenkins(url=JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    return LocustK8sScalingJenkinsHandler(server=server)
