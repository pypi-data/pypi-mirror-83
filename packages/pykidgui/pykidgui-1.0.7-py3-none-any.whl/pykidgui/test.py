name = "pykidgui"
import pykidgui as pk

'''
print(pk.version)
pk.text_title= "Loja"
pk.window_geometry = "550x550"
pk.window_name("home")

pk.add_build_map("checkbox")
pk.new_checkbox("check1")

pk.add_build_map("checkbox:LEFT")
pk.new_checkbox("check2")
pk.add_build_map("checkbox:left")
pk.new_checkbox("check clique3")



pk.add_build_map("label")
pk.new_label("Loja teste")

pk.add_build_map("on_click")
pk.new_on_click_text = "cadastar produtos"
pk.new_on_click_var=te.j

pk.add_build_map("label")



pk.add_build_map("button")
pk.new_button("sair")



print(pk.build_map)
pk.star()
'''
def msg():
     pk.new_message_erro("testando o sistem de mansagens!!")
def k():
    x = 500
    y = 500
    result = x+y
    try:
        return result
    except:
        pk.new_message_title("Erro","Erro de script")


def x():
    x = 500
    y = 500
    result = x+y
    msg="variavel msg"
    pk.new_message_title("resultado",result)
    

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
