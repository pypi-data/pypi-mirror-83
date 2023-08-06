import docx
import matplotlib.pyplot as plt
import PyPDF4
import random
import re

class GetText:
    def get_pdf(filepath=None):
        
        if filepath == None:
            raise Exception("Missing one argument: provide filepath")
        else:
            if type(filepath) != str:
                raise Exception("Type error: filepath has to be type str")
        
        filepath = filepath.strip().lower()

        try:
            pdf = open(filepath,'rb')
            pdf = PyPDF4.PdfFileReader(pdf)
        except:
            raise Exception("Filepath error: provide valid filepath to a PDF")
            pass

        content = ""
        pages = pdf.numPages

        for i in range(pages):

            page = pdf.getPage(i)
            page_text = page.extractText()

            content = content + page_text + " "

        return content

    def get_doc(filepath=None):

        if filepath == None:
            raise Exception("Missing one argument: provide filepath")
        else:
            if type(filepath) != str:
                raise Exception("Type error: filepath has to be type str")

        filepath = filepath.strip().lower()

        try:
            document = docx.Document(filepath)
        except:
            raise Exception("Error: provide valid filepath to docx file")
            pass

        content = ""

        for paragraph in document.paragraphs:
            txt = paragraph.text

            content = content + txt.strip() + " "

        return content

class Chart:
    
    def create(src=None, top=10, other=False, text_title = None, common_words='default'):
        
        if src == None:
            raise Exception("Missing one argument: provide source text")
        else:
            if type(src) != str:
                raise Exception("Type error: text has to be type str")
                
        if top < 5:
            raise Exception("Int error: argument top has to have minimum value of 5")
        if top == 'all':
            top = len(values.keys())
            
        if common_words == 'default':
            common_words = ["the", "be", "to", "of", "and", "a", "an", "in", "", "is", "you", "but", "for", "i"]
        elif common_words == 'none':
            common_words = []
        elif common_words == 'strict':
            common_words = ["the", "be", "to", "of", "and", "a", "an", "in", "", "is", "you", "but", "for", "i", "with", 
                     "it", "my", "me", "us"]
        elif type(common_words) == list:
            pass
        else:
            raise Exception("Type error: common_words has to be preset or list")
                
        values = Chart.count_words(txt=src, common=common_words)

        counts = {}
        nums = set()

        for key, value in values.items():
            nums.add(value)
            if value in counts.keys():
                counts[value].append(key)
            else:
                counts[value] = [key]

        nums = sorted(list(nums), reverse=True)
        top_words = []

        for num in nums:
            words = counts[num]

            for word in counts[num]:
                if len(top_words) >= top:
                    pass
                else:
                    top_words.append(word)

            if len(top_words) >= top:
                break

        other = 0

        for key, value in values.items():
            if key in top_words:
                pass
            else:
                other += values[key]

        sizes = [values[word] for word in top_words]
        
        if text_title == None:
            text_title = f"Top {len(top_words)} words in text"

        if not len(values.keys()) < 10 and other == True:
            top_words.append("OTHER WORDS")
            sizes.append(other)
        else:
            pass
        
        Chart.bar(labels = top_words, values = sizes, title=text_title)

            
    def count_words(common, txt=None):
        
        txt = txt.replace("\n", " ")
        punctuation = ",./?:;-\'\"\\!@#$%^&*()[]{}<>_+=–"
        
        for char in punctuation:
            txt = txt.replace(char, "")

        word_list = txt.lower().strip().split(" ")

        word_dict = {}

        for word in word_list:
            if str(word) in word_dict.keys():
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        
        for c in common:
            if c in word_dict.keys():
                del word_dict[c]
                
        return word_dict
            
    
    def bar(labels=None, values=None, title=None):
        
        if labels == None:
            raise Exception("Missing one argument: provide labels")
        elif values == None:
            raise Exception("Missing one argument: provide values")
        elif title == None:
            raise Exception("Missing one argument: provide title")
        else:
            pass
        
        plt.barh(labels, values)
        plt.title(title)
            
        
        plt.xlabel('Count')
        plt.ylabel('Words')

        plt.show()

