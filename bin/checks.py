class Checks:
    def __init__(self):
        self.custom_quality = 0.0
        self.i_file_extension = ""

    def perform(self, quality_selection, custom_quality, input_filepath, output_filepath):
        # Call this function to perform entry checks.
        # Returns True if all checks passed, False if one or more not passed.
        if self.quality_checks(quality_selection, custom_quality) and self.file_checks(input_filepath, output_filepath):
            return True
        else:
            return False

    def quality_checks(self, quality_sel, custom_q):
        if quality_sel != "Custom (will respect value below)":
            return True
        else:
            try:
                self.custom_quality = float(custom_q)
            except ValueError:
                return False
            return True

    def file_checks(self, i_fp, o_fp):
        self.i_file_extension = str(i_fp)[len(i_fp) - 4:]
        if self.i_file_extension == ".png" or self.i_file_extension == ".jpg":
            pass
        elif self.i_file_extension == "jpeg":
            if str(i_fp)[len(i_fp) - 5:] == ".jpeg":
                pass
            else:
                return False
        elif self.i_file_extension == ".mp4" or self.i_file_extension == ".mkv":
            pass
        else:
            return False

        if str(i_fp)[len(i_fp) - 4:] == str(o_fp)[len(o_fp) - 4:]:
            return True
        else:
            return False
