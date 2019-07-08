from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
import win32clipboard
import time

class HSBCAutomaton:
  def __init__(self):
    self.keyboard = KeyboardController()
    self.mouse = MouseController()

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
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

  def get_data_from_cell(self, position):
    time.sleep(0.2)
    self.move_mouse_and_click(position)
    self.copy()
    return self.get_clibboard()[:-3]

if __name__ == "__main__":
  automaton = HSBCAutomaton()
  automaton.move_mouse_and_click((62, 14))
  for plazo in range(4):
    for i in range(1, 3):
      automaton.move_mouse_and_click((390, 528))
      automaton.keyboard.type(str(i) + '0'*6)
      automaton.move_mouse_and_click((369, 553))
      automaton.move_mouse_and_click((436, 557))
      for _ in range(plazo+1):
        automaton.type_key(Key.down)
      automaton.type_key(Key.enter)
      print(f'Enganche: {automaton.get_data_from_cell((662, 411))}')
      print(f'AFORO: {automaton.get_data_from_cell((628, 515))}')
      print(f'Tasa: {automaton.get_data_from_cell((658, 528))}')
      print(f'Pago mensual: {automaton.get_data_from_cell((658, 540))}')
      print(f'CAT: {automaton.get_data_from_cell((657, 555))}')
      print(f'Ingresos: {automaton.get_data_from_cell((660, 567))}')
