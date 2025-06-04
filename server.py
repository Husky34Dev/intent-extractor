# archivo: server.py

from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class PromptInput(BaseModel):
    prompt: str

class ExtractedResult(BaseModel):
    intencion: str
    tipo_dato: str
    valor_dato: str

@app.post("/mcp", response_model=ExtractedResult)
def extract_intent_and_data(prompt_input: PromptInput):
    mensaje = prompt_input.prompt
    mensaje_lower = mensaje.lower().strip()

    intencion = "consulta_general"
    tipo_dato = "desconocido"
    valor_dato = "no_detectado"

    if re.search(r"\bfactura(s)?\b", mensaje_lower):
        intencion = "obtener_facturas"
    elif re.search(r"\bdato(s)?\b|\binformación personal\b", mensaje_lower):
        intencion = "ver_datos_personales"
    elif re.search(r"\breclamación(es)?\b|\breclamar\b", mensaje_lower):
        intencion = "consultar_reclamaciones"
    elif re.search(r"\binspección(es)?\b", mensaje_lower):
        intencion = "consultar_inspecciones"
    elif re.search(r"\bcorte(s)?\b", mensaje_lower):
        intencion = "consultar_cortes"
    elif re.search(r"\bcambio(s)?\b", mensaje_lower):
        intencion = "consultar_cambios"
    elif re.search(r"\breposición(es)?\b", mensaje_lower):
        intencion = "consultar_reposiciones"

    dni_match = re.search(r"\b\d{8}[a-zA-Z]\b", mensaje)
    poliza_match = re.search(r"\b\d{8}\b", mensaje) if not dni_match else None
    email_match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", mensaje)
    telefono_match = re.search(r"\b\d{9}\b", mensaje)
    municipio_match = re.search(r"\ben\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)", mensaje)
    direccion_match = re.search(r"(calle|av(enida)?|plaza|carrer|camino|paseo)\s+[a-záéíóúñ\s\d]+", mensaje_lower)
    nombre_match_mayus = re.search(r"(?:de\s)?((?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+){0,2}[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)", mensaje)
    nombre_match_minusc = re.search(r"(?:de\s)?((?:[a-záéíóúñ]+\s+){0,2}[a-záéíóúñ]+)", mensaje_lower)

    if dni_match:
        tipo_dato = "dni"
        valor_dato = dni_match.group()
    elif poliza_match:
        tipo_dato = "poliza"
        valor_dato = poliza_match.group()
    elif email_match:
        tipo_dato = "email"
        valor_dato = email_match.group()
    elif telefono_match:
        tipo_dato = "telefono"
        valor_dato = telefono_match.group()
    elif municipio_match:
        tipo_dato = "municipio"
        valor_dato = municipio_match.group(1).strip()
    elif direccion_match:
        tipo_dato = "direccion"
        valor_dato = direccion_match.group().strip()
    elif nombre_match_mayus:
        tipo_dato = "nombre"
        valor_dato = nombre_match_mayus.group(1).strip()
    elif nombre_match_minusc:
        tipo_dato = "nombre"
        valor_dato = nombre_match_minusc.group(1).strip()

    return {
        "intencion": intencion,
        "tipo_dato": tipo_dato,
        "valor_dato": valor_dato
    }
