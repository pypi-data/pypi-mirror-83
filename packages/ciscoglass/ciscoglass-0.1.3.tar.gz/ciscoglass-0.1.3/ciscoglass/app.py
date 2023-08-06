from contextlib import contextmanager
import os
import json
import requests
import warnings
import shutil
import time


class GlassDevice:
    def __init__(self, _id, host, device_type, name=None, username=None, password=None, *args, **kwargs):
        self.id = _id
        self.host = host
        self.device_type = device_type
        self.name = name
        self.username = username
        self.password = password
        warnings.warn(f"Dropping unknown arguments to __init__: {args}, {kwargs}")

    def is_type(self, type_to_test):
        # return True if type is None, helps in filtering lists
        return type_to_test.lower() == self.device_type.lower() if type_to_test else True

    def __repr__(self):
        return f"<GlassDevice(device_type={self.device_type}, name={self.name}, id={self.id}, host={self.host})>"


class GlassApp:
    def __init__(
            self,
            glass_api=None,
            app_input=None,
            files_input=None,
            base_path="/app",
            initialize_now=True,
            copy_on_write=False,
    ):
        self.glass_api = glass_api or os.environ.get('CISCOGLASS_DEVICES_API') or None
        if not self.glass_api:
            raise ValueError(f"Could not load Glass API url, please check env var CISCOGLASS_DEVICES_API or "
                             f"provide it as an argument while initializing!")

        self.app_input = app_input or json.loads(os.environ.get('CISCOGLASS_APP_INPUT') or "{}")
        if not self.app_input and not isinstance(self.app_input, dict):
            raise ValueError(f"Could not load Glass App input, please check env var CISCOGLASS_APP_INPUT or "
                             f"provide it as an argument while initializing!")

        self.files_input = files_input or json.loads(os.environ.get('CISCOGLASS_FILES_INPUT') or "[]")
        if not self.files_input and not isinstance(self.files_input, list):
            raise ValueError(f"Could not load Glass Files input, please check env var CISCOGLASS_APP_INPUT or "
                             f"provide it as an argument while initializing!")

        self.base_path = base_path
        self.copy_on_write = copy_on_write

        self.devices = []

        if initialize_now:
            self.initialize_glass()

    def __repr__(self):
        return f"<GlassApp_{self.__class__.__name__}(glass_api={self.glass_api}, app_input={self.app_input}, " \
               f"files_input={self.files_input}, base_path={self.base_path}, copy_on_write={self.copy_on_write})>"

    def initialize_glass(self):
        response = requests.get(self.glass_api, self.app_input)
        response.raise_for_status()
        data = response.json()
        self.devices = list(map(lambda device: GlassDevice(**device), data.get("success")))

        if not self.devices:
            warnings.warn("No devices returned from Glass, might have nothing to work on!", RuntimeWarning)

        input_path = os.path.join(self.base_path, 'input')
        if not os.path.isdir(input_path):
            print("Creating input path...")
            os.mkdir(input_path)

        output_path = os.path.join(self.base_path, 'output')
        if not os.path.isdir(output_path):
            print("Creating output path...")
            os.mkdir(output_path)

    def get_devices(self, device_type=None):
        return list(filter(lambda device: device.is_type(device_type), self.devices)) if device_type else self.devices

    def get_files(self, file_type=None):
        return list(filter(lambda file: file.endswith(file_type), self.files_input)) if file_type else self.files_input

    @contextmanager
    def file(self, name, method, is_input=False, **kwargs):
        if name.find('/') != -1 or name.find('\\') != -1:
            raise ValueError(f"Cannot work with folders yet, please create/use files only!")

        sub_folder = 'input' if is_input else 'output'
        path = os.path.join(self.base_path, sub_folder, name)

        if is_input and method != 'r' and method != 'rb':
            # Writing to an input read-only file
            # May copy it to output folder and open that as requested, or force a read only open
            if self.copy_on_write:
                name = f"{time.strftime('%Y%m%d-%H%M%S')}-{name}"
                new_path = os.path.join(self.base_path, 'output', name)
                shutil.copy(path, new_path)
                path = new_path
            else:
                method = 'rb' if 'b' in method else 'r'

        f = open(path, method, **kwargs)
        try:
            yield f
        finally:
            f.close()

    def run(self):
        raise NotImplementedError("Please override this method with your code!")
