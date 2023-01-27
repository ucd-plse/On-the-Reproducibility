import os
import sys
import time

from bugswarm.common.rest_api.database_api import DatabaseAPI
from bugswarm.common.credentials import DATABASE_PIPELINE_TOKEN

sys.path.append("..")
from utils import PatchArtifactRunner

_COPY_DIR = 'from_host'
_PATCH_NAME = 'insecure-link'
_TRAVIS_DIR = '/home/travis'
_M2_SETTINGS = '{}/.m2/settings.xml'.format(_TRAVIS_DIR)
_FAILED_BUILD_SCRIPT = '/usr/local/bin/run_failed.sh'
_PASSED_BUILD_SCRIPT = '/usr/local/bin/run_passed.sh'
_BUGSWARMAPI = DatabaseAPI(token=DATABASE_PIPELINE_TOKEN)


def _print_usage():
    print('Usage: python3 main.py <image_tags_file> <modify-edge-cases> <source_repo> <dest_repo>')
    print('image_tags_file: Path to a file containing a newline-separated list of image tags to process.')
    print('modify_edge_cases: True or False to search and patch potential edge case files '
          ' in addition to .m2 settings and pom.xml files')
    print('source_repo: DockerHub repo from which to pull images to be patched.')
    print('dest_repo: DockerHub repo to which patched images will be pushed.')


def _validate_input(argv):
    if len(argv) != 5:
        _print_usage()
        sys.exit(1)
    image_tags_file = argv[1]
    run_edge_cases = argv[2]
    source_repo = argv[3]
    dest_repo = argv[4]
    if not os.path.isfile(image_tags_file):
        print(
            'The image_tags_file argument is not a file or does not exist. Exiting.')
        _print_usage()
        sys.exit(1)
    return image_tags_file, run_edge_cases, source_repo, dest_repo


def main(argv=None):
    argv = argv or sys.argv

    image_tags_file, run_edge_cases, source_repo, dest_repo = _validate_input(
        argv)

    failed_patch_args = dict()
    passed_patch_args = dict()
    with open(image_tags_file) as f:
        image_tags_list = list(map(str.strip, f.readlines()))

    for image_tag in image_tags_list:
        artifact = _BUGSWARMAPI.find_artifact(image_tag).json()
        proj_repo = artifact['repo']
        failed_patch_args[image_tag] = '{} {}/build/failed/{}/pom.xml {}'.format(_M2_SETTINGS,
                                                                                 _TRAVIS_DIR, proj_repo, run_edge_cases)
        passed_patch_args[image_tag] = '{} {}/build/passed/{}/pom.xml {}'.format(_M2_SETTINGS,
                                                                                 _TRAVIS_DIR, proj_repo, run_edge_cases)

    t_start = time.time()
    PatchArtifactRunner(image_tags_file, _COPY_DIR, source_repo, dest_repo,
                        _PATCH_NAME, failed_patch_args, passed_patch_args, workers=4).run()
    t_end = time.time()
    print('Running patch took {}s'.format(t_end - t_start))


if __name__ == '__main__':
    sys.exit(main())
