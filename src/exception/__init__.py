from src.logger import logging
import sys
def details_message(error):
    _,_,tb_exc=sys.exc_info()
    if tb_exc is None:
        return "no error"
    else:
        file_name=tb_exc.tb_frame.f_code.co_filename
        line_number=tb_exc.tb_lineno
        message=f"Error occur on file {file_name} at line number {line_number} is {error}"
        logging.info(f"Exception occur {message}")
        return message
class MyException(Exception):
    def __init__(self,error):
        super().__init__(error)
        self.message=details_message(error)
    def __str__(self):
        return self.message