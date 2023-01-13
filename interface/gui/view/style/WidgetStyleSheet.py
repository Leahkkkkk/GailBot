from util.Style import FontSize, Dimension, Color, FontFamily

INPUT_TEXT = f" color: {Color.INPUT_TEXT};\
                border: 1px solid {Color.INPUT_BORDER};\
                background-color: {Color.INPUT_BACKGROUND}"

 
COMBO_BOX =  f"QComboBox {{background-color: {Color.INPUT_BACKGROUND};\
                color:{Color.INPUT_TEXT};\
                border:1px solid {Color.INPUT_BORDER};\
                padding: 3px 12px 3px 12px;\
                border-radius: 7px;\
                margin: 5px;}}"
                
FILE_TABLE = f"{{background-color: {Color.MAIN_BACKGROUND};\
                color:{Color.MAIN_TEXT};\
                border: 0.5px solid {Color.TABLE_BORDER};}}"

TABLE_HEADER = f"background-color:{Color.TABLE_HEADER};\
                font-size:{FontSize.SMALL};\
                font-family:{FontFamily.MAIN};\
                color:{Color.PRIMARY_INTENSE}"
                
SCROLL_BAR = f"background-color:{Color.SCROLL_BAR};\
              border: 1px solid {Color.MAIN_BACKGROUND}"


MESSAGE_BOX = f"color: {Color.MAIN_TEXT}"
MESSAGE_BOX_BTN = "color: #000;"

PROGRESS_BAR = f"QSlider::groove:horizontal {{\
                border: 1px solid #bbb;\
                background: {Color.PRIMARY_BUTTON};\
                height: 10px; border-radius: 4px;}}\
                QSlider::add-page:horizontal {{\
                background: {Color.GREYEXTRALIGHT};\
                border: 1px solid #777;\
                height: 10px; border-radius: 4px;}}\
                QSlider::handle:horizontal {{\
                background: qlineargradient(x1:0, y1:0, x2:1,\
                y2:1,stop:0 #eee, stop:1 #ccc);\
                border: 1px solid #777;width: 13px; margin-top: \
                -2px; margin-bottom: -2px; border-radius: 4px;}}"