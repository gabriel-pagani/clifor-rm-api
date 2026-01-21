from constants.abbreviations import abbreviations
import re


def format_name(name: str) -> str:
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
    # Remove "Sa", "S A" e "Ltda" em qualquer posição (como palavra), com ou sem ponto
    pattern = re.compile(r"(?:\bLtda\b\.?|\bSa\b\.?|\bS\s+A\b\.?)", flags=re.IGNORECASE)
    text = pattern.sub(" ", text)

    # Normaliza espaços após a remoção
    text = re.sub(r"\s+", " ", text).strip()
    return text


def format_phone(phone: str) -> str:
    phone = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    phone = phone.split("/")[0].strip()  # usa apenas o primeiro quando houver mais de um
    return phone
