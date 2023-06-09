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
                        "name": "OWASP ZAP",
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
                    "text": alert['alert']
                }
            })

            sarif_report['runs'][0]['results'].append({
                "ruleId": rule_id,
                "level": "error",
                "message": {
                    "text": alert['desc']
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": json_report['site'][0]['@name']
                            }
                        }
                    }
                ]
            })

    return sarif_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-J", "--json_path", help="Path to the OWASP ZAP JSON baseline file")
    args = parser.parse_args()
    
    zap_report_path = args.json_path
    sarif_report_path = "zap_report.sarif"  # Ajuste o caminho onde deseja salvar o arquivo SARIF resultante

    if zap_report_path is None:
        print("ERROR: Path to JSON file is missing.")
        exit(1)

    with open(zap_report_path, 'r') as zap_report_file:
        zap_report = json.load(zap_report_file)
        sarif_report = convert_json_to_sarif(zap_report)

    with open(sarif_report_path, 'w') as sarif_report_file:
        json.dump(sarif_report, sarif_report_file)

    print("Conversion to SARIF completed successfully.")
