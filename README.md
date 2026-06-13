

# Sistema Inteligente de Priorización de Inspecciones de Obras Urbanas (GAMLP)

Este repositorio contiene un sistema inteligente diseñado para el **Gobierno Autónomo Municipal de La Paz (GAMLP)**. Su objetivo principal es optimizar, automatizar y priorizar las inspecciones de construcciones civiles mediante el uso de **Redes Neuronales Artificiales (RNA)** y **Visión Artificial**.

---
## Grupo
* Choque Mamani Rosa Carolina
* Torrez Limachi Ester Sarai
* Lujan Nacho Oscar Luis
---
## Características Principales

*   **Evaluación Multivariable:** Procesamiento de 28 variables técnicas estructuradas para el cálculo del índice de riesgo estructural ($RN_{29}$) sobre 100 puntos.
*   **Core de Inteligencia Artificial:** Dos redes neuronales tipo Perceptrón Multicapa (MLP); una para la clasificación del riesgo (Precisión > 97%) y otra para la regresión del índice matemático (MAE < 2%).
*   **Visión Artificial Integrada:** Módulo basado en OpenCV (Detección de bordes Canny y Transformada de Hough) para la detección automática de grietas, humedad y deformaciones mediante fotografías.
*   **Interfaz Web Moderna:** Dashboard responsivo construido en Flask (Backend) y HTML/CSS/JS (Frontend) con soporte para carga de archivos por arrastre (*Drag & Drop*) y visualizaciones dinámicas.

---

## Arquitectura del Sistema

El flujo de información se procesa a través de una estructura jerárquica que elimina el sesgo subjetivo del inspector en campo:

```mermaid
---
config:
  theme: mc
  layout: fixed
---
flowchart LR
    subgraph Entrada [Capa de Entrada: 28 Variables]
        X1["Formulario Web"]
        X2["Fotografía de Fachada (OpenCV)"]
    end

    subgraph Procesamiento [Modelos MLP]
        H1(("Red de Clasificación\n(Precisión > 97%)"))
        H2(("Red de Regresión\n(MAE < 2 puntos)"))
    end

    subgraph Salida [Diagnóstico Automatizado]
        Y1[["Nivel de Riesgo\n(BAJO, MEDIO, ALTO, CRÍTICO)"]]
        Y2[["Prioridad de Inspección\n(Escala 0 al 10)"]]
    end

    X1 --> H1 & H2
    X2 --> H1 & H2
    H1 --> Y1
    H2 --> Y2

    style Y1 fill:#FFFEBEE,stroke:#FF1744,stroke-width:2px
    style Y2 fill:#FFFEBEE,stroke:#FF1744,stroke-width:2px
