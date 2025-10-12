# 🚀 Inicio Rápido - Demand Forecasting API

Guía ultra rápida para tener tu proyecto funcionando en 5 minutos.

## ⚡ Pasos Rápidos

### 1. Instalar dependencias (1 min)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Generar datos y entrenar modelo (2 min)

```bash
# Generar 10,000 registros de datos de ejemplo
python scripts/generate_data.py

# Entrenar el modelo de ML
python scripts/train_model.py
```

### 3. Iniciar la API (1 min)

```bash
# Iniciar servidor
python -m uvicorn app.main:app --reload

# O directamente:
python app/main.py
```

### 4. Probar la API (1 min)

Abre tu navegador en: **http://localhost:8000/docs**

O prueba con curl:

```bash
# Health check
curl http://localhost:8000/health

# Hacer una predicción
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 101,
    "month": 12,
    "day_of_week": 5,
    "price": 29.99,
    "promotion": 1,
    "stock": 150
  }'
```

O ejecuta el script de prueba:

```bash
python scripts/test_api.py
```

## 🐳 Método Alternativo: Docker

Si tienes Docker instalado:

```bash
# Build y run en un solo paso
docker-compose up

# La API estará en http://localhost:8000
```

## 📊 Verificar funcionamiento

1. **Abrir**: http://localhost:8000/docs
2. **Explorar** la interfaz Swagger interactiva
3. **Probar** el endpoint `/api/v1/predict`

## 🆘 Troubleshooting

### Error: "No module named 'app'"

```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd api-rest
python -m uvicorn app.main:app --reload
```

### Error: "Model not found"

```bash
# Genera datos y entrena el modelo primero
python scripts/generate_data.py
python scripts/train_model.py
```

### Puerto 8000 ocupado

```bash
# Usa otro puerto
uvicorn app.main:app --reload --port 8001
```

## 🚀 Próximos Pasos

1. **Deploy a AWS** (ver AWS_DEPLOYMENT.md)
2. **Agregar tests** con pytest
3. **Implementar CI/CD** con GitHub Actions
4. **Agregar autenticación** JWT
5. **Crear dashboard** con Streamlit

---

**¿Preguntas?** Consulta el README.md completo o la documentación automática en /docs

