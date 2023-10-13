import os
import subprocess
import sys
import re

# Function to run a script from a Markdown file using specified Python version
def runMdWithPythonVersion(mdFilePath,pythonVersion):

    """
    Execute Python code from a Markdown file using a specified Python version.

    Args:
        mdFilePath (str): The path to the Markdown file.
        pythonVersion (str): The Python version to use in the Docker container.

    Returns:
        None
    """

    # File existence validity check
    if not os.path.exists(mdFilePath):
        print(f"Error!: {mdFilePath} doesn't exist")
        return
    
    # Open and read Markdown file
    with open(mdFilePath, "r") as file:
        markdownChunks = file.read()

    chunks = re.findall(r'```(python|sql|bash)(.*?)```', markdownChunks, re.DOTALL)
    
    # Dictionary to track variables and their values across chunks
    variables = dict()

    for language, chunk in chunks:
        try:
            # Adding support for bash scripts
            if language == "bash":
                result = subprocess.run(chunk, shell=True, text=True, check=True, stdout=subprocess.PIPE)

            # Execute each chunk in a Docker container with the specified Python version
            dockerCMD = f"docker run --rm -i python:{pythonVersion}"

            # Recall variable assignemnts from previous chunks
            for variable,value in variables.items():
                chunk = f"{variable} = {value}\n{chunk}"

            result = subprocess.run(dockerCMD, shell=True, input=chunk, text=True, check=True, stdout=subprocess.PIPE)
            output = result.stdout
            

            # Update variables dictionary
            variableAssignments = re.findall(r'(\w+)\s*=\s*(.*)', output)
            for variable,value in variableAssignments:
                variables[variable] = value 

        except subprocess.CalledProcessError as e:
            print(f"Error!: Docker command failed with exit code {e.returncode}") 
        
        except Exception as e:
            print(f"Error!: Execution of {language} code failed: {e}")

if __name__ == "__main__":
    # Retrieve CLI arguments
    cliArguments = sys.argv
    
    # Number of CLI arguments validity check
    if len(cliArguments) != 4:
        print("Usage: python run-with-version.py <mdFilePath> --version <pythonVersion>")

    else:
        mdFilePath = cliArguments[1]
        pythonVersion = cliArguments[3]

        # Function call to handle main logic
        runMdWithPythonVersion(mdFilePath,pythonVersion)