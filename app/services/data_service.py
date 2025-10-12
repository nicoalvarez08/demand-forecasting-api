import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataService:
    """Servicio para procesamiento y análisis de datos"""
    
    def __init__(self):
        self.data: pd.DataFrame = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV
        
        Args:
            file_path: Ruta al archivo CSV
            
        Returns:
            DataFrame con los datos cargados
        """
        try:
            logger.info(f"Cargando datos desde {file_path}")
            self.data = pd.read_csv(file_path)
            logger.info(f"Datos cargados: {len(self.data)} registros")
            return self.data
        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise
            
    def generate_sample_data(self, n_samples: int = 10000, output_path: str = "data/training_data.csv") -> pd.DataFrame:
        """
        Genera datos de ejemplo para entrenamiento
        
        Args:
            n_samples: Número de muestras a generar
            output_path: Ruta donde guardar el CSV
            
        Returns:
            DataFrame con datos generados
        """
        np.random.seed(42)
        
        logger.info(f"Generando {n_samples} muestras de datos...")
        
        # Generar features
        data = {
            'product_id': np.random.randint(100, 200, n_samples),
            'month': np.random.randint(1, 13, n_samples),
            'day_of_week': np.random.randint(0, 7, n_samples),
            'price': np.random.uniform(10, 100, n_samples).round(2),
            'promotion': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'stock': np.random.randint(50, 500, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generar demanda basada en features (con relaciones lógicas)
        base_demand = 100
        
        # La demanda aumenta con promociones
        promotion_effect = df['promotion'] * 50
        
        # La demanda disminuye con precio alto
        price_effect = -0.5 * df['price']
        
        # La demanda es mayor en fin de semana
        weekend_effect = np.where(df['day_of_week'].isin([5, 6]), 30, 0)
        
        # La demanda es mayor en diciembre (temporada)
        season_effect = np.where(df['month'] == 12, 50, 0)
        
        # Stock bajo puede limitar la demanda
        stock_effect = np.minimum(df['stock'] * 0.3, 50)
        
        # Calcular demanda con algo de ruido
        df['demand'] = (
            base_demand + 
            promotion_effect + 
            price_effect + 
            weekend_effect + 
            season_effect + 
            stock_effect + 
            np.random.normal(0, 15, n_samples)
        )
        
        # Asegurar que la demanda sea positiva
        df['demand'] = df['demand'].clip(lower=10).round(0).astype(int)
        
        # Guardar datos
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Datos guardados en {output_path}")
        
        self.data = df
        return df
        
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcula estadísticas sobre los datos
        
        Returns:
            Diccionario con estadísticas
        """
        if self.data is None or len(self.data) == 0:
            # Intentar cargar datos de ejemplo
            try:
                self.load_data("data/training_data.csv")
            except:
                return {
                    "message": "No hay datos disponibles",
                    "total_records": 0
                }
        
        stats = {
            "total_records": len(self.data),
            "features": list(self.data.columns),
        }
        
        # Estadísticas de demanda si existe
        if 'demand' in self.data.columns:
            stats["demand"] = {
                "mean": float(self.data['demand'].mean()),
                "median": float(self.data['demand'].median()),
                "std": float(self.data['demand'].std()),
                "min": float(self.data['demand'].min()),
                "max": float(self.data['demand'].max()),
            }
            
        # Estadísticas de precio si existe
        if 'price' in self.data.columns:
            stats["price"] = {
                "mean": float(self.data['price'].mean()),
                "min": float(self.data['price'].min()),
                "max": float(self.data['price'].max()),
            }
            
        # Conteo de promociones
        if 'promotion' in self.data.columns:
            stats["promotions"] = {
                "active": int(self.data['promotion'].sum()),
                "percentage": float(self.data['promotion'].mean() * 100)
            }
            
        return stats
        
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesa datos para el modelo
        
        Args:
            df: DataFrame a preprocesar
            
        Returns:
            DataFrame preprocesado
        """
        logger.info("Preprocesando datos...")
        
        # Crear copia
        df_processed = df.copy()
        
        # Eliminar duplicados
        df_processed = df_processed.drop_duplicates()
        
        # Manejar valores nulos (si existen)
        df_processed = df_processed.fillna(df_processed.mean(numeric_only=True))
        
        # Eliminar outliers extremos (opcional)
        if 'demand' in df_processed.columns:
            q1 = df_processed['demand'].quantile(0.01)
            q99 = df_processed['demand'].quantile(0.99)
            df_processed = df_processed[
                (df_processed['demand'] >= q1) & 
                (df_processed['demand'] <= q99)
            ]
        
        logger.info(f"Datos preprocesados: {len(df_processed)} registros")
        
        return df_processed

