class ArgAssembly:
    def __init__(self):
        pass

    def get(self, quality):
        if quality == "2x":
            return "Performance"
        elif quality == "1.7x":
            return "Balanced"
        elif quality == "1.5x":
            return "Quality"
        elif quality == "1.3x":
            return "UltraQuality"
        else:
            raise Exception
