from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from validate_email_address import validate_email
from disposable_email_domains import blocklist
import smtplib
import dns.resolver
import requests

app = FastAPI()

# Modelo para recibir el email
class EmailRequest(BaseModel):
    email: str

# 1️⃣ Verificar si el email es temporal
def is_disposable_email(email: str) -> bool:
    domain = email.split("@")[-1]
    return domain in blocklist

# 2️⃣ Validar existencia del correo mediante SMTP
def verify_smtp(email: str) -> tuple:
    domain = email.split("@")[-1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)
        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)
        server.helo()
        server.mail("test@example.com")
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250, "Correo válido en el servidor SMTP."
    except dns.resolver.NoAnswer:
        return False, "El dominio no tiene registros MX."
    except dns.resolver.NXDOMAIN:
        return False, "El dominio del correo no existe."
    except smtplib.SMTPConnectError:
        return False, "No se pudo conectar al servidor SMTP."
    except Exception:
        return False, "Error desconocido en la validación SMTP."

# Endpoint principal
@app.post("/validate-email/")
async def validate_email_endpoint(request: EmailRequest):
    try:
        is_valid_format = validate_email(request.email, check_format=True, check_dns=True)
        is_disposable = is_disposable_email(request.email)
        smtp_valid, smtp_message = verify_smtp(request.email)

        return {
            "email": request.email,
            "valid_format": is_valid_format,
            "valid_format_message": "Formato correcto y dominio válido." if is_valid_format else "Formato inválido o dominio inexistente.",
            "disposable": is_disposable,
            "disposable_message": "Correo de un servicio temporal." if is_disposable else "Correo no es temporal.",
            "smtp_valid": smtp_valid,
            "smtp_message": smtp_message
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
