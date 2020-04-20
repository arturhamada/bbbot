## coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from binascii import a2b_base64
import processing
import re
## Variaveis do processo

loginUrl = "https://minhaconta.globo.com/"
login = "hostelando.br@gmail.com"
password = "benjaminA1"
url = "https://gshow.globo.com/realities/bbb/bbb20/votacao/paredao-bbb20-quem-voce-quer-eliminar-babu-gabi-ou-thelma-305135b8-b442-4cc8-888f-2a01ed79cc2d.ghtml"
nameSearch = "Gabi"

firefox = webdriver.Firefox()
ac = ActionChains(firefox)

idxName = int()

def logando ():

    firefox.get(loginUrl)
    time.sleep(3)
    firefox.find_element_by_id('login').send_keys(login)
    firefox.find_element_by_id('password').send_keys(password)
    firefox.find_elements_by_css_selector('#login-form .button')[0].click()
    time.sleep(5)
    print("iniciando o bot") 



def button_find():
    firefox.get(url)
    firefox.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    ## Encontra o titulo da página
    title = firefox.find_element_by_id('roulette-root').text
    ## Divide em uma lista com 3 nomes
    names = title.split('\n')[1:]

    ## Faz a busca pelo nome informado na entrada
    idxName = names.index(nameSearch)
    print(nameSearch + " é o botao " + str(idxName))
    return idxName



def button_click():


    element = []
    element = firefox.find_elements_by_class_name('_3HY6tUrdeykwokPXP7PdwT')
    elementBtn = element[idxName]


    ac.move_to_element(elementBtn).click().perform()

    time.sleep(2)


def captcha_read():

    captchaBox = []
    captchaBox = firefox.find_elements_by_class_name('gc__2Qtwp')
 #   if captchaBox != []:
#        if len(captchaBox[0].text) > 2:
#        break
    imageSearchName = captchaBox[0].text.split('\n')[-1]
    print("procurando por " + imageSearchName)

    captcha = []
    captcha = firefox.find_elements_by_class_name('gc__3_EfD')[0]
    captchaSrc = captcha.get_attribute("src")

    data = captchaSrc.split(';base64,')[1]
    binary_data = a2b_base64(data)

    filename = imageSearchName + '.png'
    fd = open('BBB20/captchas/' + filename, 'wb')
    fd.write(binary_data)
    fd.close()

    processing.processImage(filename)
    points = processing.findInCaptcha(filename)

    if points != []:
        print("a imagem se encontra nos pontos: " + str(points[0]) + " X " + str(points[1]))
        print("o tamanho do captcha é " + str(captcha.size['width']) + " X " + str(captcha.size['height']))
        firefox.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        posX = points[0] - captcha.size['width']/2
        posY = points[1] - captcha.size['height']/2

        ac.move_to_element(captcha).move_by_offset(posX, posY).click().perform()
        time.sleep(5)
    else:
        print("erro - captcha não encontrado")




# firefox.quit()

def main():
    print ("Iniciando")
    logando()
    button_find()
    while(1):
        button_click()
        for i in range(4):
            try:
                captcha_read()
                time.sleep(5)
            except:
                time.sleep(6)



if __name__ == "__main__":
    main()
