import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLService:
    """Servicio para manejo del modelo de Machine Learning"""
    
    def __init__(self, model_path: str = "models/demand_model.pkl"):
        self.model_path = model_path
        self.model: Optional[GradientBoostingRegressor] = None
        self.scaler: Optional[StandardScaler] = None
        self.feature_names = ['product_id', 'month', 'day_of_week', 'price', 'promotion', 'stock']
        self.last_confidence = 0.0
        
        # Intentar cargar modelo existente
        self._load_model()
        
    def _load_model(self):
        """Carga el modelo desde disco si existe"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                logger.info("Modelo cargado exitosamente")
            else:
                logger.warning("No se encontró modelo pre-entrenado. Entrenar el modelo primero.")
        except Exception as e:
            logger.error(f"Error al cargar modelo: {str(e)}")
            
    def _save_model(self):
        """Guarda el modelo en disco"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            model_data = {
                'model': self.model,
                'scaler': self.scaler
            }
            joblib.dump(model_data, self.model_path)
            logger.info("Modelo guardado exitosamente")
        except Exception as e:
            logger.error(f"Error al guardar modelo: {str(e)}")
            
    def train_model(self, data_path: str = "data/training_data.csv", test_size: float = 0.2) -> Dict[str, float]:
        """
        Entrena el modelo con datos proporcionados
        
        Args:
            data_path: Ruta al archivo CSV con datos de entrenamiento
            test_size: Porcentaje de datos para testing
            
        Returns:
            Diccionario con métricas del modelo
        """
        try:
            # Cargar datos
            logger.info(f"Cargando datos desde {data_path}")
            df = pd.read_csv(data_path)
            
            # Verificar columnas necesarias
            required_columns = self.feature_names + ['demand']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"El dataset debe contener las columnas: {required_columns}")
            
            # Preparar features y target
            X = df[self.feature_names]
            y = df['demand']
            
            # Split train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Escalar features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Entrenar modelo
            logger.info("Entrenando modelo Gradient Boosting...")
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                verbose=0
            )
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluar modelo
            y_pred = self.model.predict(X_test_scaled)
            
            metrics = {
                'r2_score': float(r2_score(y_test, y_pred)),
                'mae': float(mean_absolute_error(y_test, y_pred)),
                'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred))),
                'train_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            logger.info(f"Modelo entrenado. R² Score: {metrics['r2_score']:.4f}")
            
            # Guardar modelo
            self._save_model()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error al entrenar modelo: {str(e)}")
            raise
            
    def predict(self, features: Dict[str, Any]) -> float:
        """
        Realiza una predicción de demanda
        
        Args:
            features: Diccionario con las características del producto
            
        Returns:
            Predicción de demanda
        """
        if self.model is None or self.scaler is None:
            raise ValueError("Modelo no cargado. Entrenar el modelo primero.")
        
        try:
            # Preparar features
            feature_values = [features[name] for name in self.feature_names]
            X = np.array([feature_values])
            
            # Escalar
            X_scaled = self.scaler.transform(X)
            
            # Predecir
            prediction = self.model.predict(X_scaled)[0]
            
            # Calcular confianza (simplificado)
            self.last_confidence = min(0.95, max(0.70, float(self.model.score(X_scaled, [prediction]))))
            
            return float(max(0, prediction))  # Asegurar que no sea negativo
            
        except Exception as e:
            logger.error(f"Error al realizar predicción: {str(e)}")
            raise
            
    def get_confidence_score(self) -> float:
        """Retorna el score de confianza de la última predicción"""
        return self.last_confidence
        
    def is_model_loaded(self) -> bool:
        """Verifica si el modelo está cargado"""
        return self.model is not None and self.scaler is not None
        
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna información sobre el modelo"""
        if self.model is None:
            return {
                "loaded": False,
                "message": "Modelo no cargado"
            }
            
        return {
            "loaded": True,
            "model_type": type(self.model).__name__,
            "features": self.feature_names,
            "n_estimators": getattr(self.model, 'n_estimators', None),
            "learning_rate": getattr(self.model, 'learning_rate', None),
        }

