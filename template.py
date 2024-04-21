from langchain.prompts import PromptTemplate
def prompt_gitanalysis(message1, message2):
    prompt = PromptTemplate.from_template("""Analyze the provided code snippets (message1 and message2) and generate a summary report in the following format:

Original Code:

{message1}

Modified Code:

{message2}

Summary of Changes:

    Identify which code snippet represents the original code (message1 or message2) and which one is the modified version.
    Describe the overall changes made between the two code versions. This could include:
        Added functionality: New features or logic introduced in the modified code.
        Removed functionality: Features or logic removed from the original code.
        Refactored code: Modifications made to improve code structure, readability, or efficiency.
        Bug fixes: Specific bugs or errors addressed in the modified code.
    Highlight any key changes: If there are specific changes that are particularly important or impactful, mention them here (e.g., changes in algorithms, data structures, or performance).
""",
                                          template_format='f-string',
                                          partial_variables={'message1': message1, 'message2': message2})
    # print(prompt)
    return prompt


def prompt_generation(message):
    prompt = PromptTemplate.from_template(
        f"""You are an expert Python programmer. Your task is to generate Python code that accomplishes the following:
    {message} Please provide a step-by-step explanation of your code, including the purpose of each part and how it contributes to the overall functionality. Ensure the code is efficient, readable, and well-documented.Give the complete code in the end""",
        template_format='f-string', partial_variables={'message': message})
    return prompt


def prompt_autocomplete(message):
    prompt = PromptTemplate.from_template(""" You are an advanced AI with expertise in Python programming. Your task is to assist with code auto-completion for the following code snippet: 
    {message}
This code snippet is incomplete, and your mission is to identify the missing or incomplete parts. Once identified, you are to provide a complete version of the code, ensuring it is syntactically correct, logically sound, and follows Python best practices.
Please consider the following when completing the code:
- **Contextual Understanding**: Understand the purpose and functionality of the incomplete code. What is it supposed to do?
- **Syntax and Logic**: Ensure the completed code is syntactically correct and logically sound. It should perform the intended task without errors.
- **Best Practices**: Follow Python best practices for coding standards, including naming conventions, code structure, and documentation.
- **Comprehensive Completion**: If the code snippet is part of a larger function or program, ensure the completion is coherent with the rest of the code. Provide the entire function or program if necessary.
If the code snippet is part of a larger function or program, provide the entire function or program with the completed code.""",
                                          template_format='f-string', partial_variables={'message': message})
    return prompt


def prompt_testing(message):
    prompt = PromptTemplate.from_template("""
        You are an expert in testing Python codes. Your task is to create comprehensive unit test cases for the following code snippet: {message}
Please consider the following when generating your unit tests:
- **Coverage**: Ensure that the tests cover a wide range of inputs, including typical use cases, edge cases, and error conditions.
- **Robustness**: The tests should be robust and able to handle unexpected inputs or behaviors gracefully.
- **Maintainability**: The tests should be easy to understand and maintain, with clear and descriptive names for each test case.
Return the generated unit test with an example and the expected output code as follows:
# Function to test
{message}   
# Unit tests
def test_function_name():
    # Test case 1: Description of the test case.
    # Test case 2: Description of the test case.
    # ...""", template_format='f-string', partial_variables={'message': message})
    return prompt


def prompt_bug(message):
    #print(message)
    prompt = PromptTemplate.from_template("""
        You are an expert in testing Python codes. Your task is to find all the bugs in the given code : 
        {message}
        once you have identified all the error, rectify the error and return the code  with explanation.""",
    template_format='f-string', partial_variables={'message': message})
    #print(prompt)
    return prompt


def prompt_doc(message):
    prompt = PromptTemplate.from_template("""You are an expert at understanding the given code.Provide docstring for {message} .After giving docstring continue the code. The docstring should be in the following format: 
    def your_function_name(your_parameters):   
    "
    Brief description of what the function does.
    Parameters:
    - your_parameters (type): Description of the parameter.
    Returns:
    - return_type: Description of what the function returns.
    "
    """, template_format='f-string', partial_variables={'message': message})
    return prompt
