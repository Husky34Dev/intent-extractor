from fastapi import FastAPI
from pydantic import BaseModel
import re
from fastapi_mcp import FastApiMCP

app = FastAPI()

class PromptInput(BaseModel):
    mensaje: str

class ExtractedResult(BaseModel):
    intencion: str
    tipo_dato: str
    valor_dato: str

@app.post("/extraer", response_model=ExtractedResult)
def extraer(mensaje: PromptInput):
    texto = mensaje.mensaje.lower().strip()

    intencion = "consulta_general"
    tipo_dato = "desconocido"
    valor_dato = "no_detectado"

    if re.search(r"\bfactura(s)?\b", texto):
        intencion = "obtener_facturas"
    elif re.search(r"\bdato(s)?\b|\binformación personal\b", texto):
        intencion = "ver_datos_personales"
    elif re.search(r"\breclamación(es)?\b|\breclamar\b", texto):
        intencion = "consultar_reclamaciones"
    elif re.search(r"\binspección(es)?\b", texto):
        intencion = "consultar_inspecciones"

    dni_match = re.search(r"\b\d{8}[a-zA-Z]\b", mensaje.mensaje)
    if dni_match:
        tipo_dato = "dni"
        valor_dato = dni_match.group()

    return {
        "intencion": intencion,
        "tipo_dato": tipo_dato,
        "valor_dato": valor_dato
    }

# MCP server registration
mcp = FastApiMCP(app)
mcp.mount(path="/mcp")
