import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import pandas as pd
import joblib

st.markdown('<style>  body {    background: linear-gradient(to bottom right, #FFC0CB, #FF69B4);    font-family: "Helvetica Neue", sans-serif;    border-radius: 10px;    padding: 20px;  }  h1, h2, h3 {    color: #fff;    font-weight: bold;  }  p {    color: #fff;    line-height: 1.5;  }</style>', unsafe_allow_html=True)

# Define a mapping of landslide types to icons
landslide_icons = {
    'Debris Flow': 'cloud',  # Use cloud icon for Debris Flow
    'Rock Fall': 'tree',   # Use tree icon for Rock Fall
    'Shallow Slide': 'flag'    # Use flag icon for Shallow Slide
}

# Create a function to add landslide markers to the map
def add_landslide_markers(map_obj, prediction, latitude, longitude):
    landslide_type = {v: k for k, v in type_of_slide.items()}.get(prediction)
    icon = folium.Icon(icon=landslide_icons.get(landslide_type, 'cloud'))
    folium.Marker([latitude, longitude], icon=icon, tooltip=f'Predicted Type: {landslide_type}').add_to(map_obj)

# Title and description
st.title('Kerala Districts Map and Landslide Prediction')
st.write("This app displays a map of Kerala's districts and predicts landslide type based on input features.")

# Load Kerala GeoJSON data
kerala_geojson = 'kerela_districts.geojson'
gdf = gpd.read_file(kerala_geojson)

# Create a Folium map centered at the midpoint of Kerala
m = folium.Map(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], zoom_start=8)

# Add GeoJSON data to the map
folium.GeoJson(gdf).add_to(m)

# Sidebar
menu_selection = st.sidebar.radio("Select a page below", 
                            ["Home", 
                             "About Landslide", 
                             "Prediction", 
                             "Help"],
                            format_func=lambda x: {"Home": "🏠 Home",
                                                   "About Landslide": "ℹ️  About Landslide",
                                                   "Prediction": "🔮 Prediction",
                                                   "Help": "❓ Help"}[x])
if menu_selection == 'Home':
    st.header('Home Page')
    st.write("Welcome to the Kerala Districts Map and Landslide Prediction App!")
    st.markdown("This app is designed to provide valuable insights into landslide predictions "
                "in various districts of Kerala, India. You can explore the geographical data of Kerala's districts "
                "and predict the type of landslide based on input features like rainfall, land use, latitude, and longitude.")

elif menu_selection == 'About Landslide':
    st.header('About Landslide')
    st.markdown("Landslides are geological phenomena that involve the movement of rock, soil, and debris down a slope. "
                "They can be triggered by various factors, including heavy rainfall, earthquakes, and human activities. "
                "Understanding landslides is crucial for disaster preparedness and risk mitigation, especially in regions "
                "prone to such events, like Kerala, India.")

    st.subheader("Types of Landslides:")
    st.markdown("1. **Debris Flow (DF):** Debris flows are fast-moving landslides characterized by a mixture of rock, soil, and water. "
                "They often occur in steep terrain and can be extremely destructive.")

    st.markdown("2. **Rock Fall (RF):** Rock falls involve the sudden collapse or descent of individual rocks or boulders from cliffs or slopes. "
                "They can pose a significant risk to human safety and infrastructure.")

    st.markdown("3. **Shallow Slide (SS):** Shallow slides include landslides that occur in the uppermost layer of soil and rock. "
                "They are relatively less destructive compared to debris flows and rock falls but can still cause damage.")

    st.subheader("Why Landslide Prediction is Important:")
    st.markdown("Predicting landslides is essential for several reasons:")
    st.markdown("- **Safety:** It helps in evacuating areas at risk and ensuring the safety of residents.")
    st.markdown("- **Infrastructure Protection:** It allows for safeguarding critical infrastructure like roads, buildings, and utilities.")
    st.markdown("- **Environmental Conservation:** Predictions can aid in protecting natural resources and ecosystems.")
    st.markdown("- **Disaster Preparedness:** Early warnings can improve disaster preparedness and response efforts.")
    st.markdown("- **Risk Mitigation:** Understanding landslide probabilities assists in implementing preventive measures.")

    st.subheader("How this App Works:")
    st.markdown("This app combines geographical data and machine learning to provide landslide predictions for different districts "
                "in Kerala. It takes into account factors such as rainfall, land use, and geographical coordinates to estimate the "
                "likelihood of landslides in a specific location. The predictions are displayed on a map for easy visualization.")

    st.markdown("Feel free to explore more about landslides and their significance in disaster management. If you have questions or "
                "need assistance, check out the 'Help and Support' section of the app.")

