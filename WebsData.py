from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import datetime
import EmailSender
import datafunctions
import requests

def vlmweb():
    url = "https://www.vlm.sk/ponuky-na-odpredaj?fbclid=IwAR0BxaTbKfDhwwaY43xQjBSFWQivSYH0HJlQLDWtHHNfl3bhPD4AUzzJDb0#ponuky"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    ponuky = soup.find('tbody').find_all('tr')
    for ponuka in ponuky:
        datumponuky = ponuka.find('time', class_="journal__publish-date")
        if datumponuky and datetime.date.today().strftime("%e. %m. %Y").replace(' 0', ' ') in datumponuky.text:
            EmailSender.sendMail(f"""
            Nova ponuka na stranke www.vlm.sk\n
            Link: https://www.vlm.sk{ponuka.find('a')['href']}\n
            Ponuka:\n
            {ponuka.find('h6', class_ = "journal__title").text}\n
            {ponuka.find('p', class_ = "journal__description").text}\n
            {datumponuky.text}     
            """)
            datafunctions.savedate(datetime.date.today().strftime("%e. %m. %Y"), "---",  ponuka.find('h6', class_ = "journal__title").text, f"https://www.vlm.sk{ponuka.find('a')['href']}", "www.vlm.sk")
        else:
            break
        
def obchodnyvestnik():
    options = webdriver.ChromeOptions()
    options.headless = True
        
    driver = webdriver.Chrome(options = options)
    
    driver.get("https://obchodnyvestnik.justice.gov.sk/ObchodnyVestnik/Formular/FormulareZverejnene.aspx?fbclid=IwAR0EclHwjISrWjc1iJVxiS2sbPRgCTWvHhO98JSj-i94BCKztB05_qcZ_f0&csrt=2357372818194360177")
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.find_element(By.ID, soup.find("table", class_="Filter").find_all("tr")[1].find_all("input")[1]['id']).send_keys(datetime.date.today().strftime("%e.%m.%Y"))
    Select(driver.find_element(By.ID, soup.find("table", class_="Filter").find_all("tr")[2].find("select")['id'])).select_by_value("OV_D")
    driver.find_element(By.ID, "ctl00_ctl00_CphMain_CphMain_btnVyhladat").click()
    Select(driver.find_element(By.ID, "ctl00_ctl00_CphMain_CphMain_gvFormularZoznam_ctl13_ctl00_cmbAGVCountOnPage")).select_by_value("100")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    elements = soup.find("table", class_="GridTable").tbody.find_all("tr")
    elements.remove(elements[0])
    try:
        elements.remove(elements[0])
    except IndexError:
        quit

    try:
        elements.remove(elements[len(elements)-1])
    except IndexError:
        pass
    for i in range(len(elements)):
        data = elements[i].find_all("td")
        if (data[1].text.strip() in ["Oznámenie o dobrovoľnej dražbe", "Oznámenie o opakovanej dobrovoľnej dražbe", "Oznámenie o zmarení/neplatnosti dobrovoľnej dražby"]):
            datafunctions.savedate(data[2].text, "---", f"{data[1].text} \n{data[3].text}", f"https://obchodnyvestnik.justice.gov.sk{data[6].a['href']}", "https://obchodnyvestnik.justice.gov.sk/ObchodnyVestnik/Formular/FormulareZverejnene.aspx?fbclid=IwAR0EclHwjISrWjc1iJVxiS2sbPRgCTWvHhO98JSj-i94BCKztB05_qcZ_f0&csrt=2357372818194360177")
            body = f"""
            Nova ponuka na stranke: https://obchodnyvestnik.justice.gov.sk/ObchodnyVestnik/Formular/FormulareZverejnene.aspx?fbclid=IwAR0EclHwjISrWjc1iJVxiS2sbPRgCTWvHhO98JSj-i94BCKztB05_qcZ_f0&csrt=2357372818194360177
            Link: https://obchodnyvestnik.justice.gov.sk{data[6].a["href"]}
            Ponuka:
            {data[3].text}\n
            {data[1].text}\n
            Zverejnené dňa: {data[2].text} 
            """
            EmailSender.sendMail(body)
