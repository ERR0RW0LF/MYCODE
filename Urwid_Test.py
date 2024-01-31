from __future__ import annotations

import urwid

def exit_on_q(key):
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()

txt = urwid.Text("Hello World")
fill = urwid.Filler(txt, "top")
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()