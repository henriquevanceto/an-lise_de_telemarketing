import streamlit         as st
import pandas            as pd
import seaborn           as sns
import matplotlib.pyplot as plt
from PIL                 import Image

bank_raw = pd.read_csv(r'C:\Users\cepir\Documents\Henrique\EBAC\Análise de Telemarketing\data\input\bank-additional-full.csv', sep=';')

bank = bank_raw.copy()

st.set_page_config(
     page_title='Análise de Telemarketing',
     page_icon=r'C:\Users\cepir\Documents\Henrique\EBAC\Análise de Telemarketing\img\pngaaa.com-5596309.png',
     layout='wide',
     initial_sidebar_state='expanded'
)

st.write('# Análise de Telemarketing')
st.markdown("---")

st.write('## Antes dos filtros')
st.write(bank_raw.head())
st.markdown("---")

image = Image.open(r'C:\Users\cepir\Documents\Henrique\EBAC\Análise de Telemarketing\img\Bank-Branding.jpg')
st.sidebar.image(image)

# Idades
max_age = int(bank.age.max())
min_age = int(bank.age.min())
idades = st.sidebar.slider(label='Idade', 
                    min_value = min_age,
                    max_value = max_age, 
                    value = (min_age, max_age),
                    step = 1)
st.sidebar.write('IDADES:', idades)
st.sidebar.write('IDADE MIN:', idades[0])
st.sidebar.write('IDADE MAX:', idades[1])

# Profissões
jobs_list = bank.job.unique().tolist()
jobs_list.append('all')
jobs_selected =  st.multiselect("Profissão", jobs_list, ['all'])

# Estado Civil
marital_list = bank.marital.unique().tolist()
marital_list.append('all')
marital_selected =  st.multiselect("Estado civil", marital_list, ['all'])

# Default?
default_list = bank.default.unique().tolist()
default_list.append('all')
default_selected =  st.multiselect("Default", default_list, ['all'])

            
# Tem financiamento imobiliário?
housing_list = bank.housing.unique().tolist()
housing_list.append('all')
housing_selected =  st.multiselect("Tem financiamento imob?", housing_list, ['all'])

# Meio de contato?
contact_list = bank.contact.unique().tolist()
contact_list.append('all')
contact_selected =  st.multiselect("Meio de contato", contact_list, ['all'])

            
# Mês do contato
month_list = bank.month.unique().tolist()
month_list.append('all')
month_selected =  st.multiselect("Mês do contato", month_list, ['all'])

            
# Dia da semana
day_of_week_list = bank.day_of_week.unique().tolist()
day_of_week_list.append('all')
day_of_week_selected =  st.multiselect("Dia da semana", day_of_week_list, ['all'])

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
fig, ax = plt.subplots(1, 2, figsize = (5,3))


sns.barplot(x = bank_raw_target_perc.index, 
            y = 'y',
            data = bank_raw_target_perc, 
            ax = ax[0])
ax[0].bar_label(ax[0].containers[0])
ax[0].set_title('Dados brutos',
                fontweight ="bold")


sns.barplot(x = bank_target_perc.index, 
            y = 'y', 
            data = bank_target_perc, 
            ax = ax[1])
ax[1].bar_label(ax[1].containers[0])
ax[1].set_title('Dados filtrados',
                fontweight ="bold")