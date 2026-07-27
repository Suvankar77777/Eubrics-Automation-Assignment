import streamlit as st
from ollama import Client

# Connect to Ollama
client = Client(host="http://127.0.0.1:11434")

# Store conversation history
if "messages" not in st.session_state: st.session_state.messages = []

st.set_page_config(
    page_title="Sales Roleplay AI",
    page_icon="🤖",
    layout="centered"
)
st.sidebar.title("⚙️ Settings")
st.title("🤖 Sales Roleplay AI")

st.write("Practice your sales conversations with an AI-powered customer.")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

scenario = st.sidebar.selectbox(
    "Sales Scenario",
    [
        "Cold Calling",
        "Product Demo",
        "Price Negotiation",
        "Handling Objections"
    ]
)
customer_persona = st.sidebar.selectbox(
    "Customer Persona",
    [
        "Friendly",
        "Busy Executive",
        "Skeptical Buyer",
        "Budget Conscious",
        "Technical Buyer"
    ]
)
difficulty = st.sidebar.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)
if st.sidebar.button("🗑️ New Conversation"):
    st.session_state.messages = []
    st.rerun()

# User Message
user_message = st.text_area(
    "Your Sales Message",
    placeholder="Type your sales message here..."
)

# Send Button
if st.button("Send"):
    if user_message.strip() == "":
        st.warning("Please enter a message.")
        st.stop()
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })
    prompt = f"""
        You are acting as a customer in a sales roleplay.

        Scenario:
        {scenario}

        Respond naturally as the customer.

        Salesperson says:
        {user_message}
        """
    with st.spinner("Agent is thinking..."):
        conversation = [
            {
                "role": "system",
                "content": f"""
                    You are acting as a customer in a sales roleplay.

                    Scenario:
                    {scenario}

                    Customer Persona:
                    {customer_persona}

                    Difficulty:
                    {difficulty}

                    Stay in character throughout the conversation.
                    Respond naturally as a customer.
                    """
            }
        ]

        for msg in st.session_state.messages:
            conversation.append(msg)

        response = client.chat(
            model="gemma3:latest",
            messages=conversation
        )

    ai_reply = response["message"]["content"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    with st.chat_message("assistant"): st.markdown(ai_reply)
    
st.sidebar.markdown("---")
st.sidebar.write(f"Messages: {len(st.session_state.messages)}")

st.markdown("---")

if st.button("📊 Evaluate My Performance"):
    conversation_text = ""
    for msg in st.session_state.messages: conversation_text += f"{msg['role'].upper()}: {msg['content']}\n\n"
    evaluation_prompt = f"""
        You are an expert sales coach.
        Analyse the following sales conversation.
        Provide:
        1. Overall Score (out of 10)
        2. Strengths
        3. Weaknesses
        4. How the salesperson could improve
        Conversation:
        {conversation_text}
        """
    evaluation = client.chat(
        model="gemma3:latest",
        messages=[
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ]
    )
    st.subheader("📈 Sales Coach Feedback")
    st.write(evaluation["message"]["content"])
    
chat_text = ""
for msg in st.session_state.messages:
    chat_text += f"{msg['role'].upper()}:\n"
    chat_text += msg["content"]
    chat_text += "\n\n"
    
st.download_button(
    label="💾 Download Conversation",
    data=chat_text,
    file_name="sales_roleplay_chat.txt",
    mime="text/plain"
)

st.markdown("---")
st.caption("Built by Suvankar Paria for the Eubrics Automation Engineer Assignment")