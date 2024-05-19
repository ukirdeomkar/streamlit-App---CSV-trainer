import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

def generate_sentences(df, header_names):
  """Generates sentences from each row of a DataFrame, considering the last column as output.

  Args:
      df (pd.DataFrame): The DataFrame containing the data.
      header_names (list): List of column names (headers) from the DataFrame.

  Returns:
      list: A list of sentences, one for each row in the DataFrame.
  """
  sentences = []
  for index, row in df.iterrows():
    # Extract all columns except the last one (assumed output)
    input_cols = list(df.columns[:-1])
    input_values = [str(row[col]) for col in input_cols]
    output_value = str(row.iloc[-1])
    output_header = header_names[-1]  # Get the last header (output)

    # Use header names in sentence construction for both input and output
    sentence = f"For inputs: '{', '.join([header_names[i] + ': ' + val for i, val in enumerate(input_values)])}', the output **{output_header}** value is '{output_value}'"
    sentences.append(sentence)
  return sentences
# Define a function to send messages and receive responses with context
def send_message(context, message):
    # Load environment variables from .env file
  load_dotenv()
  GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
  genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the model (replace with your actual API key)
  model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
  chat = model.start_chat()
  response = chat.send_message(f"{context}. {message}")
  return response.parts[0].text

def main():
  """Streamlit app to import CSV, generate sentences, and display them."""
  st.title("CSV Sentence Generation App")
  uploaded_file = st.file_uploader("Upload CSV File", type='csv')

  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if len(df.columns) < 2:
      st.error("Please ensure your CSV has at least two columns.")
      return

    header_names = list(df.columns)  # Store header names


    sentences = generate_sentences(df, header_names)
    if(sentences):
      user_message = st.text_input("Type your message:")
      context_window_size = 200
      context = sentences[:context_window_size]
      st.write("The AI has studied the data and you can ask new question to it now regarding this type of data")
      context_box = st.expander("Current Context :")
      with context_box:
        for inputData in context:
            st.write(f"- {inputData}")
      
      if user_message:
        response = send_message(context, user_message)
        st.write(f"Gemini: {response}")
    
    # st.subheader("Generated Sentences:")
    # for sentence in sentences:
    #   st.write(sentence)

if __name__ == '__main__':
  main()


