from dataclasses import dataclass
from view.style.styleValues import Color, FontSize


dataclass
class buttonStyle:
    BASE = "background-color:#fff;\
            border:none;"
    
    ButtonActive = f"background-color:{Color.GREEN};\
                    color:white;\
                    border-radius:5;\
                    font-size:{FontSize.BTN}"
                    
    ButtonInactive = f"background-color:{Color.GREYMEDIUM1};\
                    color:white;\
                    border-radius:5;\
                    font-size:{FontSize.BTN}"