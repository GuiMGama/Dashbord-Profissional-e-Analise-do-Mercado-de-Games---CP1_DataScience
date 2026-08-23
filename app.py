import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 1. Configuração da página (Deve ser a primeira linha do código)
st.set_page_config(page_title="Portfólio - Guilherme Gama", page_icon="💻", layout="wide")

# 2. Sidebar Profissional (Menu Lateral fixo)
with st.sidebar:
    st.image("Foto DashBord.jpeg", width=200) # Sua foto
    st.title("Guilherme Moura Gama")
    st.markdown("📍 São Paulo, SP")
    st.markdown("🎓 **Engenharia de Software - FIAP (Cursando)**")
    st.markdown("🎓 **Ensino Medio - Instituto Madre Mazzarello (Completo)**")
    st.divider()
    st.write("Estudante de Engenharia de Software, com interesse em desenvolvimento de programas e gerenciamento de dados.")
    st.write("Experiência prática na em diversas linguagens de programação, como Java, JavaScript, Python e C++, além de gestão de dados utilizando SQL e arquivos CSV.")
    st.write("Envolvimento em projetos reais e acadêmicos, com foco em soluções digitais, organização, aprendizado contínuo e aplicação prática da tecnologia.")
    st.divider()
    st.caption("Dashboard desenvolvido para o CP1 de Data Science.")

# 3. Cabeçalho Principal
st.title("📊 Portfólio Analítico")
st.markdown("*Navegue pelas abas abaixo para explorar minhas qualificações e o estudo de mercado de games.*")

