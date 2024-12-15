import streamlit as st
import openai
import os
import json

from dotenv import load_dotenv,find_dotenv

_ =load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion(prompt,model='gpt-4o'):

    messages = [
                {"role":"user",
                "content":prompt}
                ]
    
    response = openai.chat.completions.create(
        model = model,
        messages = messages,
        temperature = 0
    )

    return response.choices[0].message.content

def ChatBotInteraction(context,user_message):

    "simplified interface to interact with the openai model"

    context.append({'role':'user','content':user_message})

    response = openai.chat.completions.create(
                        model='gpt-4o',
                        temperature=0.8,
                        messages=context
                    )
    
    context.append({'role':"assistant",'content':response.choices[0].message.content})

    return response.choices[0].message.content, context


st.set_page_config(page_title="ChatBot", layout ='wide')

st.title(':beers:ChatterBox: Your Fun & Friendly AI Chatbot:joy:')

st.image('banner_chatterbox.webp')


with st.sidebar:

    listconvs = os.listdir('conversations')

    st.text('History')

    for conv in listconvs:

        title_conv = conv.replace('.json','').replace('"','')

        convMessage = json.loads(open(f'conversations/{conv}','r').read())

        if st.button(title_conv,key=title_conv+'__button'):

            st.session_state.title=title_conv

            st.session_state.conversation = convMessage




if 'conversation' not in st.session_state.keys():

    st.session_state.conversation = [ 
        {'role':"system",
        'content':"You are an entertaining assistant. Your reply is witty and funny which is going to make the user burst into laughter."}
    ]

if prompt := st.chat_input(placeholder="Type your message here"):

    with st.chat_message('assistant'):

        with st.spinner('Thinking ...'):

            response = ChatBotInteraction(st.session_state.conversation,prompt)

            if 'title' in st.session_state.keys():

                with open(f'conversations/{st.session_state.title}.json','w+') as filename:

                    json.dump(st.session_state.conversation,filename)


# display in chatbot ui the entire conversation

for message in st.session_state.conversation[1:]:

    if message['role']=='assistant':

        avatar = 'chatbot_avatar.webp'
    
    else:

        avatar = 'user_avatar.webp'

    with st.chat_message(message['role'],avatar=avatar):

        st.write(message['content'])



if 'title' not in st.session_state.keys() and 'conversation' in st.session_state.keys() and len(st.session_state.conversation)>=3:

    promptTitle = f"""   
    Generate me a title for this conversation in less than 10 words based on
    the context array enclosed in triple backticks
    ```{st.session_state.conversation}```
    """

    title = get_completion(promptTitle)

    st.session_state.title =  title.replace('"','')