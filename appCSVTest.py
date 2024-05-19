import streamlit as st
import pandas as pd

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
    st.subheader("Generated Sentences:")
    for sentence in sentences:
      st.write(sentence)

if __name__ == '__main__':
  main()
