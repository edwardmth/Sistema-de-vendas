import requests

def consultar_cep(cep):
    """Consulta um CEP no ViaCEP"""
    cep = ''.join(filter(str.isdigit, cep))
    if len(cep) != 8:
        return None
    
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/', timeout=5)
        data = response.json()
        return {
            'rua': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'estado': data.get('uf', '')
        } if not data.get('erro') else None
    except:
        return None