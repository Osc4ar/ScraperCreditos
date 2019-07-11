from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import time
import csv
import os


def open_csv():
    myfile = open('data.csv', 'w')
    fieldnames = ["Fecha", "Producto", "Esquema", "Plazo", "Tasa", "Aforo", "Destino",
                  "Gastos notariales", "Gastos Iniciales", "Enganche", "CAT", "Comision", "Avaluo", "Pago"]
    writer = csv.DictWriter(myfile, fieldnames=fieldnames,
                            delimiter=',', lineterminator='\r')
    writer.writeheader()
    return writer


def open_browser():
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)
    browser.maximize_window()
    browser.execute_script("document.body.style.zoom='175%'")
    browser.get("https://e-credit.santander.com.mx/hipsantanderhib/")
    return browser


def crearImage(png, filename, location, size):
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save("Imagenes\\"+filename, 'PNG', optimize=True, quality=100)


writer = open_csv()
browser = open_browser()

# Getting first controls
acciones = Select(browser.find_element_by_name("accion"))
ubicacion = Select(browser.find_element_by_name("estados"))
plazos = Select(browser.find_element_by_name("plazoInicial"))
plazosL = Select(browser.find_element_by_name("plazoInicialLiquidez"))
aforos = Select(browser.find_element_by_name("aforoElegido"))
cofi = Select(browser.find_element_by_name("cofinanciamiento"))
# Getting first controls

# Input first screen
ubicacion.select_by_index(9)
acciones.select_by_index(1)
valorinmueble = browser.find_element_by_name("valorviviendainicial")
valorinmueble.send_keys("1000000")
# Input first screen

# Getting second controls
monto = browser.find_element_by_name("montocreditodeseado")
valorterreno = browser.find_element_by_name("valorterreno")
valorproyecto = browser.find_element_by_name("valorproyecto")
valoringresol = browser.find_element_by_name("valorIngresosLiquidez")
submit = browser.find_element_by_name("opciones")
# Getting second controls

cofi.select_by_index(1)

j = 0

