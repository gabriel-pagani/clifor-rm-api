from utils.formatter import format_name, suffix_remover, format_zipcode, format_phone
import requests


def cnpj_lookup(codcoligada: str, codcfo: str, cnpj: str, ie: str = ""):
    formatted_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    resp = requests.get(f"https://receitaws.com.br/v1/cnpj/{formatted_cnpj}").json()
    
    response = {
        "companyId": codcoligada,
        "code": codcfo,
        "type": 3 if codcfo.upper().startswith('C') else 2,
        "contributor": 2 if ie and "isento" in ie.strip().lower() else (1 if ie else 0),

        "shortName": suffix_remover(format_name(resp["fantasia"])) if resp["fantasia"] else suffix_remover(format_name(resp["nome"])),
        "name": format_name(resp["nome"]),
        "mainNIF": resp["cnpj"].strip(),
        "stateRegister": ie,
        "zipCode": format_zipcode(resp["cep"]),
        "streetType": "",  # Formatar
        "streetName": resp["logradouro"].title().strip(),  # Formatar
        "number": resp["numero"].upper().strip(),
        "districtType": "",  # Formatar
        "district": resp["bairro"].title().strip(),  # Formatar
        "stateCode": resp["uf"].upper().strip(),
        "cityInternalId": "",  # Formatar
        "phoneNumber": format_phone(resp["telefone"]),
        "email": resp["email"].lower().strip()
    }
    
    return response
