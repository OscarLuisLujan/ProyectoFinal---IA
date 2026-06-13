import sys

html_file = 'ProyectoFinal/templates/index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Buscar el inicio del form y el fin
match = re.search(r'<form id="evaluation-form".*?</form>', content, flags=re.DOTALL)

if match:
    new_form = """<form id="evaluation-form" class="evaluation-form single-page-form">
                    <!-- SECCIÓN: INFORMACIÓN GENERAL -->
                    <div class="form-section-block">
                        <h3 class="block-title">Información General de la Edificación</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="RN1_antiguedad">Antigüedad</label>
                                <select id="RN1_antiguedad" name="RN1_antiguedad" required>
                                    <option value="0">0 - 5 años</option>
                                    <option value="1">6 - 15 años</option>
                                    <option value="2">16 - 30 años</option>
                                    <option value="3">31 - 50 años</option>
                                    <option value="4">Más de 50 años</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN2_numero_pisos">Número de pisos</label>
                                <select id="RN2_numero_pisos" name="RN2_numero_pisos" required>
                                    <option value="0">1 piso</option>
                                    <option value="1">2 - 3 pisos</option>
                                    <option value="2">4 - 5 pisos</option>
                                    <option value="3">6 - 8 pisos</option>
                                    <option value="4">Más de 8 pisos</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN3_tipo_construccion">Tipo de construcción</label>
                                <select id="RN3_tipo_construccion" name="RN3_tipo_construccion" required>
                                    <option value="0">Vivienda</option>
                                    <option value="1">Edificio</option>
                                    <option value="2">Comercial</option>
                                    <option value="3">Industrial</option>
                                    <option value="4">Otro</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN4_estado_conservacion">Estado de conservación</label>
                                <select id="RN4_estado_conservacion" name="RN4_estado_conservacion" required>
                                    <option value="0">Muy Bueno</option>
                                    <option value="1">Bueno</option>
                                    <option value="2">Regular</option>
                                    <option value="3">Malo</option>
                                    <option value="4">Muy Malo</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- SECCIÓN: ESTRUCTURAL -->
                    <div class="form-section-block">
                        <h3 class="block-title">Estado Estructural y Fisuras</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="RN5_tamano_grietas">Tamaño de grietas</label>
                                <select id="RN5_tamano_grietas" name="RN5_tamano_grietas" required>
                                    <option value="0">0 mm</option>
                                    <option value="1">&lt; 1 mm</option>
                                    <option value="2">1 mm - 2 mm</option>
                                    <option value="3">3 mm - 5 mm</option>
                                    <option value="4">6 mm - 10 mm</option>
                                    <option value="5">&gt; 10 mm</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN6_cantidad_grietas">Cantidad de grietas</label>
                                <select id="RN6_cantidad_grietas" name="RN6_cantidad_grietas" required>
                                    <option value="0">0</option>
                                    <option value="1">1 - 2</option>
                                    <option value="2">3 - 5</option>
                                    <option value="3">6 - 10</option>
                                    <option value="4">&gt; 10</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN7_evolucion_grietas">Evolución de grietas</label>
                                <select id="RN7_evolucion_grietas" name="RN7_evolucion_grietas" required>
                                    <option value="0">Inactivas</option>
                                    <option value="1">Crecimiento anual</option>
                                    <option value="2">Crecimiento semestral</option>
                                    <option value="3">Crecimiento mensual</option>
                                    <option value="4">Crecimiento semanal</option>
                                    <option value="5">Crecimiento diario</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN8_inclinacion_muros">Inclinación de muros</label>
                                <select id="RN8_inclinacion_muros" name="RN8_inclinacion_muros" required>
                                    <option value="0">0°</option>
                                    <option value="1">&lt; 1°</option>
                                    <option value="2">1° - 2°</option>
                                    <option value="3">2° - 3°</option>
                                    <option value="4">3° - 4°</option>
                                    <option value="5">4° - 5°</option>
                                    <option value="6">&gt; 5°</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN9_hundimientos">Hundimientos</label>
                                <select id="RN9_hundimientos" name="RN9_hundimientos" required>
                                    <option value="0">Ninguno</option>
                                    <option value="1">Leve</option>
                                    <option value="2">Moderado</option>
                                    <option value="3">Severo</option>
                                    <option value="4">Crítico</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN10_estado_columnas">Estado de columnas/vigas</label>
                                <select id="RN10_estado_columnas" name="RN10_estado_columnas" required>
                                    <option value="0">Óptimo</option>
                                    <option value="1">Daños estéticos</option>
                                    <option value="2">Daño moderado</option>
                                    <option value="3">Daño severo</option>
                                    <option value="4">Falla crítica</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- SECCIÓN: HUMEDAD -->
                    <div class="form-section-block">
                        <h3 class="block-title">Humedad y Drenaje</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="RN11_filtraciones">Filtraciones</label>
                                <select id="RN11_filtraciones" name="RN11_filtraciones" required>
                                    <option value="0">Ausente</option>
                                    <option value="1">Sudoración esporádica</option>
                                    <option value="2">Exudación pluvial</option>
                                    <option value="3">Goteo intermitente</option>
                                    <option value="4">Flujo continuo</option>
                                    <option value="5">Sifonamiento</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN12_humedad_visible">Humedad visible</label>
                                <select id="RN12_humedad_visible" name="RN12_humedad_visible" required>
                                    <option value="0">Seco</option>
                                    <option value="1">Leve (&lt; 10%)</option>
                                    <option value="2">Moderada (10% - 30%)</option>
                                    <option value="3">Severa (&gt; 30%)</option>
                                    <option value="4">Crítica / Criptoflorescencia</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN13_acumulacion_agua">Acumulación de agua cercana</label>
                                <select id="RN13_acumulacion_agua" name="RN13_acumulacion_agua" required>
                                    <option value="0">Sin acumulación</option>
                                    <option value="1">Muy distante (&gt; 30 m)</option>
                                    <option value="2">Distante (15 m - 30 m)</option>
                                    <option value="3">Media (5 m - 15 m)</option>
                                    <option value="4">Cercana (1 m - 5 m)</option>
                                    <option value="5">Contacto directo (&lt; 1 m)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN14_estado_drenaje">Estado drenaje pluvial</label>
                                <select id="RN14_estado_drenaje" name="RN14_estado_drenaje" required>
                                    <option value="0">Excelente</option>
                                    <option value="1">Bueno</option>
                                    <option value="2">Regular</option>
                                    <option value="3">Malo</option>
                                    <option value="4">Inexistente</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- SECCIÓN: TERRENO -->
                    <div class="form-section-block">
                        <h3 class="block-title">Terreno y Topografía</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="RN15_ubicacion_ladera">Ubicación en ladera</label>
                                <select id="RN15_ubicacion_ladera" name="RN15_ubicacion_ladera" required>
                                    <option value="0">Llanura / Valle</option>
                                    <option value="1">Meseta superior</option>
                                    <option value="2">Pie de monte</option>
                                    <option value="3">Cresta / Borde</option>
                                    <option value="4">Cuerpo de ladera activa</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN16_pendiente_terreno">Pendiente del terreno</label>
                                <select id="RN16_pendiente_terreno" name="RN16_pendiente_terreno" required>
                                    <option value="0">Llana (0% - 2%)</option>
                                    <option value="1">Suave (3% - 5%)</option>
                                    <option value="2">Inclinada (6% - 10%)</option>
                                    <option value="3">Moderada (11% - 15%)</option>
                                    <option value="4">Fuerte (16% - 25%)</option>
                                    <option value="5">Muy fuerte (26% - 40%)</option>
                                    <option value="6">Crítica (&gt; 40%)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN17_erosion_visible">Erosión visible</label>
                                <select id="RN17_erosion_visible" name="RN17_erosion_visible" required>
                                    <option value="0">Ninguna</option>
                                    <option value="1">Incipiente</option>
                                    <option value="2">Leve</option>
                                    <option value="3">Moderada</option>
                                    <option value="4">Grave</option>
                                    <option value="5">Crítica (Cárcavas)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN18_historial_deslizamientos">Historial deslizamientos</label>
                                <select id="RN18_historial_deslizamientos" name="RN18_historial_deslizamientos" required>
                                    <option value="0">Nunca</option>
                                    <option value="1">Muy antiguo (&gt;10 años)</option>
                                    <option value="2">Antiguo (5-10 años)</option>
                                    <option value="3">Intermedio (1-5 años)</option>
                                    <option value="4">Último año</option>
                                    <option value="5">Reciente (Meses)</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- SECCIÓN: ENTORNO -->
                    <div class="form-section-block">
                        <h3 class="block-title">Entorno y Datos Administrativos</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="RN19_excavaciones_cercanas">Excavaciones cercanas</label>
                                <select id="RN19_excavaciones_cercanas" name="RN19_excavaciones_cercanas" required>
                                    <option value="0">Ninguna</option>
                                    <option value="1">Muy leve</option>
                                    <option value="2">Leve</option>
                                    <option value="3">Moderada</option>
                                    <option value="4">Intensa</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN20_movimiento_tierras">Movimiento de tierras</label>
                                <select id="RN20_movimiento_tierras" name="RN20_movimiento_tierras" required>
                                    <option value="0">Ninguno</option>
                                    <option value="1">Muy leve</option>
                                    <option value="2">Leve</option>
                                    <option value="3">Moderado</option>
                                    <option value="4">Alto</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN21_distancia_construcciones">Distancia a otras construcciones</label>
                                <select id="RN21_distancia_construcciones" name="RN21_distancia_construcciones" required>
                                    <option value="0">&gt; 15 metros</option>
                                    <option value="1">11 a 15 metros</option>
                                    <option value="2">6 a 10 metros</option>
                                    <option value="3">3 a 5 metros</option>
                                    <option value="4">0 a 2 metros</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN22_densidad_edificaciones">Densidad edificaciones</label>
                                <select id="RN22_densidad_edificaciones" name="RN22_densidad_edificaciones" required>
                                    <option value="0">Muy Baja</option>
                                    <option value="1">Baja</option>
                                    <option value="2">Media</option>
                                    <option value="3">Alta</option>
                                    <option value="4">Muy Alta</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN23_denuncias_previas">Denuncias previas</label>
                                <select id="RN23_denuncias_previas" name="RN23_denuncias_previas" required>
                                    <option value="0">0 a 10 denuncias</option>
                                    <option value="1">11 a 20 denuncias</option>
                                    <option value="2">21 a 30 denuncias</option>
                                    <option value="3">31 a 40 denuncias</option>
                                    <option value="4">41 a 50 denuncias</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN24_observaciones_municipales">Observaciones municipales</label>
                                <select id="RN24_observaciones_municipales" name="RN24_observaciones_municipales" required>
                                    <option value="0">0 a 4</option>
                                    <option value="1">5 a 8</option>
                                    <option value="2">9 a 12</option>
                                    <option value="3">13 a 16</option>
                                    <option value="4">17 a 20</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN25_reparaciones_realizadas">Reparaciones realizadas</label>
                                <select id="RN25_reparaciones_realizadas" name="RN25_reparaciones_realizadas" required>
                                    <option value="0">Ninguna</option>
                                    <option value="1">Cosmética/Estética</option>
                                    <option value="2">Mantenimiento menor</option>
                                    <option value="3">Refuerzo parcial</option>
                                    <option value="4">Refuerzo mayor</option>
                                    <option value="5">Reconstrucción total</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- SECCIÓN: IA -->
                    <div class="form-section-block ia-subgroup">
                        <div class="ia-header-sub">
                            <h3 class="block-title">Análisis de Visión Artificial (IA)</h3>
                            <span class="ia-tag">Procesado por OpenCV</span>
                        </div>
                        <p class="ia-help-text">Suba una foto arriba para autocompletar.</p>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="RN26_grietas_IA">Grietas detectadas (IA)</label>
                                <select id="RN26_grietas_IA" name="RN26_grietas_IA" required class="ia-input">
                                    <option value="0">Ninguna</option>
                                    <option value="1">Fisuras capilares</option>
                                    <option value="2">Leves</option>
                                    <option value="3">Moderadas</option>
                                    <option value="4">Severas</option>
                                    <option value="5">Falla estructural</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN27_humedad_IA">Humedad detectada (IA)</label>
                                <select id="RN27_humedad_IA" name="RN27_humedad_IA" required class="ia-input">
                                    <option value="0">Ninguna</option>
                                    <option value="1">Manchas/Sudoración</option>
                                    <option value="2">Humedad leve</option>
                                    <option value="3">Filtración moderada</option>
                                    <option value="4">Alta / Eflorescencia</option>
                                    <option value="5">Saturación / Goteo</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="RN28_deformacion_IA">Deformación detectada (IA)</label>
                                <select id="RN28_deformacion_IA" name="RN28_deformacion_IA" required class="ia-input">
                                    <option value="0">Nula</option>
                                    <option value="1">Imperceptible al ojo</option>
                                    <option value="2">Leve</option>
                                    <option value="3">Moderada</option>
                                    <option value="4">Grave</option>
                                    <option value="5">Falla / Colapso inminente</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- ACTIONS -->
                    <div class="form-actions">
                        <button type="submit" class="btn-submit" id="btn-submit">
                            <span class="btn-text">Calcular Riesgo y Prioridad</span>
                            <span class="btn-loading hidden"></span>
                        </button>
                    </div>
                </form>"""
    
    content = content[:match.start()] + new_form + content[match.end():]
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("HTML form updated successfully.")
else:
    print("Could not find form tag.")
