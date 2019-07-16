from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
import win32clipboard
import time
import csv
import db_manager

class HSBCAutomaton:
  TaskbarCoord         = ( 62,  14)
  DestinoCellCoord     = (355, 462)
  DestinoSelectorCoord = (439, 464)
  ValorViviendaCoord   = (390, 528)
  PlazoCellCoord       = (369, 553)
  PlazoSelectorCoord   = (436, 557)
  EngancheCoord        = (662, 411)
  AforoCoord           = (628, 515)
  TasaCoord            = (658, 528)
  PagoCoord            = (658, 540)
  CatCoord             = (657, 555)
  IngresosCoord        = (660, 567)
  TasasCellCoord       = (351, 489)
  TasasSelectorCoord   = (438, 489)
  AvaluoCoord          = (662, 423)
  ComisionCoord        = (688, 438)
  NotarialesCoord      = (697, 461)
  DesembolsoCoord      = (663, 475)

  plazosDict = { 0: 60 }
  plazosDict.update(dict.fromkeys([1,  5], 120))
  plazosDict.update(dict.fromkeys([2, 10], 180))
  plazosDict.update(dict.fromkeys([3, 15], 240))

  productosList = [
    19, #Crédito Hipotecario HSBC Pago Fijo
    21, #Pago de Hipoteca HSBC Pago Fijo
    23, #Liquidez HSBC
    20, #Crédito Hipotecario HSBC PAGO FIJO para clientes PREMIER
    22, #Pago de Hipoteca más Liquidez HSBC
  ]

  def __init__(self):
    self.keyboard = KeyboardController()
    self.mouse = MouseController()
    self.data = []

  def move_mouse_and_click(self, position):
    self.mouse.position = position
    self.click()

  def click(self):
    self.mouse.press(Button.left)
    self.mouse.release(Button.left)
    time.sleep(0.1)

  def type_key(self, key):
    self.keyboard.press(key)
    self.keyboard.release(key)
    time.sleep(0.1)

  def type_command(self, key1, key2):
    self.keyboard.press(key1)
    self.type_key(key2)
    self.keyboard.release(key1)
    time.sleep(0.1)

  def copy(self):
    self.type_command(Key.ctrl, 'c')

  def get_clibboard(self):
    time.sleep(0.2)
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    time.sleep(0.2)
    return data

  def get_data_from_cell(self, position):
    time.sleep(0.1)
    self.move_mouse_and_click(position)
    self.copy()
    return self.get_clibboard()[:-3]

  def type_valor_vivienda(self, valor):
    self.move_mouse_and_click(self.ValorViviendaCoord)
    self.keyboard.type(valor)
    time.sleep(0.1)

  def start_automaton(self):
    self.move_mouse_and_click(self.TaskbarCoord)
    index = 1
    for destino in range(5): #Iterando destinos
      if destino == 0:
        for tasa in range(4):
          for plazo in self.get_plazos_of_destino(destino):
            self.select_plazo(plazo)
            print(f'Destino: {destino}\tPlazo: {plazo}')
            for valor in range(4, 11): #11
              self.type_valor_vivienda(str(valor)+'0'*5)
              self.get_info_from_file(index, valor, plazo, destino)
              index += 1
            for valor in self.get_max_value_of_destino(destino):
              self.type_valor_vivienda(str(valor)+'0'*5)
              self.get_info_from_file(index, valor, plazo, destino)
              index += 1
          self.change_tasa()
      else:
        for plazo in self.get_plazos_of_destino(destino):
          self.select_plazo(plazo)
          print(f'Destino: {destino}\tPlazo: {plazo}')
          for valor in range(4, 5): #11
            self.type_valor_vivienda(str(valor)+'0'*5)
            self.get_info_from_file(index, valor, plazo, destino)
            index += 1
          for valor in self.get_max_value_of_destino(destino):
            self.type_valor_vivienda(str(valor)+'0'*5)
            self.get_info_from_file(index, valor, plazo, destino)
            index += 1
      self.change_destino()
    self.save_data_to_db()

  def change_destino(self):
    self.move_mouse_and_click(self.DestinoCellCoord)
    self.move_mouse_and_click(self.DestinoSelectorCoord)
    self.type_key(Key.down)
    self.type_key(Key.enter)

  def change_tasa(self):
    self.move_mouse_and_click(self.TasasCellCoord)
    self.move_mouse_and_click(self.TasasSelectorCoord)
    self.type_key(Key.down)
    self.type_key(Key.enter)

  def select_plazo(self, plazo):
    self.move_mouse_and_click(self.PlazoCellCoord)
    self.move_mouse_and_click(self.PlazoSelectorCoord)
    for _ in range(plazo+1):
      self.type_key(Key.down)
    self.type_key(Key.enter)

  def get_info_from_file(self, index, valor, plazo, destino):
    self.data.append((
      self.productosList[destino],
      str(valor) + '0'*5,
      self.get_data_from_cell(self.AforoCoord),
      self.plazosDict.get(plazo),
      self.clean_float_number(self.get_data_from_cell(self.IngresosCoord)),
      self.clean_float_number(self.get_data_from_cell(self.TasaCoord)),
      0,
      self.clean_float_number(self.get_data_from_cell(self.CatCoord)),
      0,
      self.clean_float_number(self.get_data_from_cell(self.PagoCoord)),
      self.clean_float_number(self.get_data_from_cell(self.AvaluoCoord)),
      self.clean_float_number(self.get_data_from_cell(self.ComisionCoord)),
      self.clean_float_number(self.get_data_from_cell(self.NotarialesCoord)),
      self.clean_float_number(self.get_data_from_cell(self.DesembolsoCoord)),
    ))

  def get_plazos_of_destino(self, destino):
    if destino == 2:
      return range(3)
    if destino == 4:
      return range(0, 20, 5)
    return range(4)

  def get_max_value_of_destino(self, destino):
    if destino == 2:
      return range(15, 55, 5)
    return range(15, 105, 5)

  def clean_float_number(self, number):
    return number.replace('$', '').replace(',', '').replace('%', '')

  def save_data_to_db(self):
    manager = db_manager.DBManager()
    for row in self.data:
        manager.insert_subproducto(row)
    manager.close_connection()

if __name__ == "__main__":
  automaton = HSBCAutomaton()
  automaton.start_automaton()
