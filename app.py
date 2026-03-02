import streamlit as st
import pandas as pd
import json
import unicodedata
import re

st.set_page_config(page_title="Calificador de Simulacros", page_icon="📝", layout="wide")

# ─────────────────────────────────────────────
# 🔹 CSS GLOBAL ESTILO ICFES
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Print styles ── */
@media print {
    /* Hide Streamlit UI chrome */
    header, footer, .stSidebar, .stDeployButton,
    [data-testid="stSidebar"], [data-testid="stHeader"],
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    .stFileUploader, .stAlert, #MainMenu, .viewerBadge,
    button, [data-testid="baseButton-secondary"] {
        display: none !important;
    }

    /* Full width */
    .main .block-container,
    [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding: 0 10mm !important;
        margin: 0 !important;
    }

    /* Page setup */
    @page {
        margin: 10mm;
    }

    /* Prevent page breaks inside elements */
    .icfes-banner, .puntaje-global, .materia-card,
    .calculo-box, .seccion-titulo {
        break-inside: avoid;
        page-break-inside: avoid;
    }

    /* Allow tables to break across pages */
    .tabla-revision {
        break-inside: auto;
        page-break-inside: auto;
    }
    .tabla-revision tr {
        break-inside: avoid;
        page-break-inside: avoid;
    }
    .tabla-revision thead {
        display: table-header-group;
    }

    /* Print colors */
    .icfes-banner {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
    }
    .barra-fill, .tabla-revision thead th {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
    }

    /* Reduce sizes for print */
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
    .materia-card { padding: 10px 12px; }
    .materia-card .mat-puntaje { font-size: 24px; }
    .materia-card .mat-nombre { font-size: 11px; }
    .materia-card .mat-detalle { font-size: 10px; }
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

/* Puntaje global */
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
.puntaje-global .icono-trofeo {
    font-size: 40px;
    line-height: 1;
}
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
.materia-card .mat-icono {
    font-size: 32px;
    margin-bottom: 4px;
}
.materia-card .mat-puntaje {
    font-family: 'Inter', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #333;
    line-height: 1.1;
}
.materia-card .mat-puntaje span {
    font-size: 15px;
    font-weight: 400;
    color: #999;
}
.materia-card .mat-detalle {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #888;
    margin-top: 4px;
}

.barra-container {
    background: #f0f0f0;
    border-radius: 6px;
    height: 10px;
    width: 100%;
    margin-top: 8px;
    overflow: hidden;
}
.barra-fill {
    height: 100%;
    border-radius: 6px;
}
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

/* Grid de tablas */
.tablas-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px 20px;
}
.tabla-bloque {
    flex: 0 0 auto;
}
.tabla-header {
    margin-bottom: 4px;
    font-family: 'Inter', sans-serif;
    text-align: center;
}
.tabla-header .tabla-materia {
    font-size: 12px;
    font-weight: 700;
    color: #333;
}
.tabla-header .tabla-stats {
    font-size: 10px;
    color: #888;
    margin-left: 6px;
}

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
.calculo-box .paso {
    font-size: 14px;
    color: #555;
    margin: 4px 0;
}
.calculo-box .resultado-final {
    font-size: 20px;
    font-weight: 700;
    color: #E8851C;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid #F5D6A0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🔹 SIDEBAR
# ─────────────────────────────────────────────

tipo_calculo = st.sidebar.radio(
    "📊 Tipo de cálculo",
    ["Promedio simple (%)", "Puntaje tipo ICFES"],
)
st.sidebar.divider()
activar_ingles = st.sidebar.checkbox("Activar Inglés", value=False)

st.sidebar.divider()

json_file = st.sidebar.file_uploader("Sube el JSON del estudiante", type=["json"])
csv_file = st.sidebar.file_uploader("Sube el CSV con respuestas correctas", type=["csv"])
# ─────────────────────────────────────────────

def normalizar(texto: str) -> str:
    texto = texto.strip().lower()
    try:
        texto = texto.encode("latin-1").decode("utf-8")
    except:
        pass
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"\s+\d+$", "", texto)
    return texto.strip()

