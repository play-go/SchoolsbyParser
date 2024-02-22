#Made by  ██╗░░██╗░█████╗░██████╗░░█████╗░████████╗
#         ██║░██╔╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
#         █████═╝░███████║██████╦╝██║░░██║░░░██║░░░
#         ██╔═██╗░██╔══██║██╔══██╗██║░░██║░░░██║░░░
#         ██║░╚██╗██║░░██║██████╦╝╚█████╔╝░░░██║░░░
#         ╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░
import aiohttp, asyncio, string, random, fake_useragent
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as BS
useragent=fake_useragent.UserAgent().chrome
quater="82"
def get_curr_monday():
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    return ("20"+monday.strftime("%y"),monday.strftime("%m"),monday.strftime("%d"))

def get_prev_monday():
    now = datetime.now()-timedelta(days=7)
    monday = now - timedelta(days=now.weekday())
    return ("20"+monday.strftime("%y"),monday.strftime("%m"),monday.strftime("%d"))

def get_next_monday():
    now = datetime.now()+timedelta(days=7)
    monday = now - timedelta(days=now.weekday())
    return ("20"+monday.strftime("%y"),monday.strftime("%m"),monday.strftime("%d"))

async def csrf_gen():
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        result_str = ''.join(random.choice(letters) for _ in range(64))
        return result_str

async def main(login, password, dates, markss=False):
    csrf = await csrf_gen()
    headers = {
        'authority': 'schools.by',
        'user-agent': useragent,
        'x-csrftoken': csrf,
        'User-Agent': useragent,
        'Origin': 'https://schools.by',
        'Referer': 'https://schools.by/',
        'Cookie': 'csrftoken=' + csrf}
    data = {
        'csrfmiddlewaretoken': csrf,
        'username': login,
        'password': password,
        '|123':'|123'
        }
    url = "https://schools.by/login"
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
        async with session.post(url, data=data, headers=headers, allow_redirects=True) as resp:
            new_header = {
                'authority': 'schools.by',
                'user-agent': useragent,
                'x-csrftoken': session.cookie_jar.filter_cookies(url)["csrftoken"].value,
                'cookie': f'csrftoken={session.cookie_jar.filter_cookies(url)["csrftoken"].value};sessionid={session.cookie_jar.filter_cookies(url)["sessionid"].value}'}
            new_url = f"{resp.url}/dnevnik/quarter/{quater}/week/{dates}"
            async with session.get(new_url, headers=new_header, allow_redirects=False) as get:
                last = await aiohttp.StreamReader.read(get.content)
                soup = BS(last, "html.parser")
                days_left = soup.find("div", {'class':'db_days_column left'}).find_all("div", {"class":"db_day"})
                days_right = soup.find("div", {'class':'db_days_column right'}).find_all("div", {"class":"db_day"})
                last = []
                for i in days_left:
                        left=''''''
                        lsoup = BS(str(i), "html.parser").find("table").find("tbody").find_all("tr")
                        llast = BS(str(i), "html.parser").find("table").find("thead").find("tr").find("th", {"class":'lesson'}).text.strip()
                        left+=f"<i>{llast}</i>\n"
                        for f in lsoup:
                                llsoup = BS(str(f), "html.parser")
                                name = llsoup.find("td", {"class":'lesson'}).find("span").text.strip().replace("\n", '').replace(" ", '')
                                if name.split(".")[1]=="":continue
                                try:
                                        homework = llsoup.find("td", {"class":'ht'}).find("div", {"class":"ht-text-wrapper"}).find("div", {"class":"ht-text"}).text.strip()
                                except AttributeError:
                                        homework = "Пусто"
                                if markss == True:
                                        mark = llsoup.find("td", {"class":'mark'}).find("div").text.strip()
                                        if mark != '':
                                                left+=f"{name} | {homework} | {mark}\n"
                                        else:
                                                left+=f"{name} | {homework}\n"
                                elif markss == False:
                                        left+=f"{name} | {homework}\n"
                        left+="\n"
                        last.append(left)
                for i in days_right:
                        left = ''''''
                        lsoup = BS(str(i), "html.parser").find("table").find("tbody").find_all("tr")
                        llast = BS(str(i), "html.parser").find("table").find("thead").find("tr").find("th", {"class":'lesson'}).text.strip()
                        left+=f"<i>{llast}</i>\n"
                        passsd=0
                        for f in lsoup:
                                llsoup = BS(str(f), "html.parser")
                                name = llsoup.find("td", {"class":'lesson'}).find("span").text.strip().replace("\n", '').replace(" ", '')
                                if name == "1.":
                                       passsd=1
                                       break
                                if name.split(".")[1]=="":continue
                                try:
                                        homework = llsoup.find("td", {"class":'ht'}).find("div", {"class":"ht-text-wrapper"}).find("div", {"class":"ht-text"}).text.strip()
                                except AttributeError:
                                        homework = "Пусто"
                                if markss == True:
                                        mark = llsoup.find("td", {"class":'mark'}).find("div").text.strip()
                                        if mark != '':
                                                left+=f"{name} | {homework} | {mark}\n"
                                        else:
                                                left+=f"{name} | {homework}\n"
                                elif markss == False:
                                        left+=f"{name} | {homework}\n"
                        left+="\n"
                        if passsd==0:
                                last.append(left)
                return last

if __name__=="__main__":
        print(asyncio.run(main("ЛОГИН","ПАРОЛЬ","-".join(get_curr_monday()),True))) #TODO: Введите логин и пароль
       