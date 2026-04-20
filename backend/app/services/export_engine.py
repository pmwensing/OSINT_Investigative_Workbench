import json


def build_export_package(hearing_package):
    bundle = {
        "manifest": {
            "type": "hearing_package",
            "version": "v1"
        },
        "data": hearing_package
    }

    return json.dumps(bundle, indent=2)
