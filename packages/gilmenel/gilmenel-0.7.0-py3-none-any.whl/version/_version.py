
# This file was generated by 'versioneer.py' (0.18) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

import json

version_json = '''
{
 "date": "2020-10-20T19:55:20+0200",
 "dirty": false,
 "error": null,
 "full-revisionid": "7f2adf243505200a56377e9c7ada5cf65a20dd83",
 "version": "v0.7.0"
}
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)
