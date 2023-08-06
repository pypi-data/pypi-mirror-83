
import json

version_json = '''
{"date": "2020-10-24T12:20:10.114306", "dirty": false, "error": null, "full-revisionid": "c0e6b673f13e798e86e9f5e2f4eaa48818622ab3", "version": "0.23.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

