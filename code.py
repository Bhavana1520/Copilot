import streamlit as st
from langchain_community.llms import Ollama
import template
import os
from git import Repo
def main():
    global file_contents

    if 'llm' not in st.session_state:
        st.session_state.llm = Ollama(model="codegemma:7b-instruct", base_url="http://localhost:11434")
        #st.session_state.llm = Ollama(model="codellama:34b-instruct-q3_K_M", base_url="http://localhost:11434")
    llm = st.session_state.llm
    #llm = Ollama(model="codellama:7b-instruct-q3_K_M", base_url="http://localhost:11434")
    # global file_contents
    # llm = Ollama(base_url="http://localhost:11434")
    st.title("Code Copilot")
    task = st.sidebar.selectbox("Choose a task",
                                ["Code Generation", "Code Autocompletion", "Find Bugs and Optimize code",
                                 "Generate Unit Tests", "Doc-String Preparation", "Git Commit Analysis"])

    if task == "Code Generation":
        st.write("### Code Generation")
        st.write("##### Mention your task correctly to generate code")
        st.write("##### For example, '''Generate a python code to implement Stack functionalities''' ")
        user_input = st.text_area("Enter your request", key="code_generation_input", height=20)
        if st.button("Generate Code", key='generate'):
            with st.spinner('Generating code...'):
                prompt = template.prompt_generation(user_input)
                chain = prompt | llm
                response = chain.invoke({"input": user_input})
                st.write(response)

    elif task == "Code Autocompletion":
        st.write("### Code Autocompletion")
        st.write("##### Provide the code, also mentioning the task it should do in a docstring. For example,")
        st.code(''' 
        def scrape_website(url):
        """
        Scrape a website and extract specific information.
        """
        ''')
        user_input = st.text_area("Enter your code:", key="code_infilling_input")
        if st.button("Autocomplete Code", key="auto_complete"):
            with st.spinner('Autocompleting your code...'):
                prompt = template.prompt_autocomplete(user_input)
                chain = prompt | llm
                response = chain.invoke({"message": user_input})
                st.write(response)

    elif task == "Generate Unit Tests":
        st.write("### Generate Unit Test Cases")
        user_input = st.text_area("Enter your code:", key="generate_unit_tests_input")
        if st.button("Generate Unit Tests", key='tests'):
            with st.spinner('Generating unit tests...'):
                prompt = template.prompt_testing(user_input)
                chain = prompt | llm
                response = chain.invoke({"message": user_input})
                st.code(response)


    elif task == "Find Bugs and Optimize code":
        def store_response(response, path="response.py"):
            try:
                response_folder = os.path.join(os.getcwd(), "response")
                os.makedirs(response_folder, exist_ok=True)
                full_path = os.path.join(response_folder, path)
                with open(full_path, 'w') as f:
                    f.write(response)
                    st.success(f"Response stored successfully in '{full_path}'.")
            except Exception as e:
                st.error(f"Error storing response: {e}")

        st.write("### Find Bugs and Optimize code")
        st.write("##### Upload .py file of the code to check for bugs and also for optimised code")
        uploaded_file = st.file_uploader("File Upload", type=["py"])
        if uploaded_file is not None:
            file_contents = uploaded_file.getvalue().decode("utf-8")
        if st.button("Find Bugs", key='bugs'):
            with st.spinner('Finding bugs and optimising ...'):
                prompt = template.prompt_bug(file_contents)
                chain = prompt | llm
                response = chain.invoke({"message": file_contents})
                filename = "response.py"
                store_response(response, filename)
                #st.code(response)

    elif task == "Doc-String Preparation":
        def store_response(response, path="docstring.py"):
            try:
                response_folder = os.path.join(os.getcwd(), "Docstring")
                os.makedirs(response_folder, exist_ok=True)
                full_path = os.path.join(response_folder, path)
                with open(full_path, 'w') as f:
                    f.write(response)
                    st.success(f"Response stored successfully in '{full_path}'.")
            except Exception as e:
                st.error(f"Error storing response: {e}")
        st.write("### Doc-string for your code ")
        st.write("### Paste your code below for providing docstring")
        user_input = st.text_area("Enter your code:", key="doc_string_input")
        if st.button("Generate Doc-String", key='docstring'):
            with st.spinner('Generating doc-string...'):
                prompt = template.prompt_doc(user_input)
                chain = prompt | llm
                response = chain.invoke({"message": user_input})
                filename='docstring.py'
                store_response(response, path=filename)
                #st.code(response)

    elif task == "Git Commit Analysis":
        st.write("### Understand the commits done and provide an description")
        st.write("### Paste both the codes below")
        user_input_1 = st.text_area("Enter your Original code:", key="git_input")
        user_input_2 = st.text_area("Enter your Modified code:", key="git_input_1")
        if st.button("Git Commit Analysis", key='git'):
            with st.spinner('Analyzing your code...'):
                prompt = template.prompt_gitanalysis(user_input_1, user_input_2)
                chain = prompt | llm
                response = chain.invoke({"message1": user_input_1, "message2": user_input_2})
                st.write(response)

if __name__ == "__main__":
    main()