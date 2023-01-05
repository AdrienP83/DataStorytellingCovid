# DataStorytellingCovid
Projet Data Science : Dresser un état des lieux de l'évolution de la pandémie de Covid-19 dans le monde. 

`pip install streamlit-folium`

# L'ensemble de données complet Our World in Data COVID-19 

Notre ensemble de données COVID-19 complet est disponible au format CSV et comprend toutes nos données historiques sur la pandémie jusqu'à la date de publication. 

Le fichier suit un format de 1 ligne par lieu et date (un jour/semaines) 

Description du Dataset :  

- 60 colonnes et 101 000 lignes environs (jusqu’a la date du jour) 

- 231 pays recenser et 6 continents 

- Plusieurs valeurs sont null  

- 24 variables en tout  

- Deux types de variables existe ici : les dépendantes et indépendantes  

# Préparation des données :  

On récupère l’index de toutes les valeurs null pour les remplacer par 0 ou autres.  

Si une série entière est null alors on la remplace pour qu’elle soit quand même en légende d’un graphe 

Si la série contient des valeurs null on utilise la fonction interpolate de Plotly.  

Les colonnes impactées :  “people_vaccinated_per_hundred”, “total_vaccinations”, “total_deaths”, “total_deaths_per_million”, “total_cases_per_million”, “icu_patients_per_million”, “hosp_patients_per_million” 