class Tools:
    
    def grade_level(text=None):
        
        if text == None:
            raise Exception("Missing one argument: provide text")
        elif type(text) != str:
            raise Exception("Type error: text has to be type str")
            
        words = text.replace("\n", " ")
        words = words.split(" ")
        bad_chars = ["", " "]
        
        for x in words:
            if x in bad_chars:
                words.remove(x)
        
        syllables = 0
        
        for word in words:
            syllables += Tools.syllables(word)
        
        word_len = syllables/len(words)
        
        txt = text.splitlines()
        txt = ".".join(txt)
        
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', txt)
        
        count = len(sentences)
        
        sent_len = len(words)/count
        
        grade_level = round((0.39*sent_len) + (11.8*word_len) - 15.59, 1)
        
        return grade_level
    
    def reading_ease(text=None):
        
        if text == None:
            raise Exception("Missing one argument: provide text")
        elif type(text) != str:
            raise Exception("Type error: text has to be type str")
            
        words = text.replace("\n", " ")
        words = words.split(" ")
        bad_chars = ["", " "]
        
        for x in words:
            if x in bad_chars:
                words.remove(x)
        
        syllables = 0
        
        for word in words:
            syllables += Tools.syllables(word)
        
        word_len = syllables/len(words)
        
        txt = text.splitlines()
        txt = ".".join(txt)
        
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', txt)
        
        count = len(sentences)
        
        sent_len = len(words)/count
        
        reading_ease = round(206.835 - (1.015 * sent_len) - (84.6 * word_len), 1)
        
        if reading_ease > 100:
            return 100
        elif reading_ease < 0:
            return 0
        else:
            return reading_ease

    def syllables(word=None):
        
        if word == None:
            raise Exception("Missing one argument: provide word")
        elif type(word) != str:
            raise Exception("Type error: word has to be type str")
        
        word = word.lower().strip()
            
        if len(word) <= 3:
            return 1
        
        count = 0
        vowels = "aeiouy"
        
        if word[0] in vowels:
            count += 1
            
        for index in range(1, len(word)):
            
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
                
        if (word.endswith("e") and not word.endswith("le")) or word.endswith("ed") or word.endswith("es"):
            count -= 1
            
        if count == 0:
            count += 1
        
        return count
    
    def split(text=None, length=None):
        
        if text == None:
            raise Exception("Missing one argument: provide text")
        elif type(text) != str:
            raise Exception("Type error: text has to be type str")
            
        if length == None:
            raise Exception("Missing one argument: provide split length")
        elif type(length) != int:
            raise Exception("Type error: length has to be type int")
        elif length < 1 or length > len(text):
            raise Exception("Int error: length has to be in between 1 and len(text)")
            
        split_text = [text[n:n+length] for n in range(0, len(text), length)]
        return split_text
    
    def sarcastext(text=None):
        
        if text == None:
            raise Exception("Missing one argument: provide text")
        elif type(text) != str:
            raise Exception("Type error: text has to be type str")
            
        sarcastic = ""
        
        for char in text: 
            if random.randint(0, 1) == 0:
                sarcastic += char.upper()
            else:
                sarcastic += char.lower()
                
        return sarcastic
    
    def table(data=None, sides = ["|", "_"]):

        if data == None:
            raise Exception("Missing one argument: provide table data")
        elif type(data) != dict:
            raise Exception("Type error: data has to be type dict in format {k:v, k2:v2}")

        if type(sides) != list:
            raise Exception("Type error: sides has to be type list in format [vertical, horizontal]")
        elif len(sides) != 2:
            raise Exception("Length error: sides has to be in format [vertical, horizontal]")

        if len(sides[0]) != 1 or len(sides[1]) != 1:
            raise Exception("Length error: sides items should have len 1")

        longest_k = 0
        longest_v = 0
        
        # n is only for my personal usage and for later updates
        n = 0

        v = sides[0]
        h = sides[1]

        for key, value in data.items():

            n +=1

            if len(str(key)) > longest_k:
                longest_k = len(str(key))

            if len(str(value)) > longest_v:
                longest_v = len(str(value))

        length = (3+longest_k)*h + (3+longest_v)*h + 3*h
        
        output = ""
        
        output = output + length + "\n"

        for key, value in data.items():
            key = str(key)
            value = str(value)
            
            output = output + v + (3+longest_k)*" " + v + (3+longest_v)*" " +v + "\n"
            output = output + v+" "+ key + ((longest_k - len(key))+2)*" " + v + " "+value+((longest_v - len(value))+2)*" "+v + "\n"
            output = output + v + (3+longest_k)*" " + v + (3+longest_v)*" " +v + "\n"
            output = output + length
            
        return output
