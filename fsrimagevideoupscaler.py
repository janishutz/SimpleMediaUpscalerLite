###########################################################
#
# FSRImageVideoUpscalerFrontend written in GTK+
#
# This code is licensed under the GPL V3 License!
# Developed 2022 by Janis Hutz
#
###########################################################

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


class ProgressIndicator(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Upscaling", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.spinner = Gtk.Spinner()
        self.label = Gtk.Label(label="                     Upscaling. This process will take long (if a Video). \n             Duration depends on your Hardware and length and resolution of video \n You may see the output of the app, if you switch to the other window that is behind it.            ")
        self.box = self.get_content_area()
        self.box.pack_start(self.label, True, True, 20)
        self.box.pack_start(self.spinner, True, True, 20)
        self.spinner.start()
        self.show_all()


class ErrorDialogFileMissing(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Error", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.label = Gtk.Label(label="    No file specified. Please select a input AND output file!     ")
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
        self.label = Gtk.Label(label="    Filechecks failed. Make sure to specify the same file extension in the output like in the input     ")
        self.box = self.get_content_area()
        self.box.pack_start(self.label, True, True, 20)
        self.show_all()


class HomeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Test")
        self.save_file = ""
        self.open_file = ""

        # Spawn box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sub_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
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
        self.quality_select_shrink.pack_start(self.quality_select, True, False, 30)

        self.quality_select_box.pack_start(self.title, True, True, 0)
        self.quality_select_box.pack_start(self.quality_select_shrink, True, True, 20)

        # Custom Quality Selector
        self.custom_quality_selector_title = Gtk.Label(label="Custom Upscaling Multiplier")
        self.custom_quality_selector_shrink = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.custom_quality_selector = Gtk.Entry()
        self.custom_quality_selector_shrink.pack_start(self.custom_quality_selector, True, False, 30)

        self.custom_quality_selector_box.pack_start(self.custom_quality_selector_title, True, True, 0)
        self.custom_quality_selector_box.pack_start(self.custom_quality_selector_shrink, True, True, 20)

        # Info
        self.infos = Gtk.Label(label="Settings")

        # Packing boxes
        self.top_box.pack_start(self.infos, True, True, 0)
        self.top_box.pack_start(self.quality_select_box, True, True, 0)
        self.top_box.pack_start(self.custom_quality_selector_box, True, True, 0)

        self.sub_box.pack_start(self.box, True, True, 30)
        self.main_box.pack_start(self.top_box, True, True, 20)
        self.main_box.pack_end(self.sub_box, True, True, 20)
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
            print("ok, selected file:", self.filechooserdialog.get_filename())
            self.open_file = self.filechooserdialog.get_filename()
        elif self.response == Gtk.ResponseType.CANCEL:
            print("cancel")
        self.filechooserdialog.destroy()

    def opfilechooser_clicked(self, widget):
        self.filechooserdialog_save = Gtk.FileChooserDialog(title="Choose output file", action=Gtk.FileChooserAction.SAVE)
        Gtk.FileChooser.set_do_overwrite_confirmation(self.filechooserdialog_save, True)
        Gtk.FileChooser.set_current_name(self.filechooserdialog_save, "video.mp4")
        self.filechooserdialog_save.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        self.response = self.filechooserdialog_save.run()
        if self.response == Gtk.ResponseType.OK:
            print("ok, selected file:", self.filechooserdialog_save.get_filename())
            self.save_file = self.filechooserdialog_save.get_filename()
        elif self.response == Gtk.ResponseType.CANCEL:
            print("cancel")
        self.filechooserdialog_save.destroy()

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
                print("ok")
                if checks.perform(self.output, self.custom_quality_selector.get_text(), self.open_file, self.save_file):
                    if self.output == "Custom (will respect value below)":
                        self.quality_selected = "custom"
                        self.q = f"{self.custom_quality_selector.get_text()} {self.custom_quality_selector.get_text()}"
                    else:
                        self.quality_selected = "default"
                        self.q = str(arg.get(self.output))
                    self.go = True
                    if self.go:
                        self.pr_i = ProgressIndicator(self)
                        self.pr_i.run()
                        self.pr_i.destroy()
                        self.scaler = multiprocessing.Process(name="scaler",
                                                              target=handler.handler,
                                                              args=("./bin/lib/FidelityFX_CLI.exe",
                                                                    self.open_file,
                                                                    self.quality_selected,
                                                                    self.q,
                                                                    self.save_file,
                                                                    "./bin/lib/ffmpeg.exe")
                                                              )
                        self.scaler.start()
                else:
                    print("File-checks unsuccessful. Please check your entries!")
                    self.checkerror()
            else:
                print("no file specified")
                self.fileerror()
        else:
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
