from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn

from app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    TrainingRequest,
    TrainingResponse,
    HealthResponse,
    StatsResponse
)
from app.services.ml_service import MLService
from app.services.data_service import DataService

# Initialize FastAPI app
app = FastAPI(
    title="Demand Forecasting API",
    description="API REST para predicción de demanda usando Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ml_service = MLService()
data_service = DataService()


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Demand Forecasting API is running",
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    model_loaded = ml_service.is_model_loaded()
    return {
        "status": "healthy" if model_loaded else "degraded",
        "message": "Model loaded" if model_loaded else "Model not loaded",
        "version": "1.0.0"
    }


@app.post("/api/v1/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
async def predict_demand(request: PredictionRequest):
    """
    Predice la demanda basándose en las características proporcionadas
    
    - **product_id**: ID del producto
    - **month**: Mes (1-12)
    - **day_of_week**: Día de la semana (0-6)
    - **price**: Precio del producto
    - **promotion**: Si hay promoción activa (0 o 1)
    - **stock**: Stock disponible
    """
    try:
        prediction = ml_service.predict(request.dict())
        
        return {
            "success": True,
            "prediction": prediction,
            "confidence": ml_service.get_confidence_score(),
            "message": "Predicción realizada exitosamente"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar predicción: {str(e)}"
        )


@app.post("/api/v1/predict/batch", response_model=List[PredictionResponse])
async def predict_demand_batch(requests: List[PredictionRequest]):
    """
    Realiza predicciones en batch para múltiples entradas
    """
    try:
        results = []
        for request in requests:
            prediction = ml_service.predict(request.dict())
            results.append({
                "success": True,
                "prediction": prediction,
                "confidence": ml_service.get_confidence_score(),
                "message": "Predicción realizada exitosamente"
            })
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar predicciones batch: {str(e)}"
        )


@app.post("/api/v1/train", response_model=TrainingResponse, status_code=status.HTTP_200_OK)
async def train_model(request: TrainingRequest):
    """
    Entrena o re-entrena el modelo con nuevos datos
    
    - **data_path**: Ruta al archivo CSV con datos de entrenamiento
    - **test_size**: Porcentaje de datos para testing (0.0-1.0)
    """
    try:
        metrics = ml_service.train_model(
            data_path=request.data_path,
            test_size=request.test_size
        )
        
        return {
            "success": True,
            "message": "Modelo entrenado exitosamente",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al entrenar modelo: {str(e)}"
        )


@app.get("/api/v1/stats", response_model=StatsResponse)
async def get_statistics():
    """
    Obtiene estadísticas del modelo y datos procesados
    """
    try:
        stats = data_service.get_statistics()
        return {
            "success": True,
            "statistics": stats,
            "message": "Estadísticas obtenidas exitosamente"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


@app.get("/api/v1/model/info")
async def get_model_info():
    """
    Obtiene información sobre el modelo actual
    """
    try:
        info = ml_service.get_model_info()
        return {
            "success": True,
            "model_info": info,
            "message": "Información del modelo obtenida exitosamente"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener información del modelo: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

