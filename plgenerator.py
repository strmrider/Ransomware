from payload.generator.generator import Generator

import pathlib

payload_src = str(pathlib.Path().absolute()) + '\payload\payload.py'
target_path = str(pathlib.Path().absolute()) +'\\'

Generator(payload_src, target_path)