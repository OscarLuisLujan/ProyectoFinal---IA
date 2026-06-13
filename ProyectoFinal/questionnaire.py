# questionnaire.py
# Cuestionario técnico estandarizado

from config import CATEGORIAS_CUESTIONARIO

class CuestionarioTecnico:
    """Cuestionario para recolección de datos en campo"""
    
    DESCRIPCIONES = {
        "RN1_antiguedad": "Años desde construcción (0-100)",
        "RN2_numero_pisos": "Número de pisos (1-30)",
        "RN3_tipo_construccion": "1=Vivienda, 2=Edificio, 3=Comercial, 4=Industrial, 5=Otro",
        "RN4_estado_conservacion": "1=Muy bueno, 2=Bueno, 3=Regular, 4=Malo, 5=Muy malo",
        "RN5_tamano_grietas": "0=Ninguna, 1=Leve, 2=Moderada, 3=Severa",
        "RN6_cantidad_grietas": "0=Ninguna, 1=Pocas, 2=Varias, 3=Muchas",
        "RN7_evolucion_grietas": "0=No crecen, 1=Crecimiento leve, 2=Moderado, 3=Acelerado",
        "RN8_inclinacion_muros": "0=Nula, 1=Leve, 2=Moderada, 3=Alta",
        "RN9_hundimientos": "0=Ninguno, 1=Leve, 2=Moderado, 3=Grave",
        "RN10_estado_columnas": "0=Sin daño, 1=Leve, 2=Moderado, 3=Grave",
        "RN11_filtraciones": "0=Ninguna, 1=Leve, 2=Moderada, 3=Alta",
        "RN12_humedad_visible": "0=Ninguna, 1=Leve, 2=Moderada, 3=Alta",
        "RN13_acumulacion_agua": "0=Nunca, 1=Ocasional, 2=Frecuente, 3=Permanente",
        "RN14_estado_drenaje": "0=Excelente, 1=Bueno, 2=Regular, 3=Deficiente",
        "RN15_ubicacion_ladera": "0=No, 1=Sí",
        "RN16_pendiente_terreno": "0=Baja, 1=Media, 2=Alta, 3=Muy alta",
        "RN17_erosion_visible": "0=Ninguna, 1=Leve, 2=Moderada, 3=Grave",
        "RN18_historial_deslizamientos": "0=Nunca, 1=Hace años, 2=Último año, 3=Reciente",
        "RN19_excavaciones_cercanas": "0=Ninguna, 1=Leve, 2=Moderada, 3=Intensa",
        "RN20_movimiento_tierras": "0=Ninguno, 1=Leve, 2=Moderado, 3=Alto",
        "RN21_distancia_construcciones": "Distancia en metros (0-20)",
        "RN22_densidad_edificaciones": "1=Baja, 2=Media, 3=Alta",
        "RN23_denuncias_previas": "Número de denuncias previas (0-50)",
        "RN24_observaciones_municipales": "Observaciones municipales previas (0-20)",
        "RN25_reparaciones_realizadas": "0=Ninguna, 1=Menor, 2=Parcial, 3=Mayor",
        "RN26_grietas_IA": "0=Ninguna, 1=Leve, 2=Moderada, 3=Severa",
        "RN27_humedad_IA": "0=Ninguna, 1=Leve, 2=Moderada, 3=Alta",
        "RN28_deformacion_IA": "0=Nula, 1=Leve, 2=Moderada, 3=Grave"
    }
    
    @staticmethod
    def mostrar():
        """Muestra el cuestionario completo"""
        print("\n" + "="*80)
        print("CUESTIONARIO TÉCNICO ESTANDARIZADO - MATRIZ DE RIESGO URBANO")
        print("Municipio de La Paz - Gobierno Autónomo Municipal")
        print("="*80)
        
        for categoria, variables in CATEGORIAS_CUESTIONARIO.items():
            print(f"\n📌 {categoria.upper()}:")
            for var in variables:
                desc = CuestionarioTecnico.DESCRIPCIONES.get(var, var)
                print(f"   • {var}: {desc}")
    
    @staticmethod
    def recoger_datos():
        """Recoge datos del usuario en consola"""
        datos = {}
        
        print("\n" + "="*80)
        print("🔮 INGRESO DE DATOS - INSPECCIÓN DE OBRA")
        print("="*80)
        
        for categoria, variables in CATEGORIAS_CUESTIONARIO.items():
            print(f"\n🏠 {categoria.upper()}:")
            for var in variables:
                desc = CuestionarioTecnico.DESCRIPCIONES.get(var, var)
                while True:
                    try:
                        valor = float(input(f"  {var} - {desc}: "))
                        datos[var] = valor
                        break
                    except ValueError:
                        print("  ❌ Ingrese un valor numérico válido")
        
        return datos