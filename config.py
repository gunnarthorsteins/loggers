from datetime import datetime

default = {'FONT': 'UBUNTU',
           'FONT_SIZE': 20,
           'DT_FORMAT': r'%Y-%m-%d %H:%M',
           'INCREMENT': 0.06,
           'now': datetime.now(),
           'BORDER': 0}

worklog = {'TITLE': 'Work Logger',
           'H': 1000,
           'W': 300,
           'REL_H': 0.07,
           'REL_W': 0.92,
           'REL_X': 0.04,
           'BACKGROUND_COLOR': '#435363',
           'FONT_COLOR': '#ffffff',
           'BUTTON_COLOR': '#586D81',
           'BUTTON_FONT_COLOR': '#ffffff'}

feedback = {'TITLE': 'Information',
            'H': 247,
            'W': 400,
            'REL_H': 0.6,
            'REL_W': 0.92,
            'REL_X': 0.04,
            'BACKGROUND_COLOR': '#435363',
            'FONT_COLOR': '#ffffff'}

exercise = {'TITLE': 'Exercise Log',
            'H': 1020,
            'W': 200,
            'REL_H': 0.056,
            'REL_W': 0.92,
            'REL_X': 0.04,
            'BACKGROUND_COLOR': '#435363',
            'FONT_COLOR': '#ffffff',
            'BUTTON_COLOR': '#586D81',
            'BUTTON_FONT_COLOR': '#ffffff'}

warning = {'TITLE': 'WARNING',
           'H': 300,
           'W': 500,
           'BACKGROUND_COLOR': '#435363'}

worklog.update(default)
feedback.update(default)
exercise.update(default)
warning.update(default)