for accion in acciones.options:
    with open('Calculadora.csv', 'a', newline='') as myfile:
        # if "Comprar tu Casa" in accion.text:
        #    continue
        if "Selecciona que deseas hacer" not in accion.text:
            accion.click()
            if "Cambiar tu hipoteca a Santander" in accion.text:
                monto.send_keys("1000000")
            if "Comprar un terreno  y construir al mismo tiempo" in accion.text:
                valorterreno.send_keys("1000000")
                valorproyecto.send_keys("700000")
            if "Obtener liquidez" in accion.text:
                valoringresol.send_keys("10000")
                time.sleep(1)
            if "Comprar un terreno" in accion.text and "y construir" not in accion.text:
                valorinmueble.send_keys("1000000")
                submit.click()
                try:
                    sleep = WebDriverWait(browser, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.ID, "informacion"))
                    )
                finally:
                    time.sleep(2)
                tabla = browser.find_element_by_xpath(
                    "//a[contains(text(),'Ver')]")
                print("Comprar terreno")
                tabla.click()

                ptasa = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Tasa')]]")
                ptasa = ptasa.text.split(":")[1]
                pfecha = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Fecha')]]")
                pfecha = pfecha.text.split(":")[1]
                pcred = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Crédito')]]")
                pcred = pcred.text.split(":")[1]
                ppago = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Pago')]]")
                ppago = ppago.text.split(":")[1]
                pesquema = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Esquema')]]")
                pesquema = pesquema.text.split(":")[1]
                pplazo = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Plazo')]]")
                pplazo = pplazo.text.split(":")[1]
                enganche = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Enganche')]]")
                enganche = enganche.text.split(":")[1]
                gastos = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Gastos Notariales')]]")
                gastos = gastos.text.split(":")[1]
                gastosIni = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Gastos Iniciales')]]")
                gastosIni = gastosIni.text.split(":")[1]

                cat = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'CAT')]]")
                cat = cat.text.split(":")[1]
                comision = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Comisión')]]")
                comision = comision.text.split(":")[1]
                avaluo = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Avalúo')]]")
                avaluo = avaluo.text.split(":")[1]

                if pfecha:
                    writer.writerow({"Fecha": pfecha, "Producto": pcred, "Esquema": pesquema, "Plazo": pplazo, "Tasa": ptasa, "Aforo": "Null", "Destino": accion.text,
                                     "Gastos notariales": gastos, "Gastos Iniciales": gastosIni, "Enganche": enganche, "CAT": cat, "Comision": comision, "Avaluo": avaluo, "Pago": ppago})
                j = j+1

                try:
                    # crearImage(png,file,location,size)
                    aux = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.ID, "MB_close"))
                    )
                    aux.click()
                finally:
                    time.sleep(1)
            if "Adquisición de consultorios" in accion.text:
                submit.click()
                try:
                    sleep = WebDriverWait(browser, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.ID, "informacion"))
                    )

                finally:
                    time.sleep(2)
                tabla = browser.find_element_by_xpath(
                    "//a[contains(text(),'Ver')]")
                print("Adquisicion de consultorios")
                tabla.click()

                #file = str(j)
                #file =  file+".png"
                #png = browser.get_screenshot_as_png()
                #location = browser.find_element_by_name("mitablaparaimprimir")
                #size = location.size
                #location = location.location
                # crearImage(png,file,location,size)
                time.sleep(1)
                ptasa = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Tasa')]]")
                ptasa = ptasa.text.split(":")[1]
                pfecha = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Fecha')]]")
                pfecha = pfecha.text.split(":")[1]
                pcred = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Crédito')]]")
                pcred = pcred.text.split(":")[1]
                ppago = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Pago')]]")
                ppago = ppago.text.split(":")[1]
                pesquema = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Esquema')]]")
                pesquema = pesquema.text.split(":")[1]
                pplazo = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Plazo')]]")
                pplazo = pplazo.text.split(":")[1]
                enganche = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Enganche')]]")
                enganche = enganche.text.split(":")[1]

                gastos = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Gastos Notariales')]]")
                gastos = gastos.text.split(":")[1]
                gastosIni = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Gastos Iniciales')]]")
                gastosIni = gastosIni.text.split(":")[1]

                cat = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'CAT')]]")
                cat = cat.text.split(":")[1]
                comision = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Comisión')]]")
                comision = comision.text.split(":")[1]
                avaluo = tabla.find_element_by_xpath(
                    "//td[b[contains(text(),'Avalúo')]]")
                avaluo = avaluo.text.split(":")[1]

                if pfecha:
                    writer.writerow({"Fecha": pfecha, "Producto": pcred, "Esquema": pesquema, "Plazo": pplazo, "Tasa": ptasa, "Aforo": "Null", "Destino": accion.text,
                                     "Gastos notariales": gastos, "Gastos Iniciales": gastosIni, "Enganche": enganche, "CAT": cat, "Comision": comision, "Avaluo": avaluo, "Pago": ppago})
                j = j+1

                try:
                    # crearImage(png,file,location,size)
                    aux = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.ID, "MB_close"))
                    )
                    aux.click()
                finally:
                    time.sleep(1)
            for plazo in plazos.options:
                if "Seleccione los años" not in plazo.text and plazo.is_displayed():

                    plazo.click()
                    if aforos.options[0].is_displayed():
                        for aforo in aforos.options:
                            if "Seleccione el aforo" not in aforo.text and aforo.is_displayed():

                                aforo.click()
                                try:

                                    submit.click()
                                except:
                                    continue

                                time.sleep(3)
                                tablas = browser.find_elements_by_xpath(
                                    "//a[contains(text(),'Ver')]")
                                for tabla in tablas:
                                    print(f'AFORO: {aforo}\tTabla: {tabla}')
                                    try:
                                        sleep = WebDriverWait(browser, 10).until(
                                            EC.visibility_of_element_located(
                                                (By.XPATH, "//select[contains(@name,'plazo')]"))
                                        )

                                        tabla.click()
                                    except:
                                        continue
                                    finally:
                                        time.sleep(1)

                                    #file = str(j)
                                    #file =  file+".png"
                                    #png = browser.get_screenshot_as_png()
                                    #location = browser.find_element_by_name("mitablaparaimprimir")
                                    #size = location.size
                                    #location = location.location
                                    # crearImage(png,file,location,size)

                                    ptasa = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Tasa')]]")
                                    ptasa = ptasa.text.split(":")[1]
                                    pfecha = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Fecha')]]")
                                    pfecha = pfecha.text.split(":")[1]
                                    pcred = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Crédito')]]")
                                    pcred = pcred.text.split(":")[1]
                                    ppago = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Pago')]]")
                                    ppago = ppago.text.split(":")[1]
                                    pesquema = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Esquema')]]")
                                    pesquema = pesquema.text.split(":")[1]
                                    pplazo = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Plazo')]]")
                                    pplazo = pplazo.text.split(":")[1]
                                    if "Cambiar tu hipoteca a Santander" in accion.text:
                                        enganche = "NULL"
                                    else:
                                        enganche = tabla.find_element_by_xpath(
                                            "//td[b[contains(text(),'Enganche')]]")
                                        enganche = enganche.text.split(":")[1]

                                    gastos = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Gastos Notariales')]]")
                                    gastos = gastos.text.split(":")[1]
                                    gastosIni = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Gastos Iniciales')]]")
                                    gastosIni = gastosIni.text.split(":")[1]

                                    cat = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'CAT')]]")
                                    cat = cat.text.split(":")[1]
                                    comision = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Comisión')]]")
                                    comision = comision.text.split(":")[1]
                                    avaluo = tabla.find_element_by_xpath(
                                        "//td[b[contains(text(),'Avalúo')]]")
                                    avaluo = avaluo.text.split(":")[1]

                                    if pfecha:
                                        writer.writerow({"Fecha": pfecha, "Producto": pcred, "Esquema": pesquema, "Plazo": pplazo, "Tasa": ptasa, "Aforo": aforo.text, "Destino": accion.text,
                                                         "Gastos notariales": gastos, "Gastos Iniciales": gastosIni, "Enganche": enganche, "CAT": cat, "Comision": comision, "Avaluo": avaluo, "Pago": ppago})
                                    j = j+1

                                    try:
                                        # crearImage(png,file,location,size)
                                        aux = WebDriverWait(browser, 10).until(
                                            EC.presence_of_element_located(
                                                (By.ID, "MB_close"))
                                        )

                                        aux.click()

                                    finally:
                                        time.sleep(1)

                    else:
                        try:
                            submit.click()
                        except:
                            continue

                        time.sleep(3)
                        tablas = browser.find_elements_by_xpath(
                            "//a[contains(text(),'Ver')]")
                        for tabla in tablas:
                            print("Ultima tabla")
                            try:
                                sleep = WebDriverWait(browser, 10).until(
                                    EC.presence_of_all_elements_located(
                                        (By.ID, "informacion"))
                                )
                                tabla.click()

                            finally:
                                time.sleep(2)
                         #file = str(j)
                            #file =  file+".png"
                            #png = browser.get_screenshot_as_png()
                            #location = browser.find_element_by_name("mitablaparaimprimir")
                            #size = location.size
                            #location = location.location
                            # crearImage(png,file,location,size)
                            ptasa = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Tasa')]]")
                            ptasa = ptasa.text.split(":")[1]
                            pfecha = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Fecha')]]")
                            pfecha = pfecha.text.split(":")[1]
                            pcred = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Crédito')]]")
                            pcred = pcred.text.split(":")[1]
                            ppago = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Pago')]]")
                            ppago = ppago.text.split(":")[1]
                            pesquema = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Esquema')]]")
                            pesquema = pesquema.text.split(":")[1]
                            pplazo = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Plazo')]]")
                            pplazo = pplazo.text.split(":")[1]
                            if "Cambiar tu hipoteca a Santander" in accion.text:
                                enganche = "NULL"
                            else:
                                enganche = tabla.find_element_by_xpath(
                                    "//td[b[contains(text(),'Enganche')]]")
                                enganche = enganche.text.split(":")[1]
                            gastos = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Gastos Notariales')]]")
                            gastos = gastos.text.split(":")[1]
                            gastosIni = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Gastos Iniciales')]]")
                            gastosIni = gastosIni.text.split(":")[1]

                            cat = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'CAT')]]")
                            cat = cat.text.split(":")[1]
                            comision = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Comisión')]]")
                            comision = comision.text.split(":")[1]
                            avaluo = tabla.find_element_by_xpath(
                                "//td[b[contains(text(),'Avalúo')]]")
                            avaluo = avaluo.text.split(":")[1]

                            if pfecha:
                                writer.writerow({"Fecha": pfecha, "Producto": pcred, "Esquema": pesquema, "Plazo": pplazo, "Tasa": ptasa, "Aforo": "Null", "Destino": accion.text,
                                                 "Gastos notariales": gastos, "Gastos Iniciales": gastosIni, "Enganche": enganche, "CAT": cat, "Comision": comision, "Avaluo": avaluo, "Pago": ppago})
                            j = j+1
                            try:
                                aux = WebDriverWait(browser, 10).until(
                                    EC.presence_of_element_located(
                                        (By.ID, "MB_close"))
                                )
                                aux.click()
                            finally:
                                time.sleep(1)
            for plazol in plazosL.options:
                if "Seleccione los años" not in plazol.text and plazol.is_displayed():
                    plazol.click()
                    submit.click()
                    time.sleep(1)
                    tablas = browser.find_elements_by_xpath(
                        "//a[contains(text(),'Ver')]")
                    for tabla in tablas:
                        print(f"Plazo: {plazol}\tTabla: {tabla.text}")
                        try:
                            sleep = WebDriverWait(browser, 10).until(
                                EC.presence_of_all_elements_located(
                                    (By.ID, "informacion"))
                            )
                            tabla.click()

                        finally:
                            time.sleep(2)
                        ptasa = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Tasa')]]")
                        ptasa = ptasa.text.split(":")[1]
                        pfecha = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Fecha')]]")
                        pfecha = pfecha.text.split(":")[1]
                        pcred = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Crédito')]]")
                        pcred = pcred.text.split(":")[1]
                        ppago = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Pago')]]")
                        ppago = ppago.text.split(":")[1]
                        pesquema = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Esquema')]]")
                        pesquema = pesquema.text.split(":")[1]
                        pplazo = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Plazo')]]")
                        pplazo = pplazo.text.split(":")[1]

                        enganche = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Enganche')]]")
                        enganche = enganche.text.split(":")[1]

                        gastos = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Gastos Notariales')]]")
                        gastos = gastos.text.split(":")[1]
                        gastosIni = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Gastos Iniciales')]]")
                        gastosIni = gastosIni.text.split(":")[1]

                        cat = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'CAT')]]")
                        cat = cat.text.split(":")[1]
                        comision = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Comisión')]]")
                        comision = comision.text.split(":")[1]
                        avaluo = tabla.find_element_by_xpath(
                            "//td[b[contains(text(),'Avalúo')]]")
                        avaluo = avaluo.text.split(":")[1]

                        if pfecha:
                            writer.writerow({"Fecha": pfecha, "Producto": pcred, "Esquema": pesquema, "Plazo": pplazo, "Tasa": ptasa, "Aforo": "Null", "Destino": accion.text,
                                             "Gastos notariales": gastos, "Gastos Iniciales": gastosIni, "Enganche": enganche, "CAT": cat, "Comision": comision, "Avaluo": avaluo, "Pago": ppago})
                        j = j+1

                        try:
                            aux = WebDriverWait(browser, 10).until(
                                EC.presence_of_element_located(
                                    (By.ID, "MB_close"))
                            )
                            aux.click()
                        finally:
                            time.sleep(1)
browser.close()
