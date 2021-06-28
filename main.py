# this program finds statistical arbitrages for betting on football
# and then send a mail with the results (development in progress)
#TODO browsert csak az elején nyisson egyszer, aztán pass as argument

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
from threading import Thread


def check_unibet(unibet, browser):
    print(" [*] check_unibet started")
    # ffox_options = Options()
    # ffox_options.add_argument("--headless")
    # browser = webdriver.Firefox()
    browser.get("https://www.unibet.co.uk/betting/sports/filter/football/matches")
    time.sleep(8)


    # clicks the cookie confirm button
    browser.find_element_by_id("CybotCookiebotDialogBodyButtonAccept").click()
    time.sleep(2)

    # opens all country dropdowns

    drops = browser.find_elements_by_xpath("//*[@data-test-name='accordionLevel1']")
    drops.pop(0)

    drops[0].click()
    drops.pop(0)
    drops.pop(0)

    drop_threads = []
    for element in drops:
        drop_threads.append(Thread(target = element.click))
    for element in drop_threads:
        element.start()

    time.sleep(1)

    # opens all expand buttons

    expamd_threads = []
    for element in browser.find_elements_by_id("expand"):
        expamd_threads.append(Thread(target = element.click))
    for element in expamd_threads:
        element.start()

    events = browser.find_elements_by_xpath("//*[@data-test-name='event']")

    counter = 0
    for match in events:
        print(counter)
        team_names = match.find_elements_by_xpath(".//*[@data-test-name='teamName']")
        odds = match.find_elements_by_xpath(".//*[@data-test-name='odds']")

        # print(len(odds))
        if len(odds) != 5:
            continue
        else:
            for i in odds:
                i.text.replace(",",".")
            versus = team_names[0].text + "-" + team_names[1].text
            values1 = [1,1] if odds[0].text == "Evens" else odds[0].text.split("/")
            values2 = [1,1] if odds[1].text == "Evens" else odds[1].text.split("/")
            values3 = [1,1] if odds[2].text == "Evens" else odds[2].text.split("/")
            values = [int(values1[0]) / int(values1[1]), int(values2[0]) / int(values2[1]),
                      int(values3[0]) / int(values3[1])]
            unibet.update({versus: values})
        counter += 1

    # browser.close()
    print(" [*] check_unibet completed")
    # return unibet

def check_betway(betway, browser):
    print(" [*] check_betway started")
    # ffox_options = Options()
    # ffox_options.add_argument("--headless")
    # browser = webdriver.Firefox()

    links = [
        "https://betway.com/en/sports/sct/soccer/copa-america",
        "https://betway.com/en/sports/sct/soccer/international-club",
        "https://betway.com/en/sports/sct/soccer/usa",
        "https://betway.com/en/sports/sct/soccer/england",
        "https://betway.com/en/sports/sct/soccer/spain",
        "https://betway.com/en/sports/sct/soccer/france",
        "https://betway.com/en/sports/sct/soccer/germany",
        "https://betway.com/en/sports/sct/soccer/brazil",
        "https://betway.com/en/sports/sct/soccer/sweden",
        "https://betway.com/en/sports/sct/soccer/european-cups",
        "https://betway.com/en/sports/sct/soccer/fifa-21-esoccer",
        "https://betway.com/en/sports/sct/soccer/australia",
        "https://betway.com/en/sports/sct/soccer/austria",
        "https://betway.com/en/sports/sct/soccer/belarus",
        "https://betway.com/en/sports/sct/soccer/egypt",
        "https://betway.com/en/sports/sct/soccer/estonia",
        "https://betway.com/en/sports/sct/soccer/faroe-islands",
        "https://betway.com/en/sports/sct/soccer/iceland",
        "https://betway.com/en/sports/sct/soccer/iran",
        "https://betway.com/en/sports/sct/soccer/ireland",
        "https://betway.com/en/sports/sct/soccer/japan",
        "https://betway.com/en/sports/sct/soccer/kazakhstan",
        "https://betway.com/en/sports/sct/soccer/kenya",
        "https://betway.com/en/sports/sct/soccer/latvia",
        "https://betway.com/en/sports/sct/soccer/lithuania",
        "https://betway.com/en/sports/sct/soccer/morocco",
        "https://betway.com/en/sports/sct/soccer/norway",
        "https://betway.com/en/sports/sct/soccer/rwanda",
        "https://betway.com/en/sports/sct/soccer/scotland",
        "https://betway.com/en/sports/sct/soccer/south-korea",
        "https://betway.com/en/sports/sct/soccer/uruguay"
    ]


    def check_subpage(link, betway):
        try:
            browser.get(link)
            time.sleep(3)
            events = browser.find_elements_by_xpath("//*[@class='oneLineEventItem']")
            for match in events:
                team1 = match.find_element_by_xpath(".//*[@class='teamNameFirstPart teamNameHomeTextFirstPart']").text
                team2 = match.find_element_by_xpath(".//*[@class='teamNameFirstPart teamNameAwayTextFirstPart']").text
                odds = match.find_elements_by_xpath(".//*[@class='odds']")
                for i in odds:
                    i.text.replace(",", ".")
                vs = team1 + "-" + team2
                odds_float = [float(odds[0].text), float(odds[1].text), float(odds[2].text)]
                betway.update({vs:odds_float})
                # return betway
        except:
            pass

    for link in links:
        check_subpage(link, betway)
    # browser.close()
    print(" [*] check_betway completed")
    # return betway

