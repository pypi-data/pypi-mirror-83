from tkinter import *
import time 
version  = '0.1.0'
author = 'github@RonanBasto'

"""
 _______________________________________________________________________
| ######  #     # #    #    ###   ######   #####    #     #   ###       | 
| #     #  #   #  #   #      #    #     # #         #     #    #        |
| #     #   # #   #  #       #    #     # #         #     #    #        |
| ######     #    ###        #    #     # #    ###  #     #    #        |
| #          #    #  #       #    #     # #      #  #     #    #        |
| #          #    #   #      #    #     # #      #  #     #    #        |
| #          #    #    #    ###   ######   #####    #####     ###       |
|_______________________________________________________________________|

"""
#[var]
button=[]
checkbox=[]
label=[]
build_map=[]
new_on_click= []
text_title="Pykidgui"
window_geometry=""
new_on_click_var = []
new_on_click_text=[]
window_name="window"

#[func]

def new_button(nb):
    button.append(nb)
    
def new_label(nl):
    label.append(nl)
    
def new_checkbox(ncb):
    checkbox.append(ncb)
    
def new_on_click(noc):
   new_on_click_var.append(noc)


def new_click_text(noct):
   new_on_click_text.append(noct)


def new_message_erro(msg):
    root = Tk()
    root.title("Erro!")
    root.geometry(window_geometry)
    Button(text="Ok")
                             
    msg = Message( root, text = msg)   
    msg.pack()


def new_message_title(title,msg):
    root = Tk()
    root.title(title)
    msg = Message( root, text = msg)
    root.geometry("150x150")
    msg.pack()    
def add_build_map(abm):
    build_map.append(abm)

def window_name(win):
    window_name= win

#[class]    
class gui(Tk):
    def __init__(window_name):
        Tk.__init__(window_name)
        if text_title != '':
                window_name.title(text_title)
        if window_geometry != '':
                window_name.geometry(window_geometry)
        
           
        count=-1
        countclick=-1
        countlabel=-1
        countbutton=-1
        countcheckbox=-1
        countonclick=-1
        countonclicktext=-1
        for x in build_map:
            count+=1 
            
            if "on_click" in build_map[count] and len(new_on_click_var )!= 0 and len(new_on_click_text)!= 0:   
                       countonclick+=1
                       countonclicktext+=1
                       Button(text=new_on_click_text[countonclicktext],command =new_on_click_var[countonclick]).pack()  
                      
            if "label" in build_map[count] and len(label)!= 0:
                     countlabel+=1   
                     if "label:LEFT" in build_map[count] or "label:left" in build_map[count]:   
                         labelleft = label[countlabel]  
                         window_name.comp = Label(text =labelleft[:6])               
                         window_name.comp.pack(side = LEFT)
                     else:
                         window_name.comp = Label(text =label[countlabel])               
                         window_name.comp.pack()    
            if "checkbox" in build_map[count] and len(checkbox)!= 0:
                    countcheckbox+=1
                    
                    if "checkbox:LEFT" in build_map[count] or "checkbox:left" in build_map[count]:
                            Checkbox   = IntVar()
                            checkleft  =checkbox[countcheckbox]
                            window_name.comp=Checkbutton(text = checkleft[:8],  
                                  variable = Checkbox, 
                                  onvalue = 1, 
                                  offvalue = 0, 
                                  height = 5, 
                                  width = 10)
                            window_name.comp.pack(side = LEFT) 
                              
                             
                    else:
                        Checkbox = IntVar()
                        window_name.comp=Checkbutton(text = checkbox[countcheckbox],  
                          variable = Checkbox, 
                          onvalue = 1, 
                          offvalue = 0, 
                          height = 5, 
                          width = 10)
                      
                        window_name.comp.pack()  
                      
            if "button" in build_map[count] and len(button)!= 0:    
                     countbutton+=1
                     if "button:LEFT" in build_map[count] or "button:left" in build_map[count]:
                         buttonLEFT=button[countbutton]   
                         window_name.comp = Button(text=buttonLEFT[:6])
                         window_name.comp.pack(side = LEFT)

                     elif button[countbutton] == "sair" or button[countbutton] == "Sair":
                             window_name.comp = Button(text=button[countbutton],command=window_name.destroy)
                             window_name.comp.pack()
                     
                     else:  
                             window_name.comp = Button(text=button[countbutton])
                             window_name.comp.pack()
           
                 


