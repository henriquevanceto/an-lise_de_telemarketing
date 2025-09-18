import streamlit         as st
import pandas            as pd
import seaborn           as sns
import matplotlib.pyplot as plt
from PIL                 import Image
from io                  import BytesIO

bank_raw = pd.read_csv(r"C:\Users\henri\OneDrive\Documentos\EBAC\Análise de Telemarketing\data\input\bank-additional-full.csv", sep=';')

bank = bank_raw.copy()

st.set_page_config(
     page_title='Análise de Telemarketing',
     page_icon=r"C:\Users\henri\OneDrive\Documentos\EBAC\Análise de Telemarketing\img\pngwing.com.png",
     layout='wide',
     initial_sidebar_state='expanded'
)

st.write('# Análise de Telemarketing')
st.markdown("---")

st.write('## Antes dos filtros')
st.write(bank_raw.head())
st.markdown("---")

image = Image.open(r"C:\Users\henri\OneDrive\Documentos\EBAC\Análise de Telemarketing\img\1691054390911.png")
st.sidebar.image(image)

def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

with st.sidebar.form(key='my_form'):

      # SELECIONA O TIPO DE GRÁFICO
     graph_type = st.radio('Tipo de gráfico:', ('Barras', 'Pizza'))
        
     # IDADES
     max_age = int(bank.age.max())
     min_age = int(bank.age.min())
     idades = st.slider(label='Idade', 
                         min_value = min_age,
                         max_value = max_age, 
                         value = (min_age, max_age),
                         step = 1)


     # PROFISSÕES
     jobs_list = bank.job.unique().tolist()
     jobs_list.append('all')
     jobs_selected =  st.multiselect("Profissão", jobs_list, ['all'])

     # ESTADO CIVIL
     marital_list = bank.marital.unique().tolist()
     marital_list.append('all')
     marital_selected =  st.multiselect("Estado civil", marital_list, ['all'])

     # DEFAULT?
     default_list = bank.default.unique().tolist()
     default_list.append('all')
     default_selected =  st.multiselect("Default", default_list, ['all'])

            
     # TEM FINANCIAMENTO IMOBILIÁRIO?
     housing_list = bank.housing.unique().tolist()
     housing_list.append('all')
     housing_selected =  st.multiselect("Tem financiamento imob?", housing_list, ['all'])

            
     # TEM EMPRÉSTIMO?
     loan_list = bank.loan.unique().tolist()
     loan_list.append('all')
     loan_selected =  st.multiselect("Tem empréstimo?", loan_list, ['all'])

            
     # MEIO DE CONTATO?
     contact_list = bank.contact.unique().tolist()
     contact_list.append('all')
     contact_selected =  st.multiselect("Meio de contato", contact_list, ['all'])

            
     # MÊS DO CONTATO
     month_list = bank.month.unique().tolist()
     month_list.append('all')
     month_selected =  st.multiselect("Mês do contato", month_list, ['all'])

            
     # DIA DA SEMANA
     day_of_week_list = bank.day_of_week.unique().tolist()
     day_of_week_list.append('all')
     day_of_week_selected =  st.multiselect("Dia da semana", day_of_week_list, ['all'])


                    
     # encadeamento de métodos para filtrar a seleção
     bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
               .pipe(multiselect_filter, 'job', jobs_selected)
               .pipe(multiselect_filter, 'marital', marital_selected)
               .pipe(multiselect_filter, 'default', default_selected)
               .pipe(multiselect_filter, 'housing', housing_selected)
               .pipe(multiselect_filter, 'loan', loan_selected)
               .pipe(multiselect_filter, 'contact', contact_selected)
               .pipe(multiselect_filter, 'month', month_selected)
               .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
)


     submit_button = st.form_submit_button(label='Aplicar')

bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]

st.write('## Após os filtros')
st.write(bank.head())
st.markdown("---")

bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
bank_raw_target_perc = bank_raw_target_perc.sort_index()
bank_raw_target_perc

bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
bank_target_perc = bank_target_perc.sort_index()
bank_target_perc

# Plots  
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

sns.barplot(x = bank_raw_target_perc.index,
            y = 'proportion',
            data = bank_raw_target_perc,
            ax = ax[0],
            palette="Blues")

ax[0].set_title('Dados brutos', fontweight="bold")
ax[0].set_ylabel("Proporção (%)")
ax[0].set_xlabel("Resposta")

sns.barplot(x = bank_target_perc.index,
            y = 'proportion',
            data = bank_target_perc,
            ax = ax[1],
            palette="Greens")

ax[1].set_title('Dados filtrados', fontweight="bold")
ax[1].set_ylabel("Proporção (%)")
ax[1].set_xlabel("Resposta")

st.pyplot(fig)