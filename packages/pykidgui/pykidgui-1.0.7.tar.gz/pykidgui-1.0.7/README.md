README
======

With simple and dynamic goal you can create a direct access class layer using import pykidgui as pk, then
Be able to create your interface using pk or even create without it using pure tkinter element.
Basic commands are used to call the class tkinter,
Line of logic is (pk.add_build_map = creating layer view // pk.new_checkbox = creating checkbox)

Ex.:
import pykidgui as pk

def msg():
     pk.new_message_erro("msg")
	 
Pk.add_build_map ('checkbox: LEFT')
Pk.new_checkbox ('check2')
pk.new_label("button 1")
pk.add_build_map("label")

pk.new_click_text("message teste") 
pk.new_on_click(msg)
pk.add_build_map("on_click")


pk.new_label("button 2")
pk.add_build_map("label")


pk.new_click_text("Resultado") 
pk.new_on_click(x)
pk.add_build_map("on_click")

pk.text_title="test title"
pk.window_geometry="200x200"


pk.gui()
