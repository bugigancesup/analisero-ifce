import streamlit as st
import pandas as pd
import math
import base64
import time
from streamlit_gsheets_connection import GSheetsConnection

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="ANALISTERO - IFCE", layout="centered")

# --- FUNÇÃO PARA VÍDEO (BASE64) ---
def get_video_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return ""

# --- INICIALIZAÇÃO DO ESTADO ---
if 'pontos' not in st.session_state: st.session_state.pontos = 0
if 'fase' not in st.session_state: st.session_state.fase = 0  
if 'feedback' not in st.session_state: st.session_state.feedback = None
if 'visor_calc' not in st.session_state: st.session_state.visor_calc = ""

# Carregamento dos vídeos (Coloque os arquivos na mesma pasta)
if 'pos_b64' not in st.session_state:
    st.session_state.pos_b64 = get_video_base64("midiapositiva.mp4")
    st.session_state.neg_b64 = get_video_base64("midianegativa.mp4")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 40px; font-weight: bold; border: 2px solid black; padding: 15px; margin-bottom: 20px; background-color: #f0f2f6; }
    .box-modulo { text-align: center; border: 1px solid black; padding: 10px; margin-bottom: 15px; font-size: 14px; background-color: #ffffff; }
    .box-enunciado { border: 1px solid black; border-radius: 25px; padding: 25px; margin-bottom: 15px; background-color: white; min-height: 180px; color: black; }
    .highlight-verde { background-color: #00FF00; padding: 2px 5px; font-weight: bold; }
    .visor-verde { background-color: #90EE90; padding: 15px; border-radius: 8px; border: 2px solid #006400; 
                   text-align: right; font-family: monospace; font-size: 22px; color: black; min-height: 50px; }
    .stButton>button { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CALCULADORA NA SIDEBAR ---
with st.sidebar:
    st.title("📊 PAINEL DO ALUNO")
    st.metric("Sua Pontuação", f"{st.session_state.pontos} XP")
    st.write("---")
    st.markdown("### CALCULADORA")
    st.markdown(f'<div class="visor-verde">{st.session_state.visor_calc or "0"}</div>', unsafe_allow_html=True)
    
    c_num, c_ops = st.columns([2, 2])
    with c_num:
        cols = st.columns(3)
        for i, n in enumerate(["1","2","3","4","5","6","7","8","9"]):
            if cols[i%3].button(n): st.session_state.visor_calc += n; st.rerun()
        if st.columns(3)[1].button("0"): st.session_state.visor_calc += "0"; st.rerun()
    with c_ops:
        o = st.columns(3)
        ops = [("+","+"), ("-","-"), ("*","*"), ("/","/"), ("√","sqrt("), ("x²","**2"), ("(","("), ("%", "/100"), (")",")")]
        for i, (label, val) in enumerate(ops):
            if o[i%3].button(label): st.session_state.visor_calc += val; st.rerun()
        if st.button("C", use_container_width=True): st.session_state.visor_calc = ""; st.rerun()
    
    if st.button("=", use_container_width=True):
        try: st.session_state.visor_calc = str(round(eval(st.session_state.visor_calc.replace("sqrt", "math.sqrt")), 4))
        except: st.session_state.visor_calc = "Erro"
        st.rerun()

# --- LÓGICA DE FEEDBACK (VÍDEO) ---
if st.session_state.feedback:
    cor = "#28a745" if st.session_state.feedback == "positivo" else "#dc3545"
    video = st.session_state.pos_b64 if st.session_state.feedback == "positivo" else st.session_state.neg_b64
    st.markdown(f"<h1 style='text-align:center; color:{cor};'>{'VOCÊ ACERTOU!' if cor=='#28a745' else 'TENTE NOVAMENTE!'}</h1>", unsafe_allow_html=True)
    if video:
        st.markdown(f'<div style="text-align:center;"><video width="100%" autoplay playsinline><source src="data:video/mp4;base64,{video}" type="video/mp4"></video></div>', unsafe_allow_html=True)
    else:
        st.info("Vídeo de feedback não encontrado, mas sua resposta foi processada!")
    
    if st.button("PRÓXIMA ETAPA ➔", use_container_width=True):
        st.session_state.feedback = None
        st.rerun()
    st.stop()

# --- TELA INICIAL ---
if st.session_state.fase == 0:
    st.markdown('<div class="main-title">ANALISTERO</div>', unsafe_allow_html=True)
    if st.button("🔓 INICIAR MÓDULO SIGMA", use_container_width=True): 
        st.session_state.fase = 1; st.rerun()
    
    if st.session_state.pontos >= 50:
        if st.button("🔓 INICIAR MÓDULO ALPHA", use_container_width=True): st.session_state.fase = 7; st.rerun()
    else:
        st.button("🔒 MÓDULO ALPHA (Bloqueado - Precisa de 50 XP)", disabled=True, use_container_width=True)

# --- MÓDULO SIGMA (1-5) ---
elif 1 <= st.session_state.fase <= 5:
    st.markdown('<div class="box-modulo">NÍVEL SIGMA : <span style="color:red; font-weight:bold;">1 módulo</span> - média, mediana, erro absoluto, erro relativo, exatidão e precisão.</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    if st.session_state.fase == 1:
        with col1: st.markdown('<div class="box-enunciado">Lembre-se, <span class="highlight-verde">a média</span> é a <span class="highlight-verde">soma dos valores das amostras dividido por todos os números de amostras.</span></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="box-enunciado">Analistas determinaram a massa atômica do lítio e coletaram os seguintes dados: amostras 6,936 g/mol; 6,942 g/mol; 6,934 g/mol; 6,940 g/mol. Encontre a média.</div>', unsafe_allow_html=True)
        resp = st.radio("Alternativas:", ["a) 6,938 g/mol", "b) 6,940 g/mol", "c) 6,936 g/mol", "d) 6,942 g/mol"])
        if st.button("VERIFICAR"):
            if "a)" in resp: st.session_state.pontos += 10; st.session_state.fase = 2; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

    elif st.session_state.fase == 2:
        with col1: st.markdown('<div class="box-enunciado">Lembre-se, <span class="highlight-verde">mediana</span> é o <span class="highlight-verde">valor central</span> dentro de um número de amostras... se for conjunto par é a média dos dois valores centrais.</div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="box-enunciado">Dados: 6,936; 6,942; 6,934; 6,940. Encontre a mediana para a massa atômica.</div>', unsafe_allow_html=True)
        resp = st.radio("Alternativas:", ["a) 6,940 g/mol", "b) 6,938 g/mol", "c) 6,936 g/mol", "d) 6,942 g/mol"])
        if st.button("VERIFICAR"):
            if "b)" in resp: st.session_state.pontos += 10; st.session_state.fase = 3; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

    elif st.session_state.fase == 3:
        with col1: st.markdown('<div class="box-enunciado">Lembre-se, o <span class="highlight-verde">erro absoluto</span> é <span class="highlight-verde">qualquer diferença entre sua amostra e o padrão</span> verdadeiro.</div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="box-enunciado">Valor aceito: 6,941 g/mol. Amostra: 6,936 g/mol. Calcule o erro absoluto.</div>', unsafe_allow_html=True)
        resp = st.radio("Alternativas:", ["a) 0,009", "b) 0,010", "c) 0,005", "d) 0,08"])
        if st.button("VERIFICAR"):
            if "c)" in resp: st.session_state.pontos += 10; st.session_state.fase = 4; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

    elif st.session_state.fase == 4:
        with col1: st.markdown('<div class="box-enunciado">Lembre-se, o <span class="highlight-verde">erro relativo</span> é o <span class="highlight-verde">erro absoluto dividido pelo valor verdadeiro</span> x 100.</div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="box-enunciado">Valor aceito: 6,941 g/mol. Amostra: 6,936 g/mol. Calcule o erro relativo.</div>', unsafe_allow_html=True)
        resp = st.radio("Alternativas:", ["a) 0,07%", "b) 0,010%", "c) 0,03%", "d) 0,072%"])
        if st.button("VERIFICAR"):
            if "d)" in resp: st.session_state.pontos += 10; st.session_state.fase = 5; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

    elif st.session_state.fase == 5:
        with col1: st.markdown('<div class="box-enunciado">Exatidão: <span class="highlight-verde">amostras próximas ao padrão</span>. Precisão: <span class="highlight-verde">amostras próximas umas às outras</span>.</div>', unsafe_allow_html=True)
        with col2: 
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Accuracy_and_precision.svg/200px-Accuracy_and_precision.svg.png")
            st.markdown('<div class="box-enunciado">Se os pontos estão agrupados, mas longe do centro, identifique:</div>', unsafe_allow_html=True)
        resp = st.radio("Escolha:", ["a) baixa exatidão, baixa precisão", "b) baixa exatidão, alta precisão", "c) alta exatidão, baixa precisão", "d) alta precisão, alta exatidão"])
        if st.button("VERIFICAR"):
            if "b)" in resp: st.session_state.pontos += 10; st.session_state.fase = 0; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

# --- MÓDULO ALPHA (7-10) ---
elif 7 <= st.session_state.fase <= 10:
    st.markdown('<div class="box-modulo">NÍVEL ALPHA : <span style="color:red; font-weight:bold;">2° módulo</span> - Desvio padrão, variância e curva de calibração.</div>', unsafe_allow_html=True)

    if st.session_state.fase == 7:
        st.markdown('<div class="box-enunciado">Lembre-se <span class="highlight-verde">Desvio Padrão</span>: 1. Calcule a média; 2. (amostra-média)²; 3. Some tudo; 4. Divida por (n-1); 5. Tire a raiz quadrada.</div>', unsafe_allow_html=True)
        st.markdown('<div class="box-enunciado">Desafio: Valores encontrados: 7,18; 7,17; 6,97. Encontre o desvio padrão.</div>', unsafe_allow_html=True)
        res = st.text_input("Resultado (use ponto como decimal):")
        if st.button("VERIFICAR"):
            if "0.11" in res: st.session_state.fase = 8; st.session_state.pontos += 15; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

    elif st.session_state.fase == 8:
        st.markdown('<div class="box-enunciado">Lembre-se <span class="highlight-verde">Variância</span>: É a mesma lógica do desvio, mas para no passo de dividir por (n-1). É o desvio ao quadrado (s²).</div>', unsafe_allow_html=True)
        st.markdown('<div class="box-enunciado">Desafio: Valores encontrados: 4,00; 3,93; 4,15; 3,86. Encontre a variância.</div>', unsafe_allow_html=True)
        res = st.text_input("Resultado:")
        if st.button("VERIFICAR"):
            if "0.015" in res: st.session_state.fase = 9; st.session_state.pontos += 15; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

    elif st.session_state.fase == 9:
        st.markdown('<div class="box-enunciado">Curva de Calibração: Relaciona <span class="highlight-verde">Concentração x Sinal</span>. Calcule o coeficiente de determinação R².</div>', unsafe_allow_html=True)
        st.markdown('<div class="box-enunciado">Conc(mg/L): 0,0; 5,0; 10,0; 15,0; 20,0 <br> Turbidez: 0,06; 1,48; 2,28; 3,98; 4,61.</div>', unsafe_allow_html=True)
        res = st.text_input("Qual o R² aproximado?")
        if st.button("VERIFICAR"):
            if "0.99" in res: st.session_state.fase = 11; st.session_state.pontos += 20; st.session_state.feedback = "positivo"
            else: st.session_state.feedback = "negativo"
            st.rerun()

# --- TELA FINAL ---
elif st.session_state.fase > 10:
    st.balloons()
    st.markdown(f'<div class="main-title">MISSÃO CUMPRIDA!<br>VOCÊ É UM ANALISTA ALPHA!<br>PONTUAÇÃO: {st.session_state.pontos} XP</div>', unsafe_allow_html=True)
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        nome = st.text_input("Seu nome para o Ranking:")
        if st.button("ENVIAR RESULTADOS"):
            df = pd.DataFrame([{"Nome": nome, "XP": st.session_state.pontos, "Hora": time.ctime()}])
            conn.create(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=df)
            st.success("Dados enviados!")
    except: st.warning("Conecte a planilha nos secrets para salvar.")

    if st.button("REINICIAR JOGO"):
        st.session_state.fase = 0; st.session_state.pontos = 0; st.rerun()