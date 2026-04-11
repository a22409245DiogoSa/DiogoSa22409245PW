import requests
import json
import os

# Configurações do enunciado
schoolYear = '202526'
course = 260  # LEI (Engenharia Informática)

# Garante que a pasta para os ficheiros existe
if not os.path.exists('files'):
    os.makedirs('files')

print("A iniciar o download dos dados da Lusófona...")

for language in ['PT', 'ENG']:
    url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'
    payload = {
        'language': language,
        'courseCode': course,
        'schoolYear': schoolYear
    }
    headers = {'content-type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_dict = response.json()
        
        filename = f"ULHT{course}-{language}.json"
        with open(os.path.join('files', filename), "w", encoding="utf-8") as f:
            json.dump(response_dict, f, indent=4)
        print(f"Sucesso: {filename} guardado.")

        # Download de cada UC do curso
        for uc in response_dict['courseFlatPlan']:
            url_uc = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'
            payload_uc = {
                'language': language,
                'curricularIUnitReadableCode': uc['curricularIUnitReadableCode'],
            }
            response_uc = requests.post(url_uc, json=payload_uc, headers=headers)
            uc_dict = response_uc.json()
            
            uc_filename = f"{uc['curricularIUnitReadableCode']}-{language}.json"
            with open(os.path.join('files', uc_filename), "w", encoding="utf-8") as f:
                json.dump(uc_dict, f, indent=4)
            
    except Exception as e:
        print(f"Erro ao descarregar: {e}")

print("Processo concluído! Verifica a pasta 'files'.")