elif menu_selection == 'Prediction':
    st.header('Landslide Prediction')
    st.sidebar.header('District Selection')
    selected_district = st.sidebar.selectbox('Select a District:', gdf['DISTRICT'].unique())

    # Filter the GeoDataFrame based on the selected district
    selected_district_gdf = gdf[gdf['DISTRICT'] == selected_district]

    # Display district-specific information in the sidebar
    if not selected_district_gdf.empty:
        # st.sidebar.subheader('District Information')
        # st.sidebar.write(f'Selected District: {selected_district}')
        # Highlight the selected district on the map
        district_boundary = folium.GeoJson(selected_district_gdf, style_function=lambda x: {'color': 'red'})
        district_boundary.add_to(m)
    else:
        st.sidebar.warning('Please select a district.')

    # Display the map using Streamlit
    folium_static(m)


    # Input fields
    st.sidebar.subheader('Landslide Prediction Input')
    rainfall = st.sidebar.number_input('Rainfall (mm):')
    normal_rainfall = st.sidebar.number_input('Normal Rainfall (mm):')
    latitude = st.sidebar.number_input('Latitude:')
    longitude = st.sidebar.number_input('Longitude:')
    land_use_2010 = st.sidebar.selectbox('Land Use in 2010:', ['QUU', 'QUA', 'CSV', 'CSB', 'ROA', 'BUI', 'RUB', 'FMP', 'FCP', 'TEA', 'SPL', 'GMC', 'BSL', 'FDN', 'FNO', 'BRF', 'BRS', 'SNA', 'BSS', 'BRG', 'BSO', 'BRO'])
    land_use_2018 = st.sidebar.selectbox('Land Use in 2018:', ['QUU', 'QUA', 'CSV', 'CSB', 'ROA', 'BUI', 'RUB', 'FMP', 'FCP', 'TEA', 'SPL', 'GMC', 'BSL', 'FDN', 'FNO', 'BRF', 'BRS', 'SNA', 'BSS', 'BRG', 'BSO', 'BRO'])
    # Define a mapping of districts to numerical values
    district_mapping = {
    'Ernakulam': 0,
    'Idukki': 1,
    'Kannur': 2,
    'Kasaragod': 3,
        'Kollam': 4,
        'Kottayam': 5,
        'Kozhikode': 6,
        'Malappuram': 7,
        'Palakkad': 8,
        'Pathanamthitta': 9,
        'Thiruvananthapuram': 10,
        'Thrissur': 11,
        'Wayanad': 12   
    }
    # Define a mapping of land use to numerical values
    land_use_mapping = {
    'BRF':1,
    'BRG':2,
    'BRO':3,
    'BRS':4,
    'BSF':5,
    'BSG':6,
    'BSL':7,
    'BSO':8,
    'BSS':9,
    'BUI':10,
    'CSB':11,
    'CSV':12,
    'FCP':13,
    'FDN':14,
    'FMP':15,
    'FNO':16,
    'GMC':17,
    'GNA':18,
    'QUA':19,
    'QUU':20,
    'ROA':21,
    'RUB':22,
    'SNA':23,
    'SPL':24,
    'TEA':25,
    }
    type_of_slide = {
    'Debris Flow':1,
    'Rock Fall':2,
    'Shallow Slide':3
    }
    

    # Check if any of the input values are 0.00
    if rainfall == 0.00 or normal_rainfall == 0.00 or latitude == 0.00 or longitude == 0.00:
        st.warning('Please fill in all input fields with valid values.')
    else:
        # Map user input to numerical values
        encoded_district = district_mapping.get(selected_district, -1)  # -1 if not found
        encoded_land_use_2010 = land_use_mapping.get(land_use_2010, -1)  # -1 if not found
        encoded_land_use_2018 = land_use_mapping.get(land_use_2018, -1)  # -1 if not found

        # Predict landslide type and probabilities
        if st.sidebar.button('Predict Landslide'):
            # Prepare input data for prediction
            input_data = pd.DataFrame({
                'District': [encoded_district],
                'LU_2010': [encoded_land_use_2010],
                'LU_2018': [encoded_land_use_2018],
                'POINT_X': [latitude],
                'POINT_Y': [longitude],
                'Rainfall(mm)': [rainfall],
                'Normal(mm)': [normal_rainfall],
            })

            # Load the trained model (replace 'rf_model.pkl' with your model filename)
            model = joblib.load('rf_model.pkl')
            
            # Predict landslide type and probabilities
            prediction = model.predict(input_data)
            probability = model.predict_proba(input_data)

            # Display prediction results
            st.subheader('Landslide Prediction Result:')
            # st.write(f'Predicted Landslide Type: {prediction[0]}')
            # st.write('Probabilities:')
            # for i, landslide_type in enumerate(model.classes_):
            #     st.write(f'{landslide_type}: {probability[0][i]:.2f}')
            
            predicted_landslide_type = {v: k for k, v in type_of_slide.items()}.get(prediction[0])
            st.write(f'Predicted Landslide Type: {predicted_landslide_type}')

