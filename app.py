import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Módulos Pendientes - BI",
    page_icon="📚",
    layout="centered"
)

# --- ESTILOS VISUALES INSTITUCIONALES ---
st.markdown("""
    <style>
    .main-title {
        color: #0F172A;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #475569;
        font-size: 14px;
        text-align: center;
        margin-bottom: 25px;
    }
    .status-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-size: 15px;
        line-height: 1.6;
    }
    .alerta-atencion {
        color: #B45309;
        font-weight: bold;
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px solid #E2E8F0;
    }
    .datos-box {
        background-color: #F1F5F9;
        border: 1px dashed #64748B;
        padding: 14px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .btn-whatsapp {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        font-weight: bold;
        text-decoration: none;
        padding: 12px 24px;
        border-radius: 6px;
        text-align: center;
        font-size: 15px;
        margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease;
    }
    .btn-whatsapp:hover {
        background-color: #128C7E;
    }
    .btn-sheet {
        display: inline-block;
        background-color: #0284C7;
        color: white !important;
        font-weight: 500;
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 5px;
        font-size: 14px;
        margin-top: 8px;
    }
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado institucional
st.markdown('<div class="main-title">MÓDULOS PENDIENTES - BACHILLERATO INTERNACIONAL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Capacitación de docentes y educadores en los principios del Bachillerato Internacional</div>', unsafe_allow_html=True)

# --- ENLACES Y ARCHIVO ---
EXCEL_FILE = "progreso_modulos_ib.xlsx"
ENLACE_WHATSAPP = "https://chat.whatsapp.com/C80yUxnCccS2Fb0sjgJ9C6"
ENLACE_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1Qmq-WKFR8X5eaXux11FUR0cagjBouUhJB1y8aX4l1ng/edit?usp=sharing"

@st.cache_data
def cargar_datos(ruta):
    try:
        df = pd.read_excel(ruta, dtype=str)
        df.columns = [str(c).strip() for c in df.columns]
        return df, None
    except Exception as e:
        return None, str(e)

if not os.path.exists(EXCEL_FILE):
    st.error(f"❌ El archivo '{EXCEL_FILE}' no se encuentra en el repositorio.")
    st.stop()

df_datos, error = cargar_datos(EXCEL_FILE)
if error:
    st.error(f"❌ Error al abrir la nómina: {error}")
    st.stop()

# Validación de columnas
cols_requeridas = ['Nombre y Apellido', 'Cédula', 'M1', 'M2', 'M3', 'M4']
cols_faltantes = [c for c in cols_requeridas if c not in df_datos.columns]
if cols_faltantes:
    st.error(f"❌ La planilla requiere las siguientes columnas exactas: {', '.join(cols_faltantes)}")
    st.stop()

# Normalización de cédula
df_datos['Cédula'] = df_datos['Cédula'].astype(str).str.strip().str.replace(".", "", regex=False).str.replace("-", "", regex=False)

# --- FORMULARIO DE CONSULTA ---
with st.form(key="form_consulta_ib"):
    cedula_in = st.text_input(
        "Número de Cédula de Identidad:",
        placeholder="Ej: 1234567 (sin puntos ni guiones)",
        help="Ingrese los dígitos de su cédula sin símbolos."
    )
    btn_consultar = st.form_submit_button(label="🔍 Consultar Avance")

# --- PROCESAMIENTO ---
if btn_consultar or st.session_state.get('verificado_ib', False):
    cedula_limpia = cedula_in.strip().replace(".", "").replace("-", "")
    
    if not cedula_limpia:
        st.warning("⚠️ Debe introducir un número de documento válido.")
    else:
        resultado = df_datos[df_datos['Cédula'] == cedula_limpia]
        
        if not resultado.empty:
            st.session_state['verificado_ib'] = True
            reg = resultado.iloc[0]
            
            nombre = reg['Nombre y Apellido']
            ci = reg['Cédula']
            m1 = reg['M1']
            m2 = reg['M2']
            m3 = reg['M3']
            m4 = reg['M4']
            
            st.success("✅ ¡Registro localizado con éxito!")
            
            # 1. Reporte visual una línea sobre otra
            st.markdown(f"""
            <div class="status-card">
                <div><b>{nombre}</b></div>
                <div>{ci}</div>
                <div>M1: {m1}</div>
                <div>M2: {m2}</div>
                <div>M3: {m3}</div>
                <div>M4: {m4}</div>
                <div class="alerta-atencion">⚠️ ATENCIÓN: Solicite matriculación al Módulo pendiente - Ingrese a la comunidad de aprendizaje del WhatsApp</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("👋 Copie este bloque para enviarlo a la coordinación al ingresar:")
            
            # 2. Bloque listo para copiar
            texto_copiar = (
                f"{nombre}\n"
                f"{ci}\n"
                f"M1: {m1}\n"
                f"M2: {m2}\n"
                f"M3: {m3}\n"
                f"M4: {m4}\n"
                f"ATENCIÓN: Solicite matriculación al Módulo pendiente - Ingrese a la comunidad de aprendizaje del WhatsApp"
            )
            st.markdown(f'<div class="datos-box"><code style="color: #0F172A; font-weight: bold; white-space: pre-wrap;">{texto_copiar}</code></div>', unsafe_allow_html=True)
            
            # 3. Checkbox de confirmación con el texto solicitado
            confirmado = st.checkbox("👉 Confirmo mis datos - Deseo culminar mi capacitación")
            
            if confirmado:
                st.markdown(f'<a href="{ENLACE_WHATSAPP}" target="_blank" class="btn-whatsapp">💬 Unirse al Grupo de WhatsApp</a>', unsafe_allow_html=True)
            else:
                st.warning("🔒 Marque la casilla superior para habilitar el botón de WhatsApp.")
                
        else:
            st.session_state['verificado_ib'] = False
            st.error("❌ Documento no encontrado en la nómina de participantes.")
            
            # Mensaje con enlace a Google Sheets
            st.markdown(f"""
            <div style="background-color: #FFF7ED; border: 1px solid #FDBA74; padding: 14px; border-radius: 6px; color: #9A3412; font-size: 14px;">
                ⚠️ <b>Si Ud. ha realizado el curso y no reconoce su CI, puede que haya cargado con error sus datos.</b><br>
                Abra el siguiente enlace y verifique la correcta carga de sus datos:<br><br>
                <a href="{ENLACE_GOOGLE_SHEETS}" target="_blank" class="btn-sheet">📋 Abrir Planilla de Verificación de Datos ➔</a>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="footer">Programa de Bachillerato Internacional © 2026</div>', unsafe_allow_html=True)
