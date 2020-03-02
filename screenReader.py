try:
    from PIL import Image
    from PIL import ImageGrab
except ImportError:
    import Image
import pytesseract
import time
import numpy as np
import mss
import sys
from googletrans import Translator
import tkinter as tk

#set path of tesseract
pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract'

class ScreenReader:
    def __init__(self):
        self.imageVar = 'Capture.png'
        self.root = tk.Tk()

        self.output_text = tk.StringVar()
        self.output_label = tk.Label(self.root, textvariable=self.output_text, font=("Helvetica", 16), width=100, height=30).pack()


    def getmouseloc(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        return x, y


    def screen_record(self):
        translator = Translator()
        last_time = time.time()
        with open('file.txt', 'w+', encoding='utf-8') as f, mss.mss() as sct:
            for i in range(0,sys.maxsize):
                start_time = time.time()
                
                # screencapture
                mon = {"top":160, "left": 0, "width": 960, "height": 270}
                screencap = sct.grab(mon)
                mss.tools.to_png(screencap.rgb, screencap.size, output="screenshot.png")
                printscreen = Image.fromarray(np.asarray(screencap))

                scr_time = time.time() - start_time
                #print('screencapture took {} seconds'.format(scr_time))

                # apply ocr
                output = pytesseract.image_to_string(image=printscreen, lang='jpn')

                ocr_time = time.time() - start_time - scr_time
                #print('ocr-ing took {} seconds'.format(ocr_time))

                # translate text

                print(output)
                output = str(translator.translate(output, src='ja', dest='en'))

                trans_time = time.time() - start_time - ocr_time
                #print('translating took {} seconds'.format(trans_time))

                # write text to file
                f.truncate(0)
                f.write(output)

                total_time = time.time() - start_time
                time_output = '''screencapture took {} seconds
    ocr-ing took {} seconds
    translating took {} seconds
    total took {} seconds'''.format(scr_time, ocr_time, trans_time, total_time)
                
                self.output_text.set(output + '\n\n\n\n\n' + time_output)
                self.root.update()

ScreenReader().screen_record()

