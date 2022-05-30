from gtts import gTTS

pdfToString = ""
try:
    try:
        with open('./output.txt', 'r+') as f:
            pdfToString += f.read()
    except Exception as e:
        print('File output.txt not found')
        print(e)
        exit()

    pdfToSpeech = gTTS(pdfToString, lang='es')
    pdfToSpeech.save('./output_audio.mp3')

except Exception as e:
    print(e)

