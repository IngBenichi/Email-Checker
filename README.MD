# 📧 API de Validación de Correos Electrónicos con FastAPI

Esta API permite validar direcciones de correo electrónico mediante varios criterios:

✅ **Verifica si el formato del correo es correcto.**
✅ **Detecta si el correo es de un servicio temporal (desechable).**
✅ **Valida la existencia del correo a través de consultas SMTP.**

---

## 🚀 Instalación y Ejecución

### 🔹 1️⃣ Requisitos

Asegúrate de tener instalado **Python 3.12.6** y los siguientes paquetes:

```bash
pip install fastapi uvicorn validate_email_address dnspython smtplib
```

### 🔹 2️⃣ Ejecutar la API

Guarda el siguiente código en `main.py` y ejecuta:

```bash
uvicorn main:app --reload
```

---

## 📜 Endpoints

### 🔹 **POST /validate-email/**

Valida un correo electrónico basado en su formato, si es temporal y su existencia mediante SMTP.

📌 **Ejemplo de solicitud:**
```json
{
  "email": "test@example.com"
}
```

📌 **Ejemplo de respuesta si el correo es válido:**
```json
{
  "email": "test@example.com",
  "valid_format": true,
  "valid_format_message": "Formato correcto y dominio válido.",
  "disposable": false,
  "disposable_message": "Correo no es temporal.",
  "smtp_valid": true,
  "smtp_message": "Correo válido en el servidor SMTP."
}
```

📌 **Ejemplo de respuesta si el correo es inválido:**
```json
{
  "email": "correo@dominioinvalido.com",
  "valid_format": false,
  "valid_format_message": "Formato inválido o dominio inexistente.",
  "disposable": false,
  "disposable_message": "Correo no es temporal.",
  "smtp_valid": false,
  "smtp_message": "El dominio del correo no existe."
}
```

---

## 🛠 Funcionalidades y Explicación del Código

1️⃣ **Verificación de formato y existencia de dominio:**
   - Se usa `validate_email_address` para validar el formato y los registros DNS.

2️⃣ **Detección de correos temporales:**
   - Se compara el dominio con una lista de correos desechables.

3️⃣ **Verificación mediante SMTP:**
   - Se conecta al servidor de correo y verifica si la dirección existe.

---

## ⚠️ Consideraciones

🔹 Algunos servidores pueden bloquear peticiones SMTP, por lo que la validación puede fallar.
🔹 Es recomendable usar una API de pago si necesitas validaciones en tiempo real y con mayor precisión.
🔹 Se puede agregar una base de datos para almacenar resultados y evitar validaciones repetidas.

---

## 📌 Mejoras Futuras

🚀 **Integrar detección de correos maliciosos con una API externa.**
🚀 **Implementar límites de uso para evitar abuso del servicio.**
🚀 **Agregar soporte para almacenamiento de resultados en una base de datos.**

---

## ✨ Autor

🔹 **Desarrollado por:** Camilo Benítez
🔹 **Contacto:** [Tu Email o LinkedIn]

