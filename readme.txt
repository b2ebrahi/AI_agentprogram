Steps to Set Up and Run the AI Agent
Step 1: Install Ollama
Ollama is required to manage and run the Llama model.

For Linux
Download and install Ollama with the following command:

$curl -fsSL https://ollama.com/install.sh | sh

For macOS and Windows
Download the Ollama installer from the official website: https://ollama.com/

Verify Installation

Once installed, you can check that Ollama is properly set up by running:

$ollama

You should see output similar to:
=======================================
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.
======================================

Step 2: Download the Llama Model

Use Ollama to download the 3.8 billion parameter Llama model by running:

$ollama pull llama3:8b

This will download the required model.

Step 3: Create a Python Virtual Environment

Create a virtual environment to manage dependencies:

$python -m venv api_gen

Step 4: Activate the Virtual Environment

$source api_gen/bin/activate

Step 5: Install Dependencies

Use the provided requirements.txt file to install all required packages:

pip install -r requirements.txt

Step 6: Run the Project

Run the main Python script to start the AI agent:

$python project1.py

When prompted, you can enter the description of the code you'd like to create. For example:
=============================
Please enter the description of code you want to create? factorial
============================

The output will include a generated Python function along with testing :

================================
Here is an example of how you can write a Python function to calculate the factorial of a given number:

#Template code:
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)
#End of code Template
Another round of testing...
Another round of testing...
Another round of testing...
the code is correct and pass several test. the final code is:
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)
done

================================

Notes
Ensure Python 3.8 or higher is installed.
Make minor adjustments to the commands for macOS or Windows if necessary.











