import streamlit as st
import pylint.lint
import io
import os
import ollama
import tempfile


def analyze_code(code):
    # Redirect stdout to capture pylint output
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    # Run pylint on the temporary file
    pylint_output = io.StringIO()
    pylint.lint.Run([temp_file_path], exit=False, reporter=pylint.reporters.text.TextReporter(pylint_output))

    # Read the pylint output
    pylint_output.seek(0)
    analysis_results = pylint_output.read()

    # Clean up the temporary file
    os.remove(temp_file_path)

    return analysis_results

def send_message(message, task, message2=None):
    if task == "find_bugs":
        # Assuming message contains the uploaded Python code
        analysis_results = analyze_code(message)
        return analysis_results
    else:
        # Handle other tasks as before
        system_content = {
            "code_generation": f"""
            You are an expert Python programmer. Your task is to generate Python code that accomplishes the following:

            {message}

            Please provide a step-by-step explanation of your code, including the purpose of each part and how it contributes to the overall functionality. Ensure the code is efficient, readable, and well-documented.
            """,
            "code_infilling": f"""
            You are an advanced AI with expertise in Python programming. Your task is to assist with code auto-completion for the following code snippet:


            {message}


        This code snippet is incomplete, and your mission is to identify the missing or incomplete parts. Once identified, you are to provide a complete version of the code, ensuring it is syntactically correct, logically sound, and follows Python best practices.

        Please consider the following when completing the code:

        - **Contextual Understanding**: Understand the purpose and functionality of the incomplete code. What is it supposed to do?
        - **Syntax and Logic**: Ensure the completed code is syntactically correct and logically sound. It should perform the intended task without errors.
        - **Best Practices**: Follow Python best practices for coding standards, including naming conventions, code structure, and documentation.
        - **Comprehensive Completion**: If the code snippet is part of a larger function or program, ensure the completion is coherent with the rest of the code. Provide the entire function or program if necessary.

        If the code snippet is part of a larger function or program, provide the entire function or program with the completed code.
            """,
            "generate_unit_tests": f"""
                    You are an expert in testing Python codes. Your task is to create comprehensive unit test cases for the following code snippet: {message}

            Please consider the following when generating your unit tests:

            - **Coverage**: Ensure that the tests cover a wide range of inputs, including typical use cases, edge cases, and error conditions.
            - **Robustness**: The tests should be robust and able to handle unexpected inputs or behaviors gracefully.
            - **Maintainability**: The tests should be easy to understand and maintain, with clear and descriptive names for each test case.

            Return the generated unit test with an example and the expected output code as follows:
            # Unit tests
            def test_function_name():
                # Test case 1: Description of the test case.
                # Test case 2: Description of the test case.
                # ...

        """,
            "generate_doc": f"""
            You are an expert at understanding the given code.Provide docstring for {message} .The docstring should be in the following format: 
            def your_function_name(your_parameters):   
            "
            Brief description of what the function does.
            Parameters:
            - your_parameters (type): Description of the parameter.

            Returns:
            - return_type: Description of what the function returns.
            "
            Give the input full code here.
        """,
            "git_commit": f"""
        You are an expert at analyzing Python code changes.
        This function takes two code snippets as input and compares them line by line carefully to identify every little change made in every line of the second code compared to the first.
        If there are no changes, then just ignore that line and move to the next line.
        Below are two code snippets which you should perform the task with:

        {message}

        {message2}

        Please follow these guidelines when performing git commit:

        1. **Analyze Code Differences**: Analyze the differences between the two provided Python code snippets. Report the changes in a tabular format with columns for "Code1","Code2" and "Description".

        2. **Compare Code Snippets**: Compare the two given Python code snippets. Identify any additions, deletions, or modifications and describe them in a table with "Lines Affected" and "Description" columns.

        3. **Diff Analysis**:Perform a diff analysis on the two Python code snippets provided. Highlight the changes in a table format, listing the affected lines and a brief description of each change.

        4. **Code Comparison**:Compare the two Python code snippets and summarize the differences in a table. Include the line numbers of changes and a brief description of each modification.

        5. **Code Change Report**:Generate a report on the changes between the two Python code snippets. The report should be in a table format, detailing the lines affected and a description of the changes.

        """,
        }[task]
        response = ollama.chat(model='codegemma:instruct', messages=[
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": system_content,
            }
        ])
        return response['message']['content']


def main():
    st.title("Code Assistant")
    task = st.sidebar.selectbox("Choose a task",
                                ["Code Generation", "Code Infilling", "Find Bugs and Optimize code",
                                 "Generate Unit Tests", "Doc-String Preparation", "Git Commit Analysis"])
    if task == "Code Generation":
        st.write("### Code Generation")
        st.write("##### Mention your task correctly to generate code")
        st.write("##### For example, '''Generate a python code to implement Stack functionalities''' ")
        user_input = st.text_input("Enter your request", key="code_generation_input")
        if st.button("Generate Code"):
            with st.spinner('Generating code...'):
                response = send_message(user_input, "code_generation")
                st.write(response)
    elif task == "Code Infilling":
        st.write("### Code Infilling")
        st.write(
            "##### Copy the code and include the comment line #fill where you want autocomplete to occur. For example,")
        st.code(''' 
        #Program to find simple interest
def simple_interest(p,t,r):
    print('The principal is', p)
    print('The time period is', t)
    print('The rate of interest is',r)
    #fill
    print('The Simple Interest is', si) 
P = int(input("Enter the principal amount :")
T = int(input("Enter the time period :"))
R = int(input("Enter the rate of interest :"))
simple_interest(P,T,R)
        ''')
        user_input = st.text_area("Enter your code:", key="code_infilling_input")
        if st.button("Infill Code"):
            with st.spinner('Infilling code...'):
                response = send_message(user_input, "code_infilling")
                st.code(response)
    elif task == "Generate Unit Tests":
        st.write("### Generate Unit Test Cases")
        user_input = st.text_area("Enter your code:", key="generate_unit_tests_input")
        if st.button("Generate Unit Tests"):
            with st.spinner('Generating unit tests...'):
                response = send_message(user_input, "generate_unit_tests")
                st.code(response)
    elif task == "Find Bugs and Optimize code":
        st.write("### Find Bugs")
        st.write("##### Upload your .py file of your code to check for bugs")
        uploaded_file = st.file_uploader("File Upload", type=["py"])
        if uploaded_file is not None:
            file_contents = uploaded_file.getvalue().decode("utf-8")
        if st.button("Find Bugs"):
            with st.spinner('Finding bugs...'):
                response = send_message(file_contents, "find_bugs")
                st.write(response)
    elif task == "Doc-String Preparation":
        st.write("### Doc-string for your code ")
        st.write("### Paste your code below for providing docstring")
        user_input = st.text_area("Enter your code:", key="doc_string_input")
        if st.button("Generate Doc-String"):
            with st.spinner('Generating doc-string...'):
                response = send_message(user_input, "generate_doc")
                st.code(response)
    elif task == "Git Commit Analysis":
        user_input_1 = st.text_area("Enter your code:", key="git_input")
        user_input_2 = st.text_area("Enter your code:", key="git_input_1")
        if st.button("Git Commit Analysis"):
            with st.spinner('Analyzing git commits...'):
                response = send_message(user_input_1, "git_commit", user_input_2)
                st.write(response)


if __name__ == "__main__":
    main()
