import requests
import streamlit as st 
import base64
from streamlit_chat import message
from streamlit_modal import Modal
import utils as utl
#from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import streamlit.components.v1 as components
#import cv2



st.set_page_config(layout="wide")
#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
with open("streamlit.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp{
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return




def process_answer(instruction):
    print(instruction)
    headers = {
        'x-api-key': 'sec_Ip374sjUb6uj94WP6UQlxQRtZHKmWhXD',
        "Content-Type": "application/json",
    }

    data = {
        'sourceId': "src_njxNG6mcYq6m89HQUs6TA",
        'messages': [
            {
                'role': "user",
                'content': instruction,
            }
        ]
    }
    #data['sourceId']['messages']['content']=instruction
    print(data)
    
    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)
    print(response.status_code)
    if response.status_code == 200:
        print('Result:', response.json()['content'])
        answer = response.json()['content']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        answer = "Error"
    
    
    response = ''
    instruction = instruction
    #qa = qa_llm()
    #generated_text = qa(instruction)
    #answer = "My Ansqwer"
    return answer
    
    
def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    #pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# Display conversation history using Streamlit messages
def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i],key=str(i))

def main():
    set_png_as_page_bg('Background.png')
    if "ButtonClick" not in st.session_state:
        st.session_state['ButtonClick']=0

    st.markdown("<h1 style='text-align: center; color: White;'>Volga!!!</h1><h1 style='text-align: center; color: #c9878a;'><b>Your one-stop solution for Medical policy queries</b></h1>", unsafe_allow_html=True)
    open_modal = st.button("OpenChat")

    #close_modal = st.button("CloseChat")
    #close_modal = st.button("CloseColumnChat")
    col1, col2, col3= st.columns([1,2,1], gap="medium")
    #open_modal = st.button("OpenColumnChat")
    if open_modal:
        print(st.session_state['ButtonClick'])
        if st.session_state['ButtonClick']==0:
            st.session_state['ButtonClick']=1
        else:
            st.session_state['ButtonClick']=0
    with col1:
        st.image('Background.png')
        #st.image('Background.png')
    ##b8bfc2
    if st.session_state['ButtonClick'] == 1:
        st.markdown(
            """
        <style>
            
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
                      background-color: #d7dcde;
                    }
               
        </style>
        """,
            unsafe_allow_html=True,
        )
        with col2:
            #st.text("Test")
            if "messages" not in st.session_state:
                st.session_state.messages = []
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            st.chat_message("user").markdown("Ask Me Anything")
            if prompt := st.text_input("", key="input", placeholder="Please ask me anything about the policy documents"):
                # Display user message in chat message container
                #st.chat_message("user").markdown(prompt)
                #st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner('Pleasde wait while we get the answer for you...'):
                    answer = process_answer(prompt)
                    response = f"Volga: {answer}"
                    with st.chat_message("assistant"):
                        st.markdown(response)
                #with st.chat_message("user"):
                 #   st.markdown(prompt)
                # Add user message to chat history
            #st.image('Background.png')
            #webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
                
            #st.markdown("<h1 style='text-align: center; color: blue;'>Your one-stop solution for Medical policy queries</h1>", unsafe_allow_html=True)
    
    with col3:
        st.image('Background_New.png')
        video_file = open('VolGA.mp4', 'rb')
        video_bytes = video_file.read()

        st.video(video_bytes)

if __name__ == "__main__":
    main()


