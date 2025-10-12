#!/usr/bin/env python3
"""
Script para generar datos de ejemplo para el modelo
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.data_service import DataService


def main():
    print("=" * 60)
    print("Generador de Datos de Entrenamiento")
    print("=" * 60)
    
    data_service = DataService()
    
    # Generar datos
    print("\nGenerando 10,000 registros de datos de ejemplo...")
    df = data_service.generate_sample_data(
        n_samples=10000,
        output_path="data/training_data.csv"
    )
    
    print("\n✓ Datos generados exitosamente!")
    print(f"\nPrimeras 5 filas:")
    print(df.head())
    
    print(f"\nEstadísticas básicas:")
    print(df.describe())
    
    print("\n" + "=" * 60)
    print("Archivo guardado en: data/training_data.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()

