from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import cloudscraper
import os
from config import *
import mysql.connector
import re


db = mysql.connector.connect(**database())
cursor = db.cursor()

scraper = cloudscraper.create_scraper()

options = Options()
options.headless = True


def empty_program():
    cursor.execute("""
        TRUNCATE TABLE Program
    """)
    db.commit()


def empty_channel():
    cursor.execute("""
        TRUNCATE TABLE Channel
    """)
    db.commit()


def set_data_channel(data):
    cursor.execute("""
        INSERT INTO Channel (nom, lien)
        VALUES (%s, %s)
    """, list(data.values()))
    db.commit()


def set_data_program(data):
    cursor.execute("""
        INSERT INTO Program (jour, heure, titre, chaine, statut)
        VALUES (%s, %s, %s, %s, %s)
    """, list(data.values()))
    db.commit()


def get_program():
    try:
        res = scraper.get(os.environ['LINK'])

        if res.status_code == 200 :
            sp = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
            sp = sp.text

            file_path = "prog"

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            prog_name = "programme.txt"
            prog_file = os.path.join(file_path, prog_name)

            f = open(prog_file, "w")
            f.write(sp)
            f.close()
            
            os.system("sed -i '1,23d' " + prog_file + " && sed -i '/^$/d' " + prog_file + " && sed -i '/^H/d' " + prog_file + " && sed -i '/^B/d' " + prog_file + " > /dev/null")

            with open(prog_file) as file:
                output = ''
                hold = ''

                global link_list
                link_list = []

                for line in file:
                    try: 
                        if line[0].isupper():
                            hold = line.split()[0]
                        else:
                            output = hold + ' | ' + line.split()[0] + ' | ' +  ' '.join(line.split()[1:]) 
                            final = list(map(lambda x: x.strip(), output.split("|")))

                            h, m = tuple(final[1].split(':'))

                            jour = final[0]
                            heure = time(hour=int(h), minute=int(m))
                            titre = final[2].replace(" x ", " vs ")
                            titre = titre.replace(" @ ", " vs ")

                            chaine = final[3].split("/")[-1].split(".")[0].upper()

                            program = {
                                "jour":jour, "heure":heure, "titre":titre, "chaine":chaine, "statut":"Terminé"
                            }

                            link_list.append(final[3])
                            set_data_program(program)

                    except IndexError:
                        continue
   
    except Exception as e:
        print(e)


def get_channel():
    driver = webdriver.Firefox(options=options)
    lien_pass = []

    for link in link_list:
        if link not in lien_pass:

            driver.get(link)

            def page_has_loaded():
                return driver.execute_script('return document.readyState;') == 'complete'

            while not page_has_loaded():
                sleep(0.5)

            try:

                iframe = WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))

                html = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'html'))
                )

                html_file = html.get_property('outerHTML')

                soup = BeautifulSoup(html_file, features = "html.parser")

                if soup.find_all('script')[1]:
                    soup.find_all('script')[1].decompose()

                if soup.find_all('div')[1]:
                    soup.find_all('div')[1].decompose()

                if soup.find('div', id = "btn-unmute"):
                    soup.find('div', id = "btn-unmute").decompose()

                if soup.find('div', class_ = "tb stream-offline"):
                    soup.find('div', class_ = "tb stream-offline").decompose()

                if soup.find('script', src = "https://www.googletagmanager.com/gtag/js?id=UA-184968220-1"):
                    soup.find('script', src = "https://www.googletagmanager.com/gtag/js?id=UA-184968220-1").decompose()

                if soup.find('script', src = "https://www.google-analytics.com/analytics.js"):
                    soup.find('script', src = "https://www.google-analytics.com/analytics.js").decompose()

                if soup.find('link', href = "/css/embed.min.css?v=0.3"):
                    soup.find('link', href = "/css/embed.min.css?v=0.3").decompose()

                if soup.find('style', type = "text/css"):
                    soup.find('style', type = "text/css").decompose()

                if soup.find('script', src = "/js/jquery.min.js"):
                    soup.find('script', src = "/js/jquery.min.js").decompose()

                if soup.find('object'):
                    soup.find('object').decompose()

                if soup.find_all('script', admn = "ZnluZmhjX3Bieg=="): 
                    admn = soup.find_all('script', admn = "ZnluZmhjX3Bieg==")
                    for ad in admn:
                        ad.decompose()

                if soup.find_all('script', type = "text/javascript"):
                    no_script = soup.find_all('script', type = "text/javascript")
                    for script in no_script:
                        script.decompose()

                if soup.find('div', onclick = "$(this).remove();"):
                    soup.find('div', onclick = "$(this).remove();").decompose()

                if soup.find_all('script')[-1]:
                    soup.find_all('script')[-1].decompose()

                if soup.find_all('div')[-1]:
                    soup.find_all('div')[-1].decompose()

                if soup.find_all('script')[-1]:
                    soup.find_all('script')[-1].decompose()

                if soup.find('a', dont = ""):
                    soup.find('a', dont = "").decompose()

                if soup.find(text = re.compile("abd()")):
                    abd = soup.find(text = re.compile("abd()"))
                    fixed_abd = abd.replace("abd()", "abdx()")
                    abd.replace_with(fixed_abd)

                soup.find('body')['style'] = "margin:0px !important"

                pretty_html = (soup.prettify())

                path = "api/channels"

                if not os.path.exists(path):
                    os.makedirs(path)

                file_name = link.split("/")[-1].split(".")[0]+".html"
                file = os.path.join(path, file_name)

                f = open(file, "w")
                f.write(pretty_html)
                f.close()

                lien = "localhost:1806/" + file
                nom_chaine = link.split("/")[-1].split(".")[0].upper()

                channel = {
                    "nom":nom_chaine, "lien":lien
                }

                set_data_channel(channel)

                lien_pass.append(link)
                
            except Exception as e:
                print(e)

    driver.close()


if __name__ == "__main__":
    empty_program()
    get_program()
    empty_channel()
    get_channel()