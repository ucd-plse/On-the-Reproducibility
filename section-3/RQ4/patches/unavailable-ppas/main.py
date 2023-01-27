import os
import subprocess
import sys
import time
from builtins import Exception

from bugswarm.analyzer.analyzer import Analyzer

from bugswarm.common import log
from bugswarm.common.shell_wrapper import ShellWrapper
from bugswarm.common.artifact_processing.runners import ParallelArtifactRunner
from bugswarm.common.rest_api.database_api import DatabaseAPI
from bugswarm.common.credentials import DATABASE_PIPELINE_TOKEN

from pathlib import Path

_TRAVIS_DIR = '/home/travis'
_HOME_DIR = str(Path.home())

sys.path.append("..")
from utils import get_and_write_log


class PatchArtifactRunner(ParallelArtifactRunner):
    def __init__(self, image_tags_file: str, workers: int = 1):
        """
        :param image_tags_file: Path to a file containing a newline-separated list of image tags.
        :param workers: The same as for the superclass initializer.
        """
        with open(image_tags_file) as f:
            image_tags = list(map(str.strip, f.readlines()))
        super().__init__(image_tags, workers)

    def pre_run(self):
        _create_work_space()

    def process_artifact(self, image_tag: str):
        _, stdout, stderr, ok = _run_command('sudo mkdir -m 777 $HOME/bugswarm-sandbox/tmp/{}'.format(image_tag))
        _patch_artifact_and_run(image_tag.strip())

    def post_run(self):
        print("[POST_RUN]---------------------------")
        _verify_patch(self._image_tags)


def _create_work_space():
    sandbox_dir = '{}/bugswarm-sandbox'.format(_HOME_DIR)
    tmp_dir = '{}/tmp'.format(sandbox_dir)

    _, stdout, _, _ = _run_command('sudo mkdir {} && sudo chmod 777 {}'.format(tmp_dir, tmp_dir))


def _run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8').strip()
    stderr = stderr.decode('utf-8').strip()
    ok = process.returncode == 0
    return process, stdout, stderr, ok


def _print_error(msg, stdout=None, stderr=None):
    print('Error: ' + msg)
    if stdout is not None:
        print('stdout:\n{}'.format(stdout))
    if stderr is not None:
        print('stderr:\n{}'.format(stderr))


def _print_usage():
    log.info('Usage: python3 main.py <image_tags_file>')
    log.info('image_tags_file: Path to a file containing a newline-separated list of image tags to process.')


def _validate_input(argv):
    image_tags_file = argv[1]
    if not os.path.isfile(image_tags_file):
        log.error('The image_tags_file argument is not a file or does not exist. Exiting.')
        _print_usage()
        sys.exit(1)
    return image_tags_file


def _create_container(image_tag, docker_image_tag, f_or_p):
    """
    Creates a contaniner from the image on dockerhub repo bugswarm/images
    :param image_tag: The image tag associated with the artifact on DockerHub
    :param docker_image_tag: The full image tag for the image on DockerHub. E.g. bugswarm/images:image-tag
    :param f_or_p: Create the failed or passed container
    :return:
    """
    _, stdout, stderr, ok = _run_command('docker pull {}'.format(docker_image_tag))
    if ok:
        print('Successfully pulled {}'.format(image_tag))
    else:
        _print_error('Error pulling {}'.format(image_tag), stdout, stderr)
    if f_or_p is not None:
        _, stdout, stderr, ok = _run_command(
            'docker run -t -d  --name {}-{} {} /bin/bash'.format(image_tag, f_or_p, docker_image_tag))
        if ok:
            print('Created Docker container for {}'.format(image_tag))
        else:
            _print_error('Error creating Docker container for {}'.format(image_tag), stdout, stderr)
            sys.exit(1)
    else:
        _, stdout, stderr, ok = _run_command(
            'docker run -t -d  --name {} {} /bin/bash'.format(image_tag, docker_image_tag))
        if ok:
            print('Created Docker container for {}'.format(image_tag))
        else:
            _print_error('Error creating Docker container for {}'.format(image_tag), stdout, stderr)
            sys.exit(1)


