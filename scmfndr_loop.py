import requests, time, random, webbrowser, json, wget, os
from colorama import init, Fore
from audioplayer import AudioPlayer
init(autoreset=True)

d = {}
maild = ''
idd = ''
pwd = ''
c1 = 0

price1 = 0
t1me = 0
c1 = 0

def login():
    global c1, acs_tkn, rfr_tkn, uid
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.MAGENTA + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 2
        elif mail.count('@') == 1:
            pw = input(Fore.MAGENTA + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={replaces(pw)}").json()
                if 'data' in lrqst:
                    if lrqst['code'] == 0:
                        if 'totp_session_token' in lrqst['data']:
                            tfa = ''
                            while True:
                                while tfa == "":
                                    tfa = input('Введите код 2FA:')
                                else:
                                    auth2 = requests.get(f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                    if auth2['code'] == 0:
                                        c1 = 1
                                        acs_tkn = auth2['data']['access_token']
                                        rfr_tkn = auth2['data']['refresh_token']
                                        uid = auth2['data']['user_id']
                                        return acs_tkn, rfr_tkn, uid
                                    else:
                                        print(Fore.RED + 'Ошибка')
                                        tfa = ''
                        else:
                            c1 = 1
                            acs_tkn = lrqst['data']['access_token']
                            rfr_tkn = lrqst['data']['refresh_token']
                            uid = lrqst['data']['user_id']
                            return acs_tkn, rfr_tkn, uid

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={maild}&password={replaces(pwd)}").json()
            #print(lrqst)
            if 'data' in lrqst:
                if lrqst['code'] == 0:
                    if 'totp_session_token' in lrqst['data']:
                        tfa = ''
                        while True:
                            while tfa == "":
                                tfa = input('Введите код 2FA:')
                            else:
                                auth2 = requests.get(
                                    f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                if auth2['code'] == 0:
                                    c1 = 1
                                    acs_tkn = auth2['data']['access_token']
                                    rfr_tkn = auth2['data']['refresh_token']
                                    uid = auth2['data']['user_id']
                                    return acs_tkn, rfr_tkn, uid
                                else:
                                    print(Fore.RED + 'Ошибка')
                                    tfa = ''
                    else:
                        c1 = 1
                        acs_tkn = lrqst['data']['access_token']
                        rfr_tkn = lrqst['data']['refresh_token']
                        uid = lrqst['data']['user_id']
                        return acs_tkn, rfr_tkn, uid
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')

def params():
    global chk,gms,num,count,needids
    needids = 0
    while needids == 0:
        needi = input(Fore.MAGENTA + 'Введите id необх. прототипов(F - если из файла):').split()
        if needi[0] == 'F':
            read()
            needids = idd.split()
        if needi[0].isdigit() == 1:
            needids = needi
    needids = set(needids)
    print(Fore.LIGHTYELLOW_EX + str(needids))
    chk = input(Fore.MAGENTA + 'Включить проверку уровня?')
    if chk != '':
        chk = int(chk)
        gms = int(input(Fore.MAGENTA + 'Включить проверку по играм?'))
    else:
        gms = 0
        chk = 0
    num = int(input(Fore.MAGENTA + 'Выберите направление поиска(0 - прямое, 1 - обратное):'))
    count = int(requests.get(f'https://monopoly-one.com/api/games.getLive?access_token={acs_tkn}').json()['data']['count'])

def scmfndr():
    if num == 0:
        offset = -25
    else:
        offset = 0
    #print(Fore.LIGHTYELLOW_EX + str(offset))
    while True:
        #print(Fore.LIGHTYELLOW_EX + f'{num} {offset}')
        if num == 0:
            if int(offset) < (count - 25):
                offset += 25
            else:
                print(Fore.LIGHTWHITE_EX + 'Ожидание новых матчей')
                time.sleep(random.randint(15,45))
                offset = 0
        elif num == 1:
            if int(offset) > 25:
                offset -= 25
            else:
                print(Fore.LIGHTWHITE_EX + 'Ожидание новых матчей')
                time.sleep(random.randint(15, 45))
                offset = count - 25
        else:
            print(Fore.RED + 'Неверный формат данных')
            exit()
        print(Fore.LIGHTYELLOW_EX + f'Новый запрос с отбором в {offset}')
        mtvt = requests.get(f'https://monopoly-one.com/api/games.getLive?access_token={acs_tkn}&offset={offset}&count=25').json()['data']['games']
        #print(mtvt)
        dup = set()
        for mts in mtvt:
            if mts['game_mode'] != 4 or gms == 0:
                ids = mts['players']
                for id in ids:
                    uid = id['user_id']
                #print(uid)
                dup.add(uid)
        #print(uids)
        checkd = []
        if len(buffer) < 5555:
            for ids in dup:
                if not ids in buffer:
                    buffer.add(ids)
                    print(Fore.LIGHTYELLOW_EX + f'В буфере: {len(buffer)}')
                    if chk != 0:
                        profile = requests.get(f'https://monopoly-one.com/api/execute.profile?access_token={acs_tkn}&user_id={ids}').json()['result']['user']
                        #print(profile)
                        xpl = profile['xp_level']
                        print(Fore.LIGHTBLACK_EX + str(xpl))
                        if gms != 0:
                            games = profile['games']
                        else:
                            games = 0
                    if chk == 0 or (xpl <= chk & games <= gms):
                        checkd.append(ids)
                #else:
                    #print(Fore.LIGHTYELLOW_EX + 'Повтор')
        else:
            buffer.clear()
        checkd.sort(reverse=True)
        dup.clear()
        print(Fore.GREEN + str(checkd))
        for ids in checkd:
            check(ids, needids)

def check(ids, needids):
    #print('цикл запущен')
    invt = requests.get(f'https://monopoly-one.com/api/execute.prepareTrade?user_id={ids}&access_token={acs_tkn}').json()['result']
    #print(invt)
    if 'items' in invt:
        invts = invt['items'][1]
        if 'list' in invts:
            invtss = invts['list']
            #print(invts)
            protoids = set()
            for invtt in invtss:
                protoids.add(invtt['item_proto_id'])
            if len(needids) != 0:
                print(Fore.LIGHTBLACK_EX + f'{ids}: {protoids}')
                for needid in needids:
                    if int(needid) in protoids:
                        webbrowser.open_new(f'https://monopoly-one.com/trades/new?to={ids}')
                        protoids.clear()
                        time.sleep(random.randint(500,1500)/100)
            else:
                #print('Открываю')
                webbrowser.open_new(f'https://monopoly-one.com/trades/new?to={ids}')
                time.sleep(random.randint(500,1500)/100)
    time.sleep(random.randint(500,1000)/100)

def read():
    global maild, pwd, idd
    with open("config.txt",'r',-1,'utf-8') as file:
        str = file.read()
        dicti = json.loads(str)
    if bool(dicti['email']) == 1 & bool(dicti['password']) == 1:
        maild = dicti['email']
        pwd = dicti['password']
    if bool(dicti['ids']) == 1:
        idd = dicti['ids']

def config():
    if not os.path.exists('config.txt'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/config.txt')
        print('==> Загружен файл параметров. Вы можете изменить его в любом текстовом редакторе')

def error():
    print('Токен недействителен, либо лимиты')
    if not os.path.exists('error.mp3'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/error.mp3')
    AudioPlayer('error.mp3').play(block=True)
    os.remove('error.mp3')
    exit()

def refresh():
    global acs_tkn,rfr_tkn
    if c1 == 1:
        refreshh = requests.get(f'https://monopoly-one.com/api/auth.refresh?refresh_token={rfr_tkn}').json()
        print(refreshh)
        if refreshh['code'] == 0:
            print('Обновил токены')
            acs_tkn = refreshh['data']['access_token']
            rfr_tkn = refreshh['data']['refresh_token']
            time.sleep(random.randint(400,800)/100)
            return acs_tkn,rfr_tkn
    else:
        error()

def replaces(var):
    var = var.replace('!','%21')
    var = var.replace('\"', '%22')
    var = var.replace('#', '%23')
    var = var.replace('$', '%24')
    var = var.replace('&', '%26')
    var = var.replace('\'', '%27')
    var = var.replace('(', '%28')
    var = var.replace(')', '%29')
    var = var.replace('!', '%21')
    var = var.replace('*', '%2A')
    var = var.replace('+', '%2B')
    var = var.replace('/', '%2F')
    return var

print(Fore.LIGHTWHITE_EX + 'ScmFndr. Made by AssKiss Studio https://github.com/AssKissStudio/M1ScmFndr')

config()
login()
params()
while True:
    #refresh()
    buffer = set()
    try:
        scmfndr()
    except:
        if c1 == 1:
            refresh()
        else:
            error()