def check_neobet(neobet, browser):
    print(" [*] check_neobet started")
    # ffox_options = Options()
    # ffox_options.add_argument("--headless")
    # browser = webdriver.Firefox()
    browser.get("https://neo.bet/en/Sportbets/Football")
    time.sleep(5)
    browser.find_element_by_xpath("//*[@class='sc-jMZWZw hvwdXB']").click()
    time.sleep(2)
    drops = browser.find_elements_by_xpath("//*[@class='sc-LELic fobHiZ']")
    for element in drops:
        element.click()

    events = browser.find_elements_by_xpath("//*[@class='matchRow s1y_matchRow']")
    counter = 0
    for match in events:
        team_names = match.find_elements_by_xpath(".//*[@class='sc-jLuWEH WDEOL']")
        odds = match.find_elements_by_xpath(".//*[@class='s1w_odds s1w_decimal']")
        if len(odds) < 3:
            continue
        else:
            for i in odds:
                i.text.replace(",",".")
            vs = team_names[0].text + "-" + team_names[1].text
            odds_float = [float(odds[0].text), float(odds[1].text), float(odds[2].text)]
            neobet.update({vs:odds_float})
        counter += 1

    # browser.close()
    print(" [*] check_neobet completed")
    # return neobet

print("Hi")
# options = Options()
# # options.add_argument("--disable-infobars")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.log.level = "trace"
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# options.add_argument("--disable-dev-shm-usage")

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")
chromeOptions.add_argument("--remote-debugging-port=9222")  # this
chromeOptions.add_argument("--disable-dev-shm-using")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("disable-infobars")

try:
    browser = webdriver.Chrome(service_args=["--verbose", "--log-path=./chrome.log"])
except NoSuchElementException as e:
    print(e)
time.sleep(10)
print("1")
browser.get("https://444.hu")

print("browser opened")

while True:
    try:
        unibet = dict()
        betway = dict()
        neobet = dict()

        # unibet_thread = Thread(target=check_unibet, args=(unibet,))
        # betway_thread = Thread(target=check_betway, args=(betway,))
        # neobet_thread = Thread(target=check_neobet, args=(neobet,))
        #
        # unibet_thread.start()
        # betway_thread.start()
        # neobet_thread.start()
        check_unibet(unibet, browser)
        check_betway(betway, browser)
        check_neobet(neobet, browser)


        arbitrage = []
        # while True:
            # if not unibet_thread.is_alive() and not betway_thread.is_alive() and not neobet_thread.is_alive():
        print(" [*] all scraping threads are done, looking for arbitrage opportunities")
        for key in unibet.keys():
            if key in betway and key in neobet:
                bet1 = unibet[key][0]
                bet2 = betway[key][1]
                bet3 = neobet[key][2]
                if (bet1-bet2-bet3) > 0 or (-bet1+bet2-bet3) > 0 or (-bet1-bet2+bet3) > 0:
                    arbitrage.append([key, '1: unibet, x: betway, 2: neobet'])
                    print(key, '1: unibet, x: betway, 2: neobet')
                bet1 = unibet[key][0]
                bet2 = neobet[key][1]
                bet3 = betway[key][2]
                if (bet1-bet2-bet3) > 0 or (-bet1+bet2-bet3) > 0 or (-bet1-bet2+bet3) > 0:
                    arbitrage.append([key, '1: unibet, x: neobet, 2: betway'])
                    print(key, '1: unibet, x: neobet, 2: betway')
                bet1 = betway[key][0]
                bet2 = unibet[key][1]
                bet3 = neobet[key][2]
                if (bet1-bet2-bet3) > 0 or (-bet1+bet2-bet3) > 0 or (-bet1-bet2+bet3) > 0:
                    arbitrage.append([key, '1: betway, x: unibet, 2: neobet'])
                    print(key, '1: betway, x: unibet, 2: neobet')
                bet1 = betway[key][0]
                bet2 = neobet[key][1]
                bet3 = unibet[key][2]
                if (bet1-bet2-bet3) > 0 or (-bet1+bet2-bet3) > 0 or (-bet1-bet2+bet3) > 0:
                    arbitrage.append([key, '1: betway, x: neobet, 2: unibet'])
                    print(key, '1: betway, x: neobet, 2: unibet')
                bet1 = unibet[key][0]
                bet2 = neobet[key][1]
                bet3 = betway[key][2]
                if (bet1 - bet2 - bet3) > 0 or (-bet1 + bet2 - bet3) > 0 or (-bet1 - bet2 + bet3) > 0:
                    arbitrage.append([key, '1: unibet, x: neobet, 2: betway'])
                    print(key, '1: unibet, x: neobet, 2: betway')
                bet1 = unibet[key][0]
                bet2 = betway[key][1]
                bet3 = neobet[key][2]
                if (bet1 - bet2 - bet3) > 0 or (-bet1 + bet2 - bet3) > 0 or (-bet1 - bet2 + bet3) > 0:
                    arbitrage.append([key, '1: unibet, x: betway, 2: neobet'])
                    print(key, '1: unibet, x: betway, 2: neobet')
        if len(arbitrage) != 0:
            for i in arbitrage:
                print(i)
                # break
    except:
        pass
    print("finished, starting sleep")
    time.sleep(300)

