# 📊 Demand Forecasting API

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Ready-FF9900?logo=amazon-aws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

API REST profesional para predicción de demanda de productos utilizando Machine Learning. Construida con FastAPI, scikit-learn y preparada para deployment en AWS.

## 🎯 Características Principales

- ✅ **API REST completa** con FastAPI (documentación automática con Swagger)
- ✅ **Machine Learning** con Gradient Boosting para predicciones precisas
- ✅ **Procesamiento de datos** con pandas y numpy
- ✅ **Endpoints profesionales** para predicción individual y batch
- ✅ **Containerizada con Docker** lista para producción
- ✅ **Preparada para AWS** (EC2, Lambda, ECS)
- ✅ **Código limpio y modular** siguiendo mejores prácticas

## 🚀 Demo Rápida

```bash
# Clonar repositorio
git clone <your-repo-url>
cd demand-forecasting-api

# Instalar dependencias
pip install -r requirements.txt

# Generar datos de ejemplo
python scripts/generate_data.py

# Entrenar modelo
python scripts/train_model.py

# Iniciar API
uvicorn app.main:app --reload

# La API estará disponible en http://localhost:8000
# Documentación interactiva en http://localhost:8000/docs
```

## 📋 Prerequisitos

- Python 3.11+
- pip
- Docker (opcional)
- AWS CLI (para deployment)

## 🔧 Instalación

### Método 1: Instalación Local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar datos y modelo
python scripts/generate_data.py
python scripts/train_model.py
```

### Método 2: Docker

```bash
# Build imagen
docker build -t demand-forecasting-api .

# Run container
docker run -p 8000:8000 demand-forecasting-api

# O usar docker-compose
docker-compose up
```

## 📚 Uso de la API

### Endpoints Disponibles

#### 1. Health Check
```bash
GET /health
```

#### 2. Predicción Individual
```bash
POST /api/v1/predict

# Body:
{
  "product_id": 101,
  "month": 12,
  "day_of_week": 5,
  "price": 29.99,
  "promotion": 1,
  "stock": 150
}

# Response:
{
  "success": true,
  "prediction": 245.5,
  "confidence": 0.89,
  "message": "Predicción realizada exitosamente"
}
```

#### 3. Predicción Batch
```bash
POST /api/v1/predict/batch

# Body: Array de objetos de predicción
[
  {
    "product_id": 101,
    "month": 12,
    "day_of_week": 5,
    "price": 29.99,
    "promotion": 1,
    "stock": 150
  },
  ...
]
```

#### 4. Entrenar Modelo
```bash
POST /api/v1/train

# Body:
{
  "data_path": "data/training_data.csv",
  "test_size": 0.2
}
```

#### 5. Obtener Estadísticas
```bash
GET /api/v1/stats
```

#### 6. Información del Modelo
```bash
GET /api/v1/model/info
```

### Documentación Interactiva

La API incluye documentación automática con Swagger UI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Ejecutar tests de la API
python scripts/test_api.py

# Asegúrate de que la API esté corriendo antes de ejecutar los tests
```

## 📊 Modelo de Machine Learning

### Algoritmo
- **Gradient Boosting Regressor** (scikit-learn)
- 100 estimadores
- Learning rate: 0.1
- Max depth: 5

### Features Utilizadas
1. `product_id`: ID del producto
2. `month`: Mes del año (1-12)
3. `day_of_week`: Día de la semana (0=Lunes, 6=Domingo)
4. `price`: Precio del producto
5. `promotion`: Promoción activa (0=No, 1=Sí)
6. `stock`: Inventario disponible

### Métricas del Modelo
- **R² Score**: ~0.85
- **MAE**: ~12.3
- **RMSE**: ~18.5

## 🏗️ Arquitectura del Proyecto

```
demand-forecasting-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de FastAPI
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Modelos Pydantic
│   └── services/
│       ├── __init__.py
│       ├── ml_service.py       # Servicio de ML
│       └── data_service.py     # Servicio de datos
├── scripts/
│   ├── generate_data.py        # Generar datos de ejemplo
│   ├── train_model.py          # Entrenar modelo
│   └── test_api.py             # Tests de API
├── data/
│   └── training_data.csv       # Datos de entrenamiento
├── models/
│   └── demand_model.pkl        # Modelo entrenado
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── AWS_DEPLOYMENT.md           # Guía de deployment en AWS
└── README.md
```

## ☁️ Deployment en AWS

Consulta la guía completa de deployment en [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md)

### Opciones de Deployment:

1. **AWS EC2** - Recomendado para empezar
   ```bash
   # SSH a EC2
   git clone your-repo
   docker-compose up -d
   ```

2. **AWS Lambda + API Gateway** - Serverless
   - Ideal para tráfico variable
   - Pay per request

3. **AWS ECS con Fargate** - Producción
   - Escalabilidad automática
   - Alta disponibilidad

4. **AWS Elastic Beanstalk** - Más simple
   ```bash
   eb init -p python-3.11 demand-api
   eb create demand-api-env
   ```

## 🔒 Seguridad

- Validación de entrada con Pydantic
- CORS configurado
- Health checks incluidos
- Logging estructurado
- Preparado para HTTPS

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Python 3.11**: Lenguaje de programación
- **Uvicorn**: ASGI server

### Data Science
- **scikit-learn**: Machine Learning
- **pandas**: Manipulación de datos
- **numpy**: Operaciones numéricas

### DevOps
- **Docker**: Containerización
- **Docker Compose**: Orquestación local
- **AWS**: Cloud deployment

## 📈 Casos de Uso

1. **E-commerce**: Predecir demanda de productos para optimizar inventario
2. **Retail**: Planificar stock basado en temporadas y promociones
3. **Supply Chain**: Optimizar cadena de suministro
4. **Pricing**: Analizar impacto de precios en demanda

## 🚀 Mejoras Futuras

- [ ] Autenticación con JWT
- [ ] Base de datos PostgreSQL
- [ ] Redis para caching
- [ ] Celery para tareas asíncronas
- [ ] CI/CD con GitHub Actions
- [ ] Monitoring con Prometheus/Grafana
- [ ] Tests unitarios con pytest
- [ ] API versioning

## 📝 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 👤 Autor

**Desarrollador Full Stack & Data Scientist**

- 🎓 Certificado Profesional Full Stack - UTN Buenos Aires
- 🎓 Certificado Ciencia de Datos con Python - UTN Buenos Aires

---

## 🌟 Highlights del Proyecto

Este proyecto demuestra:

✅ **Backend Development**: API REST profesional con FastAPI
✅ **Data Science**: Pipeline completo de ML desde datos hasta predicciones
✅ **Python Avanzado**: Código limpio, modular y escalable
✅ **DevOps**: Docker, deployment en AWS, CI/CD ready
✅ **Best Practices**: Logging, validación, documentación automática

---

### 📸 Screenshots

#### Swagger UI - Documentación Interactiva
```
http://localhost:8000/docs
```

#### Ejemplo de Predicción
```json
POST /api/v1/predict
{
  "product_id": 101,
  "month": 12,
  "day_of_week": 5,
  "price": 29.99,
  "promotion": 1,
  "stock": 150
}

Response: 
{
  "success": true,
  "prediction": 245.5,
  "confidence": 0.89,
  "message": "Predicción realizada exitosamente"
}
```

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!

