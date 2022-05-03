from time import sleep
import math
import serial
import tkinter
from tkinter import ttk


REAL_ZERO = [0, -3, 17, -7, 0, 0]
FACTOR = [1, 1, 0.725, 1, 1, 1]


def send_pos(f, pos):
    f.write(bytes(';'.join((str(int(p * f)) for p, f in zip(pos, FACTOR))) + '\n', 'ascii'))


def smooth(f, a, b):
    for i in range(0, 20):
        t = (i + 1) / 20
        l = [int(c + t * (d - c)) for c, d in zip(a, b)]
        send_pos(f, l)
        sleep(0.025)


#with open('/dev/null', 'wb') as f:
with serial.Serial('/dev/ttyACM0', 9600) as f:
    sleep(2)

    pos = [0] * 6
    send_pos(f, pos)

    tk = tkinter.Tk()
    tk.wm_title("Servo GUI")

    sliderfr = ttk.Frame(tk)
    sliderfr.pack(side='left')
    fr = ttk.Frame(sliderfr, width=300)
    fr.pack()

    cb_disable = False
    def cb(i, s):
        def inner(a, b, c):
            if not cb_disable:
                pos[i] = s._variable.get()
                send_pos(f, pos)
        return inner

    scales = [ttk.LabeledScale(sliderfr, from_=-90, to=90) for i in range(6)]
    for i, s in enumerate(scales):
        s.scale.set(0)
        s._variable.trace_add('write', cb(i, s))
        s.pack(padx=5, pady=5, fill='both')

    statefr = ttk.Frame(tk)
    statefr.pack(side='right')

    buttonsfr = ttk.Frame(statefr)
    buttonsfr.pack(side='top')

    def reset():
        global cb_disable, pos
        cb_disable = True
        for s in scales:
            s.scale.set(0)
        cb_disable = False
        pos = [0] * 6
        send_pos(f, pos)

    ttk.Button(buttonsfr, text='Reset', command=reset).pack(side='left')

    GRAB_AMOUNT = -67

    saved = [
        REAL_ZERO.copy(),
        [-32, 59, 44, 90, 0, 0],
        [-32, 59, 44, 90, 0, GRAB_AMOUNT],
        [-54, -43, -38, -90, 0, GRAB_AMOUNT],
        [-54, -50, -36, -90, 0, 0],
    ]

    names = [
        'Straight',
        'Hover',
        'Grab',
        'Place',
        'Drop',
    ]

    lbox = tkinter.Listbox(statefr, selectmode='SINGLE', )
    lbox.pack(side='top', fill='both')
    lbox.insert(tkinter.END, *[names[i] if i < len(names) else str(i+1) for i in range(len(saved))])

    def do_state(s):
        global cb_disable, pos
        prev = pos.copy()
        pos = saved[s].copy()

        cb_disable = True
        for i, s in enumerate(scales):
            s.scale.set(pos[i])
        cb_disable = False
        smooth(f, prev, pos)

    def select_state(e):
        global pos
        if len(e.widget.curselection()) > 0:
            sel = e.widget.curselection()[0]
            do_state(sel)

    lbox.bind("<<ListboxSelect>>", select_state)

    def save():
        saved.append(pos.copy())
        lbox.insert(tkinter.END, str(len(saved)))

    ttk.Button(buttonsfr, text='Save', command=save).pack(side='right')

    def run():
        for i in range(5):
            do_state(i)
            sleep(1)

    ttk.Button(statefr, text='Run', command=run).pack(fill='both', side='bottom')

    tk.mainloop()
