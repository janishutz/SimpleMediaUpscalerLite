###########################################################
#
# FSRImageVideoUpscalerFrontend written in GTK+
#
# This code is licensed under the GPL V3 License!
# Developed 2022 by Janis Hutz
#
###########################################################
import sys
import gi
import bin.handler
import multiprocessing
import bin.checks
import bin.arg_assembly

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


arg = bin.arg_assembly.ArgAssembly()
checks = bin.checks.Checks()
handler = bin.handler.Handler()


class ErrorDialogFileMissing(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Error", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.label = Gtk.Label(label="    No file specified. Please select an input AND output file!     ")
        self.box = self.get_content_area()
        self.box.pack_start(self.label, True, True, 20)
        self.show_all()


class ErrorDialogRunning(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Error", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.label = Gtk.Label(label="    You are already upscaling. Please wait for the current job to finish!      ")
        self.box = self.get_content_area()
        self.box.pack_start(self.label, True, True, 20)
        self.show_all()


class ErrorDialogCheckFail(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Error", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.label = Gtk.Label(label="       File and settings check failed. \n       Make sure to specify the same file extension in the output like in the input                 \n       make sure that the entries you made as settings are valid! (4 >= scale >= 1)                 ")
        self.box = self.get_content_area()
        self.box.pack_start(self.label, True, True, 20)
        self.show_all()


class HomeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Test")
        self.os_type = sys.platform
        self.save_file = ""
        self.open_file = ""

        # Spawn box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sub_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.orient_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.quality_select_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.custom_quality_selector_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # Headerbar
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "FSR Image & Video Upscaler"
        self.set_titlebar(self.hb)

        # Create filechooser button
        self.filechoosebutton = Gtk.Button(label="Choose Input File")
        self.filechoosebutton.connect("clicked", self.filechooser_clicked)
        self.box.pack_start(self.filechoosebutton, True, True, 0)

        # Create output filechooser button
        self.opfchooserbutton = Gtk.Button(label="Choose Output File")
        self.opfchooserbutton.connect("clicked", self.opfilechooser_clicked)
        self.box.pack_start(self.opfchooserbutton, True, True, 0)

        # Create start button
        self.start_button = Gtk.Button(label="Start upscaling")
        self.start_button.connect("clicked", self.start_clicked)
        self.box.pack_start(self.start_button, True, True, 0)

        # Create Input File label
        self.ip_file_label = Gtk.Label(label="Choose input file")

        # Create Output File label
        self.op_file_label = Gtk.Label(label="Choose output file")

        # Pack File labels
        self.filebox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.filebox.pack_start(self.ip_file_label, True, True, 10)
        self.filebox.pack_start(self.op_file_label, True, True, 10)

        # QualitySelect
        self.title = Gtk.Label(label="Upscaling Multiplier Presets")
        self.qualities = Gtk.ListStore(str)
        self.qualities.append(["2x"])
        self.qualities.append(["1.7x"])
        self.qualities.append(["1.5x"])
        self.qualities.append(["1.3x"])
        self.qualities.append(["Custom (will respect value below)"])
        self.quality_select = Gtk.ComboBox.new_with_model(self.qualities)
        self.text_renderer = Gtk.CellRendererText()
        self.quality_select.pack_start(self.text_renderer, True)
        self.quality_select.add_attribute(self.text_renderer, "text", 0)
        self.quality_select.connect("changed", self.on_quality_change)
        self.quality_select_shrink = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.quality_select_shrink.pack_start(self.quality_select, True, False, 10)

        self.quality_select_box.pack_start(self.title, True, True, 0)
        self.quality_select_box.pack_start(self.quality_select_shrink, True, True, 20)

        # Custom Quality Selector
        self.custom_quality_selector_title = Gtk.Label(label="Custom Upscaling Multiplier\nNOTE that factors greater than 2 are not recommended!\nFactors greater than 4 will not run!")
        self.custom_quality_selector_shrink = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.custom_quality_selector = Gtk.Entry()
        self.custom_quality_selector_shrink.pack_start(self.custom_quality_selector, True, False, 10)

        self.custom_quality_selector_box.pack_start(self.custom_quality_selector_title, True, True, 0)
        self.custom_quality_selector_box.pack_start(self.custom_quality_selector_shrink, True, True, 20)

        # Info
        self.infos = Gtk.Label(label="Settings")

        # Details
        self.details = Gtk.Label(label="Ready")

        # Separator
        self.separator = Gtk.Separator().new(Gtk.Orientation.HORIZONTAL)

        # Packing boxes
        self.top_box.pack_start(self.infos, True, True, 0)
        self.top_box.pack_start(self.quality_select_box, True, True, 0)
        self.top_box.pack_start(self.custom_quality_selector_box, True, True, 0)
        self.top_box.pack_start(self.details, True, True, 0)
        self.top_box.pack_start(self.separator, True, False, 0)


        self.orient_box.pack_start(self.filebox, True, True, 0)
        self.orient_box.pack_start(self.box, True, True, 0)
        self.sub_box.pack_start(self.orient_box, True, True, 30)
        self.main_box.pack_start(self.top_box, True, True, 0)
        self.main_box.pack_end(self.sub_box, True, True, 5)
        self.add(self.main_box)

    def on_quality_change(self, quality):
        # get data from quality changer
        self.tree_iter = quality.get_active_iter()
        if self.tree_iter is not None:
            self.model = quality.get_model()
            self.output = self.model[self.tree_iter][0]

    def filechooser_clicked(self, widget):
        self.filechooserdialog = Gtk.FileChooserDialog(title="Choose input file", action=Gtk.FileChooserAction.OPEN)
        self.filechooserdialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.response = self.filechooserdialog.run()
        if self.response == Gtk.ResponseType.OK:
            self.ip_file_label.set_text(self.filechooserdialog.get_filename())
            self.open_file = self.filechooserdialog.get_filename()
        elif self.response == Gtk.ResponseType.CANCEL:
            pass
        self.filechooserdialog.destroy()

    def opfilechooser_clicked(self, widget):
        self.filechooserdialog_save = Gtk.FileChooserDialog(title="Choose output file", action=Gtk.FileChooserAction.SAVE)
        Gtk.FileChooser.set_do_overwrite_confirmation(self.filechooserdialog_save, True)
        if self.os_type == "linux":
            Gtk.FileChooser.set_current_folder(self.filechooserdialog_save, "/home")
        elif self.os_type == "win32":
            Gtk.FileChooser.set_current_folder(self.filechooserdialog_save, "%HOMEPATH%")
        else:
            pass
        if str(self.open_file)[len(self.open_file) - 4:] == ".mp4":
            Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "video.mp4")
        elif str(self.open_file)[len(self.open_file) - 4:] == ".mkv":
            Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "video.mkv")
        elif str(self.open_file)[len(self.open_file) - 4:] == ".png":
            Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "image.png")
        elif str(self.open_file)[len(self.open_file) - 4:] == ".jpg":
            Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "image.jpg")
        elif str(self.open_file)[len(self.open_file) - 4:] == ".jpeg":
            Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "image.jpeg")
        else:
            Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "")
        self.filechooserdialog_save.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        self.response = self.filechooserdialog_save.run()
        if self.response == Gtk.ResponseType.OK:
            self.op_file_label.set_text(self.filechooserdialog_save.get_filename())
            self.save_file = self.filechooserdialog_save.get_filename()
        elif self.response == Gtk.ResponseType.CANCEL:
            pass
        self.filechooserdialog_save.destroy()

    def info_button(self):
        self.info_dialog = Gtk.Dialog()
        self.remove_event = Gtk.Button(label="Don't show again")
        self.info_dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.info_dialog.set_default_size(150, 100)
        self.box = self.info_dialog.get_content_area()
        self.label = Gtk.Label(label="                     Upscaling. This process will take long (if a Video). \n             Duration depends on your Hardware and length and resolution of video \n           You may see the output of the app, if you switch to the other window that is behind it.            \n\n\n           click \"ok\" to start upscaling")
        self.box.pack_start(self.label, True, True, 0)
        self.info_dialog.show_all()
        self.info_response = self.info_dialog.run()
        self.info_dialog.destroy()

    def start_clicked(self, widget):
        self.respawn = True
        try:
            if self.scaler.is_alive():
                self.respawn = False
            else:
                self.respawn = True

        except AttributeError:
            self.respawn = True

        if self.respawn:
            if str(self.open_file) != "" and str(self.save_file) != "":
                if checks.perform(self.output, self.custom_quality_selector.get_text(), self.open_file, self.save_file):
                    if self.output == "Custom (will respect value below)":
                        self.quality_selected = "custom"
                        if self.custom_quality_selector.get_text()[len(self.custom_quality_selector.get_text()) - 1] == "x":
                            self.q = f"{self.custom_quality_selector.get_text()} {self.custom_quality_selector.get_text()}"
                        else:
                            self.q = f"{self.custom_quality_selector.get_text()}x {self.custom_quality_selector.get_text()}x"
                    else:
                        self.quality_selected = "default"
                        self.q = str(arg.get(self.output))
                    self.go = True
                    if self.go:
                        print("\n\nStarting upscaling process!\n\n")
                        self.info_button()
                        if self.info_response == Gtk.ResponseType.OK:
                            self.scaler = multiprocessing.Process(name="scaler",
                                                                  target=handler.handler,
                                                                  args=("./bin/lib/FidelityFX_CLI.exe",
                                                                        self.open_file,
                                                                        self.quality_selected,
                                                                        self.q,
                                                                        self.save_file,)
                                                                  )
                            self.scaler.start()
                        elif self.info_response == Gtk.ResponseType.CANCEL:
                            print("aborted")
                        else:
                            raise Exception
                else:
                    print("File-checks unsuccessful. Please check your entries!")
                    self.checkerror()
            else:
                print("no file specified")
                self.fileerror()
        else:
            self.runningerror()
            print("Already running!")

    def runningerror(self):
        self.runningerrordialog = ErrorDialogRunning(self)
        self.runningerrordialog.run()
        self.runningerrordialog.destroy()

    def fileerror(self):
        self.fileerrordialog = ErrorDialogFileMissing(self)
        self.fileerrordialog.run()
        self.fileerrordialog.destroy()

    def checkerror(self):
        self.checkerrordialog = ErrorDialogCheckFail(self)
        self.checkerrordialog.run()
        self.checkerrordialog.destroy()


win = HomeWindow()
win.set_default_size(800, 600)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