def color_barra(pct):
    if pct >= 70: return "barra-green"
    if pct >= 50: return "barra-yellow"
    if pct >= 30: return "barra-orange"
    return "barra-red"

def icono_materia(materia):
    return {
        "Lectura crítica": "📖",
        "Matemáticas": "🧮",
        "Ciencias naturales": "🧪",
        "Sociales y ciudadanas": "🌎",
        "Inglés": "🌐",
    }.get(materia, "📘")

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

if json_file and csv_file:

    data = json.load(json_file)
    nombre = data.get("informacion_estudiante", {}).get("nombre", "Estudiante")
    respuestas_raw = data.get("respuestas", {})
    respuestas_map = {normalizar(k): v for k, v in respuestas_raw.items()}

    df = pd.read_csv(csv_file)

    columnas_materias = {
        "lectura": "Lectura crítica",
        "matematicas": "Matemáticas",
        "naturales": "Ciencias naturales",
        "sociales": "Sociales y ciudadanas",
        "ingles": "Inglés",
    }

    nombres = [
        "Lectura crítica", "Matemáticas", "Ciencias naturales",
        "Sociales y ciudadanas", "Inglés",
    ]

    df.columns = [normalizar(str(c)) for c in df.columns]
    col_pregunta = df.columns[0]

    claves = {}
    for col_csv, nombre_mat in columnas_materias.items():
        col_encontrada = None
        for c in df.columns:
            if col_csv in normalizar(c):
                col_encontrada = c
                break
        if col_encontrada is None:
            continue
        claves[nombre_mat] = {}
        for _, row in df.iterrows():
            p = row[col_pregunta]
            r = row[col_encontrada]
            if pd.notna(p) and pd.notna(r):
                try:
                    claves[nombre_mat][str(int(float(p)))] = str(r).strip().upper()
                except (ValueError, TypeError):
                    continue

    # ── Calcular resultados ──
    resultados_pct = {}
    resultados_correctas = {}
    resultados_total = {}
    pesos = {}
    detalle_por_materia = {}

    for materia in nombres:
        if materia == "Inglés" and not activar_ingles:
            continue
        if materia not in claves:
            continue

        resp_est = respuestas_map.get(normalizar(materia), {})
        resp_correctas = claves[materia]
        correctas = 0
        total = len(resp_correctas)
        detalle = []

        for pregunta, correcta in resp_correctas.items():
            resp_alumno = resp_est.get(pregunta, "")
            resp_alumno_str = resp_alumno.strip().upper() if isinstance(resp_alumno, str) else ""
            es_correcta = resp_alumno_str == correcta
            if es_correcta:
                correctas += 1
            detalle.append({
                "pregunta": int(pregunta),
                "resultado": es_correcta,
                "estudiante": resp_alumno_str if resp_alumno_str else "—",
                "correcta": correcta,
            })

        detalle_por_materia[materia] = sorted(detalle, key=lambda x: x["pregunta"])
        porcentaje = (correctas / total * 100) if total > 0 else 0
        resultados_pct[materia] = porcentaje
        resultados_correctas[materia] = correctas
        resultados_total[materia] = total
        pesos[materia] = 1 if materia == "Inglés" else 3

    # ── Nombre del estudiante ──
    st.markdown(f'<div class="nombre-estudiante">👤 Estudiante: <strong>{nombre}</strong></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # 🔹 PUNTAJE GLOBAL + CARDS (single HTML block)
    # ─────────────────────────────────────────

    if tipo_calculo == "Puntaje tipo ICFES":
        suma_ponderada = sum(resultados_pct[m] * pesos[m] for m in resultados_pct)
        divisor = sum(pesos[m] for m in resultados_pct)
        promedio_base = suma_ponderada / divisor if divisor > 0 else 0
        puntaje_final = promedio_base * 5
        puntaje_mostrar = f"{puntaje_final:.0f}"
        puntaje_max = "500"
    else:
        promedio = sum(resultados_pct.values()) / len(resultados_pct) if resultados_pct else 0
        puntaje_mostrar = f"{promedio:.1f}"
        puntaje_max = "100%"

    # Cards de materias (full width)
    st.markdown('<div class="seccion-titulo" style="margin-top:0;">Puntaje por pruebas</div>', unsafe_allow_html=True)
    n_materias = len(resultados_pct)
    cols_mat = st.columns(n_materias if n_materias > 0 else 1)

    for i, (materia, porcentaje) in enumerate(resultados_pct.items()):
        with cols_mat[i]:
            corr = resultados_correctas[materia]
            tot = resultados_total[materia]
            icono = icono_materia(materia)
            color = color_barra(porcentaje)

            st.markdown(f"""<div class="materia-card">
<div class="mat-nombre">{materia}</div>
<div class="mat-icono">{icono}</div>
<div class="mat-puntaje">{porcentaje:.0f}<span>/100</span></div>
<div class="mat-detalle">{corr}/{tot} correctas</div>
<div class="barra-container"><div class="barra-fill {color}" style="width: {porcentaje}%"></div></div>
</div>""", unsafe_allow_html=True)

    # Puntaje global (debajo)
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
        for materia, porcentaje in resultados_pct.items():
            peso = pesos[materia]
            valor = porcentaje * peso
            sp += valor
            div += peso
            pasos += f'<div class="paso">{porcentaje:.0f} × {peso} = {valor:.0f} &nbsp; ({materia})</div>'

        pb = sp / div if div > 0 else 0
        pf = pb * 5
        pasos += f'<div class="paso" style="margin-top:8px;"><strong>Suma = {sp:.0f} ÷ {div} = {pb:.2f}</strong></div>'
        pasos += f'<div class="paso"><strong>{pb:.2f} × 5 = {pf:.1f}</strong></div>'
        pasos += f'<div class="resultado-final">🎯 Puntaje ICFES: {pf:.1f} / 500</div>'

        st.markdown(f'<div class="calculo-box">{pasos}</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # 🔹 TABLAS DE REVISIÓN DETALLADA
    # ─────────────────────────────────────────────

    st.markdown('<div class="seccion-titulo">🔍 Revisión Detallada por Materia</div>', unsafe_allow_html=True)

    materias_lista = list(detalle_por_materia.items())

    # Render in rows of 3
    for i in range(0, len(materias_lista), 3):
        if i > 0:
            st.markdown('<hr style="border:none; border-top:1px solid #eee; margin:16px 0 130px 0;">', unsafe_allow_html=True)

        grupo = materias_lista[i:i+3]
        cols = st.columns(len(grupo))

        for j, (materia, detalle) in enumerate(grupo):
            with cols[j]:
                pct = resultados_pct.get(materia, 0)
                corr = resultados_correctas.get(materia, 0)
                tot = resultados_total.get(materia, 0)

                filas = ""
                for item in detalle:
                    clase = "correcta" if item["resultado"] else "incorrecta"
                    emoji = "✅" if item["resultado"] else "❌"
                    filas += f'<tr><td><strong>{item["pregunta"]}</strong></td><td class="{clase}">{emoji}</td><td>{item["estudiante"]}</td><td><strong>{item["correcta"]}</strong></td></tr>'

                st.markdown(f"""
<div class="tabla-header">
    <span class="tabla-materia">{icono_materia(materia)} {materia}</span>
    <span class="tabla-stats">{corr}/{tot} — {pct:.0f}%</span>
</div>
<table class="tabla-revision">
    <thead><tr><th>#</th><th></th><th>Est.</th><th>Clave</th></tr></thead>
    <tbody>{filas}</tbody>
</table>
""", unsafe_allow_html=True)

else:
    st.info("📂 Sube ambos archivos para ver los resultados.")
