import os
import subprocess
import sys
import time
from pathlib import Path
from distutils.dir_util import copy_tree

from bugswarm.analyzer.analyzer import Analyzer
from bugswarm.common import log
from bugswarm.common.shell_wrapper import ShellWrapper
from bugswarm.common.artifact_processing import utils as procutils
from bugswarm.common.artifact_processing.runners import ParallelArtifactRunner
from bugswarm.common.rest_api.database_api import DatabaseAPI
from bugswarm.common.credentials import DATABASE_PIPELINE_TOKEN

_HOME_DIR = str(Path.home())

sys.path.append("..")
from utils import get_and_write_log


DOCKERHUB_REPO = 'bugswarm/images'
_COPY_DIR = 'from_host'
_PROCESS_SCRIPT = 'patch_build_script.py'
_FAILED_BUILD_SCRIPT = '/usr/local/bin/run_failed.sh'
_PASSED_BUILD_SCRIPT = '/usr/local/bin/run_passed.sh'
_TRAVIS_DIR = '/home/travis'
_BUGSWARMAPI = DatabaseAPI(token=DATABASE_PIPELINE_TOKEN)
_CHECK_PATH = '/src/test/java/com/puppycrawl/tools/checkstyle/filters'


class PatchArtifactRunner(ParallelArtifactRunner):
    def __init__(self, image_tags_file: str, copy_dir: str, workers: int = 1):
        """
        :param image_tags_file: Path to a file containing a newline-separated list of image tags.
        :param copy_dir: A directory to copy into the host-side sandbox before any artifacts are processed.
        :param command: A callable used to determine what command(s) to execute in each artifact container. `command` is
                        called once for each processed artifact. The only parameter is the image tag of the artifact
                        about to be processed.
        :param workers: The same as for the superclass initializer.
        """
        with open(image_tags_file) as f:
            image_tags = list(map(str.strip, f.readlines()))
        super().__init__(image_tags, workers)
        self.copy_dir = copy_dir

    def pre_run(self):
        _create_work_space()
        copy_tree(_COPY_DIR, os.path.join(procutils.HOST_SANDBOX, _COPY_DIR))

    def process_artifact(self, image_tag: str):
        _patch_artifact_and_run(image_tag.strip())

    def post_run(self):
        _verify_patch(self._image_tags)


def _create_work_space():
    sandbox_dir = '{}/bugswarm-sandbox'.format(_HOME_DIR)
    tmp_dir = '{}/tmp'.format(sandbox_dir)

    _, stdout, _, _ = _run_command('sudo mkdir {} && sudo chmod 777 {}'.format(tmp_dir, tmp_dir))


def _run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
    print('Usage: python3 main.py <image_tags_file>')
    print('image_tags_file: Path to a file containing a newline-separated list of image tags to process.')


def _validate_input(argv):
    if len(argv) != 2:
        _print_usage()
        sys.exit(1)

    image_tags_file = argv[1]
    if not os.path.isfile(image_tags_file):
        log.error(
            'The image_tags_file argument is not a file or does not exist. Exiting.')
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
    _, stdout, stderr, ok = _run_command(
        'docker pull {}'.format(docker_image_tag))
    if ok:
        print('Successfully pulled {}'.format(image_tag))
    else:
        _print_error('Error pulling {}'.format(image_tag), stdout, stderr)
    if f_or_p is not None:
        _, stdout, stderr, ok = _run_command('docker run -t -d  --name {}-{} {} /bin/bash'
                                             .format(image_tag, f_or_p, docker_image_tag))
        if ok:
            print('Created Docker container for {}'.format(image_tag))
        else:
            _print_error('Error creating Docker container for {}'.format(
                image_tag), stdout, stderr)
            sys.exit(1)
    else:
        _, stdout, stderr, ok = _run_command(
            'docker run -t -d  --name {} {} /bin/bash'.format(image_tag, docker_image_tag))
        if ok:
            print('Created Docker container for {}'.format(image_tag))
        else:
            _print_error('Error creating Docker container for {}'.format(
                image_tag), stdout, stderr)
            sys.exit(1)


