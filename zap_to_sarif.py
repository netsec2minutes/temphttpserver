import os
import json

def convert_json_to_sarif(json_report):
    sarif_report = {
        "$schema" : "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "version" : "2.1.0",
        "runs" : [
            {
                "tool" : {
                    "driver" : {
                        "name" : "DASTARDLY",
                        "version" : "1.0.0",
                        "rules" : []
                    }
                },
                "results": []
            }
        ]
    }

    zap_report = json.loads(json_report)

    if 'rules' not in zap_report:
        print("No 'rules' key in the report.")
        return json.dumps(sarif_report)

    for rule in zap_report['rules']:
        rule_id = rule['id']
        sarif_report['runs'][0]['tool']['driver']['rules'].append({
            "id": rule_id,
            "name": rule['name'],
            "shortDescription": {
                "text": rule['name']
            }
        })

    if 'results' not in zap_report:
        print("No 'results' key in the report.")
        return json.dumps(sarif_report)

    for result in zap_report['results']:
        rule_id = result['ruleId']
        sarif_report['runs'][0]['results'].append({
            "ruleId": rule_id,
            "level": "error",
            "message": {
                "text": result['message']
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
    zap_report_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "report_json.json")
    sarif_report_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "zap_report.sarif")
    
    with open(zap_report_path, 'r') as zap_report_file:
        zap_report = zap_report_file.read()
        sarif_report = convert_json_to_sarif(zap_report)

    with open(sarif_report_path, 'w') as sarif_report_file:
        sarif_report_file.write(sarif_report)
