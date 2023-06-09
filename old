import os
import json

def convert_zap_json_to_sarif(json_report):
    sarif_report = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0-rtm.5.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "informationUri": "https://github.com/goodwithtech/dockle",
                        "name": "Dockle",
                        "rules": []
                    }
                },
                "results": []
            }
        ]
    }

    zap_report = json.loads(json_report)

    if 'alerts' not in zap_report:
        print("No 'alerts' key in the report.")
        return json.dumps(sarif_report)

    for alert in zap_report['alerts']:
        rule_id = alert['pluginid']
        sarif_report['runs'][0]['tool']['driver']['rules'].append({
            "id": rule_id,
            "name": alert['alert'],
            "shortDescription": {
                "text": alert['desc']
            },
            "helpUri": alert['reference']
        })

        sarif_report['runs'][0]['results'].append({
            "ruleId": rule_id,
            "level": "error",
            "message": {
                "text": alert['alert']
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": alert['url']
                        }
                    }
                }
            ]
        })

    return json.dumps(sarif_report, indent=2)

if __name__ == "__main__":
    zap_report_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "report_json.json")
    sarif_report_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "zap_report.sarif")
    
    with open(zap_report_path) as zap_report_file:
        zap_report = zap_report_file.read()
        sarif_report = convert_zap_json_to_sarif(zap_report)
    
    with open(sarif_report_path, 'w') as sarif_report_file:
        sarif_report_file.write(sarif_report)
