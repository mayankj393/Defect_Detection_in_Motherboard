from genericpath import isfile
#from macpath import join
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from io import BytesIO
import torch
import os
import detect
import numpy as np
from PIL import Image, ImageOps
import cv2
import json
import pathlib
import time
import operator as op
names = ['CPU_FAN_NO_Screws', 'CPU_FAN_Screw_loose', 'CPU_FAN_Screws', 'CPU_fan', 'CPU_fan_port', 'CPU_fan_port_detached', 'Incorrect_Screws', 'Loose_Screws', 'No_Screws', 'Scratch', 'Screws']
st.set_page_config(page_title="Defect Detection in Motherboard ", page_icon=":tada:", layout="wide")
st.markdown("""<style>
.css-18ni7ap.e8zbici2{
visibility: hidden;
}
</style>
""",unsafe_allow_html=True)
cascade_style = """<style>
.block-container.css-z5fcl4.egzxvld4{
    background-color: #ffef96;
    align-content:center;
    
}

.css-164nlkn.egzxvld1{
    display: none;
}
h2{
    text-align: center;
    font-family:math;
    color: Gray; 
    font-size: 30px;
    padding: 0;
    margin-bottom: 8px;
    font-weigth: bolder;
    letter-spacing: 1px;
    text-shadow: 2px 2px 2px black;
}

.stAlert.success {
    background-color: #D4EDDA;
    border: 1.5px;
    border-style: solid;
    border-color: black;
    color: Blue;
    padding: 2px;
    font-weight: bold;
    flex: 1;
    display: flex;
    justify-content: center;
    font-size: 24px;
    border-radius: 5px;
    font-family: Space Grotesk;
    letter-spacing: 1px;
    margin-bottom: 10px;
    box-shadow: 2.5px 3px 2.5px gray
}

# .stAlert div{ 
#     background: inherit;
# }

# .stAlert p{
#     color: Blue;
#     font-family: cursive;
#     padding: 2px;
#     letter-spacing: 1px;
#     font-weight: bold;
#     font-size: 24px;
# }

.sidebar .sidebar-title{
    font-size: 24px;
    font-weight: bolder;
    color: green;
}

hr{
    margin: 0;
    padding: 0;
    border-width:2px;
    border-color:blue;
}
.element-container.css-lnx6n4.e1tzin5v3{
    
    height: 100%;
    width: 100%;
}

.h1_style{
    text-align: center;
    font-family:"Arial, Helvetica, Verdana, Georgia, Times New Roman, Open Sans, Roboto";
    color: #563f46; 
    font-size: 48px;
    padding: 0;
    margin-bottom: 8px;
    font-weigth: bolder;
    text-shadow: 2px 2px 2px gray;
    background-color: #c8c3cc;
    border-style: solid;
    box-shadow: 2.5px 3px 2.5px gray
    border-color:black;
    border-width:2px;
    border-radius: 5px;
    
}


img{
    border: 2px;
    background: border-box;
    border-style: solid;
    border-color: black;
    border-radius: 6px;
    box-shadow: 2.5px 3px 2.5px gray
}

iframe {
    border: 2px;
    width: 100%; 
    align-item: center;
    border-style: solid;
    border-color: black;
    border-radius: 6px;
    box-shadow: 2.5px 3px 2.5px gray
}


section{
    border: 2px;
    border-style: solid;
    border-radius: 5px;
    padding: 2.5px;
    margin: 5px;
    border-color: black;
    box-shadow: 2.5px 3px 2.5px gray;
}

.stTextInput{
    border: 2px;
    border-style: solid;
    border-radius: 5px;
    padding: 6px;
    border-color: black;
    box-shadow: 2.5px 3px 2.5px gray;
}

.stTextInput input{
    border: 2px;
    border-style: solid;
    border-radius: 5px;
    padding: 6px;
    border-color: black;
    box-shadow: 2.5px 3px 2.5px gray;
}
.stAppViewContainer
{
background-color:#D4EDDA;
}


label div p{
    font-style:italic;
    font-weight: bold;
    border: 2px;
    border-style: solid;
    border-radius: 5px;
    padding: 4px;
    border-color: black;
    box-shadow: 2.5px 3px 2.5px gray;
}

.row-widget{
    border: 2px;
    border-style: solid;
    border-radius: 5px;
    padding: 2px;
    border-color: black;
    box-shadow: 2.5px 3px 2.5px gray;
}

.css-ocqkz7 .e1tzin5v4{
    flex: 1;
    display: flex;
    justify-content: center;
}

.css-fis6aj.exg6vvm10{
    display: none;
}
.stMarkdown{
 width: 2048;
 height: 2048;
}
.stHeader{
    background-color: #D4EDDA;
    border: 1.5px;
    border-style: solid;
    border-color: black;
    color: Blue;
    padding: 2px;
    font-weight: bold;
    flex: 1;
    display: flex;
    justify-content: center;
    font-size: 24px;
    border-radius: 5px;
    font-family: Space Grotesk;
    letter-spacing: 1px;
    margin-bottom: 10px;
    box-shadow: 2.5px 3px 2.5px gray

}

.stAlert.info {
    background-color: #d1ecf1;
    color: #333333;
    border: 2px;
    border-style: solid;
    border-color: black;
    # font-weight: bold;
    border-radius: 5px;
    font-family: Roboto;
    padding: 5px;
    letter-spacing: 1px;
    margin-bottom: 10px;
    box-shadow: 2.5px 3px 2.5px gray
}

.row-widget.stButton{
    border: none;
    box-shadow: none;
    color: green;
    height: 100px;
    font-size: 24px;

}

</style>
"""
st.markdown(cascade_style, unsafe_allow_html=True)
#buttons = st.button("Choose Option to Import Image")
# Display a title with custom CSS style





    


