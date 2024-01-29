import requests, time, random, webbrowser, json, wget, os
from colorama import init, Fore
init(autoreset=True)

d = {}
maild = ''
idd = ''
pwd = ''
c1 = 0

def login():
    global c1, acs_tkn
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.BLUE + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 1
        elif mail.count('@') == 1:
            pw = input(Fore.BLUE + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
                if lrqst['code'] == 0:
                    c1 = 1
                    acs_tkn = lrqst['data']['access_token']
                    return acs_tkn

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            mail = maild
            pw = pwd
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
            if lrqst['code'] == 0:
                c1 = 1
                acs_tkn = lrqst['data']['access_token']
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')
        print(Fore.LIGHTYELLOW_EX + acs_tkn)

def main():
    count = ''
    needids = 0
    while needids == 0:
        needi = input(Fore.BLUE + 'Введите id необх. прототипов(F - если из файла):').split()
        if needi[0] == 'F':
            read()
            needids = idd.split()
        if needi[0].isdigit() == 1:
            needids = needi
    needids = set(needids)
    print(Fore.LIGHTYELLOW_EX + str(needids))
    chk = input(Fore.BLUE + 'Включить проверку уровня?')
    if chk != '':
        chk = int(chk)
        gms = int(input(Fore.BLUE + 'Включить проверку по играм?'))
    else:
        gms = 0
        chk = 0
    num = int(input(Fore.BLUE + 'Выберите направление поиска(0 - прямое, 1 - обратное):'))
    count = int(requests.get(f'https://monopoly-one.com/api/games.getLive?access_token={acs_tkn}').json()['data']['count'])
    if num == 0:
        offset = -25
    else:
        offset = 0
    print(Fore.LIGHTYELLOW_EX + str(offset))
    while True:
        print(Fore.LIGHTYELLOW_EX + f'{num} {offset}')
        if num == 0:
            if int(offset) < (count - 25):
                offset += 25
            else:
                offset = 0
        elif num == 1:
            if int(offset) > 25:
                offset -= 25
            else:
                offset = count - 25
        else:
            print(Fore.RED + 'Неверный формат данных')
            exit()
        print(Fore.LIGHTYELLOW_EX + f'Новый запрос с отбором в {offset}')
        mtvt = requests.get(f'https://monopoly-one.com/api/games.getLive?access_token={acs_tkn}&offset={offset}&count=25').json()['data']['games']
        #print(mtvt)
        uids = set()
        for mts in mtvt:
            if mts['game_mode'] != 4 or gms == 0:
                ids = mts['players']
                for id in ids:
                    uid = id['user_id']
                #print(uid)
                uids.add(uid)
        #print(uids)
        check(uids, needids, chk, gms)


def check(uids, needids, chk, gms):
    #print('цикл запущен')
    if len(buffer) < 555:
        for ids in uids:
            if not ids in buffer:
                buffer.add(ids)
                print(Fore.LIGHTYELLOW_EX + f'В буфере: {len(buffer)}')
                if chk != 0:
                    profile = requests.get(f'https://monopoly-one.com/api/execute.profile?access_token={acs_tkn}&user_id={ids}').json()['result']['user']
                    xpl = profile['xp_level']
                    print(Fore.LIGHTBLACK_EX + str(xpl))
                    if gms != 0:
                        games = profile['games']
                    else:
                        games = 0
                if chk == 0 or (int(xpl) <= chk & games <= gms):
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
            else:
                print(Fore.LIGHTYELLOW_EX + 'Повтор')
    else:
        buffer.clear()

def read():
    global maild, pwd, idd
    with open("config.txt") as file:
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

print(Fore.LIGHTWHITE_EX + 'ScmFndr. Made by AssKiss Studio https://github.com/AssKissStudio/M1ScmFndr')
config()
login()
buffer = set()
main()