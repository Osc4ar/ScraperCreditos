from pynput.mouse import Controller as MouseController
mouse = MouseController()
print('{0}'.format(mouse.position))