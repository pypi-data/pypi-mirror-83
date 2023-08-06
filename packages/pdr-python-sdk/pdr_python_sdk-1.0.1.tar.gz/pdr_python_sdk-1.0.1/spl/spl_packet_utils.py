import json
import sys

class SplPacketUtils(object):
    def parse_head(self, input_stream=sys.stdin.buffer):
        try:
            header = input_stream.readline().decode("utf-8")
        except Exception as error:
            raise RuntimeError('Failed to read spl protocol header: {}'.format(error))
        parts = str.split(header, ",")
        metaLength = int(parts[1])
        bodyLength = int(parts[2])

        return metaLength, bodyLength

    def parse_meta(self, input_stream=sys.stdin.buffer, length=0):
        try:
            metabody = input_stream.read(length).decode("utf-8")
            metaInfo = json.loads(metabody)
        except Exception as error:
            raise RuntimeError('Failed to parser spl protocol meta: {}'.format(error))

        return metaInfo

    def parse_body(self, input_stream=sys.stdin.buffer, length=0):
        records = []
        if length <= 0:
            return records

        try:
            body = input_stream.read(length).decode("utf-8")
            rows = str.split(body, '\n')
            if len(rows) < 2:
                return records

            fields = str.split(rows[0], '\t')
            for row in rows[1:]:
                record = {}
                parts = str.split(row, '\t')
                for i in range(len(fields)):
                    if i < len(parts):
                        record[fields[i]] = self.format_field(parts[i])
                records.append(record)

            return records
        except Exception as error:
            raise RuntimeError('Failed to parser spl protocol body: {}'.format(error))

    def format_field(self, part):
        type, value = str.split(part, ',', 1)
        if int(type) == 0:
            return self.decodeString(value)
        elif int(type) == 1:
            return int(value)
        elif int(type) == 2:
            return float(value)
        elif int(type) == 3:
            return ''
        elif int(type) == 4:
            return str.islower(value) == 'true'
        elif int(type) == 5:
            return value
        return value


    def send_packet(self, output_stream=sys.stdout.buffer, meta_info=None, lines=None):
        if meta_info is None:
            meta_info = {}
        if lines is None:
            lines = []
        meta = json.dumps(meta_info).encode("utf-8")

        body = self.convert_body_to_str(lines).encode("utf-8")

        head = ('chunked 1.0,%s,%s\n' % (len(meta), len(body))).encode("utf-8")
        output_stream.write(head)
        output_stream.write(meta)
        if len(body) > 0:
            output_stream.write(body)

        output_stream.flush()
        return

    def convert_body_to_str(self, lines=[]):
        if lines is None:
            return ''

        if len(lines) == 0:
            return ''

        fieldStr = ""
        lineStrs = []
        fields = []
        allFields = {}
        for line in lines:
            if not isinstance(line, dict):
                continue
            row = dict(line)
            lineStr = ''
            if len(fields) != 0:
                for field in fields:
                    if field not in row:
                        lineStr += '\t'
                    else:
                        lineStr = lineStr + self.encodeString(str(row[field])) + '\t'

            for key in row:
                if key in allFields:
                    continue
                allFields[key] = 0
                fields.append(key)
                lineStr = lineStr + self.encodeString(str(row[key])) + '\t'

            lineStrs.append(lineStr[:len(lineStr) - 1])

        for field in fields:
            fieldStr = fieldStr + field + '\t'

        fieldStr = fieldStr[:len(fieldStr) - 1]

        body = fieldStr
        for lineStr in lineStrs:
            body += '\n' + lineStr

        return body

    def encodeString(self, value):
        value = str.replace(value, '\t', '\\t')
        value = str.replace(value, '\n', '\\n')
        return value

    def decodeString(self, value):
        value = str.replace(value, '\\t', '\t')
        value = str.replace(value, '\\n', '\n')
        return value
