import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq()

# Function to interact with the Groq API
def get_response_from_groq(chat_history):
    # Query the model using the Groq API
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=chat_history,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,  # Stream is not needed as Streamlit handles responses dynamically
        stop=None,
    )
    # Return the full assistant response
    return completion.choices[0].message["content"]

# Streamlit App
def main():
    st.title("Motor Parts Chatbot 🤖")
    st.write("Ask me anything about motor parts, and I'll do my best to help!")
    st.write("Examples: *What is a piston?*, *Explain the function of a crankshaft.*")
    
    # Chat history stored in Streamlit session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "system", "content": "You are an expert on motor parts."}]
    
    # User Input
    user_input = st.text_input("Type your question here:", placeholder="What do you want to know about motor parts?")
    
    if st.button("Ask"):
        if user_input.strip() != "":
            # Add user query to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get response from the Groq model
            with st.spinner("Thinking..."):
                bot_response = get_response_from_groq(st.session_state.chat_history)
            
            # Add bot response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            
            # Display the conversation
            st.success("Bot: " + bot_response)
        else:
            st.warning("Please enter a valid question.")

    # Show Chat History
    st.subheader("Chat History")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Bot:** {message['content']}")

    # Clear Chat Button
    if st.button("Clear Chat"):
        st.session_state.chat_history = [{"role": "system", "content": "You are an expert on motor parts."}]
        st.success("Chat history cleared.")

# Run the app
if __name__ == "__main__":
    main()
