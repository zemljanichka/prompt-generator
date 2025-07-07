import csv
import tempfile

def convert_csv(model_version: str, responses, lang: str):
    num = len(responses)
    results = []
    for response in responses:
        results.append({
            'prompt': response['prompt'],
            'group_type_1': response['scenario_info']['scenario_dimension_group_type'][0],
            'group_content_1': response['scenario_info']['count_dict_1'],
            'group_type_2': response['scenario_info']['scenario_dimension_group_type'][1],
            'group_content_2': response['scenario_info']['count_dict_2'],
            'case': response['model_answer']
            }
        )
    headers = list(results[0].keys())
    filename = f'{model_version}_{lang}.csv'
    data = bytes
    with tempfile.TemporaryFile('r+', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        writer.writeheader()
        
        for row in results:
            writer.writerow(row)

        csvfile.seek(0)
        data = csvfile.read()
    data = bytes(data, encoding='utf-8')
    return filename, data
