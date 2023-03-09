import os
import tempfile
from typing import List

import colink as CL


class GetTempFileName(object):

    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        return self.temp_file.name

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.unlink(self.temp_file.name)


def store_error(err_dir):
    def store_error_dec(f):
        def new_f(cl: CL.CoLink, param: bytes, participants: List[CL.Participant]):
            try:
                return f(cl, param, participants)
            except Exception as e:
                cl.create_entry(f"{err_dir}:{cl.get_task_id()}:error", str(e))
        return new_f
    return store_error_dec


def store_return(ret_dir):
    def store_return_dec(f):
        def new_f(cl: CL.CoLink, param: bytes, participants: List[CL.Participant]):
            ret = f(cl, param, participants)
            cl.create_entry(f"{ret_dir}:{cl.get_task_id()}:return", ret)
            return ret
        return new_f
    return store_return_dec


def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return my_ip


if __name__ == "__main__":
    print(get_local_ip())
