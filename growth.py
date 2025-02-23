import pandas as pd
import streamlit as st
import os
from io import BytesIO
st.set_page_config( page_title="Data sweeper", layout='wide')
#  custum css  
st.markdowm(
    """
    <style>
    .stApp{
    background-color : black ;
    color : white ;
    }
    """,
    unsafe_allow_html= True
)
#  title and discription
st.title('Datasweeper Sterling Integrator By Zia Sheikh')
st.write('Transform your files between CSV and Excel formats with built-in data cleaning')

# upload your file
upload_files = st.file_uploader("Upload your files (accepts CVS or Excel):" , type=['cvs' , 'xlsx'], accept_multiple_files=(True))
if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv" :
            df = pd.read_csv(file)
        elif file_ext == "xlxs" :
            df = pd.read_excel(file)    
        else:
            st.error(f"unsupported file type : {file_ext}")    

            continue
    # file details 
    st.write ("Preview the head of Data frame")
    st.dataframe(df.head())

    # Data Cleaning 
    st.subheader("Data Cleaning Options")
    if st.checkbox(f"clean data for {file.name}"):
       col1, col2 =st.columns(2)

       with col1:
        if st.button(f"Remove duplicates from the file : {file.name}"):
            df.drop_duplicates(inplace=True)
       with col2:
        if st.button(f"Fill missing values {file.name}"):
          numeric_cols = df.select_dtypes(include = ['number']).columns
          df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())  
          st.write("Missing values have been filled!")
    st.subheader(' Select Colums to keep')
    columns = st.multiselect(f'Choose columns for {file.name}' ,df.columns, default=df.columns)
    df = df[columns]

    # Data visualizaation 
    st.subheader('Data Visualization ')
    if st.checkbox(f'Show visualization for {file.name}'):
        st.bar_chart(df.select_dtypes(include='number').iloc[: , :2])

    # conversation 

    st.subheader('Conversion Data')
    conversation_type =st.radio(f'Convert {file.name} to :', ["CVS" , "Excel"], key=file.name)
    if st.button(f'Convert{file.name}'):
        buffer = BytesIO()
        if conversation_type == "CSV" :
                df.to.sv(buffer,index=False)
                file_name = file.name.replace(file-file_ext , 'csv')
                mime_type = "text/csv"
        elif conversation_type == "Excel" :
            df.to_excel(buffer , index =False)
            file_name =file.name.replace(file_ext , "xlxs")
            mime_type = "application/vnd.openxmlformats-officedocument.speradsheet.sheet"
        buffer.seek(0)
        st.download_button(
            label= f"Download {file.name} as {conversation_type}",
            data = buffer,
            file_name = file_name,
            mime = mime_type
        )
st.success('All files processed successfully!')

        
