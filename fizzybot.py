# Interactive python client for fizzbot

import json
import urllib.request
import urllib.error

domain = 'https://api.noopschallenge.com'


FIZZ = False
NOOP = False
INIT = True
answer = ""


def print_sep(): print('----------------------------------------------------------------------')

def FizzBuzz(numbers):
    answer = ""

    for n in numbers:
        if n%3==0 and n%5==0:
            answer = answer + "FizzBuzz "
        elif n%3==0:
            answer = answer + "Fizz "
        elif n%5==0:
            answer = answer + "Buzz "
        else:
            answer = answer + str(n) + " "
    
    lnth = len(answer)
    return answer[:lnth-1]

def Beep(numbers):
    answer = ""

    for n in numbers:
        if n%2==0 and n%5==0:
            answer = answer + "BeepBoop "
        elif n%2==0:
            answer = answer + "Beep "
        elif n%5==0:
            answer = answer + "Boop "
        else:
            answer = answer + str(n) + " "
    
    lnth = len(answer)
    return answer[:lnth-1]

def MeetTheNoops(numbers):
    answer = ""

    for n in numbers:
        if n%3==0 and n%5==0 and n%7==0:
            answer = answer + "MeetTheNoops "
        elif n%3==0 and n%5==0:
            answer = answer + "MeetThe "
        elif n%3==0 and n%7==0:
            answer = answer + "MeetNoops "
        elif n%5==0 and n%7==0:
            answer = answer + "TheNoops "
        elif n%3==0:
            answer = answer + "Meet "
        elif n%5==0:
            answer = answer + "The "
        elif n%7==0:
            answer = answer + "Noops "
        else:
            answer = answer + str(n) + " "
    
    lnth = len(answer)
    return answer[:lnth-1]

def match(msg, num):
    global answer, FIZZ, NOOP

    print(num)
    if ('final challenge' in msg):
        print('----- Noops -------')
        NOOP = True
    elif 'Beep' in msg:
        print('----- Beep -------')
        FIZZ = False
    elif 'Fizz' in msg:
        print('----- Fizz -------')
        FIZZ = True
    
    if FIZZ and (num is not None):
        answer = FizzBuzz(num)
    elif (NOOP) and (not FIZZ) and (num is not None):
        answer = MeetTheNoops(num)
    elif (not FIZZ) and (num is not None):
        answer = Beep(num)
    

# print server response
def print_response(dict):
    print('')
    print('message:')
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

    match(dict.get('message'), dict.get('numbers'))

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        print_response(response)
        print_sep()
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

# keep trying answers until a correct one is given
def get_correct_answer(question_url):
    global INIT, FIZZ, answer, NOOP
    while True:
        if INIT:
            answer = input('Enter your answer:\n')
            INIT=False
        elif NOOP:
            answer = answer
            NOOP = False
        elif FIZZ:
            answer = answer

        response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        if (response.get('result') == 'correct'):
            return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url):
    print_sep()
    print('*** GET %s' % question_url)

    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    if next_question: return next_question
    return get_correct_answer(question_url)



def main():
    question_url = '/fizzbot'
    while question_url:
        question_url = do_question(domain, question_url)

if __name__ == '__main__':
     main()