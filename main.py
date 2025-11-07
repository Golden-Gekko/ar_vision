# from camera_tool import CameraTool

# import cv2
# # cam = CameraTool(0)
# import win32api
# monitors = win32api.EnumDisplayMonitors()

# for monitor in monitors:
#     print(win32api.GetMonitorInfo(monitor[0])['Monitor'])
# # win32api.GetMonitorInfo(monitors[0][0])

# cv2.namedWindow('AR View', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('AR View', 100, 100)
# cv2.moveWindow('AR View', 100, 100)

# while True:
#     if cv2.waitKey(1) == ord('q'):
#         break


from window import Window

def m_func():
    print('m_func')
def t_func():
    print('t_func')
def plus_func():
    print('+_func')

ar_win = Window(window_name='AR View', width=600, height=400)


ar_win.set_key_callback('m', m_func)
ar_win.set_key_callback('t', t_func)
ar_win.set_key_callback('+', plus_func)


ar_win.run()