def _copy_files_to_container(image_tag, f_or_p):
    """
    Copy patch_build_script.py into container.
    :param image_tag: The image tag associated with the artifact on DockerHub
    :param f_or_p: Copying files to the failed or passed container
    :return: None
    """
    if f_or_p is not None:
        _, container_id, _, _ = _run_command(
            'docker ps -a --format "{{.ID}}" --filter "name=%s-%s"' % (image_tag, f_or_p))
        _, stdout, stderr, ok = _run_command(
            'docker cp {}/{}/{} {}:{}/{}'.format(procutils.HOST_SANDBOX, _COPY_DIR, _PROCESS_SCRIPT, container_id,
                                                 _TRAVIS_DIR, _PROCESS_SCRIPT))
        if ok:
            print('Copied {} into container'.format(_PROCESS_SCRIPT))
        else:
            _print_error('Error copying {} into container for {}'.format(
                _PROCESS_SCRIPT, image_tag), stdout, stderr)
            sys.exit(1)

    else:
        _, container_id, _, _ = _run_command(
            'docker ps -a --format "{{.ID}}" --filter "name=%s"' % image_tag)
        _, stdout, stderr, ok = _run_command(
            'docker cp {}/{}/{} {}:{}/{}'.format(procutils.HOST_SANDBOX, _COPY_DIR, _PROCESS_SCRIPT, container_id,
                                                 _TRAVIS_DIR, _PROCESS_SCRIPT))
        if ok:
            print('Copied {} into container'.format(_PROCESS_SCRIPT))
        else:
            _print_error('Error copying {} into container for {}'.format(
                _PROCESS_SCRIPT, image_tag), stdout, stderr)
            sys.exit(1)

    return container_id


def _run_patch(container_id, repo):
    """
        Run patch_build_script.py inside the container. Adds write permissions to /usr/local/bin because the user travis
        needs to write to the run_failed/passed.sh scripts.
        :param container_id: id associated with the container for the artifact
        :return: None
        """

    _, stdout, stderr, ok = _run_command(
        'docker exec -td {} sudo chmod -R o+w /usr/local/bin'.format(container_id))
    if ok:
        print('Successfully changed permissions container {}'.format(container_id))
        _, stdout, stderr, ok = _run_command(
            'docker exec {} python {}/{} {}/build/failed/{}{}/SuppressionsLoaderTest.java '
            '{}/build/failed/{}{}/SuppressionFilterTest.java failed False'
            .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT, _TRAVIS_DIR, repo, _CHECK_PATH,
                    _TRAVIS_DIR, repo, _CHECK_PATH))
        if ok:
            print(stdout)
            print('Ran {} on container {} for failed'.format(
                _PROCESS_SCRIPT, container_id))
        else:
            _print_error('Error running {} on container {} for failed'.format(_PROCESS_SCRIPT, container_id), stdout,
                         stderr)
        _, stdout, stderr, ok = _run_command(
            'docker exec {} python {}/{} {}/build/passed/{}{}/SuppressionsLoaderTest.java '
            '{}/build/passed/{}{}/SuppressionFilterTest.java passed False'
            .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT, _TRAVIS_DIR, repo, _CHECK_PATH,
                    _TRAVIS_DIR, repo, _CHECK_PATH))
        if ok:
            print(stdout)
            print('Ran {} on container {} for passed'.format(
                _PROCESS_SCRIPT, container_id))
        else:
            _print_error('Error running {} on container {} for passed'.format(_PROCESS_SCRIPT, container_id), stdout,
                         stderr)
            sys.exit(1)
    else:
        _print_error('Error changing permissions in container {}'.format(
            container_id), stdout, stderr)
        sys.exit(1)


def _run_patch_and_build(container_id, f_or_p, repo):
    """
    Run patch_build_script.py inside the container. Adds write permissions to /usr/local/bin because the user travis
    needs to write to the run_failed/passed.sh scripts.
    :param container_id: id associated with the container for the artifact
    :param f_or_p: run patch and build for the failed or passed container
    :return: None
    """

    _, stdout, stderr, ok = _run_command(
        'docker exec -td {} sudo chmod -R o+w /usr/local/bin'.format(container_id))
    if ok:
        if f_or_p == 'failed':
            print('Successfully changed permissions container {}'.format(container_id))
            _, stdout, stderr, ok = _run_command(
                'docker exec {} python {}/{} {}/build/failed/{}{}/SuppressionsLoaderTest.java '
                '{}/build/failed/{}{}/SuppressionFilterTest.java failed True'
                .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT, _TRAVIS_DIR, repo, _CHECK_PATH,
                        _TRAVIS_DIR, repo, _CHECK_PATH))
            if ok:
                print(stdout)
                print('Ran {} on container {} for failed'.format(
                    _PROCESS_SCRIPT, container_id))
            else:
                _print_error('Error running {} on container {} for failed'
                             .format(_PROCESS_SCRIPT, container_id), stdout, stderr)
        elif f_or_p == 'passed':
            _, stdout, stderr, ok = _run_command(
                'docker exec {} python {}/{} {}/build/passed/{}{}/SuppressionsLoaderTest.java '
                '{}/build/passed/{}{}/SuppressionFilterTest.java passed True'
                .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT, _TRAVIS_DIR, repo, _CHECK_PATH,
                        _TRAVIS_DIR, repo, _CHECK_PATH))
            if ok:
                print(stdout)
                print('Ran {} on container {} for passed'.format(
                    _PROCESS_SCRIPT, container_id))
            else:
                _print_error('Error running {} on container {} for passed'
                             .format(_PROCESS_SCRIPT, container_id), stdout, stderr)
    else:
        _print_error('Error changing permissions in container {}'.format(
            container_id), stdout, stderr)
        sys.exit(1)