elif menu_selection == 'Help':
    st.header('Help and Support')
    st.markdown("Welcome to the 'Kerala Districts Map and Landslide Prediction' app. If you have any questions or need assistance, "
                "please refer to the information below.")

    st.subheader("Getting Started:")
    st.markdown("1. **Home Page:** Learn about the app and its purpose. Click 'Home' in the menu to access this page.")
    st.markdown("2. **About Landslide:** Discover essential information about landslides, their types, and why landslide prediction is crucial. "
                "Click 'About Landslide' in the menu to access this page.")
    st.markdown("3. **Landslide Prediction:** Predict landslide types based on input features for specific districts in Kerala. "
                "Click 'Prediction' in the menu to access this page.")
    st.markdown("4. **Help and Support:** You're here! If you have any questions or need assistance, you're in the right place. "
                "Click 'Help' in the menu to access this page.")

    st.subheader("Contact Information:")
    st.markdown("If you encounter any issues or have inquiries related to this app or its functionality, please don't hesitate "
                "to reach out to us. You can contact us via the following methods:")
    st.markdown("- **Email:** help@sheffielduniv.com")
    st.markdown("- **Phone:** +44 114 222 2000")
    
    st.subheader("FAQs (Frequently Asked Questions):")
    st.markdown("Here are some common questions and answers to assist you:")
    st.markdown("- **Q1:** How accurate are the landslide predictions?")
    st.markdown("  - **A1:** The accuracy of predictions depends on various factors, including the quality of data and the machine learning model used. "
                "Our app strives to provide reliable predictions based on available data sources.")
    st.markdown("- **Q2:** Can I input custom data for predictions?")
    st.markdown("  - **A2:** Currently, the app supports predefined input features such as rainfall, land use, and geographical coordinates. "
                "Custom data input may be available in future updates.")
    st.markdown("- **Q3:** How often is the data updated?")
    st.markdown("  - **A3:** Data updates may vary. We aim to provide the most recent information available, but it depends on the source and "
                "frequency of updates from relevant authorities.")

    st.markdown("Thank you for using the 'Kerala Districts Map and Landslide Prediction' app. We hope it serves as a valuable tool for "
                "disaster preparedness and risk mitigation in Kerala.")