# title_style =""" <style>{
# color:Blue;
# font-size: 20px;
# font-family:Cascdia Code;
# }</style>"""

# img = Image.open(response.raw)

# st.image(img, caption='Uploaded image', use_column_width=True)
def urlInput():
    url = st.text_input("Enter Image URL")
    col1, col2 = st.columns(2)
    if url!='':
        response=requests.get(url)
        img = Image.open(BytesIO(response.content))
        with col1:
              file_path = os.path.abspath(os.path.join("","temp.jpg"))
              with open(file_path,"wb") as f:
                 f.write(response.content)
              command =f'python detect.py --source "{file_path}" --weights runs/detect/exp3/best.pt' 
              return_value = os.popen(command).read()

              image2 = Image.open(file_path)
              new_img = image2.resize((600,400))
              st.write("<div class='stAlert success'>{}</div>".format("Uploaded Image"), unsafe_allow_html=True)
              st.info('Image path of Uploaed Image to local storage: : {}'.format(file_path))
              st.image(new_img, use_column_width=True)
        with col2:
            path, str = detect.run(source=file_path)
            img_paths = os.path.join(path,"temp.jpg")
            image1 = Image.open(img_paths)
            new_image2 = image1.resize((600, 400))
            st.write("<div class='stAlert success'>{}</div>".format("Defect Detected Image "), unsafe_allow_html=True)
            st.warning('Image path of defected Image : {}'.format(file_path))
            st.image(new_image2, use_column_width=True)
            st.write("<div class='stAlert success'>{}</div>".format("Succesulfully detected:"),unsafe_allow_html=True)
            printresult(str)
            os.remove(file_path)


def imgInput():
    uploaded_file = st.file_uploader("Test Your Image Here...", type=['png', 'jpeg', 'jpg', 'JPG'])
    col1, col2 = st.columns(2)

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        with col1:
            file_path = os.path.abspath(os.path.join("", uploaded_file.name))
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            command = f'python detect.py --source "{file_path}" --weights runs/detect/exp3/best.pt'
            image = Image.open(file_path)
            new_image1 = image.resize((600, 400))
            return_value = os.popen(command).read()
            with st.spinner('Wait for it...'):
                time.sleep(5)

            st.write("<div class='stAlert success'>{}</div>".format("Uploaded Image"), unsafe_allow_html=True)
            st.info('Image path of Uploaed Image: : {}'.format(file_path))
            st.image(new_image1, use_column_width=True)

        with col2:
            path,str = detect.run(source=file_path)
            img_paths = os.path.join(path, uploaded_file.name)

            image1 = Image.open(img_paths)
            new_image2 = image1.resize((600, 400))
            st.write("<div class='stAlert success'>{}</div>".format("Defect Detected Image "), unsafe_allow_html=True)
            st.warning('Image path of defected Image : {}'.format(file_path))
            st.image(new_image2, use_column_width=True)
            st.write("<div class='stAlert success'>{}</div>".format("Succesulfully detected:"),unsafe_allow_html=True)
            printresult(str)
            os.remove(file_path)
def printresult(str):
     occur=[]
     my_str=""
     count = 1
     
     target=['no cpu fan screws','Loose CPU fan screws','CPU fan screws','CPU Fan','CPU Fan port','CPU fan port detached',' Incorrect screws','Loose Screws','No Screws','Scratch','Screws']
     for i in range(0,11):
      occur.append(op.countOf(str,i))
      
     #st.write("Succesulfully detected:")
     for i in range(len(occur)):
         if occur[i] != 0:
             st.warning(f'({count})  {occur[i]} {target[i]}  detected')
             count+=1
             #my_str.join(occur[i] + "times" +target[i])   
                  
             
   

# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     body {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def main():
    #buttons = st.button("Choose Option to Import Image")
    st.write("<h1 class='h1_style'>Defect Detection in Mother Board</h1>", unsafe_allow_html=True)
    # set_background('background.png')
    # -- Sidebarst.markdown(title_style, unsafe_allow_html=True)
    
    url = requests.get(
            "https://assets10.lottiefiles.com/packages/lf20_4kji20Y93r.json")
    url_json = dict()

    if url.status_code == 200:
        url_json = url.json()
    else:
        print("Error in the URL")
    st_lottie(url_json, reverse=True,
              # height and width of animation
              # speed of animation
              speed=1,
              # means the animation will run forever like a gif, and not as a still image
              loop=True,
              # quality of elements used in the animation, other values are "low" and "medium"
              quality='high',
              # THis is just to uniquely identify the animation
              key='Animation')
    
    
   
    with st.sidebar:
            
         st.sidebar.title('⚙️ Choose option')
         datasrc = st.sidebar.radio("Select input source.", ['From Device', 'From URL'])
    

        # st.markdown(
        # """
        # <style>
        # .reportview-container {
        #   background: url(" <a href='https://pngtree.com/free-backgrounds'>free background photos from pngtree.com/</a>")
        # }
        # .sidebar .sidebar-content {
        # background: url("url_goes_here")
        # }
        # </style>
        # """,
        # unsafe_allow_html=True
        # )

        #option = st.sidebar.radio("Select input type.", ['DEVICE', 'URL'])
        # if torch.cuda.is_available():
        #     deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = False, index=1)
        # else:
        #     deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = True, index=0)
        # # -- End of Sidebar

        # st.header('Livestock Farming')
        # st.subheader('Select options left-haned menu bar.')
        
        # st.sidebar.markdown("https://github.com/thepbordin/Obstacle-Detection-for-Blind-people-Deployment")
       
    if datasrc == "From Device":
            imgInput()

    elif datasrc == "From URL":
            urlInput()


if __name__ == '__main__':
    main()