def _copy_files_out_of_container(image_tag, container_id, f_or_p):
    """
    Copies logs out of the container into a
    :param image_tag: The image tag associated with the artifact on DockerHub
    :param container_id: id associated with the container for the artifact
    :param f_or_p: Copying the log from the failed or passed container
    :return: None
    """
    _, stdout, stderr, ok = _run_command('cd $HOME')
    _, stdout, stderr, ok = _run_command(
        'sudo mkdir -m 777 $HOME/bugswarm-sandbox/tmp/{}'.format(image_tag))
    if ok:
        print('Successfully created directory for {}'.format(image_tag))
    else:
        _print_error('Error with mkdir', stdout, stderr)
    if f_or_p == 'failed':
        _, stdout, stderr, ok = _run_command(
            'sudo docker cp {}:{}/log-failed.log {}/tmp/{}/log-failed.log'.format(container_id, _TRAVIS_DIR,
                                                                                  procutils.HOST_SANDBOX, image_tag))
        if ok:
            print("Successfully copied failed files")
        else:
            _print_error('Error copying failed files', stdout, stderr)
    elif f_or_p == 'passed':
        _, stdout, stderr, ok = _run_command(
            'sudo docker cp {}:{}/log-passed.log {}/tmp/{}/log-passed.log'.format(container_id, _TRAVIS_DIR,
                                                                                  procutils.HOST_SANDBOX, image_tag))
        if ok:
            print("Successfully copied passed files")
        else:
            _print_error('Error copying passed files', stdout, stderr)


def _remove_files(container_id, f_or_p):
    """
    Remove logs and patch_build_script.py from the container.
    :param container_id: id associated with the container for the artifact
    :return: None
    """
    if f_or_p == 'failed':
        _, stdout, stderr, ok = _run_command('docker exec {} sudo rm {}/{} {}/log-failed.log'
                                             .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT, _TRAVIS_DIR))
        if ok:
            print('Successfully removed files from {}-{}'.format(container_id, f_or_p))
        else:
            _print_error(
                'Error removing files from {}-{}'.format(container_id, f_or_p), stdout, stderr)
    elif f_or_p == 'passed':
        _, stdout, stderr, ok = _run_command('docker exec {} sudo rm {}/{} {}/log-passed.log'
                                             .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT, _TRAVIS_DIR))
        if ok:
            print('Successfully removed files from {}-{}'.format(container_id, f_or_p))
        else:
            _print_error(
                'Error removing files from {}-{}'.format(container_id, f_or_p), stdout, stderr)
    else:
        _, stdout, stderr, ok = _run_command('docker exec {} sudo rm {}/{}'
                                             .format(container_id, _TRAVIS_DIR, _PROCESS_SCRIPT))
        if ok:
            print('Successfully removed files from {}-{}'.format(container_id, f_or_p))
        else:
            _print_error(
                'Error removing files from {}-{}'.format(container_id, f_or_p), stdout, stderr)


def _patch_artifact_and_run(image_tag):
    """
    Creates a container, copies patch_build_script.py, runs the script to modify the run_failed/passed.sh scripts to add
    flags to the mvn commands to use TLSv1.2.
    :param image_tag: The image tag associated with the artifact on DockerHub
    :return: None
    """
    artifact = _BUGSWARMAPI.find_artifact(image_tag).json()
    repo = artifact['repo']

    docker_image_tag = '{}:{}'.format(DOCKERHUB_REPO, image_tag)
    for fail_or_pass in ['failed', 'passed']:
        # Create Docker container
        _create_container(image_tag, docker_image_tag, fail_or_pass)
        # Copy files into container
        container_id = _copy_files_to_container(image_tag, fail_or_pass)
        # Run process script in container
        _run_patch_and_build(container_id, fail_or_pass, repo)
        _copy_files_out_of_container(image_tag, container_id, fail_or_pass)
        # Remove files used for patch
        _remove_files(container_id, fail_or_pass)
        # Remove docker container
        _, stdout, stderr, ok = _run_command(
            'docker rm -f {}'.format(container_id))
        if ok:
            print('Successfully removed docker container {}'.format(container_id))
        else:
            _print_error('Error removing docker container {}'.format(
                container_id), stdout, stderr)


