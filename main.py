from kivy.config import Config
# Config.set('graphics', 'resizable', False)

import numpy as np
import pandas as pd

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import ObjectProperty, ReferenceListProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.textfield import MDTextField

scale = 4
Window.size = (73.9 * scale, 155 * scale)
Window.clearcolor = (1, 1, 1, 1)
Config.set("kivy", "exit_on_escape", "0") # to prevent app from exiting on esc

KV = """
Screen:

    NavigationLayout:

        ScreenManager:
            id: screen_manager

            Screen:
                name: "main_screen"

                BoxLayout:
                    orientation: "vertical"
                    # padding_left, padding_top, padding_right, padding_bottom
                    padding: 8, 0, 8, 8

                    BoxLayout:
                        orientation: "horizontal"
                        size_hint_y: 0.12

                        MDIconButton:
                            icon: "menu"
                            on_press: nav_drawer.set_state()

                        MDTextField:
                            id: search_field
                            hint_text: "Search your notes"
                            # on_text: root.set_list_md_icons(self.text, True)

                        list_grid_view_button:

                        # need a function here later to determine alphabet etc
                        MDIconButton:
                            icon: "alpha-m-circle"
                            on_press:

                    # recycle view here
                    RV:
                        id: rv


                MDFloatingActionButton:
                    icon: "plus"
                    user_font_size: "30sp"
                    pos_hint: {"center_x": 0.85, "center_y": 0.1}
                    md_bg_color: 1, 1, 1, 1
                    elevation_normal: 10
                    on_press: 
                        screen_manager.current = "new_note_screen"
                        screen_manager.transition.direction = "left"
                        app.clear_screen()
                        
                MDNavigationDrawer:
                    id: nav_drawer

                    ContentNavigationDrawer:
                        id: content_drawer

            Screen:
                name: "new_note_screen"

                BoxLayout:
                    orientation: "vertical"

                    BoxLayout:
                        id: top_panel
                        
                        orientation: "horizontal"
                        size_hint_y: 0.12

                        MDIconButton:
                            icon: "arrow-left"
                            on_press: 
                                screen_manager.current = "main_screen"
                                screen_manager.transition.direction = "right"

                        # adds an empty widget to take up the space
                        Widget:

                        MDIconButton:
                            id: pin_outline
                            icon: "pin-outline"
                            on_press:

                        MDIconButton:
                            id: bell_plus_outline
                            icon: "bell-plus-outline"
                            on_press:
                        
                        MDIconButton:
                            id: archive_arrow_down_outline
                            icon: "archive-arrow-down-outline"
                            on_press:
                            
                        MDIconButton:
                            id: trash_can_outline
                            icon: "trash-can-outline"
                            on_release: app.show_alert_dialog()

                        MDIconButton:
                            icon: "check"
                            on_press:
                                screen_manager.current = "main_screen"
                                screen_manager.transition.direction = "right"

                    BoxLayout:
                        orientation: "vertical"
                        padding: 10, 0

                        MDTextField:
                            id: note_title
                            hint_text: "Title"
                            helper_text: "Max text length = 100"
                            helper_text_mode: "on_focus"
                            max_text_length: 100
                            # font_size: 30
                            on_text: app.scale_font_size(self.text)
                            multiline: True
                            size_hint_y: None
                            # on_text_validate: this runs when u hit enter when multiline = False

                        TextInput:
                            id: note_text
                            hint_text: "Note"
                            # font_size: 15 is default
                            background_color: 0, 0, 0, 0
                            foreground_color: 0, 0, 0, 1
                            cursor_color: 0, 0, 0, 1
                            
                FloatLayout:
                    
                    Label:
                        id: time_now
                    
                        # text: "31 Sep 2019, 13:59"
                        # pos_hint: {"x": 0.24, "y": 0.383}
                        # 
                        # text: "today, 13:59"
                        # pos_hint: {"x": 0.317, "y": 0.383}
                        
                        font_size: "15sp"
                        size: self.texture_size
                        color: 0, 0, 0, 0.5
                        



# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, 1
            # size: "56dp", "56dp"
            source: "stickynotes.png"

    MDLabel:
        text: "Keep Mau Notes"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "additional caption here?"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:

        DrawerList:
            id: md_list


<list_grid_view_button@MDIconButton>
    icon: "view-grid-outline"
    on_press: 
        self.icon = "view-grid-outline" if self.icon == "view-agenda-outline" else "view-agenda-outline"
        app.list_grid_view()


<BorderButton@Button+BorderBehavior>:
    borders: 1, "solid", (0, 0, 0, 1)
    color: 0, 0, 0, 1
    background_color: 1, 1, 1, 0
    size: self.texture_size
    size_hint_y: None # this is to ensure that it fits the Button
    text_size: self.width, None
    padding: 10, 10
    on_press:


<SelectableLabel>:
    on_release: app.on_click()
    
    # Draw a background to indicate selection
    # canvas.before:
    #     Color:
    #         rgba: (0, 1, 1, 0.1) if self.selected else (0, 0, 0, 0)
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size

<RV>:
    viewclass: "SelectableLabel"

    SelectableRecycleGridLayout:
        id: rv_layout
        
        spacing: dp(10)
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"
        multiselect: True
        touch_multiselect: True
        cols: 1

"""


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

    def set_icon(self, instance_item):
        pass


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """
    # RecycleGridLayout.cols = 2


class BorderBehavior(Widget):
    borders = ObjectProperty(None)
    border_origin_x = NumericProperty(0.)
    border_origin_y = NumericProperty(0.)
    border_origin = ReferenceListProperty(border_origin_x, border_origin_y)

    left_border_points = []
    top_border_points = []
    right_border_points = []
    bottom_border_points = []

    CAP = "square"
    JOINT = "none"

    dash_styles = {
        "dashed":
            {
                "dash_length": 10,
                "dash_offset": 5
            },
        "dotted":
            {
                "dash_length": 1,
                "dash_offset": 1
            },
        "solid":
            {
                "dash_length": 1,
                "dash_offset": 0
            }
    }

    def draw_border(self):
        line_kwargs = {
            "points": [],
            "width": self.line_width,
            "cap": self.CAP,
            "joint": self.JOINT,
            "dash_length": self.cur_dash_style["dash_length"],
            "dash_offset": self.cur_dash_style["dash_offset"]
        }

        with self.canvas.after:
            self.border_color = Color(*self.line_color)
            # left border
            self.border_left = Line(**line_kwargs)

            # top border
            self.border_top = Line(**line_kwargs)

            # right border
            self.border_right = Line(**line_kwargs)

            # bottom border
            self.border_bottom = Line(**line_kwargs)

    def update_borders(self):
        if hasattr(self, "border_left"):
            # test for one border is enough so we know that the borders are
            # already drawn
            width = self.line_width
            dbl_width = 2 * width

            self.border_left.points = [
                self.border_origin_x,
                self.border_origin_y,
                self.border_origin_x,
                self.border_origin_y +
                self.size[1] - dbl_width
            ]

            self.border_top.points = [
                self.border_origin_x,
                self.border_origin_y + self.size[1] - dbl_width,
                self.border_origin_x + self.size[0] - dbl_width,
                self.border_origin_y + self.size[1] - dbl_width
            ]

            self.border_right.points = [
                self.border_origin_x + self.size[0] - dbl_width,
                self.border_origin_y + self.size[1] - dbl_width,
                self.border_origin_x + self.size[0] - dbl_width,
                self.border_origin_y
            ]

            self.border_bottom.points = [
                self.border_origin_x + self.size[0] - dbl_width,
                self.border_origin_y,
                self.border_origin_x,
                self.border_origin_y
            ]

    def set_border_origin(self):
        self.border_origin_x = self.pos[0] + self.line_width
        self.border_origin_y = self.pos[1] + self.line_width

    def on_border_origin(self, instance, value):
        # print(self.border_origin, "border origin")
        self.update_borders()

    def on_size(self, instance, value):
        # not sure if it"s really needed, but if size is changed
        # programatically the border have to be updated
        # --> needs further testing
        if hasattr(self, "line_width"):
            self.set_border_origin()
            self.pos = self.border_origin

    def on_pos(self, instance, value):
        # print instance, value, "pos changed"
        if hasattr(self, "line_width"):
            self.set_border_origin()

    def on_borders(self, instance, value):
        self.line_width, self.line_style, self.line_color = value
        self.cur_dash_style = self.dash_styles[self.line_style]
        # print self.cur_dash_style, "dash_style selected"
        self.set_border_origin()
        self.draw_border()

    # touch events for testing
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # I received my grabbed touch
            print("touch")
            self.pos = (touch.x, touch.y)
        # else:
        #     print "only touched"
        #     # it"s a normal touch

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
            touch.ungrab(self)
        # else:
        #     # it"s a normal touch
        #     print("normal touch up")
        #     pass


class BorderButton(Button, BorderBehavior):
    pass

# initiate the note index that is pressed
note_index = ""

class SelectableLabel(RecycleDataViewBehavior, BorderButton):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            print("touched Note " + str(self.index + 1))

            global note_index
            note_index = self.index

            # self.selected = True if self.selected == False else False

            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
    #     if is_selected:
    #         # print("selection changed to {0}".format(rv.data[index]))
    #     else:
    #         print("selection removed for {0}".format(rv.data[index]))


def refresh_notes_data():
    notes_data = pd.read_csv("notes_data.csv")
    col_data = list(notes_data.columns)
    notes_data["datetime64"] = pd.to_datetime(notes_data["Timestamp"])
    notes_data.sort_values(by="datetime64", ascending=False, ignore_index=True, inplace=True)
    notes_data["title_empty_index"] = notes_data[notes_data["Title"].apply(lambda x: x.split(" ")[0]) == "Note"].index.to_series() + int(1)
    notes_data["title_empty_index"].fillna(value="", inplace=True)
    notes_data["Title"] = (notes_data["Title"].apply(lambda x: x.split(" "))).apply(lambda x: "Note " if x[0] == "Note" else " ".join(x))
    notes_data["title_empty_index"] = notes_data["title_empty_index"].astype(str).apply(lambda x: x.split(".")[0])
    notes_data["Title"] = notes_data["Title"] + notes_data["title_empty_index"]
    notes_data = notes_data[col_data]
    notes_data.to_csv("notes_data.csv", index=False, encoding="utf-8")


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

        refresh_notes_data()
        self.notes_data = pd.read_csv("notes_data.csv")

        # how to bold or change size of title?
        self.notes_data_title = self.notes_data.Title
        self.notes_data_text = self.notes_data.Text

        # less than len = 250 should be good
        # print(len((self.data[0])["text"]))
        # cleans up data to display up to len = 250!
        self.notes_data_trunc = (self.notes_data_title + ":\n" + self.notes_data_text).apply(lambda x: x[:250])
        self.notes_data_len = self.notes_data_trunc.str.len()
        self.notes_data_trunc = np.where(self.notes_data_len == 250, self.notes_data_trunc + "...", self.notes_data_trunc)

        self.data = [{"text": str(x)} for x in self.notes_data_trunc]


# to identify if the note is clicked
note_on_click = False

class MauApp(MDApp):
    dialog = None

    def build(self):
        self.disable_enter = False
        self.disable_paste = False

        Window.bind(on_keyboard=self._on_keyboard_handler)
        return Builder.load_string(KV)


    def on_start(self):
        icons_item = {
            "lightbulb-outline": "Mau Notes",
            "bell-outline": "Reminders",
            "plus": "Create new label",
            "archive-arrow-down-outline": "Archive",
            "delete-outline": "Deleted",
            "settings-outline": "Settings",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )

    def on_click(self):
        # print("why does this gets called twice???")

        sm = self.root.ids.screen_manager
        sm.current = "new_note_screen"
        sm.transition.direction = "left"

        self.root.ids.pin_outline.opacity = 1
        self.root.ids.pin_outline.disabled = False
        self.root.ids.bell_plus_outline.opacity = 1
        self.root.ids.bell_plus_outline.disabled = False
        self.root.ids.archive_arrow_down_outline.opacity = 1
        self.root.ids.archive_arrow_down_outline.disabled = False
        self.root.ids.trash_can_outline.opacity = 1
        self.root.ids.trash_can_outline.disabled = False

        global note_on_click
        note_on_click = True
        # print(note_index)

        self.root.ids.note_title.text = RV().notes_data_title[note_index]
        self.root.ids.note_text.text = RV().notes_data_text[note_index]


    def scale_font_size(self, text):
        # print(len(text))

        extra_text = len(text) - 16
        extra_text_2 = len(text) - 19
        extra_text_3 = len(text) - 22
        extra_text_4 = len(text) - 28

        self.disable_enter = True

        if len(text) <= 16:
            self.root.ids.note_title.font_size = 30
        elif len(text) > 16 and len(text) <= 19:
            self.root.ids.note_title.font_size = 30 - extra_text*2
        elif len(text) > 19 and len(text) <= 22:
            self.root.ids.note_title.font_size = 24 - extra_text_2
        elif len(text) > 22 and len(text) <= 26:
            self.root.ids.note_title.font_size = 21 - extra_text_3//2
        elif len(text) > 26 and len(text) <= 28:
            self.root.ids.note_title.font_size = 18
        elif len(text) > 28 and len(text) <= 30: # set max limit for Title to be 31
            self.root.ids.note_title.font_size = 18 - extra_text_4
        # elif len(text) > 30:
        #     pass
        #     print(self.disable_enter)

        elif len(text) > 100:
            self.disable_paste = True


    def clear_screen(self):
        # the title hint_text will not display properly when you click on a note, exit and click a new note
        # self.root.ids.note_title.focus = True

        self.root.ids.note_title.text = ""
        self.root.ids.note_text.text = ""

        self.root.ids.pin_outline.opacity = 0
        self.root.ids.pin_outline.disabled = True
        self.root.ids.bell_plus_outline.opacity = 0
        self.root.ids.bell_plus_outline.disabled = True
        self.root.ids.archive_arrow_down_outline.opacity = 0
        self.root.ids.archive_arrow_down_outline.disabled = True
        self.root.ids.trash_can_outline.opacity = 0
        self.root.ids.trash_can_outline.disabled = True

        # pd.Timestamp.now().strftime("%B-%d-%Y %H:%M:%S")
        self.root.ids.time_now.text = "today, " + pd.Timestamp.now().strftime("%H:%M")
        self.root.ids.time_now.pos_hint = {"x": 0.317, "y": 0.383}

    def _on_keyboard_handler(self, instance, key, *args):
        if key == 13 and self.disable_enter == True:
            self.root.ids.note_title.do_backspace(from_undo=False, mode="bkspc")
            self.root.ids.note_title.focus = False

        elif args == (25, "v", ["ctrl"]) and self.disable_paste == True: # ctrl + v
            self.root.ids.note_title.do_undo()
            self.disable_paste = False

        elif args != (25, "v", ["ctrl"]) and len(self.root.ids.note_title.text) >= 100 and self.root.ids.note_title.focus == True:
            # self.root.ids.note_title.do_backspace(from_undo=False, mode="bkspc")
            self.root.ids.note_title.focus = False
            print("this is executed")
            print()

        elif args == (41, None, []):
            if self.root.ids.screen_manager.current == "new_note_screen":
                self.root.ids.screen_manager.current = "main_screen"
                self.root.ids.screen_manager.transition.direction = "right"
            elif self.root.ids.screen_manager.current == "main_screen":
                MauApp.get_running_app().stop()

    def list_grid_view(self):
        self.root.ids.rv.ids.rv_layout.cols = 2 if self.root.ids.rv.ids.rv_layout.cols == 1 else 1

        self.notes_data = pd.read_csv("notes_data.csv")

        # how to bold or change size of title?
        self.notes_data_title = self.notes_data.Title
        self.notes_data_text = self.notes_data.Text

        if self.root.ids.rv.ids.rv_layout.cols == 2:

            # less than len = 100 should be good
            # cleans up data to display up to len = 100!
            self.notes_data_trunc = (self.notes_data_title + ":\n" + self.notes_data_text).apply(lambda x: x[:100])
            self.notes_data_len = self.notes_data_trunc.str.len()
            self.notes_data_trunc = np.where(self.notes_data_len == 100, self.notes_data_trunc + "...", self.notes_data_trunc)

            self.root.ids.rv.data = [{"text": str(x)} for x in self.notes_data_trunc]

        else:

            self.notes_data_trunc = (self.notes_data_title + ":\n" + self.notes_data_text).apply(lambda x: x[:250])
            self.notes_data_len = self.notes_data_trunc.str.len()
            self.notes_data_trunc = np.where(self.notes_data_len == 250, self.notes_data_trunc + "...", self.notes_data_trunc)

            self.root.ids.rv.data = [{"text": str(x)} for x in self.notes_data_trunc]

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Delete this note?", size_hint=(0.9, None), pos_hint={"y": 0.1},
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.cancel_dialog
                    ),
                    MDFlatButton(
                        text="DELETE", text_color=(1,0,0,1), on_release=self.delete_note
                    ),
                ],
            )
        # self.dialog.set_normal_height()
        self.dialog.open()

    def cancel_dialog(self, inst):
        self.dialog.dismiss()

    def delete_note(self, inst):
        self.dialog.dismiss()

if __name__ == "__main__":
    MauApp().run()


# notes:
# why does on_click gets called twice?
# refresh view of recycle
# do_undo()
# do_redo()
# search function
# make a date time stamp!
# the time label is not there until the new note plus is pressed but it stays for the note screen as well,
# time only updates when the plus is pressed
# long press multi selection
# firebaseloginscreen?