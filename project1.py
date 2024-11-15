import ollama
import re
import subprocess

# Create a class for  Agent that asks job-related questions and stores all messages."
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
#  Calling the claas
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
# Reach the LLM to get the answer
    def execute(self):
        response = ollama.chat(
                        model='llama3:8b', 
                        # temperature=0,
                        messages=self.messages)
        return response['message']['content']   #Return the answer



# Function to extract the code part from the LLM's answer.
def extracted_code(text):
    pattern = r"#Template code:\s*(.*?)\s*(#End of code Template)" 
    match = re.search(pattern, text, re.DOTALL)
   # Extract and display the code if the match is found
    if match:
        code_text = match.group(1).strip()  # Extract the code part and remove any surrounding whitespace
        # print("Extracted code:\n", code_text)        
        return code_text
    else:
        print("No matching code block found.")


#syastem messege:
System_descrpt = ''' You are a software developer working with Python and should suggest code 
based on user prompts. The code must follow a fixed template for easy extraction in the next
 step. Start the suggested code with the statement "Template code:" and end it with "#End of 
 code Template." The generated code should not include print statements or output handling
for the given inputs. It should only consist of the function(s) or class(es) that address
 the problem.

Example session:
Question: Write a code that finds the minimum number of two numbers.

Answer:

Here is an example of how you can write a Python function to find the minimum of two numbers:

#Template code:
def find_min(a, b):
    return a if a < b else b
#End of code Template
It is important to use exactly this template format so that the code can be extracted in the next step.


After generating the code, a function will be used to extract only the code part from the 
message. Then, you will generate test code for the extracted code to verify its correctness 
over several iterations. The test code should only include the test class and related functionality.
'''
#create the class with system messege
Myagent = Agent(System_descrpt)



## Get the description from the user.
# loopcondition = True
# while loopcondition: 
#     code_descrpt = input("Please enter the description of code you want to create? ")
   
#     if code_descrpt:
#         loopcondition= False

code_descrpt="write a code in Python that sort numbers in a list, without using builted function sorted ?"
generate_code = Myagent(code_descrpt) # text of code generate from agent 
# print(generate_code)
extract_code=extracted_code(generate_code) # the exracted part related to code
# print(extract_code)



#description for creating test file
test_descrpt='''The generated code for the description {} is {}, now generate a test file for
 this code. Only generate the class related to it, without including the description or 
 imports. The test should use unittest, and at the end of the test, include:
 if __name__ == '__main__':
    unittest.main()
 The template should be like code file:

#Template code:
Put code here
if __name__ == '__main__':
    unittest.main()
#End of code Template 
 '''.format(System_descrpt,code_descrpt)

generate_test= Myagent(test_descrpt) # text of test code generate from agent  
# print(generate_test)

extract_test =extracted_code(generate_test)
# print(extract_test)

# save code and test code both in a python file 
code_test_file=extract_code + "\n" +"import unittest"+"\n"+ extract_test
with open("test_code.py", "w") as file:
    file.write(code_test_file)
    

code_pass=0 # number of time code did not pass and changed 
test_pass=0 # number of time that code was good and fixed and around of test perform
while ((test_pass < 3) and (code_pass<5)):
    # run the test code
    run_result = subprocess.run(["python3", "-m", "unittest","test_code.py"], capture_output=True, text=True)
    # Print the output and any errors
    # print("Output:", run_result.stdout)
    # print("Errors:", run_result.stderr)
    if "FAILED" in run_result.stderr: # check if the code did not pass the test 
        print("the code has not pass and failed testing ")
        #generate new code base on errors
        codefail_descrpt='''The code {} did not pass the test code {}, and encountered the 
        following errors: {}. Please regenerate the code with fixes to address these issues,
        using the template introduced earlier.
        #Template code:
    def find_min(a, b):
    return a if a < b else b    
    #End of code Template
        '''.format(extract_code,extract_test,run_result.stderr)
        
        generate_code = Myagent(codefail_descrpt)
        extract_code=extracted_code(generate_code) # extract new code
        print(extract_code)
        test_pass=0  # because of new code generated , the test round reset
        code_pass +=1 # add one round for code fail

    newtest_descrpt='''Create a new set of test file for the code {} using the previously discussed template.
    The test should use unittes
    #Template code:
    Put code here
    if __name__ == '__main__':
    unittest.main()
    #End of code Template
    '''.format(extract_code)
    generate_test = Myagent(newtest_descrpt)
    extract_test=extracted_code(generate_test)      
    test_pass=test_pass+1 # add one round for test passsing
    testcode=extract_code +"\n" +"import unittest"+"\n" +extract_test
    with open("test_code.py", "w") as file:
        file.write(testcode)

if code_pass >= 10:
    print("the code didnt pass the test after seveal time updates and test")
elif test_pass>=5:
    print("the code is correct and pass several test. the final code is:")
    print(extract_code)        
print("done")





