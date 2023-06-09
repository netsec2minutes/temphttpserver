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

    if 'results' not in zap_report:
        print("No 'results' key in the report.")
        return json.dumps(sarif_report)

    for result in zap_report['results']:
        rule_id = result['ruleId']
        sarif_report['runs'][0]['tool']['driver']['rules'].append({
            "id": rule_id,
            "name": result['ruleId'],
            "shortDescription": {
                "text": result['message']['text']
            },
            "helpUri": result['helpUri']
        })

        sarif_report['runs'][0]['results'].append({
            "ruleId": rule_id,
            "ruleIndex": len(sarif_report['runs'][0]['tool']['driver']['rules']) - 1,
            "level": result['level'],
            "message": {
                "text": result['message']['text']
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": result['locations'][0]['physicalLocation']['artifactLocation']['uri']
                        }
                    }
                }
            ]
        })

    return json.dumps(sarif_report)


if __name__ == "__main__":
    zap_report_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "report.json")
    sarif_report_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "zap_report.sarif")

    with open(zap_report_path, 'r') as zap_report_file:
        zap_report = zap_report_file.read()
        sarif_report = convert_zap_json_to_sarif(zap_report)

    with open(sarif_report_path, 'w') as sarif_report_file:
        sarif_report_file.write(sarif_report)
