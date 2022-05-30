import argparse 
import os 
import openai
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi as YtA
import pdfplumber

api_key = open('API_KEY', 'r+').read().splitlines()[0]
openai.api_key = api_key

parser = argparse.ArgumentParser(description='Python CLI For Text summarization (Ekatra-Hackathon)')
parser.add_argument('-input', type=str, required=True, help="-input <URL|Path> Provide file URL/Path")
parser.add_argument('-type', type=str, required=True, help="-type <OPTION> OPTIONS [t]ext file | [p]df file | [w]eb article link | [y]outube link")

args = parser.parse_args()

class Summarizer:
    def __init__(self , data):
        self.data = data

    #call_openai() method to connect with GPT-3
    def call_openai(self, prompt_var):
        try:
            return openai.Completion.create(engine="text-davinci-002", prompt=prompt_var, temperature=0, max_tokens=300, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
        except Exception as e:
            print(e)
            exit()

    def generate(self, value, link_text):
        prompt_var = f"""
Generate {value} From {link_text}
{link_text} : {self.data}
"""
        response = self.call_openai(prompt_var).choices[0].text.strip()
        return response

    def generate_pdfsummary(self):
        prompt_var = f'''Generate Summary in number list for text
        Text : {self.data}'''
        return self.call_openai(prompt_var).choices[0].text.strip()
    
def filter_keypoint_keyterms(key_points, key_terms):

    #filter key points into list form
    pattern_key_p = "\n\d\)|\n-|\n\d.|\n\d-"
    raw_keypoints = re.split(pattern_key_p, key_points)
    key_points_l = [value.strip() for value in raw_keypoints]

    #filter key terms into list form
    pattern_key_t = "\n\d\)|\n-|\n\d.|\n\d-|,"
    raw_keyterms = re.split(pattern_key_t, key_terms)
    key_terms_l = [value.strip() for value in raw_keyterms]

    return key_points_l[1:], key_terms_l[1:]

def generate_outputfile(data, text_link):
    sum_obj = Summarizer(data)

    summary = sum_obj.generate('Summary', text_link)
    key_points = "\n"+sum_obj.generate('Key Points', text_link)
    key_terms = "\n"+sum_obj.generate('Key Terms', text_link)
    key_points_l, key_terms_l = filter_keypoint_keyterms(key_points, key_terms)

    dict = {
        "Summary":summary
        ,"Key Points":key_points_l
        ,"Key Terms":key_terms_l
    }

    with open('output.json', 'w+') as fp:
        json.dump(dict, fp)

    with open('output.txt','w+') as f:
        output = f"""
Summary :
{summary}

Key Points :
{key_points.strip()}

Key Terms :
{key_terms.strip()}
"""
        f.write(output)


def main(url_path, file_type):

    if (file_type == 't'): #if input is text file
        try: #Checking if file exist at the given path or not
            with open(url_path, 'r+') as f:
                data = f.read()
                f.close()
        except Exception as e: #raise an error if file does not exist
            print(e)
            exit()

        generate_outputfile(data=data, text_link='Text') #calling output function
   

    elif (file_type == 'w'): #if the input is web article link

        generate_outputfile(data=url_path, text_link="Link")

    elif (file_type == 'y'): #if input is youtube video link

        video_id = url_path.split("=")[1] #extracting video id from the youtube link

        try:
            raw_data = YtA.get_transcript(video_id) #pulling a transcript of the video
            data = """ """

            for value in raw_data:
                data += value['text'] + " " 

            generate_outputfile(data, "Text") #calling output function
        except Exception as e:
            print("Transcript For Youtube Video Not Available. Try Other Video Link")
            print(e)
            exit()
    
    elif (file_type == 'p'): #if input is pdf file

        try:
            url_l = url_path.split("-")
            
            url_path = url_l[0]
            
            if len(url_l) == 3:
                try:
                    start_page = int(url_l[1])
                    end_page = int(url_l[2])
                except Exception as e:
                    print(e)
                    exit()

            elif len(url_l) == 2:
                try:
                    start_page = int(url_l[1])
                    end_page = start_page
                except Exception as e:
                    print(e)
                    exit()
            elif len(url_l) == 1:
                try:
                    start_page = 1
                    end_page = len(pdfplumber.open(url_path).pages)
                except Exception as e:
                    print(e)
                    exit()
            else:
                print("Error Try Again")
                exit()

            with pdfplumber.open(url_path) as pdf: #read pdf file

                f = open('output.txt', 'w+')
                f.write('Summary : \n\n')
                dict_summary = {'Summary' : []}

                for page_no in range(start_page, end_page+1):
                    page = pdf.pages[page_no]
                    data =  ''

                    data = page.extract_text()

                    sum_obj = Summarizer(data)
                    summary = "\n"+sum_obj.generate_pdfsummary()

                    pattern_key_p = "\n\d\)|\n-|\n\d.|\n\d-" # filter data
                    raw_summary = re.split(pattern_key_p, summary)[1:]
                    new_summary = " ".join([value.strip() for value in raw_summary])

                    dict_summary['Summary'].append({page_no:new_summary})
                    f.write(f'Page # {page_no} :'+'\n')
                    f.write(f'{new_summary}' + '\n\n')

                f.close()

            with open('output.json', 'w+') as fp:
                json.dump(dict_summary, fp)
                fp.close()

        except Exception as e:
            print(e)
            exit()


def read_input_values():

    url_path = args.input 
    type = args.type 

    type_l = ('t','p','w','y')

    if type not in type_l:
        print("""Choose the correct file type
t : text file
p : pdf file
w : web article link
y : youtube link
""")
        exit()
    else:
        main(url_path, type)


if __name__ == "__main__":
    read_input_values()
