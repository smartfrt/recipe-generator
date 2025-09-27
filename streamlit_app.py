import streamlit as st
# from st_chat_message import message
from openai import OpenAI
import copy
import uuid
import base64

# Create a chat feature where the user can type in messages
# and the screen will display ChatGPT's response

clear_btn = st.button("Clear chat history")
if clear_btn and "chat_history" in st.session_state:
    st.session_state["chat_history"] = []

with open(".env", "r") as file:
    open_ai_api_key = file.read()

client = OpenAI(
    api_key=open_ai_api_key
)

system_prompt = "The user will input some ingredients and some restraints & limitations, " \
"please suggest 3 to 5 different dishes from the list of ingredients the user entered and " \
"these dishes should meet the conditions the user provided. The user might send messages" \
"about the ingredients they have, or they might upload one or more pictures of their " \
"fridge or kitchen containing the ingredients. " \
"For the images, please identify the available ingredients the user has. If the user doesn't" \
"include dietary restrictions or preferences, then assume there is none"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "system", "content": system_prompt}
    ]

# Display all chat messages
# for chat_message in st.session_state["chat_history"]:
#     if chat_message["role"] == "user" and chat_message["content"] != "":
#         message(chat_message["content"], is_user=True, key=str(uuid.uuid4()))

#     elif chat_message["role"] == "assistant":
#         message(chat_message["content"], key=str(uuid.uuid4()))

#     else:
#         continue

for chat_message in st.session_state["chat_history"]:
    role = chat_message["role"]
    content = chat_message["content"]
    image_path = chat_message.get("image")

    is_user = role == "user"

    col_1, col_2 = st.columns([1, 6]) if is_user else st.columns([6, 1])

    with col_2 if is_user else col_1:

        with st.container():
            bubble_color = "#7DAC47" if is_user else "#F1F0F0"
            bubble_content = content.replace("\n", "<br>")

            bubble_html = f"""
                <div style='
                    background-color: {bubble_color};
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    max_width: 85%%;
                    word-wrap: break-word;
                    font-size: 16px;
                    color: #000000;
                    '>
                    {bubble_content}
                </div>
            """

            if bubble_content != "" and (role == "user" or role == "assistant"):
                st.markdown(bubble_html, unsafe_allow_html=True)

            if image_path:
                st.image(image_path, use_column_width=True)


# User sending messages & receiving response from ChatGPT
with st.form("input"):
    user_message = st.text_area("Enter your ingredients")
    
    image_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    # We want to add some checkboxes, so the user can check wheter he wants to add
    # particular limitation

    col_1, col_2, col_3 = st.columns([1, 1, 1])

    with col_1:
        check_microwave = st.checkbox("Use Microwave", key="micro", value=True)
        check_oven = st.checkbox("Use Oven", key="oven", value=True)

    with col_2:
        check_stove = st.checkbox("Use Stove", key="stove", value=True)
        check_knife = st.checkbox("Use knife", key="knife", value=True)

    with col_3:
        check_vegetarian = st.checkbox("Vegetarian", key="vegetarian")

    submit_btn = st.form_submit_button("Submit")

    if submit_btn and (user_message != "" or image_file is not None):

        full_message = user_message
        if check_microwave:
            full_message += "(The user puts microwave as an available equipment)"

        if check_oven:
            full_message += "(The user puts oven as an available equipment)"

        if check_stove:
            full_message += "(The user puts stove as an available equipment)"

        if check_knife:
            full_message += "(The user puts knife as an available tool)"

        if check_vegetarian:
            full_message += "(The user is a vegetarian!)"



        # append user message to chat history
        st.session_state["chat_history"].append(
            {"role": "user", "content": user_message}
        )

        send_list = copy.deepcopy(st.session_state["chat_history"])

        send_list[-1]["content"] = []
        send_list[-1]["content"].append(
            {"type": "input_text", "text": full_message}
        )
        if image_file is not None:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            image_type = image_file.type or "image/png"

            send_list[-1]["content"].append(
                {"type": "input_image", "image_url": f"data:{image_type};base64,{image_base64}"}
            )

            st.session_state["chat_history"][-1]["image"] = image_bytes

        response = client.responses.create(
            model="gpt-4.1",
            input=send_list,
        )

        chatgpt_message = response.output_text

        # if image_file is not None:
        #     image_bytes = image_file.read()
        #     st.session_state["chat_history"][-1]["image"] = image_bytes

        # append assistant message to chat history
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": chatgpt_message}
        )

        # refresh our screen
        st.rerun()