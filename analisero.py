import streamlit as st
import math
import os
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURAÇÕES DE PÁGINA ---
st.set_page_config(page_title="ANALISTERO - IFCE", layout="centered")

# --- CONEXÃO COM GOOGLE SHEETS (VERSÃO CORRIGIDA) ---
def salvar_no_sheets(nome, pontos):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(credentials)
        
        # Tenta abrir pelo ID da planilha para não ter erro de nome
        # O ID fica na URL da sua planilha: docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
        # Se preferir usar o nome, mantenha client.open("analisero_dados")
        sheet = client.open("analisero_dados").sheet1
        
        # Prepara a linha
        nova_linha = [nome, pontos]
        
        # Envia e ignora a resposta do objeto (evita o erro Response 200)
        sheet.append_row(nova_linha)
        
        return True
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("Erro: Planilha 'analisero_dados' não encontrada. Verifique o nome.")
        return False
    except gspread.exceptions.APIError as e:
        st.error(f"Erro de permissão da API: {e}")
        return False
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return False

# --- RESTANTE DO CÓDIGO (IGUAL AO ANTERIOR) ---
# ... (mantenha a inicialização do estado, CSS, calculadora e fases aqui) ...

# --- INICIALIZAÇÃO DO ESTADO ---
if 'pontos' not in st.session_state: st.session_state.pontos = 0
if 'fase' not in st.session_state: st.session_state.fase = 0  
if 'feedback' not in st.session_state: st.session_state.feedback = None
if 'visor_calc' not in st.session_state: st.session_state.visor_calc = ""

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 40px; font-weight: bold; border: 2px solid black; padding: 15px; margin-bottom: 20px; background-color: #f0f2f6; }
    .box-enunciado { border: 1px solid black; border-radius: 15px; padding: 20px; margin-bottom: 15px; background-color: white; color: black; font-size: 16px; line-height: 1.5; }
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
        botoes_num = ["1","2","3","4","5","6","7","8","9",".","0"]
        for i, n in enumerate(botoes_num):
            if cols[i%3].button(n, key=f"btn_{n}"): 
                st.session_state.visor_calc += n
                st.rerun()
    with c_ops:
        o = st.columns(3)
        ops = [("+","+"), ("-","-"), ("*","*"), ("/","/"), ("√","sqrt("), ("x²","**2"), ("(","("), ("%", "/100"), (")",")")]
        for i, (label, val) in enumerate(ops):
            if o[i%3].button(label, key=f"op_{label}"): 
                st.session_state.visor_calc += val
                st.rerun()
        if st.button("C", use_container_width=True): 
            st.session_state.visor_calc = ""
            st.rerun()
    
    if st.button("=", use_container_width=True):
        try: 
            st.session_state.visor_calc = str(round(eval(st.session_state.visor_calc.replace("sqrt", "math.sqrt")), 4))
        except: 
            st.session_state.visor_calc = "Erro"
        st.rerun()

# --- LÓGICA DE FEEDBACK ---
if st.session_state.feedback:
    cor = "#28a745" if st.session_state.feedback == "positivo" else "#dc3545"
    st.markdown(f"<h1 style='text-align:center; color:{cor};'>{'VOCÊ ACERTOU!' if cor=='#28a745' else 'TENTE NOVAMENTE!'}</h1>", unsafe_allow_html=True)
    
    video_path = "midiapositiva.mp4" if st.session_state.feedback == "positivo" else "midianegativa.mp4"
    if os.path.exists(video_path):
        st.video(video_path, autoplay=True)
    
    if st.button("PRÓXIMA ETAPA ➔", use_container_width=True):
        st.session_state.feedback = None
        st.session_state.fase += 1
        st.rerun()
    st.stop()

# --- TELAS DO JOGO ---
if st.session_state.fase == 0:
    st.markdown('<div class="main-title">ANALISTERO</div>', unsafe_allow_html=True)
    if st.button("🔓 INICIAR MÓDULO SIGMA", use_container_width=True): 
        st.session_state.fase = 1
        st.rerun()

