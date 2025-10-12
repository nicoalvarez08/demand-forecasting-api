from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List


class PredictionRequest(BaseModel):
    """Schema para solicitud de predicción"""
    product_id: int = Field(..., description="ID del producto", ge=1)
    month: int = Field(..., description="Mes del año", ge=1, le=12)
    day_of_week: int = Field(..., description="Día de la semana (0=Lunes, 6=Domingo)", ge=0, le=6)
    price: float = Field(..., description="Precio del producto", gt=0)
    promotion: int = Field(..., description="Promoción activa (0=No, 1=Sí)", ge=0, le=1)
    stock: int = Field(..., description="Stock disponible", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 101,
                "month": 12,
                "day_of_week": 5,
                "price": 29.99,
                "promotion": 1,
                "stock": 150
            }
        }


class PredictionResponse(BaseModel):
    """Schema para respuesta de predicción"""
    success: bool
    prediction: float = Field(..., description="Demanda predicha")
    confidence: Optional[float] = Field(None, description="Nivel de confianza del modelo")
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": 245.5,
                "confidence": 0.89,
                "message": "Predicción realizada exitosamente"
            }
        }


class TrainingRequest(BaseModel):
    """Schema para solicitud de entrenamiento"""
    data_path: str = Field(default="data/training_data.csv", description="Ruta al archivo de datos")
    test_size: float = Field(default=0.2, description="Porcentaje de datos para testing", ge=0.1, le=0.5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "data_path": "data/training_data.csv",
                "test_size": 0.2
            }
        }


class TrainingResponse(BaseModel):
    """Schema para respuesta de entrenamiento"""
    success: bool
    message: str
    metrics: Dict[str, float] = Field(..., description="Métricas del modelo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Modelo entrenado exitosamente",
                "metrics": {
                    "r2_score": 0.85,
                    "mae": 12.3,
                    "rmse": 18.5
                }
            }
        }


class HealthResponse(BaseModel):
    """Schema para health check"""
    status: str
    message: str
    version: str


class StatsResponse(BaseModel):
    """Schema para respuesta de estadísticas"""
    success: bool
    statistics: Dict[str, Any]
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "statistics": {
                    "total_records": 10000,
                    "avg_demand": 180.5,
                    "max_demand": 500,
                    "min_demand": 10
                },
                "message": "Estadísticas obtenidas exitosamente"
            }
        }

