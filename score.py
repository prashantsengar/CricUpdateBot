import requests
import time
import traceback
shout = {'4':'That\'s a four', '6':'Huge SIX', 'W':'A wicket fell down'}

##def show_score(msg):
##    

def get_score(url, ID, last_ball):
    print("here")
    try:
        global shout
        
        page = requests.get(url).json()
        current_score = page['matches'][ID]['score']['batting']['score'] 
        overs= current_score.split('(')[1].split(')')[0].replace('Ovs','')
        show_score = current_score.split('(')[0]
        print(f'{overs} Overs')
        print(f'{show_score} score')
        previous = current_score = page['matches'][ID]['score']['prev_overs']

        diff = int((float(overs.replace(' ',''))-last_ball)*10)
        print(type(diff))
        print(f'{diff} diff')
        if last_ball ==0.0 or last_ball==float(overs):
            last_ball=float(overs)
            print("in loop last ball")
            print(last_ball)
            return last_ball, None

        print("before loop")
        for i in range(diff):
            print("in upper loop")
            for item in list(previous)[-2-i::2]:
                print("in inner")
                print("item is {}" .format(item))
                if item in shout:
                    msg = f'{shout[item]}\nCurrent Score: {show_score}'
                    print(msg)
                    print(f'last ball {last_ball}')
                    last_ball=float(overs)
                    print(f'last ball updated {last_ball}')
                    return last_ball, msg

        print(f'last over {overs}')
        return float(overs), None
    except Exception as e:
        print(e)
        traceback.print_exc()
    
##
###get overs
##    overs = cl[0].text.find('Ovs')
##    
##
##    overs = cl[0].text[overs-6: overs-1]
##    try:
##        overs = float(overs)
##    except ValueError:
##        try:
##            overs = float(overs[1:])
##        except:
##            overs = overs.split('(')[1].split(')')
##            overs = float(overs[0])
##    
##    urll = url.replace('scores','scorecard')
##    print(urll)
##    new_page = requests.get(urll).text
##    soupp = bs(new_page, 'html.parser')
##    card=soup.find_all('div', {'class' : 'cb-col cb-col-100 cb-scrd-hdr-rw'})
##    card = card[0].find_all('span', {'class': 'pull-right'})
##    card = card[0].text
##    print(card)
##
##    global last_over
##    if last_over==overs or last_over==0.0:
##    	last_over = (overs)
##    	return
##
##    	
##    
##
##    text = soup.find(text='Recent: ')
##    recent_span = text.parent
##    next_span = recent_span.findNext('span')
##
##    score = next_span.text
##    print(score)
##    i = (float(overs) - float(last_over))*10
##
##    last_over = (overs)
##    if i==5:
##    	i=1
##
##    i = round(i)
##    
##
##    global shout
##    for item in shout:
##    	if item in score[-1-i:-1]:
##            notify.notify(msg=shout[item])
##            notify.notify(msg=card)
##
