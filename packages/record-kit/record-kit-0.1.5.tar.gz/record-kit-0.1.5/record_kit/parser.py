import markdown
import pandas as pd
from html.parser import HTMLParser
import numpy as np
import pathlib
from .recorder import Recorder

class HTMLRecordParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_string = None
        self.data_string = None
        self.stage = 0

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if data == "\n":
            return
        if data == "Meta":
            self.stage = 1
            return
        elif data == "Data":
            self.stage = 2
            return
        if self.stage == 1:
            self.meta_string = data
        elif self.stage == 2:
            self.data_string = data


class Record:
    def __init__(self, record_path):
        if isinstance(record_path, Recorder):
            self.record_path = record_path.record_name
        else:
            self.record_path = pathlib.Path(record_path)
        self.text = None
        self.html = None
        self.meta = {}
        self.data = None
        self._load_record()

    def reload(self):
        self._load_record()

    def _load_record(self):
        with self.record_path.open("r") as f:
            self.text = f.read()
        parser = HTMLRecordParser()

        self.html_text = markdown.markdown(self.text)
        parser.feed(self.html_text)
        self._parse_meta(parser.meta_string)
        self._parse_data(parser.data_string)

    def _parse_table(self, table_string: str):
        table = table_string.split("\n")
        def parse_line(line):
            line = line.split('|')
            words = line[1:-1]
            words = list(map(lambda x:x[1:-1], words))
            return words
        header = parse_line(table[0])
        body = map(parse_line, table[2:])
        return header, body

    def _parse_meta(self, meta_string):
        header, body = self._parse_table(meta_string)
        for item in body:
            self.meta[item[0]] = item[1]

    def _parse_data(self, data_string):
        header, body = self._parse_table(data_string)
        # df = pd.DataFrame(columns=header)
        data = np.array(list(body)).astype(float)
        df = pd.DataFrame(columns=header, data=data)
        # for item in body:
        #     data = pd.Series(map(float, item))
        #     df = df.append(data, ignore_index=True)
        self.data = df

    def get_meta(self):
        pass

    def get_data(self):
        pass