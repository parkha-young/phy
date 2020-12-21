#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests, hgtk, random


# In[ ]:


print('''
- 실행 방법 설명 -
게임 모드를 선택하면 바로 실행
숫자 1 또는 2 입력
1 : 1인용 끝말잇기
2 : 2인용 끝말잇기
- 게임 규칙 -
기본적인 끝말잇기 게임입니다.
국립국어원 표준국어대사전에 등록된 단어만 허용됩니다.
두음법칙은 자동으로 적용됩니다. (ㄹ->ㄴ, ㄹ->ㅇ, ㄴ->ㅇ)
1인용의 경우 20라운드까지 진행하면 승리합니다.
- 추가 명령어 -
무효 : 이전 차례로 돌아가기
gg : 항복
re : 다시하기
end : 게임 종료
-------------------------------
''')


# In[ ]:


#'?'로 시작하는 단어 검색
def wsgs(h, b, c): #ex) wsgs(gs.text,'<item>','</item>')
    if b in h:
        w = h.split(b) #split : 문자열 나누기 ex)<item>이 나올때마다 끊어줌
        h = []
        for i in range(0, len(w)):
            if c in w[i]: 
                h.append(w[i][:w[i].find(c)])
    else:
        h = []
    return h

def wgs(h, b, c): #ex) wgs(w,'<pos>','</pos>')
    if b in h:
        h = h[h.find(b)+len(b):]
        if c in h:
            h = h[:h.find(c)]
    return h



