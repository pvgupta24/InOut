from .aqgFunction import *


# Main Function
def getAnswers(inputText):
    # Create AQG object
    aqg = AutomaticQuestionGenerator()

    # inputTextPath = "/Users/anumehaagrawal/Documents/Hacks/InOut/sample.txt"
    # readFile = open(inputTextPath, 'r+', encoding="utf8")
    # #readFile = open(inputTextPath, 'r+', encoding="utf8", errors = 'ignore')

    # inputText = readFile.read()
    # #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

    questionList = aqg.aqgParse(inputText)
    answers = aqg.display(questionList)

    return answers



