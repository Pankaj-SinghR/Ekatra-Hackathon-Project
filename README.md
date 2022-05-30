# Ekatra-Hackathon-Project
- #### Summarizer for Text File / PDF File / Web Article/ Youtube Podcast Video Using OpenAI GPT-3 Model API Build in Python3 (Python CLI)
- #### This tool can also Generate Audio file (.mp3) for output file (output.txt) using Google translation API
---
## Instructions for Setup
### Prerequisite
- ##### Python3 should be install in your system 
- ##### API KEY of OpenAI should be present
#### Clone this github repo
```
git clone https://github.com/Pankaj-SinghR/Ekatra-Hackathon-Project.git
```
#### Change directory
```
cd Ekatra-Hackathon-Project/Ekatra-Hackathon/
```
#### Add API key in API_KEY file
```
echo "YOUR API KEY GOES HERE" > API_KEY
```
- ######  Or simply copy & paste API key inside the API_KEY file if your are window user
#### Change directory to previous one
```
cd ..
```
#### Create a Virtual Environment for this project
```
python3 -m venv env
```
#### Activate the Virtual Environment
- ##### On Window
```
env\Scripts\activate.bat
```
- ##### On Linux & Mac OS
```
source env/bin/activate
```
#### Install all the dependencies using requirements.txt file
```
pip install -r requirements.txt 
```
---
## Instruction for using Python CLI tool for summarization
#### Change directory to the Ekatra-Hackathon Folder
```
cd Ekatra-Hackathon
```
### Types of Input Data
- #### Text file : <i> You can Summarize and text file data. If you want to summarize the paragraph create text file (*.txt) for it and put your data inside txt file </i>
- #### PDF file : <i> You can summarize pdf files. You can also mention any particular page number or can give a range of page numbers for summarization. If you only provide the path for pdf file it will summarize whole PDF </i>
- #### Web article : <i> To summarize web article you only have to provide the complete URL or web link. </i>
- #### Youtube podcast : <i> You can also summarize youtube podcast but subtitle for the video should be present. Provide the url as input </i>

### Arguments in the Python CLI tool
```
python3 main.py -h
```
- OUTPUT
```
usage: main.py [-h] -input INPUT -type TYPE

Python CLI For Text summarization (Ekatra-Hackathon)

optional arguments:
  -h, --help    show this help message and exit
  -input INPUT  -input <URL|Path> Provide file URL/Path
  -type TYPE    -type <OPTION> OPTIONS [t]ext file | [p]df file | [w]eb article link | [y]outube link
```

### Working of CLI Tool
- ### For Text file : Generate summary for text file
```
python3 main.py -input ./Data/text_file.txt -type t
```
##### CLI Tool Generate output.txt & output.json file as Output

- ### For PDF file : Generate summary for pdf file
- #### Summary for whole pdf
```
python3 main.py -input ./Data/pdf_file.pdf -type p
```
- #### Summary for any particular page number 
> let say page number is 45

```
python3 main.py -input ./Data/pdf_file.pdf-45 -type p
```
- #### Summary for any range of page number
> let say we want summary from page number 36 to 50

```
python3 main.py -input ./Data/pdf_file.pdf-36-50 -type p
```
- ### For web article : Generate summary for any web article
```
python3 main.py -input <pass your web article link here> -type w
```
- ### For Youtube video : Generate summary for any youtube video
```
python3 main.py -input <pass your youtube video link here> -type y
```
### About output file (output.txt/ ouput.json)
- #### Output file contains 
- ##### Summary
- ##### Key Points (Key points container important points from the input paragraph)
- ##### Key Terms (Key terms give intution about the summary and makes it easy to understand)

