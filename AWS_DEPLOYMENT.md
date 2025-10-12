# Deployment en AWS

Este documento describe cómo desplegar la API de Predicción de Demanda en AWS usando diferentes servicios.

## Opción 1: AWS EC2 (Recomendado para empezar)

### Paso 1: Crear instancia EC2

```bash
# Crear instancia EC2 con Amazon Linux 2 o Ubuntu
# Tipo: t2.micro (Free tier) o t2.small
# Configurar Security Group para permitir:
# - SSH (puerto 22)
# - HTTP (puerto 80)
# - Custom TCP (puerto 8000)
```

### Paso 2: Conectar y configurar

```bash
# Conectar via SSH
ssh -i your-key.pem ec2-user@your-instance-ip

# Actualizar sistema
sudo yum update -y  # Amazon Linux
# o
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Instalar Python 3.11
sudo yum install python3.11 -y

# Instalar Git y Docker
sudo yum install git docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user
```

### Paso 3: Desplegar aplicación

```bash
# Clonar repositorio
git clone your-repo-url
cd demand-forecasting-api

# Usando Docker
docker build -t demand-api .
docker run -d -p 8000:8000 --name demand-api demand-api

# O usando Python directamente
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/train_model.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Paso 4: Configurar Nginx (Opcional)

```bash
sudo yum install nginx -y
sudo systemctl start nginx

# Configurar reverse proxy
sudo nano /etc/nginx/conf.d/api.conf
```

Contenido de `api.conf`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Opción 2: AWS Lambda + API Gateway (Serverless)

### Crear función Lambda

1. Crear función Lambda con Python 3.11
2. Empaquetar aplicación:

```bash
# Instalar dependencias en carpeta
pip install -r requirements.txt -t ./lambda_package
cp -r app lambda_package/
cd lambda_package && zip -r ../function.zip .
```

3. Subir ZIP a Lambda
4. Configurar handler: `app.main.handler`
5. Configurar API Gateway para exponer endpoints

### lambda_handler.py (adicional)

```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

## Opción 3: AWS ECS con Fargate

### Crear repositorio ECR

```bash
# Crear repositorio
aws ecr create-repository --repository-name demand-api

# Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

# Build y push
docker build -t demand-api .
docker tag demand-api:latest your-account.dkr.ecr.us-east-1.amazonaws.com/demand-api:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/demand-api:latest
```

### Crear Task Definition y Service en ECS

1. Ir a AWS ECS Console
2. Crear nuevo Task Definition (Fargate)
3. Configurar container con imagen de ECR
4. Crear Service con Load Balancer

## Opción 4: AWS Elastic Beanstalk

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar
eb init -p python-3.11 demand-api

# Crear archivo Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port 8000" > Procfile

# Desplegar
eb create demand-api-env
eb open
```

## Almacenamiento de Modelos en S3

```python
# Guardar modelo en S3
import boto3

s3 = boto3.client('s3')
s3.upload_file('models/demand_model.pkl', 'your-bucket', 'models/demand_model.pkl')

# Cargar modelo desde S3
s3.download_file('your-bucket', 'models/demand_model.pkl', 'models/demand_model.pkl')
```

## Monitoreo con CloudWatch

```python
# Agregar logs a CloudWatch
import logging
import watchtower

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

## Costos Estimados

- **EC2 t2.micro**: Free tier (12 meses) o ~$8/mes
- **Lambda**: Free tier 1M requests/mes, luego $0.20/1M requests
- **ECS Fargate**: ~$15-30/mes (0.25 vCPU, 0.5GB RAM)
- **Elastic Beanstalk**: Free (pagas por recursos usados)

## Seguridad

1. Usar IAM roles apropiados
2. Configurar HTTPS con Certificate Manager
3. Implementar API Key authentication
4. Configurar WAF para protección
5. Habilitar CloudTrail para auditoría

## CI/CD con GitHub Actions

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy to EC2
        run: |
          # Tu script de deployment
```

## Conclusión

Para un proyecto de portfolio, recomiendo:
- **EC2 con Docker**: Más control, fácil de entender
- **Elastic Beanstalk**: Más simple, menos configuración

Para producción real:
- **ECS Fargate**: Escalable, managed
- **Lambda**: Cost-effective para tráfico variable

