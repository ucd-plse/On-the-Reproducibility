import sys
import time

from bugswarm.common.rest_api.database_api import DatabaseAPI
from bugswarm.common.credentials import DATABASE_PIPELINE_TOKEN

sys.path.append("..")
from utils import PatchArtifactRunner, _validate_input

_COPY_DIR = 'ivy-insecure-link'
_PATCH_NAME = 'modules-format'
_TRAVIS_DIR = '/home/travis'
_BUGSWARMAPI = DatabaseAPI(token=DATABASE_PIPELINE_TOKEN)


def main(argv=None):
    argv = argv or sys.argv

    image_tags_file, source_repo, dest_repo = _validate_input(argv)

    with open(image_tags_file) as f:
        image_tags_list = list(map(str.strip, f.readlines()))

    failed_patch_args = dict()
    passed_patch_args = dict()
    for image_tag in image_tags_list:
        artifact = _BUGSWARMAPI.find_artifact(image_tag).json()
        proj_repo = artifact['repo']
        failed_patch_args[image_tag] = '{}/build/failed/{}/ivysettings.xml'.format(_TRAVIS_DIR, proj_repo)
        passed_patch_args[image_tag] = '{}/build/passed/{}/ivysettings.xml'.format(_TRAVIS_DIR, proj_repo)

    t_start = time.time()
    PatchArtifactRunner(image_tags_file, _COPY_DIR, source_repo, dest_repo,
                        _PATCH_NAME, failed_patch_args, passed_patch_args, workers=4).run()
    t_end = time.time()
    print('Running patch took {}s'.format(t_end - t_start))


if __name__ == '__main__':
    sys.exit(main())
