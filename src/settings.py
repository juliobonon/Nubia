import platform

def get_tesseract_path():
    # Set the path to the Tesseract executable (modify this according to your system)

    match platform.system():
        case 'Windows':
            # most common case
            return "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        case 'MacOS':
            return "/opt/homebrew/bin/tesseract"
        case 'Linux':
            raise NotImplementedError("Developer did not implement get_tesseract_path in Linux")
        case _:
            raise Exception("Invalind System")

TESSERACT_CMD = get_tesseract_path()