
import codecs
from flask import *
from forms import StemmingForm
class Stemming:
    def __init__(self):
        self.prefix_words=None
        self.stop_words=None
        self.postfix_words=None
        self.exception_words=None

    # load required files
    def loadFile(self):
        # prefix
        pre=codecs.open("pre1.txt","r","utf-8-sig")
        prefix=pre.read()
        self.prefix_words=tuple(sorted(prefix.split(),key=len,reverse=True)) # in order for long match
        #print(prefix_words)

        # postfix
        post=codecs.open("post1.txt","r","utf-8-sig")
        postfix=post.read()
        self.postfix_words=tuple(sorted(postfix.split(),key=len,reverse=True)) # long match
        #print(postfix_words)

        # stopwords
        stopW= codecs.open("stopword.txt", "r", "utf-8-sig")
        stopword= stopW.read()
        self.stop_words = tuple(stopword.split())
        #print(stop_words)

        # exceptions
        exceptionW= codecs.open("exception.txt", "r", "utf-8-sig")
        exception=exceptionW.read()
        self.exception_words=tuple(exception.split())
        #print(exception_words)

    # length rule
    def str_len(self,word):
        return len(word)<=2

    # remove the postfix
    def postfix_remove(self,word):
        oWord=word
        for pfix in self.postfix_words:
            if word.endswith(pfix):
                new_word=word.replace(pfix,'')
                if len(new_word)>1:
                	return new_word
                return oWord

    # remove the postfix
    def prefix_remove(self,word):
        oWord=word
        for prefx in self.prefix_words:
            if word.startswith(prefx):
                new_word=word.replace(prefx,'')
                if len(new_word)>1:
                	return new_word
                return oWord

    # check if the word is stopword
    def isStopword(self,word):
        return word in self.stop_words

    # check if the word is exception word
    def isException(self,word):
        return word in self.exception_words

     #removes duplicate
    def remove_duplicate(self,word):
        val={"ሃሀ":"ሀ","ላለ":"ለ","ላል":"ለ","ሓሐ":"ሐ","ማመ":"መ","ራረ":"ረ","ሳሰ":"ሰ","ሻሸ":"ሸ","ቃቀ":"ቀ",
        "ቓቐ":"ቐ","ባበ":"በ","ቫቨ":"ቨ","መፅ":"መፀ","መፂ":"መፀ","መፁ":"መፀ","ታተ":"ተ","ቻቸ":"ቸ","ላዕ":"ልዐ","መፃ":"መፀ","ናነ":"ነ",
        "ኛኘ":"ኘ","ኣአ":"አ","ካከ":"ከ","ኻኸ":"ኸ","ዋወ":"ወ","ዓዐ":"ዐ","ዛዘ":"ዘ","ዣዠ":"ዠ",
        "ከድ":"ከደ","ከዱ":"ከደ","ከዳ":"ከደ","ያየ":"የ","ዳደ":"ደ","ጣጠ":"ጠ","ጫጨ":"ጨ","ፃፀ":"ፀ","ፋፈ":"ፈ","ፓፐ":"ፐ"}
        new_word=word
        for w in val.keys():
            if w in word:
                new_word=word.replace(w,val[w])
                return new_word
        return new_word
    # rule for words with len of two
    def ruleTwo(self,word): # Not implimented yet
        wTwo={"ከድ":"ከደ","መፃ":"መፀ","መፅ":"መፀ"}
        new_word=word
        for w in val.keys():
            if w in word:
                new_word=word.replace(w,val[w])
                return new_word
        return new_word
    # stemming process
    def Stem_It(self,input_snt):
        stem_result = ''          # a variable that holds the stemmed result
        space = ' '
        for word_index in range(len(input_snt)):
            Tword=input_snt[word_index]
            if self.isStopword(Tword):
                continue
            elif self.isException(Tword) or self.str_len(Tword):
                stem_result += space + Tword
            elif Tword.endswith(self.postfix_words):
                step1=self.postfix_remove(Tword)
                if self.str_len(Tword):
                    stem_result += space + step1
                elif step1.startswith(self.prefix_words):
                    step2 = self.prefix_remove(step1)
                    stem_result += space + step2
                else:
                    stem_result += space + step1
            elif Tword.startswith(self.prefix_words):
                step3 = self.prefix_remove(Tword)
                stem_result += space + step3
            else:
                stem_result += space + Tword
        return stem_result

# accept input to be stemmed


s=Stemming()
s.loadFile()

# save the result in file [optional]
#with open("output.txt", "w",encoding='utf-8') as f:
    #f.write(result)
#f.close()
app=Flask(__name__)
app.config['SECRET_KEY']='73df9820f333e51e87754216a4af35a473717b2b17f66e33b19e5ccff584012d'
@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/stem", methods=['GET','POST'])
def stem():
    form=StemmingForm(request.form)
    if request.method == 'POST':
        characters= request.form ['characters']
        input_snt=characters.split()
    if form.validate():
            last_val=s.remove_duplicate(s.Stem_It(input_snt))
            flash(last_val)

    #return redirect (url_for('stem'))
    return render_template('stem.html', title= stem, form= form)




if __name__ == '__main__':
    app.run(debug=True)