elif st.session_state.fase == 1:
    st.markdown('<div class="box-enunciado"><b>lição 1 : explicação:</b> vamos exercitar média, mediana, erro absoluto e relativo, exatidão e precisão. Lembre-se, a média é a soma dos valores das amostras dividido por todos os números de amostras.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>1° questão:</b> Analistas determinaram a massa atômica do lítio e coletaram os seguintes dados: amostra 6,936 g/mol; 6,942 g/mol; 6,934 g/mol; 6,940 g/mol. Calcule a massa atômica média das amostras.</div>', unsafe_allow_html=True)
    resp = st.radio("Escolha:", ["a) 6,938 g/mol", "b) 6,940 g/mol", "c) 6,936 g/mol", "d) 6,942 g/mol"])
    if st.button("VERIFICAR"):
        if "a)" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 2:
    st.markdown('<div class="box-enunciado"><b>lição 2: explicação:</b> Lembre-se, mediana é o valor central dentro de um número de amostras, se for conjunto ímpar é o valor do meio, se for conjunto par é a média dos dois valores centrais.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>2° questão:</b> Analistas determinaram a massa atômica do lítio e coletaram os seguintes dados: amostra 6,936 g/mol; 6,942 g/mol; 6,934 g/mol; 6,940 g/mol. Encontre a mediana para a massa atômica.</div>', unsafe_allow_html=True)
    resp = st.radio("Escolha:", ["a) 6,940 g/mol", "b) 6,938 g/mol", "c) 6,936 g/mol", "d) 6,942 g/mol"])
    if st.button("VERIFICAR"):
        if "b)" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 3:
    st.markdown('<div class="box-enunciado"><b>lição 3 explicação:</b> Lembre-se, o erro absoluto é quando o sistema considerou 1 medida como padrão verdadeiro, e qualquer diferença entre sua amostra e o padrão é considerado o erro absoluto.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>3° questão:</b> Considerando que o valor atualmente aceito para a massa atômica do lítio seja 6,941g/mol, calcule o erro absoluto.</div>', unsafe_allow_html=True)
    resp = st.radio("Alternativas:", ["a) 0,009", "b) 0,010", "c) 0,003", "d) 0,08"])
    if st.button("VERIFICAR"):
        if "c)" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 4:
    st.markdown('<div class="box-enunciado"><b>lição 4 explicação:</b> Lembre-se, o erro relativo de uma medida é o erro absoluto dividido pelo valor verdadeiro. geralmente é expresso em porcentagem por isso multiplica por 100.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>4° questão:</b> Considerando que o valor atualmente aceito para a massa atômica do lítio seja 6,941g/mol, calcule o erro relativo.</div>', unsafe_allow_html=True)
    resp = st.radio("Alternativas:", ["a) 0,07%", "b) 0,010%", "c) 0,03%", "d) 0,043%"])
    if st.button("VERIFICAR"):
        if "d)" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 5:
    st.markdown('<div class="box-enunciado"><b>lição 5 explicação:</b> Lembre-se o que é exatidão e o que é precisão? A exatidão é sobre suas amostras serem próximas ao padrão verdadeiro, precisão é sobre suas amostras estarem próximas umas às outras em valores.</div>', unsafe_allow_html=True)
    if os.path.exists("questao5.drawio.png"):
        st.image("questao5.drawio.png", caption="Observe o alvo")
    st.markdown('<div class="box-enunciado"><b>5°questão:</b> imagem do alvo com baixa precisão e alta exatidão. qual a opção correta? 4 imagens</div>', unsafe_allow_html=True)
    resp = st.radio("Escolha:", ["a) baixa precisão e baixa exatidão", "b) alta precisão e alta exatidão", "c) alta precisão e baixa exatidão", "d) baixa precisão e alta exatidão"])
    if st.button("VERIFICAR"):
        if "d)" in resp: st.session_state.pontos += 10; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 6:
    st.markdown('<div class="box-enunciado"><b>lição 6 explicação:</b> Lembre-se Desvio Padrão é quando todos os dados das amostras tem alguma distância do valor médio do conjunto. A fórmula  é dada por s = √ ( valor da amostra - valor médio)² / número de amostras - 1.<br>passo 1: após identificar dos dados, calcule a média. passo 2: para a cada amostra ( valor das amostras - valor médio)² passo 3: divida pelo número de amostras -1. passo 4: tire a raiz, prontinho.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>6° questão:</b> desafio: As análises de várias preparações alimentares envolvendo a determinação de potássio geraram os seguintes dados: 1 analista  descobriu os seguintes valores 5,15, 5,03, 5,04, 5,18, 5,20.</div>', unsafe_allow_html=True)
    res = st.text_input("Resultado (Ex: 0.08):").replace(",", ".")
    if st.button("VERIFICAR"):
        if "0.08" in res: st.session_state.pontos += 15; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 7:
    st.markdown('<div class="box-enunciado"><b>lição 7 explicação:</b> Lembre-se Desvio Padrão é quando todos os dados das amostras tem alguma distância do valor médio do conjunto. A fórmula  é dada por s = √ ( valor da amostra - valor médio)² / número de amostras - 1.<br>passo 1: após identificar dos dados, calcule a média. passo 2: para cada amostra ( valor das amostras - valor médio)² passo 3: divida pelo número de amostras -1. passo 4: tire a raiz, prontinho.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>7° questão:</b> desafio: As análises de várias preparações alimentares envolvendo a determinação de potássio geraram os seguintes dados: 1 analista  descobriu os seguintes valores 7,18; 7,17; 6,97 (mg/L).</div>', unsafe_allow_html=True)
    res = st.text_input("Resultado (Ex: 0.11):").replace(",", ".")
    if st.button("VERIFICAR"):
        if "0.11" in res: st.session_state.pontos += 15; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase == 8:
    st.markdown('<div class="box-enunciado"><b>lição 8: explicação:</b> Lembre-se Variança é quando todos os dados das amostras tem alguma distância do valor médio do conjunto. Qual a diferença entre o desvio padrão? apenas não tem mais raiz. Para o tratamento estatístico ela é melhor.<br>passo 1: após identificar dos dados, calcule a média. passo 2: para cada amostra ( valor das amostras - valor médio)² passo 3: divida pelo número de amostras -1.</div>', unsafe_allow_html=True)
    st.markdown('<div class="box-enunciado"><b>8° questão:</b> Usando os dados da questão anterior (7,18; 7,17; 6,97), calcule a variância.</div>', unsafe_allow_html=True)
    res = st.text_input("Resultado (Ex: 0.012):").replace(",", ".")
    if st.button("VERIFICAR"):
        if "0.01" in res: st.session_state.pontos += 15; st.session_state.feedback = "positivo"
        else: st.session_state.feedback = "negativo"
        st.rerun()

elif st.session_state.fase >= 9:
    st.balloons()
    st.markdown(f'<div class="main-title">PARABÉNS ANALISTA ALPHA!<br>PONTUAÇÃO FINAL: {st.session_state.pontos} XP</div>', unsafe_allow_html=True)
    nome_usuario = st.text_input("Digite seu nome para o ranking:")
    if st.button("SALVAR MEU RESULTADO"):
        if nome_usuario:
            sucesso = salvar_no_sheets(nome_usuario, st.session_state.pontos)
            if sucesso:
                st.success(f"Excelente, {nome_usuario}! Dados salvos com sucesso na planilha.")
        else:
            st.warning("Por favor, digite seu nome.")
