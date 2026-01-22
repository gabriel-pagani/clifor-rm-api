from constants.abbreviations import abbreviations
import re


def format_name(name: str) -> str:
    if not name:
        return ""
    
    name = name.strip()

    name = re.sub(r" & ", " e ", name)

    # remove pontuação (mantém acentos) e números
    name = re.sub(r"[^\w\s]", " ", name, flags=re.UNICODE)
    name = re.sub(r"\d+", " ", name)  # Remove dígitos

    name = name.title()

    # Aplica abreviações (case-insensitive)
    for key, value in abbreviations.items():
        pattern = re.compile(rf"\b{re.escape(key)}\b", flags=re.IGNORECASE)
        name = pattern.sub(value, name)

    name = re.sub(r"\s+", " ", name).strip()  # Colapsa espaços repetidos
    return name


def suffix_remover(text: str) -> str:
    if not text:
        return ""
    
    # Remove "Sa", "S A" e "Ltda" em qualquer posição (como palavra), com ou sem ponto
    pattern = re.compile(r"(?:\bLtda\b\.?|\bSa\b\.?|\bS\s+A\b\.?)", flags=re.IGNORECASE)
    text = pattern.sub(" ", text)

    # Normaliza espaços após a remoção
    text = re.sub(r"\s+", " ", text).strip()
    return text


def format_zipcode(zipCode: str) -> str:
    if not zipCode:
        return ""
    
    return zipCode.replace(".", "").replace("-", "").strip()


def format_street(street: str) -> list:
    if not street:
        return ["", ""]
    
    street = street.strip().upper()
    street_type = street.split()[0]
    
    street_types = {
        "ACESSO": "2",
        "AEROPORTO": "3",
        "ALAMEDA": "4",
        "ATALHO": "5",
        "AVENIDA": "6",
        "AV": "6",
        "BECO": "7",
        "BOULEVARD": "8",
        "CAMINHO": "9",
        "CAMPO": "12",
        "CHACARA": "10",
        "CONJUNTO": "11",
        "CORREDOR": "13",
        "DESVIO": "48",
        "ENTRONCAM.": "14",
        "ESPLANADA": "15",
        "ESTACAO": "17",
        "ESTIVA": "16",
        "ESTRADA": "18",
        "FAZENDA": "19",
        "FERROVIA": "20",
        "GALERIA": "21",
        "JARDIM": "22",
        "LADEIRA": "23",
        "LAGO": "24",
        "LAGOA": "25",
        "LARGE": "26",
        "LOGRADOURO": "49",
        "MARGINAL": "50",
        "MORRO": "27",
        "PARQUE": "28",
        "PASSAGEM": "29",
        "PASSEIO": "33",
        "PORTO": "32",
        "PRACA": "30",
        "PRAIA": "31",
        "RIO": "36",
        "RODOVIA": "34",
        "ROD": "34",
        "RUA": "1",
        "R": "1",
        "RUELA": "35",
        "SERVIDAO": "46",
        "SITIO": "37",
        "SUP QUADRA": "38",
        "TRAVESSA": "39",
        "VALE": "40",
        "VARGEM": "45",
        "VIA": "43",
        "VIADUTO": "41",
        "VIELA": "42",
        "VILA": "44",
        # Adicionar mais conforme necessário
    }

    if street_type in street_types:
        street = re.sub(f'{street_type} ', '', street)
        street_type = street_types[street_type]
        return [street_type, street.title()]
    else:
        return ["1", street.title()]


def format_district(district: str) -> list:
    if not district:
        return ["", ""]
    
    district = district.strip().upper()
    district_type = district.split()[0]
    
    district_types = {
        "BAIRRO": "1",
        "BOSQUE": "2",
        "CHACARA": "3",
        "CONJUNTO": "4",
        "DESMEMB.": "5",
        "DISTRITO": "6",
        "FAVELA": "7",
        "FAZENDA": "8",
        "GLEBA": "9",
        "HORTO": "10",
        "JARDIM": "11",
        "LOTEAMENTO": "12",
        "NUCLEO": "13",
        "PARQUE": "14",
        "RESIDENC.": "15",
        "SITIO": "16",
        "TROPICAL": "17",
        "VILA": "18",
        "ZONA": "19",
        # Adicionar mais conforme necessário
    }

    if district_type in district_types:
        district = re.sub(f"{district_type} ", "", district)
        district_type = district_types[district_type]
        return [district_type, district.title()]
    else:
        return ["1", district.title()]


def format_phone(phone: str) -> str:
    if not phone:
        return ""
    
    phone = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    phone = phone.split("/")[0].strip()  # usa apenas o primeiro quando houver mais de um
    return phone
