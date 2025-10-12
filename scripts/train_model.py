#!/usr/bin/env python3
"""
Script para entrenar el modelo de Machine Learning
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ml_service import MLService


def main():
    print("=" * 60)
    print("Entrenamiento del Modelo de Predicción de Demanda")
    print("=" * 60)
    
    ml_service = MLService()
    
    # Entrenar modelo
    print("\nEntrenando modelo con datos de training_data.csv...")
    print("Esto puede tomar algunos segundos...\n")
    
    metrics = ml_service.train_model(
        data_path="data/training_data.csv",
        test_size=0.2
    )
    
    print("\n✓ Modelo entrenado exitosamente!")
    print("\nMétricas del modelo:")
    print(f"  R² Score:         {metrics['r2_score']:.4f}")
    print(f"  MAE:              {metrics['mae']:.2f}")
    print(f"  RMSE:             {metrics['rmse']:.2f}")
    print(f"  Muestras train:   {metrics['train_samples']}")
    print(f"  Muestras test:    {metrics['test_samples']}")
    
    print("\n" + "=" * 60)
    print("Modelo guardado en: models/demand_model.pkl")
    print("=" * 60)


if __name__ == "__main__":
    main()

