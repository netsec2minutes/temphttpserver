import json
import argparse

def convert_json_to_sarif(json_report):
    sarif_report = {
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "DASTARDLY",
                        "version": "1.0.0",
                        "rules": []
                    }
                },
                "results": []
            }
        ]
    }

    if 'alerts' in json_report:
        for alert in json_report['alerts']:
            rule_id = alert['pluginid']
            sarif_report['runs'][0]['tool']['driver']['rules'].append({
                "id": rule_id,
                "name": alert['alert'],
                "shortDescription": {
                    "text": alert