# 4. Abas redesenhadas
tab1, tab2, tab3 = st.tabs(["🎓 Qualificações & Skills", "📈 Estudo de Mercado (Análise de Dados)", "⚙️ Metodologia"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("🛠️ Hard Skills")
        st.markdown("""
        - **Linguagens:** Python, JavaScript / TypeScript, Java, C++
        - **Ecossistema Web:** React, Node.js, Vite
        - **Noções de UX/UI**
        - **Dados & Estatística:** SQL, Pandas, NumPy, Matplotlib, Streamlit
        - **Design:** Modelagem 3D (Autodesk Maya) e Edição Gráfica
        - **Metodologias:** Básico Relacionado a Área de Scrum
        """)
        
    with col2:
        st.subheader("📚 Experiência Acadêmica")
        st.markdown("""
        - **Bacharelado em Engenharia de Software** (FIAP)
        - Desenvolvimento de APIs e integração de serviços web.
        - Modelagem estruturada de bancos de dados.
        - Aplicação de métodos estatísticos inferenciais para suporte à decisão.
        """)

with tab2:
    st.header("Indústria de Software de Entretenimento")
    st.markdown("Nesta seção, exploramos a previsibilidade de sucesso comercial no mercado de jogos. O objetivo não é apenas ver quem 'vende mais', mas sim usar a estatística para descobrir **quais gêneros oferecem o investimento mais seguro** para um estúdio de desenvolvimento.")
    
    try:
        # Leitura Inteligente do CSV
        df = pd.read_csv("vgsales.csv", encoding="latin1")
        if len(df.columns) == 1:
            df = pd.read_csv("vgsales.csv", encoding="latin1", sep=";")
            
        df_clean = df.dropna(subset=['Global', 'Genre']).copy()
        df_clean['Global'] = pd.to_numeric(df_clean['Global'], errors='coerce')
        df_clean = df_clean.dropna(subset=['Global'])
        
        # --- SEÇÃO DE MÉTRICAS (Cards) ---
        st.subheader("Visão Geral do Mercado")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Softwares Analisados", f"{len(df_clean):,}".replace(",", "."))
        m2.metric("Média Global de Vendas", f"{df_clean['Global'].mean():.2f} mi")
        m3.metric("Gênero Mais Frequente", df_clean['Genre'].mode()[0])
        st.divider()

        # --- PROCESSAMENTO ESTATÍSTICO ---
        stats_df = df_clean.groupby('Genre')['Global'].agg(['mean', 'count', 'std']).reset_index()
        ci95_lo, ci95_hi = [], []
        
        for i in range(len(stats_df)):
            m, c, s = stats_df.loc[i, 'mean'], stats_df.loc[i, 'count'], stats_df.loc[i, 'std']
            if c > 1 and s > 0:
                se = s / np.sqrt(c)
                ci = stats.t.interval(0.95, df=c-1, loc=m, scale=se)
                ci95_lo.append(max(0, ci[0])) 
                ci95_hi.append(ci[1])
            else:
                ci95_lo.append(np.nan), ci95_hi.append(np.nan)
                
        stats_df['Limite Inferior'] = ci95_lo
        stats_df['Limite Superior'] = ci95_hi
        stats_df = stats_df.dropna()
        
        # --- GRÁFICO REFINADO PARA O TEMA ESCURO ---
        st.subheader("Performance e Risco Comercial por Gênero")
        st.write("O gráfico abaixo apresenta a média de vendas de cada gênero. As hastes verticais representam a **Margem de Erro** com 95% de confiança.")
        
        yerr = [stats_df['mean'] - stats_df['Limite Inferior'], stats_df['Limite Superior'] - stats_df['mean']]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Barras escuras com hastes de erro em dourado
        bars = ax.bar(stats_df['Genre'], stats_df['mean'], yerr=yerr, capsize=4, 
                      color='#2b2b2b', edgecolor='#ffffff', ecolor='#d4af37', alpha=0.9, linewidth=0.5)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#555555')
        ax.spines['bottom'].set_color('#555555')
        ax.tick_params(colors='#cccccc')
        
        ax.set_ylabel('Vendas Globais Médias (Milhões)', color='#cccccc')
        plt.xticks(rotation=45, ha='right')
        
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        st.pyplot(fig)
        
        # --- INSIGHTS EM DESTAQUE ---
        st.info("""
        💡 **Interpretação Estratégica dos Dados (Tomada de Decisão):**
        
        A análise das barras de erro nos revela o comportamento real do mercado:
        * **Alta Volatilidade (Intervalos Longos - Hastes Douradas Maiores):** Gêneros como *Platform* ou *Shooter* apresentam médias altas, mas barras de erro enormes. Isso indica um mercado de "Tudo ou Nada", impulsionado por grandes hits. É um setor de **Alto Risco**.
        * **Alta Previsibilidade (Intervalos Curtos):** Gêneros como *Adventure* ou *Strategy* possuem médias menores, mas com barras de erro muito curtas. Isso significa que as vendas variam pouco em relação à média. Para um estúdio, é um setor de **Baixo Risco** e retorno previsível.
        """)
        
        with st.expander("Ver Tabela de Dados Completa (Limites Estatísticos)"):
            st.dataframe(
                stats_df[['Genre', 'count', 'mean', 'Limite Inferior', 'Limite Superior']]
                .rename(columns={'Genre': 'Gênero', 'count': 'Amostras', 'mean': 'Média (Mi)'})
                .style.format(precision=2),
                use_container_width=True
            )
            
    except FileNotFoundError:
        st.error("🚨 Arquivo 'vgsales.csv' não encontrado.")

with tab3:
    st.header("Metodologia e Rigor Científico")
    st.markdown("""
    Para garantir que os insights gerados na análise não sejam meros "palpites", a estruturação dos dados baseou-se nos fundamentos de **Estatística Inferencial**. 
    
    Como não temos os dados de *todos* os jogos já lançados na história (a População), usamos a base de dados atual (a Amostra) para estimar a realidade do mercado.
    """)
    
    st.subheader("O Cálculo do Intervalo de Confiança")
    st.markdown("O sistema calcula a probabilidade do verdadeiro valor médio populacional estar dentro de um intervalo delimitado, garantindo uma precisão de **95%**. A fórmula matemática aplicada no código é:")
    
    # Renderização da fórmula em LaTeX
    st.latex(r"\bar{x} \pm t_{\alpha/2, n-1} \left( \frac{s}{\sqrt{n}} \right)")
    
    st.markdown("""
    **Onde:**
    * $\bar{x}$ = Média amostral das vendas do gênero.
    * $t$ = Valor crítico da **Distribuição t de Student** (utilizada por não sabermos o desvio padrão da população real e termos amostras de tamanhos diferentes).
    * $s$ = Desvio padrão da amostra.
    * $n$ = Número total de jogos (tamanho da amostra).
    * $\frac{s}{\sqrt{n}}$ = Erro Padrão da Média.
    """)
    
    st.divider()
    
    st.subheader("Pipelines de Processamento (Passo a Passo)")
    st.markdown("""
    1. **Data Cleaning e Mapeamento:** Leitura do arquivo e remoção de registros corrompidos ou sem classificação de gênero.
    2. **Coerção de Tipagem (Type Casting):** Conversão explícita da coluna de Vendas Globais para tipo numérico, garantindo que o algoritmo trate os dados como grandezas matemáticas.
    3. **Agregação e Estatística Descritiva:** Uso da biblioteca `pandas` para agrupar as instâncias por gênero e extrair a média, contagem e desvio padrão.
    4. **Modelagem Matemática:** Aplicação do pacote `scipy.stats` para calcular automaticamente as caudas inferior e superior da margem de erro, construindo o gráfico com `matplotlib`.
    """)