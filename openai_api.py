# Analysis of two speakers using integration to OpenAI with API

import os
import openai

# change directory
my_directory = "/Users/oleg_vysotskyy/Documents/Work/Python"
os.chdir(my_directory)
print(my_directory)

# define a secret key

from openai import OpenAI
client = OpenAI()


def analyze_files_with_prompt(prompt, file_paths):
    results = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            content = f.read()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI assistant analyzing uploaded files."},
                    {"role": "user", "content": f"{prompt}\n\nFile content:\n{content}"}
                ],
                # max_tokens=500,
                temperature=0
            )
            results.append({"file": file_path, "response": response.choices[0].message.content})
    return results


# File paths for speeches
folder_path = '/Users/oleg_vysotskyy/Documents/Work/Python/Speeches/Decoded'
files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# Group files into two categories by speaker
speaker1_files = [file for file in files if "Trump" in file]
speaker2_files = [file for file in files if "Harris" in file]

speaker1_results = "Trump_all_speeches.txt"
speaker2_results = "Harris_all_speeches.txt"


# Loop  entering name of file with prompt until input is 'done'
while True:
    prompt_file = input(f"\nEnter file name with prompt or put 'done' for exit: ")
    if prompt_file.lower() == "done":  # Break when the user types 'done'
        break
    else:
        # read prompt from file
        file_i = open(prompt_file, 'r')
        prompt = file_i.read()
        file_i.close()

	# analyze files using a prompt
        print(f"\nRequesting OpenAI for analysis of speaker1...")
        analysis1_results = analyze_files_with_prompt(prompt, speaker1_files)
        print("Done")

        file_o = open("Trump_all_speeches_results.txt", 'w')

        for element in analysis1_results:
            for key, value in element.items():
                print(f"  {key}: {value}")
                file_o.write(f"\n{key}: {value}")

        file_o.close()
            
        print(f"\nRequesting OpenAI for analysis of speaker2")
        analysis2_results = analyze_files_with_prompt(prompt, speaker2_files)
        print("Done")

        file_o = open("Harris_all_speeches_results.txt", 'w')

        for element in analysis2_results:
            for key, value in element.items():
                print(f"  {key}: {value}")
                file_o.write(f"\n{key}: {value}")

        file_o.close()
            
        print(f"\nSpeeches analysis have been done and stored in\n", speaker1_results, f"\n", speaker2_results)
    

