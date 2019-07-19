from . import selenium_automaton
from selenium.webdriver.support.ui import Select

import time
import csv

class BancomerAutomaton(selenium_automaton.SeleniumAutomaton):
    def __init__(self):
        self.set_control_data()
        self.connect(10)
        self.get_data()
        self.driver.quit()

    def set_control_data(self):
        self.url = 'https://www.bancomer.com/personas/productos/creditos/credito-hipotecario/simulador-credito-hipotecario.html'
        self.destinos = {
            'Comprar casa': 'D01',
            'Comprar un terreno': 'D02',
            'Remodelar tu casa': 'D05',
            'Cambiar tu hipoteca': 'D06',
            'Obtener liquidez': 'D07'
        }
        self.iframe_xpath = '//*[@id="par-iframe"]'
        self.set_producto_controls_data()
        self.set_subproducto_controls_data()

    def set_producto_controls_data(self):
        self.contenedor_productos_xpath = '//*[@id="destinos"]/div/div/ul'
        self.select_plazos_xpath = '//*[@id="selectPlazoResponsive"]'
        self.minimo_xpath = '//*[@id="minSlider1"]'
        self.maximo_xpath = '//*[@id="maxSlider1"]'
        self.valor_vivienda_xpath = '//*[@id="input1"]'
        self.credito_infovissste_xpath = '//*[@id="creditoInfovissste "]'
        self.calcular_xpath = '//*[@id="calcularCredito"]'

    def set_subproducto_controls_data(self):
        self.encabezado_xpath = '//*[@id="productos"]/div/div[1]/p'
        self.cat_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[8]'
        self.ingresos_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[7]'
        self.tasa_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[6]'
        self.pago_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[3]'
        self.prestamo_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[1]'
        self.tipo_tasa_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[5]'
        self.pago_inicial_xpath = '//*[@id="productos"]/div/div[2]/dl/dd[4]'
        self.amortizacion_xpath = '//*[@id="productos"]/div/div[3]/button[1]'
        self.datos_credito_button_xpath = '//*[@id="datosCredito"]'
        self.gastos_notariales_xpath = '//*[@id="datos-GastosNotariales"]'

    def get_controls(self):
        self.switch_iframe()
        self.get_controls_iframe()

    def switch_iframe(self):
        self.iframe = self.driver.find_element_by_xpath(self.iframe_xpath)
        self.driver.switch_to.frame(self.iframe)

    def get_controls_iframe(self):
        self.contenedor_productos = self.driver.find_element_by_xpath(self.contenedor_productos_xpath)
        self.productos = self.contenedor_productos.find_elements_by_tag_name('a')
        self.select_plazos = Select(self.driver.find_element_by_xpath(self.select_plazos_xpath))
        self.minimo = self.driver.find_element_by_xpath(self.minimo_xpath)
        self.maximo = self.driver.find_element_by_xpath(self.maximo_xpath)
        self.valor_vivienda = self.driver.find_element_by_xpath(self.valor_vivienda_xpath)
        self.calcular = self.driver.find_element_by_xpath(self.calcular_xpath)

    def get_subproducto_controls(self):
        self.encabezado_element = self.driver.find_element_by_xpath(self.encabezado_xpath)
        self.cat_element = self.driver.find_element_by_xpath(self.cat_xpath)
        self.ingresos_element = self.driver.find_element_by_xpath(self.ingresos_xpath)
        self.tasa_element = self.driver.find_element_by_xpath(self.tasa_xpath)
        self.pago_element = self.driver.find_element_by_xpath(self.pago_xpath)
        self.prestamo_element = self.driver.find_element_by_xpath(self.prestamo_xpath)
        self.tipo_tasa_element = self.driver.find_element_by_xpath(self.tipo_tasa_xpath)
        self.pago_inicial_element = self.driver.find_element_by_xpath(self.pago_inicial_xpath)
        self.amortizacion_element = self.driver.find_element_by_xpath(self.amortizacion_xpath)
        self.datos_credito_button = self.driver.find_element_by_xpath(self.datos_credito_button_xpath)
        self.gastos_notariales_element = self.driver.find_element_by_xpath(self.gastos_notariales_xpath)

    def get_data(self):
        self.get_controls()
        self.get_productos()

    def get_productos(self):
        self.data_dictionary = []
        self.subproducto_id = 0
        for index_producto in range(len(self.productos)-1):
            producto = self.productos[index_producto]
            #self.click_delay(producto, 2)
            self.driver.execute_script('arguments[0].click();', producto)
            time.sleep(1)
            print(f'\n\tDestino: {producto.text}\n\tMinimo: {self.minimo.text}\n\tMaximo: {self.maximo.text}\n\tPrograma: {producto.text == "Comprar casa"}\n\tDestino: {self.destinos[producto.text]}\n')
            minimo_int = int(self.minimo.text[9:].replace(',', '')[:-4])
            maximo_int = int(self.maximo.text[9:].replace(',', '')[:-4])
            step = int((maximo_int - minimo_int)/10)
            print(f'Step: {step}')
            for index_plazo in range(len(self.select_plazos.options)):
                print(f'Index Plazo: {index_plazo}')
                plazo = self.select_plazos.options[index_plazo]
                self.click_delay(plazo, 0.1)
                self.get_subproductos(plazo.text, range(minimo_int, maximo_int, step))
                print('\nRefresh!')
                self.driver.refresh()
                time.sleep(3)
                self.get_controls()
                self.driver.execute_script('arguments[0].click();', self.productos[index_producto])
                time.sleep(1)
        self.export_csv('bancomer.csv')

    def get_subproductos(self, plazo, rango):
        self.valor_vivienda = self.driver.find_element_by_xpath(self.valor_vivienda_xpath)
        for i in rango:
            self.subproducto_id += 1
            valor = str(i) + '0'*4
            print(f'Valor: {valor}')
            self.valor_vivienda.clear()
            self.valor_vivienda.send_keys(valor)
            time.sleep(1)
            #self.click_delay(self.calcular, 10)
            self.driver.execute_script('arguments[0].click();', self.calcular)
            time.sleep(5)
            self.get_subproducto_controls()
            aforo = float(self.prestamo_element.text.replace(' ', '').replace(',', '').replace('$', ''))/float(valor)*100
            self.data_dictionary.append({
                'Subproducto': self.subproducto_id,
                'Producto': self.encabezado_element.text,
                'Valor Vivienda': '$'+str(valor)+'.00',
                'AFORO': str(aforo)+'%',
                'Plazo': plazo,
                'Ingresos Requeridos': self.ingresos_element.text,
                'Tasa de Interes': self.tasa_element.text,
                'Tipo de Tasa': self.tipo_tasa_element.text,
                'CAT sin IVA': self.cat_element.text,
                'Pago': self.pago_element.text,
                'Frecuencia de Pago': 'Mensual'
            })
            self.driver.execute_script('arguments[0].click();', self.amortizacion_element)
            time.sleep(1)
            self.driver.execute_script('arguments[0].click();', self.datos_credito_button)
            time.sleep(0.5)
            print(f'Gastos Notariales: {self.gastos_notariales_element.text}')
            #print(f'Subproducto: {self.subproducto_id}\tProducto: {self.encabezado_element.text}\tValor: ${valor}.00\tPrestamo: {self.prestamo_element.text}\tCAT: {self.cat_element.text}\tIngresos: {self.ingresos_element.text}\tPago: {self.pago_element.text}\tTasa: {self.tasa_element.text}\tTipo Tasa: {self.tipo_tasa_element.text}')

    def export_csv(self, file_name):
        with open(file_name, mode='w', newline='') as csv_file:
            fieldnames = ['Subproducto', 'Producto', 'Valor Vivienda', 'AFORO', 'Plazo', 'Ingresos Requeridos', 'Tasa de Interes', 'Tipo de Tasa', 'CAT sin IVA', 'Pago', 'Frecuencia de Pago']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data_dictionary:
                writer.writerow(row)