def _patch_artifact(image_tag, repo):
    """
    Creates a container, copies patch_build_script.py, runs the script to modify the run_failed/passed.sh scripts to add
    flags to the mvn commands to use TLSv1.2.
    :param image_tag: The image tag associated with the artifact on DockerHub
    :return: container_id
    """
    docker_image_tag = '{}:{}'.format(DOCKERHUB_REPO, image_tag)
    # Create Docker container
    _create_container(image_tag, docker_image_tag, None)
    # Copy files into container
    container_id = _copy_files_to_container(image_tag, None)
    # Run process script in container
    _run_patch(container_id, repo)
    # Remove files used for patch
    _remove_files(container_id, None)
    print('Successfully packaged image {}'.format(image_tag))
    return container_id


def _verify_patch(image_tags):
    """
    For each docker container, it downloads the respective failing and passing original logs and compares them with the
    reproduced logs using Analyzer. If they match then the patched containers are pushed to dockerhub and the patch meta
    data is put into the database.
    :return: None
    """

    not_reproducible = {}
    sandbox_dir = '{}/bugswarm-sandbox'.format(_HOME_DIR)
    tmp_dir = '{}/tmp'.format(sandbox_dir)

    _, stdout, _, _ = _run_command(
        'sudo mkdir {} && sudo chmod 777 {}'.format(tmp_dir, tmp_dir))

    # Commit, push and delete all the patched containers to DockerHub
    for image_tag in image_tags:
        try:
            artifact = _BUGSWARMAPI.find_artifact(image_tag).json()
            failed_job_id = artifact['failed_job']['job_id']
            passed_job_id = artifact['passed_job']['job_id']
            repo = artifact['repo']
            failed_job_trigger_sha = artifact['failed_job']['trigger_sha']
            passed_job_trigger_sha = artifact['passed_job']['trigger_sha']

            _, stdout, _, _ = _run_command(
                'sudo mkdir -m 777 {}/{}'.format(tmp_dir, failed_job_id))
            _, stdout, _, _ = _run_command(
                'sudo mkdir -m 777 {}/{}'.format(tmp_dir, passed_job_id))

            failed_job_orig_log_path = '{}/{}/log-failed.log'.format(
                tmp_dir, failed_job_id)
            failed_job_repr_log_path = '{}/{}/log-failed.log'.format(
                tmp_dir, image_tag)
            passed_job_orig_log_path = '{}/{}/log-passed.log'.format(
                tmp_dir, passed_job_id)
            passed_job_repr_log_path = '{}/{}/log-passed.log'.format(
                tmp_dir, image_tag)

            get_and_write_log(str(failed_job_id), failed_job_orig_log_path)
            get_and_write_log(str(passed_job_id), passed_job_orig_log_path)

            analyzer = Analyzer()
            failed_job_reproduced_result = analyzer.compare_single_log(failed_job_repr_log_path,
                                                                       failed_job_orig_log_path,
                                                                       failed_job_id,
                                                                       trigger_sha=failed_job_trigger_sha,
                                                                       repo=repo)
            passed_job_reproduced_result = analyzer.compare_single_log(passed_job_repr_log_path,
                                                                       passed_job_orig_log_path,
                                                                       passed_job_id,
                                                                       trigger_sha=passed_job_trigger_sha,
                                                                       repo=repo)

            if failed_job_reproduced_result[0] and passed_job_reproduced_result[0]:
                print('Both failed and passed are reproduced for {}.'.format(image_tag))
                container_id = _patch_artifact(image_tag, repo)

                ShellWrapper.run_commands('docker commit {} {}:{}'
                                          .format(container_id, DOCKERHUB_REPO, image_tag),
                                          shell=True)
                ShellWrapper.run_commands('sudo docker push {}:{}'
                                          .format(DOCKERHUB_REPO, image_tag),
                                          shell=True)
                ShellWrapper.run_commands('sudo docker rm -f {}'
                                          .format(container_id),
                                          shell=True)

                _BUGSWARMAPI.set_artifact_failed_patch(
                    image_tag, 'checkstyle-supp')
                _BUGSWARMAPI.set_artifact_passed_patch(
                    image_tag, 'checkstyle-supp')

            else:
                not_reproducible[image_tag] = {'failed_job': failed_job_reproduced_result,
                                               'passed_job': passed_job_reproduced_result}

        except (Exception, BaseException) as e:
            not_reproducible[image_tag] = {'exception': repr(e)}
            continue

    print('The following were not reproducible:')
    print(not_reproducible)


def main(argv=None):
    argv = argv or sys.argv

    image_tags_file = _validate_input(argv)

    t_start = time.time()
    PatchArtifactRunner(image_tags_file, _COPY_DIR, workers=4).run()
    t_end = time.time()
    print('Running patch took {}s'.format(t_end - t_start))


if __name__ == '__main__':
    sys.exit(main())