def _get_container_id(image_tag, f_or_p):
    """
    get container_id
    :param image_tag: The image tag associated with the artifact on DockerHub
    :param f_or_p: failed or passed job container
    :return: container_id
    """
    if f_or_p is not None:
        _, container_id, _, _ = _run_command(
            'docker ps -a --format "{{.ID}}" --filter "name=%s-%s"' % (image_tag, f_or_p))
    else:
        _, container_id, _, _ = _run_command('docker ps -a --format "{{.ID}}" --filter "name=%s"' % image_tag)

    return container_id


def _run_patch(container_id):
    """
    Remove the PPA and clean apt-get
    :param container_id: id associated with the container for the artifact
    :return: None
    """
    _, stdout, stderr, ok = _run_command(
        'docker exec {} sudo bash -c \'rm -rf /var/lib/apt/lists/* && rm -rf /etc/apt/sources.list.d/* '
        '&& apt-get clean\''.format(container_id))
    if ok:
        print('removed PPA in container {}'.format(container_id))
    else:
        _print_error('Error removing PPA in container for {}'.format(container_id), stdout, stderr)
        sys.exit(1)


def _run_patch_and_build(container_id, f_or_p, image_tag):
    # Remove PPA and clean apt-get
    _, stdout, stderr, ok = _run_command(
        'docker exec {} sudo bash -c \'rm -rf /var/lib/apt/lists/* && rm -rf /etc/apt/sources.list.d/* '
        '&& apt-get clean\''.format(container_id))
    if ok:
        print('removed PPA in container {}'.format(container_id))
    else:
        _print_error('Error removing PPA in container for {}'.format(container_id), stdout, stderr)
        sys.exit(1)

    # run_passed/failed script
    if f_or_p == 'failed':
        _, stdout, stderr, ok = _run_command(
            'docker exec {} bash -c \'/usr/local/bin/run_failed.sh\' > '
            '$HOME/bugswarm-sandbox/tmp/{}/log-failed.log 2>/dev/null'.format(container_id, image_tag))
        if ok:
            print('Test finished in {}'.format(container_id))
        else:
            _print_error('Error running test in container for {}'.format(container_id), stdout, stderr)
    elif f_or_p == 'passed':
        _, stdout, stderr, ok = _run_command(
            'docker exec {} bash -c \'/usr/local/bin/run_passed.sh\' > '
            '$HOME/bugswarm-sandbox/tmp/{}/log-passed.log 2>/dev/null'.format(container_id, image_tag))
        if ok:
            print('Test finished in {}'.format(container_id))
        else:
            _print_error('Error running test in container for {}'.format(container_id), stdout, stderr)


def _patch_artifact_and_run(image_tag):
    """
    :param image_tag: The image tag associated with the artifact on DockerHub
    :return: None
    """
    bugswarmapi = DatabaseAPI(token=DATABASE_PIPELINE_TOKEN)
    sandbox_dir = '{}/bugswarm-sandbox'.format(_HOME_DIR)
    tmp_dir = '{}/tmp'.format(sandbox_dir)

    artifact = bugswarmapi.find_artifact(image_tag).json()
    failed_job_id = artifact['failed_job']['job_id']
    passed_job_id = artifact['passed_job']['job_id']

    _, stdout, _, _ = _run_command(
        'sudo mkdir -m 777 {}/{}'.format(tmp_dir, failed_job_id))
    _, stdout, _, _ = _run_command(
        'sudo mkdir -m 777 {}/{}'.format(tmp_dir, passed_job_id))

    failed_job_orig_log_path = '{}/{}/log-failed.log'.format(tmp_dir, failed_job_id)
    passed_job_orig_log_path = '{}/{}/log-passed.log'.format(tmp_dir, passed_job_id)

    get_and_write_log(str(failed_job_id), failed_job_orig_log_path)
    get_and_write_log(str(passed_job_id), passed_job_orig_log_path)

    docker_image_tag = 'bugswarm/images:{}'.format(image_tag)
    for fail_or_pass in ['failed', 'passed']:
        # Create Docker container
        _create_container(image_tag, docker_image_tag, fail_or_pass)
        # Copy files into container
        container_id = _get_container_id(image_tag, fail_or_pass)

        if fail_or_pass == "failed":
            _run_patch_and_build(container_id, fail_or_pass, image_tag)
        else:
            _run_patch_and_build(container_id, fail_or_pass, image_tag)

        # Remove docker container
        _, stdout, stderr, ok = _run_command('docker rm -f {}'.format(container_id))
        if ok:
            print('Successfully removed docker container {}'.format(container_id))
        else:
            _print_error('Error removing docker container {}'.format(container_id), stdout, stderr)


