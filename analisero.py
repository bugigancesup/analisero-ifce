import streamlit as st
import pandas as pd
import math
import base64
import time

# --- FUNÇÕES AUXILIARES ---
def get_video_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="ANALISTERO - IFCE", layout="centered")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'pontos' not in st.session_state: st.session_state.pontos = 0
if 'fase' not in st.session_state: st.session_state.fase = 0  
if 'feedback' not in st.session_state: st.session_state.feedback = None
if 'visor_calc' not in st.session_state: st.session_state.visor_calc = ""

# Carregamento dos vídeos
if 'pos_b64' not in st.session_state:
    st.session_state.pos_b64 = get_video_base64("midiapositiva.mp4")
    st.session_state.neg_b64 = get_video_base64("midianegativa.mp4")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 40px; font-weight: bold; border: 2px solid black; padding: 15px; margin-bottom: 20px; background-color: #f0f2f6; }
    .box-modulo { text-align: center; border: 1px solid black; padding: 10px; margin-bottom: 15px; font-size: 14px; background-color: #ffffff; }
    .box-enunciado { border: 1px solid black; border-radius: 25px; padding: 20px; margin-bottom: 15px; background-color: white; color: black; font-size: 16px; }
    .highlight-verde { background-color: #00FF00; padding: 2px 5px; font-weight: bold; }
    .visor-verde { background-color: #90EE90; padding: 15px; border-radius: 8px; border: 2px solid #006400; 
                   text-align: right; font-family: monospace; font-size: 22px; color: black; min-height: 50px; }
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

# --- LÓGICA DE FEEDBACK ---
if st.session_state.feedback:
    cor = "#28a745" if st.session_state.feedback == "positivo" else "#dc3545"
    video = st.session_state.pos_b64 if st.session_state.feedback == "positivo" else st.session_state.neg_b64
    st.markdown(f"<h1 style='text-align:center; color:{cor};'>{'VOCÊ ACERTOU!' if cor=='#28a745' else 'TENTE NA PRÓXIMA!'}</h1>", unsafe_allow_html=True)
    if video:
        st.markdown(f'<div style="text-align:center;"><video width="100%" autoplay playsinline><source src="data:video/mp4;base64,{video}" type="video/mp4"></video></div>', unsafe_allow_html=True)
    
    if st.button("AVANÇAR ➔", use_container_width=True):
        st.session_state.feedback = None
        st.session_state.fase += 1
        st.rerun()
    st.stop()

# --- TELAS DO JOGO ---
if st.session_state.fase == 0:
    st.markdown('<div class="main-title">ANALISTERO</div>', unsafe_allow_html=True)
    if st.button("🔓 INICIAR MÓDULO SIGMA", use_container_width=True): 
        st.session_state.fase = 1; st.rerun()

# QUESTÕES
elif st.session_state.fase == 1:
    st.markdown('<div class="box-enunciado"><b>Lição 1:</b> Vamos exercitar média, mediana, erro absoluto e relativo, exatidão e precisão. Lembre-se, a média é a soma dos valores das amostras dividido por todos os números de amostras.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>1° questão:</b> Analistas determinaram a massa atômica do lítio: 6,936; 6,942; 6,934; 6,940 g/mol. Calcule a massa atômica média.</div>', unsafe_allow_html=True)
    resp = st.radio("Escolha:", ["6,938 g/mol", "6,940 g/mol", "6,936 g/mol", "6,942 g/mol"])
    if st.button("VERIFICAR"):
        if "6,938" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 2:
    st.markdown('<div class="box-enunciado"><b>Lição 2:</b> Lembre-se, mediana é o valor central. Se for conjunto ímpar é o valor do meio, se for conjunto par é a média dos dois valores centrais.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>2° questão:</b> Dados: 6,936; 6,942; 6,934; 6,940. Encontre a mediana.</div>', unsafe_allow_html=True)
    resp = st.radio("Escolha:", ["6,940 g/mol", "6,938 g/mol", "6,936 g/mol", "6,942 g/mol"])
    if st.button("VERIFICAR"):
        if "6,938" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 3:
    st.markdown('<div class="box-enunciado"><b>Lição 3:</b> O erro absoluto é a diferença entre sua amostra e o padrão verdadeiro.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>3° questão:</b> Se o valor aceito é 6,941 g/mol e a amostra média foi 6,938 g/mol, calcule o erro absoluto (use valor positivo).</div>', unsafe_allow_html=True)
    resp = st.radio("Alternativas:", ["0,003", "0,010", "0,005", "0,08"])
    if st.button("VERIFICAR"):
        if "0,003" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 4:
    st.markdown('<div class="box-enunciado"><b>Lição 4:</b> O erro relativo é o erro absoluto dividido pelo valor verdadeiro, multiplicado por 100 para ter a porcentagem.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>4° questão:</b> Valor aceito: 6,941. Erro absoluto: 0,003. Calcule o erro relativo.</div>', unsafe_allow_html=True)
    resp = st.radio("Alternativas:", ["0,043%", "0,010%", "0,03%", "0,072%"])
    if st.button("VERIFICAR"):
        if "0,043%" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 5:
    st.markdown('<div class="box-enunciado"><b>Lição 5:</b> Exatidão é proximidade ao padrão. Precisão é proximidade entre as amostras.</div>', unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Accuracy_and_precision_pt.svg/800px-Accuracy_and_precision_pt.svg.png", caption="Observe o alvo D")
    st.markdown('<div class="box-enunciado"><b>5° questão:</b> No alvo (d), os pontos estão próximos ao centro mas espalhados. Isso indica:</div>', unsafe_allow_html=True)
    resp = st.radio("Escolha:", ["baixa precisão e baixa exatidão", "alta precisão e alta exatidão", "alta precisão e baixa exatidão", "baixa precisão e alta exatidão"])
    if st.button("VERIFICAR"):
        if "baixa precisão e alta exatidão" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 6:
    st.markdown('<div class="box-enunciado"><b>Lição 6:</b> Desvio Padrão (s). 1.Média; 2.(amostra-média)²; 3.Soma; 4.Divida por n-1; 5.Raiz.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>6° questão:</b> Valores de potássio: 5,15; 5,03; 5,04; 5,18; 5,20. Qual o desvio padrão?</div>', unsafe_allow_html=True)
    res = st.text_input("Resultado (ex: 0.08):")
    if st.button("VERIFICAR"):
        if "0.08" in res: st.session_state.pontos += 15; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 7:
    st.markdown('<div class="box-enunciado"><b>Lição 7:</b> Repetindo o processo de Desvio Padrão.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>7° questão:</b> Valores: 7,18; 7,17; 6,97 mg/L. Calcule o Desvio Padrão.</div>', unsafe_allow_html=True)
    res = st.text_input("Resultado (ex: 0.11):")
    if st.button("VERIFICAR"):
        if "0.11" in res: st.session_state.pontos += 15; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 8:
    st.markdown('<div class="box-enunciado"><b>Lição 8:</b> Variância (s²) é o desvio padrão ao quadrado (sem a raiz).</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>8° questão:</b> Se o desvio padrão s foi 0.11, qual a variância s²?</div>', unsafe_allow_html=True)
    res = st.text_input("Resultado (ex: 0.012):")
    if st.button("VERIFICAR"):
        if "0.012" in res: st.session_state.pontos += 15; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase >= 9:
    st.balloons()
    st.markdown(f'<div class="main-title">PARABÉNS ANALISTA!<br>PONTUAÇÃO: {st.session_state.pontos} XP</div>', unsafe_allow_html=True)
    nome = st.text_input("Seu nome:")
    if st.button("FINALIZAR"):
        st.success(f"Excelente, {nome}! Você concluiu o treinamento.")
