import curses, time

#--------------------------------------
def input_char(message):
    try:
        win = curses.initscr()
        while True: 
            ch = win.getch()
            if ch in range(32, 127): break
            time.sleep(0.05)
    except: raise
    finally:
        curses.endwin()
    return chr(ch)
#--------------------------------------
while(1):
	c = input_char('')
	print(c+"\n")
	time.sleep(0.1)
