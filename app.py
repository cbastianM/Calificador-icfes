import streamlit as st
import pandas as pd
import json
import unicodedata
import re
import io

st.set_page_config(page_title="Calificador de Simulacros", page_icon="📝", layout="wide")

# ─────────────────────────────────────────────
# 🔹 CSS GLOBAL ESTILO ICFES
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Print styles ── */
@media print {
    header, footer, .stSidebar, .stDeployButton,
    [data-testid="stSidebar"], [data-testid="stHeader"],
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    .stFileUploader, .stAlert, #MainMenu, .viewerBadge,
    button, [data-testid="baseButton-secondary"] {
        display: none !important;
    }
    .main .block-container,
    [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding: 0 10mm !important;
        margin: 0 !important;
    }
    @page { margin: 10mm; }
    .icfes-banner, .puntaje-global, .materia-card,
    .calculo-box, .seccion-titulo {
        break-inside: avoid;
        page-break-inside: avoid;
    }
    .tabla-revision { break-inside: auto; page-break-inside: auto; }
    .tabla-revision tr { break-inside: avoid; page-break-inside: avoid; }
    .tabla-revision thead { display: table-header-group; }
    .icfes-banner { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    .barra-fill, .tabla-revision thead th { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    .icfes-banner { padding: 14px 20px; margin-bottom: 12px; }
    .icfes-banner h1 { font-size: 22px; }
    .icfes-banner p { font-size: 12px; }
    .puntaje-global { padding: 12px 16px; }
    .puntaje-global .icono-trofeo { font-size: 30px; }
    .puntaje-global .pg-texto .label { font-size: 12px; }
    .puntaje-global .valor { font-size: 36px; }
    .puntaje-global .valor span { font-size: 16px; }
    .materia-card { padding: 8px 6px; }
    .materia-card .mat-nombre { font-size: 10px; min-height: 24px; }
    .materia-card .mat-icono { font-size: 22px; }
    .materia-card .mat-puntaje { font-size: 24px; }
    .materia-card .mat-puntaje span { font-size: 12px; }
    .materia-card .mat-detalle { font-size: 9px; }
    .tabla-revision { font-size: 9px; }
    .tabla-revision thead th { padding: 3px 4px; font-size: 8px; }
    .tabla-revision tbody td { padding: 2px 4px; }
    .tablas-grid { gap: 8px 14px; }
    .tabla-header .tabla-materia { font-size: 10px; }
    .tabla-header .tabla-stats { font-size: 8px; }
    .seccion-titulo { font-size: 13px; margin: 10px 0 6px 0; }
    .calculo-box { padding: 12px; }
    .calculo-box .paso { font-size: 12px; }
    .calculo-box .resultado-final { font-size: 16px; }
    .nombre-estudiante { font-size: 14px; margin-bottom: 10px; }
}

/* ── Screen styles ── */

.icfes-banner {
    background: linear-gradient(135deg, #E8851C, #F5A623);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    color: white;
}
.icfes-banner h1 {
    font-family: 'Inter', sans-serif;
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 4px 0;
    color: white;
}
.icfes-banner p {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    margin: 0;
    opacity: 0.9;
    font-style: italic;
    color: white;
}

.puntaje-global {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-top: 12px;
    margin-bottom: 16px;
}
.puntaje-global .icono-trofeo { font-size: 40px; line-height: 1; }
.puntaje-global .pg-texto .label {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #555;
    line-height: 1.3;
}
.puntaje-global .valor {
    font-family: 'Inter', sans-serif;
    font-size: 52px;
    font-weight: 800;
    color: #333;
    white-space: nowrap;
}
.puntaje-global .valor span {
    font-size: 22px;
    font-weight: 500;
    color: #E8851C;
}

.materia-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 14px 10px 12px;
    text-align: center;
    flex: 1;
    min-width: 0;
}
.materia-card .mat-nombre {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #333;
    margin-bottom: 4px;
    line-height: 1.3;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.materia-card .mat-icono { font-size: 32px; margin-bottom: 4px; }
.materia-card .mat-puntaje {
    font-family: 'Inter', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #333;
    line-height: 1.1;
}
.materia-card .mat-puntaje span { font-size: 15px; font-weight: 400; color: #999; }
.materia-card .mat-detalle { font-family: 'Inter', sans-serif; font-size: 11px; color: #888; margin-top: 4px; }

.barra-container {
    background: #f0f0f0;
    border-radius: 6px;
    height: 10px;
    width: 100%;
    margin-top: 8px;
    overflow: hidden;
}
.barra-fill { height: 100%; border-radius: 6px; }
.barra-green { background: linear-gradient(90deg, #4CAF50, #66BB6A); }
.barra-yellow { background: linear-gradient(90deg, #FFC107, #FFD54F); }
.barra-orange { background: linear-gradient(90deg, #FF9800, #FFB74D); }
.barra-red { background: linear-gradient(90deg, #F44336, #E57373); }

.nombre-estudiante {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    color: #555;
    margin-bottom: 16px;
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}

.info-preguntas {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #999;
    margin-top: 3px;
}

.tabla-revision {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    margin: 0 auto 14px auto;
    max-width: 220px;
}
.tabla-revision thead th {
    background: #F5A623;
    color: white;
    padding: 4px 5px;
    text-align: center;
    font-weight: 600;
    font-size: 10px;
}
.tabla-revision thead th:first-child { border-radius: 6px 0 0 0; width: 28px; }
.tabla-revision thead th:nth-child(2) { width: 24px; }
.tabla-revision thead th:nth-child(3) { width: 30px; }
.tabla-revision thead th:last-child { border-radius: 0 6px 0 0; width: 34px; }
.tabla-revision tbody td {
    padding: 2px 4px;
    text-align: center;
    border-bottom: 1px solid #f0f0f0;
}
.tabla-revision tbody tr:hover { background: #FFF8F0; }
.tabla-revision .correcta { color: #4CAF50; }
.tabla-revision .incorrecta { color: #F44336; }
.tabla-revision .sin-respuesta { color: #bbb; font-style: italic; }

.tabla-header {
    margin-bottom: 4px;
    font-family: 'Inter', sans-serif;
    text-align: center;
}
.tabla-header .tabla-materia { font-size: 12px; font-weight: 700; color: #333; }
.tabla-header .tabla-stats { font-size: 10px; color: #888; margin-left: 6px; }

.seccion-titulo {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #E8851C;
    margin: 16px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #F5A623;
}

.calculo-box {
    background: #FFFAF3;
    border: 1px solid #F5D6A0;
    border-radius: 10px;
    padding: 20px;
    font-family: 'Inter', sans-serif;
    margin-bottom: 16px;
}
.calculo-box .paso { font-size: 14px; color: #555; margin: 4px 0; }
.calculo-box .resultado-final {
    font-size: 20px;
    font-weight: 700;
    color: #E8851C;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid #F5D6A0;
}

.alert-info {
    background: #FFF8F0;
    border: 1px solid #F5D6A0;
    border-radius: 8px;
    padding: 10px 14px;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #805020;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🔹 FUNCIONES AUXILIARES
# ─────────────────────────────────────────────

def normalizar(texto: str) -> str:
    """Normaliza texto: minúsculas, sin tildes, sin espacios extra."""
    texto = texto.strip().lower()
    try:
        texto = texto.encode("latin-1").decode("utf-8")
    except Exception:
        pass
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"\s+\d+$", "", texto)
    return texto.strip()


# Mapa canónico: cualquier variante normalizada → nombre de display
NOMBRE_DISPLAY = {
    "matematicas": "Matemáticas",
    "matematica": "Matemáticas",
    "lectura": "Lectura crítica",
    "lectura critica": "Lectura crítica",
    "sociales": "Sociales y ciudadanas",
    "sociales y ciudadanas": "Sociales y ciudadanas",
    "naturales": "Ciencias naturales",
    "ciencias naturales": "Ciencias naturales",
    "ingles": "Inglés",
    "ingles (a1-b1)": "Inglés",
}

# Orden de presentación
ORDEN_MATERIAS = [
    "Lectura crítica",
    "Matemáticas",
    "Ciencias naturales",
    "Sociales y ciudadanas",
    "Inglés",
]

ICONO_MATERIA = {
    "Lectura crítica": "📖",
    "Matemáticas": "🧮",
    "Ciencias naturales": "🧪",
    "Sociales y ciudadanas": "🌎",
    "Inglés": "🌐",
}

PESO_MATERIA = {
    "Inglés": 1,  # peso menor en ICFES
}
PESO_DEFAULT = 3


def color_barra(pct: float) -> str:
    if pct >= 70: return "barra-green"
    if pct >= 50: return "barra-yellow"
    if pct >= 30: return "barra-orange"
    return "barra-red"


def parsear_csv(archivo) -> dict[str, dict[str, str]]:
    """
    Parsea un CSV con formato de columnas pareadas:
        pregunta,materia1,pregunta,materia2,...

    Retorna: { "Nombre Display": { "num_pregunta": "RESPUESTA" } }
    Solo incluye materias que tengan al menos 1 pregunta con respuesta.
    """
    archivo.seek(0)
    raw = archivo.read()
    if isinstance(raw, bytes):
        for enc in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                text = raw.decode(enc)
                break
            except Exception:
                text = raw.decode("latin-1")
    else:
        text = raw

    lines = text.strip().replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) < 2:
        return {}

    headers = [h.strip() for h in lines[0].split(",")]

    # Detectar pares (col_pregunta, col_respuesta, nombre_materia)
    pares = []
    i = 0
    while i < len(headers) - 1:
        if normalizar(headers[i]) == "pregunta":
            nombre_norm = normalizar(headers[i + 1])
            pares.append((i, i + 1, nombre_norm))
            i += 2
        else:
            i += 1

    resultado = {}
    for col_preg, col_resp, nombre_norm in pares:
        display = NOMBRE_DISPLAY.get(nombre_norm, nombre_norm.title())
        preguntas = {}

        for line in lines[1:]:
            campos = [c.strip() for c in line.split(",")]
            if col_preg >= len(campos) or col_resp >= len(campos):
                continue
            val_preg = campos[col_preg]
            val_resp = campos[col_resp].upper()
            if val_preg and val_resp:
                try:
                    num = str(int(float(val_preg)))
                    preguntas[num] = val_resp
                except (ValueError, TypeError):
                    continue

        if preguntas:  # solo incluir si tiene preguntas
            resultado[display] = preguntas

    return resultado


def calcular_resultados(clave: dict, estudiante: dict) -> dict:
    """
    Compara clave vs estudiante para cada materia disponible en ambos.
    Solo califica las preguntas presentes en la clave (hoja de respuestas oficial).
    Si el estudiante no respondió una pregunta, se cuenta como incorrecta.

    Retorna dict con info por materia.
    """
    resultados = {}

    for materia in ORDEN_MATERIAS:
        if materia not in clave:
            continue  # materia sin clave → omitir

        preg_clave = clave[materia]           # { "num": "RESP" }
        preg_est = estudiante.get(materia, {})  # puede estar vacío

        total_calificables = len(preg_clave)
        correctas = 0
        detalle = []

        for num_preg, resp_correcta in preg_clave.items():
            resp_alumno = preg_est.get(num_preg, "")
            if isinstance(resp_alumno, str):
                resp_alumno = resp_alumno.strip().upper()
            else:
                resp_alumno = ""

            es_correcta = resp_alumno == resp_correcta
            if es_correcta:
                correctas += 1

            detalle.append({
                "pregunta": int(num_preg),
                "resultado": es_correcta,
                "sin_respuesta": resp_alumno == "",
                "estudiante": resp_alumno if resp_alumno else "—",
                "correcta": resp_correcta,
            })

        detalle.sort(key=lambda x: x["pregunta"])
        porcentaje = (correctas / total_calificables * 100) if total_calificables > 0 else 0

        resultados[materia] = {
            "porcentaje": porcentaje,
            "correctas": correctas,
            "total": total_calificables,
            "respondidas": sum(1 for d in detalle if not d["sin_respuesta"]),
            "peso": PESO_MATERIA.get(materia, PESO_DEFAULT),
            "detalle": detalle,
        }

    return resultados


# ─────────────────────────────────────────────
# 🔹 SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.markdown("### ⚙️ Configuración")

tipo_calculo = st.sidebar.radio(
    "📊 Tipo de cálculo",
    ["Promedio simple (%)", "Puntaje tipo ICFES"],
)
st.sidebar.divider()

st.sidebar.markdown("**Archivos**")
csv_clave = st.sidebar.file_uploader(
    "📋 Hoja de respuestas (clave)",
    type=["csv"],
    help="CSV con las respuestas correctas del simulacro",
)
csv_estudiante = st.sidebar.file_uploader(
    "🎓 Respuestas del estudiante",
    type=["csv"],
    help="CSV con las respuestas del estudiante (mismo formato)",
)

st.sidebar.divider()
st.sidebar.markdown(
    "<small style='color:#aaa;'>El sistema califica solo las preguntas "
    "presentes en la hoja de respuestas. Las materias sin clave se omiten automáticamente.</small>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# 🔹 BANNER
# ─────────────────────────────────────────────

st.markdown("""
<div class="icfes-banner">
    <h1>📝 Resultados del Simulacro</h1>
    <p>SMS GROUP Pre-ICFES — Reporte de calificación</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🔹 PROCESAMIENTO
# ─────────────────────────────────────────────

if csv_clave and csv_estudiante:

    # Parsear ambos CSV
    clave = parsear_csv(csv_clave)
    estudiante_csv = parsear_csv(csv_estudiante)

    if not clave:
        st.error("❌ No se pudieron leer respuestas del CSV de clave. Verifica el formato.")
        st.stop()

    # Calcular resultados (solo materias con clave)
    resultados = calcular_resultados(clave, estudiante_csv)

    if not resultados:
        st.warning("⚠️ No hay materias calificables. Verifica que los CSV tengan el formato correcto.")
        st.stop()

    # Nombre del estudiante: intentar leer desde columna extra o usar nombre del archivo
    nombre_estudiante = csv_estudiante.name.replace(".csv", "").replace("_", " ").title()

    # ── Info de materias detectadas ──
    materias_con_clave = list(clave.keys())
    materias_sin_clave = [m for m in ORDEN_MATERIAS if m not in clave]

    if materias_sin_clave:
        st.markdown(
            f'<div class="alert-info">ℹ️ Materias sin clave en este simulacro (omitidas): '
            f'<strong>{", ".join(materias_sin_clave)}</strong></div>',
            unsafe_allow_html=True,
        )

    # ── Nombre del estudiante ──
    st.markdown(
        f'<div class="nombre-estudiante">👤 Estudiante: <strong>{nombre_estudiante}</strong></div>',
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────
    # 🔹 CARDS DE MATERIAS
    # ─────────────────────────────────────────

    st.markdown('<div class="seccion-titulo" style="margin-top:0;">Puntaje por pruebas</div>', unsafe_allow_html=True)

    n = len(resultados)
    cols_mat = st.columns(n if n > 0 else 1)

    for i, (materia, r) in enumerate(resultados.items()):
        pct = r["porcentaje"]
        corr = r["correctas"]
        tot = r["total"]
        resp = r["respondidas"]
        icono = ICONO_MATERIA.get(materia, "📘")
        color = color_barra(pct)

        with cols_mat[i]:
            st.markdown(f"""<div class="materia-card">
<div class="mat-nombre">{materia}</div>
<div class="mat-icono">{icono}</div>
<div class="mat-puntaje">{pct:.0f}<span>/100</span></div>
<div class="mat-detalle">{corr}/{tot} correctas</div>
<div class="info-preguntas">{resp} respondidas · {tot} en clave</div>
<div class="barra-container"><div class="barra-fill {color}" style="width: {pct}%"></div></div>
</div>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # 🔹 PUNTAJE GLOBAL
    # ─────────────────────────────────────────

    if tipo_calculo == "Puntaje tipo ICFES":
        suma_pond = sum(r["porcentaje"] * r["peso"] for r in resultados.values())
        divisor = sum(r["peso"] for r in resultados.values())
        promedio_base = suma_pond / divisor if divisor > 0 else 0
        puntaje_final = promedio_base * 5
        puntaje_mostrar = f"{puntaje_final:.0f}"
        puntaje_max = "500"
    else:
        promedio = sum(r["porcentaje"] for r in resultados.values()) / len(resultados)
        puntaje_mostrar = f"{promedio:.1f}"
        puntaje_max = "100%"

    st.markdown(f"""<div class="puntaje-global">
<div class="icono-trofeo">🏆</div>
<div class="pg-texto"><div class="label">Puntaje global</div></div>
<div class="valor">{puntaje_mostrar}<span>/{puntaje_max}</span></div>
</div>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # 🔹 PROCESO DE CÁLCULO (solo ICFES)
    # ─────────────────────────────────────────

    if tipo_calculo == "Puntaje tipo ICFES":
        st.markdown('<div class="seccion-titulo">📐 ¿Cómo se calcula?</div>', unsafe_allow_html=True)

        pasos = ""
        sp = 0
        div = 0
        for materia, r in resultados.items():
            pct = r["porcentaje"]
            peso = r["peso"]
            valor = pct * peso
            sp += valor
            div += peso
            pasos += f'<div class="paso">{pct:.0f} × {peso} = {valor:.0f} &nbsp; ({materia}: {r["correctas"]}/{r["total"]} correctas)</div>'

        pb = sp / div if div > 0 else 0
        pf = pb * 5
        pasos += f'<div class="paso" style="margin-top:8px;"><strong>Suma ponderada = {sp:.0f} ÷ {div} = {pb:.2f}</strong></div>'
        pasos += f'<div class="paso"><strong>{pb:.2f} × 5 = {pf:.1f}</strong></div>'
        pasos += f'<div class="resultado-final">🎯 Puntaje ICFES: {pf:.1f} / 500</div>'

        st.markdown(f'<div class="calculo-box">{pasos}</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # 🔹 TABLAS DE REVISIÓN DETALLADA
    # ─────────────────────────────────────────

    st.markdown('<div class="seccion-titulo">🔍 Revisión Detallada por Materia</div>', unsafe_allow_html=True)

    materias_lista = [(m, resultados[m]) for m in resultados]

    for i in range(0, len(materias_lista), 3):
        if i > 0:
            st.markdown('<hr style="border:none; border-top:1px solid #eee; margin:16px 0 130px 0;">', unsafe_allow_html=True)

        grupo = materias_lista[i:i + 3]
        cols = st.columns(len(grupo))

        for j, (materia, r) in enumerate(grupo):
            with cols[j]:
                pct = r["porcentaje"]
                corr = r["correctas"]
                tot = r["total"]
                detalle = r["detalle"]

                filas = ""
                for item in detalle:
                    if item["sin_respuesta"]:
                        clase = "sin-respuesta"
                        emoji = "➖"
                    elif item["resultado"]:
                        clase = "correcta"
                        emoji = "✅"
                    else:
                        clase = "incorrecta"
                        emoji = "❌"

                    filas += (
                        f'<tr>'
                        f'<td><strong>{item["pregunta"]}</strong></td>'
                        f'<td class="{clase}">{emoji}</td>'
                        f'<td class="{clase}">{item["estudiante"]}</td>'
                        f'<td><strong>{item["correcta"]}</strong></td>'
                        f'</tr>'
                    )

                icono = ICONO_MATERIA.get(materia, "📘")
                st.markdown(f"""
<div class="tabla-header">
    <span class="tabla-materia">{icono} {materia}</span>
    <span class="tabla-stats">{corr}/{tot} — {pct:.0f}%</span>
</div>
<table class="tabla-revision">
    <thead><tr><th>#</th><th></th><th>Est.</th><th>Clave</th></tr></thead>
    <tbody>{filas}</tbody>
</table>
""", unsafe_allow_html=True)

elif csv_clave and not csv_estudiante:
    # Mostrar preview de la clave cargada
    clave_preview = parsear_csv(csv_clave)
    materias_ok = [m for m in ORDEN_MATERIAS if m in clave_preview]
    materias_vacias = [m for m in ORDEN_MATERIAS if m not in clave_preview]

    st.success(f"✅ Hoja de respuestas cargada — {len(materias_ok)} materia(s) con preguntas")

    if materias_ok:
        cols_p = st.columns(len(materias_ok))
        for i, m in enumerate(materias_ok):
            n_preg = len(clave_preview[m])
            icono = ICONO_MATERIA.get(m, "📘")
            rango = sorted(int(k) for k in clave_preview[m].keys())
            rango_txt = f"P{rango[0]}–P{rango[-1]}" if rango else "—"
            with cols_p[i]:
                st.markdown(f"""<div class="materia-card">
<div class="mat-nombre">{m}</div>
<div class="mat-icono">{icono}</div>
<div class="mat-puntaje">{n_preg}<span> pregs.</span></div>
<div class="mat-detalle">{rango_txt}</div>
</div>""", unsafe_allow_html=True)

    if materias_vacias:
        st.markdown(
            f'<div class="alert-info">ℹ️ Sin clave en este simulacro: <strong>{", ".join(materias_vacias)}</strong></div>',
            unsafe_allow_html=True,
        )

    st.info("📂 Ahora sube el CSV del estudiante para ver los resultados.")

else:
    st.info("📂 Sube la hoja de respuestas y el CSV del estudiante para comenzar.")

    st.markdown("""
<div class="calculo-box" style="margin-top:24px;">
<div class="paso"><strong>📋 Formato esperado del CSV</strong></div>
<div class="paso" style="margin-top:8px;">Columnas pareadas: <code>pregunta,materia1,pregunta,materia2,...</code></div>
<div class="paso">Ejemplo de encabezado: <code>pregunta,lectura,pregunta,matematicas,pregunta,naturales</code></div>
<div class="paso">Si una materia no tiene preguntas, déjala con celdas vacías o simplemente omítela.</div>
<div class="paso" style="margin-top:8px;">✅ El sistema detecta automáticamente las materias disponibles y califica solo las que tienen clave.</div>
</div>
""", unsafe_allow_html=True)
