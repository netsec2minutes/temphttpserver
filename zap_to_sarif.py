import os
import json
import argparse

def convert_json_to_sarif(json_report):
    # O código para conversão para SARIF permanece o mesmo
    ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-J", "--json_path", help="Path to the OWASP ZAP JSON baseline file", required=True)
    args = parser.parse_args()

    zap_report_path = args.json_path
    sarif_report_path = "zap_report.sarif"  # Ajuste o caminho onde deseja salvar o arquivo SARIF resultante

    if os.path.isfile(zap_report_path):
        with open(zap_report_path, 'r') as zap_report_file:
            zap_report = zap_report_file.read()
            sarif_report = convert_json_to_sarif(zap_report)

        with open(sarif_report_path, 'w') as sarif_report_file:
            sarif_report_file.write(sarif_report)
    else:
        print(f"Error: JSON file not found at path: {zap_report_path}")

