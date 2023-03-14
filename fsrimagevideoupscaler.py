"""
*		FSRImageVideoUpscalerFrontend - fsrimagevideoupscaler.py
*
*	Created by Janis Hutz 03/14/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
"""

import sys
import bin.handler
import multiprocessing
import bin.checks
import bin.arg_assembly

arg = bin.arg_assembly.ArgAssembly()
checks = bin.checks.Checks()
handler = bin.handler.Handler()

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QFileDialog, QComboBox, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl


class HomeWindow(QMainWindow):
    def __init__( self, parent=None ):
        super( HomeWindow, self ).__init__( parent  )
        self.os_type = sys.platform
        self.save_file = ""
        self.open_file = ""

        box = QVBoxLayout();
        actionsBox = QHBoxLayout();

        widget = QWidget();
        actionsWidget = QWidget();

        self.button = QPushButton( 'Input file' );
        self.button.clicked.connect( self.filechooser_clicked );
        self.button_out = QPushButton( 'Output file' );
        self.button_out.clicked.connect( self.opfilechooser_clicked );
        self.button_run = QPushButton( 'Upscale' );
        self.button_run.clicked.connect( self.info_button );

        self.qualitySelector = QComboBox();
        self.qualitySelector.addItems( ['2x', '1.7x', '1.5x', '1.3x', 'Custom (will respect value below)' ] );

        actionsBox.addWidget( self.button );
        actionsBox.addWidget( self.button_out );
        actionsBox.addWidget( self.button_run );
        actionsWidget.setLayout( actionsBox );

        box.addWidget( self.qualitySelector );
        box.addWidget( actionsWidget );
        widget.setLayout( box );

        self.setCentralWidget( widget );

        self.setWindowTitle( 'FSRImageVideoUpscalerFrontend' );


    def on_quality_change(self, quality):
        # get data from quality changer
        self.tree_iter = quality.get_active_iter()
        if self.tree_iter is not None:
            self.model = quality.get_model()
            self.output = self.model[self.tree_iter][0]

    def filechooser_clicked( self ):
        self.open_file = QFileDialog.getOpenFileName( self, 'Open input file', '', 'Image & Video files (*.jpg *.png *.mp4 *.mkv *.jpeg)' );
        

    def opfilechooser_clicked( self ):       
        self.path = '';

        if str( self.open_file )[len(self.open_file) - 4:] == '.mp4':
            self.path = 'video.mp4';
        elif str( self.open_file )[len(self.open_file) - 4:] == '.mkv':
            self.path = 'video.mkv';
        elif str( self.open_file )[len(self.open_file) - 4:] == '.png':
            self.path = 'image.png';
        elif str( self.open_file )[len(self.open_file) - 4:] == '.jpg':
            self.path = 'image.jpg';
        elif str( self.open_file )[len(self.open_file) - 4:] == '.jpeg':
            self.path = 'image.jpeg';

        self.open_file_out = QFileDialog.getOpenFileName( self, 'Select output file', '', 'Image & Video files (*.jpg *.png *.mp4 *.mkv *.jpeg)' );

    def info_button(self):
        self.fileMissingErrorDialog = QDialog( self );
        self.fileMissingErrorDialog.setWindowTitle( 'Upscaling! This process might take a LONG time!' );
        self.fileMissingErrorDialog.exec();
        self.start_clicked();

    def start_clicked(self):
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
                        self.details.set_text("Starting upscaling process")
                        print("\n\nStarting upscaling process!\n\n")
                        self.info_button()
                        if self.info_response == Gtk.ResponseType.OK:
                            self.details.set_text("Upscaling")
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
                            self.details.set_text("Ready")
                            print("aborted")
                        else:
                            raise Exception
                else:
                    self.details.set_text("File-checks failed! Please check your entries!")
                    print("File-checks unsuccessful. Please check your entries!")
                    self.checkerror()
            else:
                self.details.set_text("No file specified!")
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
        self.fileMissingErrorDialog = QDialog( self );
        self.fileMissingErrorDialog.setWindowTitle( 'Missing file selection! Please ensure you have selected both an input and output file!' );
        self.fileMissingErrorDialog.exec();

    def checkerror(self):
        self.checkerrordialog = ErrorDialogCheckFail(self)
        self.checkerrordialog.run()
        self.checkerrordialog.destroy()


app = QApplication( sys.argv );
ex = HomeWindow();
ex.show();
sys.exit( app.exec_() );