def _patch_artifact(image_tag):
    """
    :param image_tag: The image tag associated with the artifact on DockerHub
    :return: container_id
    """
    docker_image_tag = 'bugswarm/images:{}'.format(image_tag)
    # Create Docker container
    _create_container(image_tag, docker_image_tag, None)
    # get container_id
    container_id = _get_container_id(image_tag, None)
    # Remove PPA
    _run_patch(container_id)
    print('Successfully packaged image {}'.format(image_tag))
    return container_id


def _verify_patch(image_tags):
    """
    For each docker container, it downloads the respective failing and passing original logs and compares them with the
    reproduced logs using Analyzer. If they match then the patched containers are pushed to dockerhub and the patch meta
    data is put into the database.
    :return: None
    """
    bugswarmapi = DatabaseAPI(token=DATABASE_PIPELINE_TOKEN)
    not_reproducible = {}
    sandbox_dir = '{}/bugswarm-sandbox'.format(_HOME_DIR)
    tmp_dir = '{}/tmp'.format(sandbox_dir)

    # # Commit, push and delete all the patched containers to DockerHub
    for image_tag in image_tags:
        try:
            artifact = bugswarmapi.find_artifact(image_tag).json()
            failed_job_id = artifact['failed_job']['job_id']
            passed_job_id = artifact['passed_job']['job_id']

            failed_job_orig_log_path = '{}/{}/log-failed.log'.format(tmp_dir, failed_job_id)
            failed_job_repr_log_path = '{}/{}/log-failed.log'.format(tmp_dir, image_tag)
            passed_job_orig_log_path = '{}/{}/log-passed.log'.format(tmp_dir, passed_job_id)
            passed_job_repr_log_path = '{}/{}/log-passed.log'.format(tmp_dir, image_tag)

            analyzer = Analyzer()
            failed_job_reproduced_result = analyzer.compare_single_log(failed_job_repr_log_path, failed_job_orig_log_path)
            passed_job_reproduced_result = analyzer.compare_single_log(passed_job_repr_log_path, passed_job_orig_log_path)

            if failed_job_reproduced_result[0] and passed_job_reproduced_result[0]:
                print('Both failed and passed are reproduced for {}.'.format(image_tag))
                print('Packaging image to dockerhub for {}.'.format(image_tag))
                container_id = _patch_artifact(image_tag)

                ShellWrapper.run_commands('docker commit {} bugswarm/images:{}'.format(container_id, image_tag), shell=True)
                ShellWrapper.run_commands('sudo docker push bugswarm/images:{}'.format(image_tag), shell=True)
                ShellWrapper.run_commands('sudo docker rm -f {}'.format(container_id), shell=True)

                bugswarmapi.set_artifact_failed_patch(image_tag, 'remove-ppa')
                bugswarmapi.set_artifact_passed_patch(image_tag, 'remove-ppa')
            else:
                not_reproducible[image_tag] = {
                    'failed_job': failed_job_reproduced_result,
                    'passed_job': passed_job_reproduced_result
                }
        except (Exception, BaseException) as e:
            not_reproducible[image_tag] = {'exception': e}
            continue
        print(not_reproducible)


def main(argv=None):
    argv = argv or sys.argv
    image_tags_file = _validate_input(argv)

    t_start = time.time()
    PatchArtifactRunner(image_tags_file, workers=4).run()
    t_end = time.time()
    print('Running patch took {}s'.format(t_end - t_start))


if __name__ == '__main__':
    sys.exit(main())