def two(n):

    #두음법칙 : 봇이 입력한 단어에 두음법칙 적용
    du = 0 #두음법칙 사용 여부
    zz = hgtk.letter.decompose(n) #hgtk모듈로 마지막 글자 분해 (ex. '감' > 'ㄱ', 'ㅏ', 'ㅁ')
    #zz : 튜플 -> 변경 불가능
    z1 = n

    if zz[0] == 'ㄹ' and zz[1] in ('ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅐ', 'ㅔ', 'ㅚ'): #ㄹ두음법칙 : ㄹ -> ㄴ
        n = hgtk.letter.compose('ㄴ', zz[1], zz[2]) #hgtk모듈로 분해되어있는 자음, 모음을 합침 (ex. 'ㄱ', 'ㅏ', 'ㅁ' -> '감'
        du = du + 1
    elif zz[0] == 'ㄹ' and zz[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅖ'): #ㄹ두음법칙 : ㄹ -> ㅇ
        n = hgtk.letter.compose('ㅇ', zz[1], zz[2]) #hgtk모듈로 분해되어있는 자음, 모음을 합침 (ex. 'ㄱ', 'ㅏ', 'ㅁ' -> '감'
        du = du + 1
    elif zz[0] == 'ㄴ' and zz[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ'): #ㄴ두음법칙 : ㄴ -> ㅇ
        n = hgtk.letter.compose('ㅇ', zz[1], zz[2]) #hgtk모듈로 분해되어있는 자음, 모음을 합침 (ex. 'ㄱ', 'ㅏ', 'ㅁ' -> '감')
        du = du + 1

    if du != 0: #du가 0이 아니면 두음법칙이 적용된 것 그러므로 아래 문구 출력
        print('\'' + z1 +'\'' + ',' + '\'' + n + '\'' + '모두 사용 가능합니다.\n')
    
    return n


# In[ ]:


while True:

    #게임 모드 선택
    #입력값을 문자열 형태로 받음
    mod = str(input())

    while True:
      if mod == '1': #입력값이 1이면 1인용 모드 선택 
          bot = True
          break
      elif mod == '2': #입력값이 2이면 2인용 모드 선택
          bot = False
          break
      else:
          print('''
없는 명령어 입니다.
1 : 1인용 끝말잇기
2 : 2인용 끝말잇기
          ''')

          mod = str(input())


          
    #게임시작
    #게임 초기 설정
    z = '' #마지막 글자 저장
    z1 = '' #두음법칙이 적용된 마지막 글자 저장
    mod2 = 1
    r = 1 #몇 번째 라운드인지 저장
    history = [] #이미 사용한 단어들 저장
    print('게임을 시작합니다.')
        


    while True: #게임 루프
            
        print('\nRound %d' %r)

        #1인용 끝말잇기 : 플레이어1 입력
        if  bot == True:
            player1 = str(input('플레이어1의 차례입니다 : '))


        #2인용 끝말잇기 : 플레이어1, 2 입력
        if bot == False:
            player1 = str(input('플레이어%d의 차례입니다 : ' %mod2))
        
        if player1 == 'gg':
            print('\n패배\n')
            break

        if player1 == 'end':
            print('\n게임 종료\n')
            break

        if player1 == 're':
            print('\n게임을 처음부터 다시 시작합니다.\n')
            r = 1
            history = []
            continue


        print('...')        


        if r == 1 and mod2 == 2 and player1 == '무효' and bot == False: #2인용 무효 (1라운드에만 적용)
            print("다시 한 번 입력해주세요.\n")
            mod2 = mod2 - 1
            del history[-1] #마지막에 사용한 단어를 이미 사용한 단어에서 삭제
            continue

        if r != 1 and player1 == '무효':
            print("다시 한 번 입력해주세요.\n")
                
            del history[-1] #마지막에 사용한 단어를 이미 사용한 단어에서 삭제
            z = history[-1][len(history[-1]) - 1] #이전 끝말을 다시 불러옴

            #두음법칙
            z1 = two(z)

            if bot == False:
                mod2 = mod2 - 1 #플레이어1 또는 2가 다시 입력

            if mod2 == 0: #위의 코드에서 1-1=0의 경우 2로 만들어줌
                mod2 = 2
                r = r - 1
                continue
                

        if r == 1 or player1 != '무효':

            pw = [] #플레이어의 단어검색 결과를 임시저장하는 곳
            bb = '' #단어
            dd = '' #뜻

            #단어 체크 시작
            gs = requests.get('https://krdict.korean.go.kr/api/search?key=7B1C781BAAC001CF565FECB56BD9C5DB&part=word&pos=1&q=' + player1 + '*')

            #단어 목록 불러오기
            words = wsgs(gs.text,'<item>','</item>') #입력한 단어로 시작하는 명사가 많을 경우 순서대로 저장


            for w in words:
                if not (w in history): #이미 쓴 단어가 아닐때
                    word = wgs(w,'<word>','</word>')
                    pos = wgs(w,'<pos>','</pos>')
                    if len(word) > 1 and pos == '명사': #한글자가 아니고 품사가 명사일때
                        pw.append(w) #명사 단어들을 순서대로 저장
                        dicword1 = pw[0] #그 중 첫번째 단어 저장 (뜻을 여러개 불러올 것이 아니기 때문)
                        bb = wgs(dicword1, '<word>', '</word>') #단어 불러오기
                        dd = wgs(dicword1, '<definition>', '</definition>') #뜻 불러오기
                                
                
                
            if player1[0] == z1:
                zzz = z1
            else:
                zzz = z

            if player1 == '': #의도치 않게 엔터를 쳤을 경우
                print('입력값이 없습니다. 다시 입력해 주세요.')
                continue
            elif len(player1) == 1:
                print('두 글자 이상의 단어를 입력해주세요.')
                continue
            elif r != 1 and player1[0] != zzz: #입력값을 넣었으나 끝말잇기가 아닌 경우
                print("단어가 '" + zzz + "'로 시작되지 않습니다. 다시 입력해 주세요.")
                continue
            elif r == 1 and player1[0] != zzz and mod2 == 2: #위의 경우에서 2인용 1라운드의 경우
                print("단어가 '" + zzz + "'로 시작되지 않습니다. 다시 입력해 주세요.")
                continue 
            elif player1 == '무르기' and r == 1 :
                print('첫 입력에서는 무효가 불가능합니다. 다시 입력해 주세요.')
                continue
            elif pw == []:
                print('존재하지 않는 단어입니다. 다시 입력해 주세요.')
                continue



            #플레이어1이 입력한 단어와 이미 사용한 단어 매칭
            em = 0 #이미 사용된 단어이면 1 이상, 아니면 0
            for i in range(len(history)):
                if history[i] == player1:
                    em = em + 1

            if em != 0: #e가 1 이상이면 이미 사용한 단어
                print('이미 사용한 단어입니다.')
                continue
                    
            else: #단어가 조건을 충족할 경우
                z = player1[-1] #z에 마지막 글자 저장
                history.append(player1) #입력 받은 단어를 history에 추가, append : 리스트 마지막에 요소 추가
                print('(' + dd + ')\n') #플레이어가 입력한 단어의 뜻 출력
          

            #두음법칙
            z1 = two(z)

        # while문 끝



        if bot == False: #2인용 끝말잇기 루프가 돌아가게 만들어줌
            mod2 = mod2 + 1 #플레이어1, 2의 차례를 결정
            if mod2 == 3: #mod2가 1, 2, 1, 2, ...로 반복
                mod2 = 1
                r = r + 1 #플레이어2의 차례가 끝나면 라운드 + 1
            continue

        else: #1인용 끝말잇기 : 봇 입력
            bw = [] #봇이 사용할 단어의 후보들 저장
            gs = requests.get('https://krdict.korean.go.kr/api/search?num=100&key=7B1C781BAAC001CF565FECB56BD9C5DB&part=word&pos=1&q=' + z + '*')
            gsdu = requests.get('https://krdict.korean.go.kr/api/search?num=100&key=7B1C781BAAC001CF565FECB56BD9C5DB&part=word&pos=1&q=' + z1 + '*')
                
            #단어 목록 불러오기
            words = wsgs(gs.text,'<item>','</item>')
            wordsdu = wsgs(gsdu.text,'<item>','</item>')

            for w in words: #ex) 랑으로 시작하는 단어
                if not (w in history): #이미 쓴 단어가 아닐때
                    word = wgs(w,'<word>','</word>')
                    pos = wgs(w,'<pos>','</pos>')
                    if len(word) > 1 and pos == '명사' and not word in history: #한글자가 아니고 품사가 명사일때
                        bw.append(w)
            for w in wordsdu: #ex) 낭으로 시작하는 단어
                if not (w in history): #이미 쓴 단어가 아닐때
                    word = wgs(w,'<word>','</word>')
                    pos = wgs(w,'<pos>','</pos>')
                    if len(word) > 1 and pos == '명사' and not word in history: #한글자가 아니고 품사가 명사일때
                        bw.append(w)

            if len(bw)>0:
                botword = random.choice(bw) #랜덤 단어 추출
            else:
                botword = ''



        if botword == '': #봇이 입력할 단어 소진
            print('BOT이 사용할 단어가 모두 소진되었습니다.')
            break

        elif r == 20: #20라운드 도달시 승리
            print('최대 라운드에 도달하셨습니다.')
            break

        else: #그외 : 이어서 게임 진행
            bb = wgs(botword, '<word>', '</word>') #단어 불러오기
            dd = wgs(botword, '<definition>', '</definition>') #뜻 불러오기
            history.append(bb) #이미 사용한 단어장에 저장
            r = r + 1 #라운드 + 1
            print('BOT : ' + bb + '\n(' + dd + ')\n') #봇 : 랜덤 선택 된 단어 + 단어의 뜻 출력
            z = bb[-1] #z에 마지막 글자 저장


        #두음법칙
        z1 = two(z)


        if r != 1 and player1 == '무효' and mod2 == 1: #1라운드를 제외한 라운드에서 무르기인 경우 봇이 실행되도록 해줌
            r = r - 1


    print('다시 게임 모드를 선택하세요.')


# In[ ]:




