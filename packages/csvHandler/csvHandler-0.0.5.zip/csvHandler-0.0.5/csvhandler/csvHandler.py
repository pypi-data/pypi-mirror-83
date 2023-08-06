import pandas as pd

NEW_VALUE_COLUMN_SUFFIX = '_new'
RECORD_TYPE_STR = 'recordType'
ID_COLUMN_STR = 'Id'

def combine(added_path, deleted_path, changed_original_path, changed_new_path, result_path):
    added = pd.read_csv(added_path)
    deleted = pd.read_csv(deleted_path)
    changed_original = pd.read_csv(changed_original_path)
    changed = pd.read_csv(changed_new_path)

    added[RECORD_TYPE_STR] = 'added'
    deleted[RECORD_TYPE_STR] = 'deleted'

    changed_merge = changed_original.merge(
        changed, on=ID_COLUMN_STR, suffixes=('', NEW_VALUE_COLUMN_SUFFIX))
    changed_merge[RECORD_TYPE_STR] = 'changed'

    result = pd.concat([added, deleted, changed_merge])
    result.to_csv(result_path, index=False)


class CsvHandler():
    def __init__(self, path):
        self.file_path = path
        data_frame = pd.read_csv(self.file_path)
        self.metadata = {'rows': {'total': data_frame.shape[0],
                                  'added': len(data_frame[data_frame[RECORD_TYPE_STR] == 'added']),
                                  'deleted': len(data_frame[data_frame[RECORD_TYPE_STR] == 'deleted']),
                                  'changed': len(data_frame[data_frame[RECORD_TYPE_STR] == 'changed'])},
                         'filePath': self.file_path,
                         'columns': data_frame.columns.tolist()}

    def get_metadata(self):
        return self.metadata

    def get_page(self, page_number, page_size):
        data_frame = pd.read_csv(self.file_path, skiprows=range(
            1, (page_number-1)*page_size+1), nrows=page_size)
        return self.__page_format(data_frame)

    def __page_format(self, data_frame):
        records = data_frame.to_dict('records')
        page = []
        for record_dict in records:
            record = {}
            record['id'] = record_dict[ID_COLUMN_STR]
            record[RECORD_TYPE_STR] = record_dict[RECORD_TYPE_STR]
            data = []
            for column_name, value in record_dict.iteritems():
                if (column_name.find(NEW_VALUE_COLUMN_SUFFIX, len(column_name)-len(NEW_VALUE_COLUMN_SUFFIX), len(column_name)) > -1 or
                    column_name == RECORD_TYPE_STR or
                        column_name == ID_COLUMN_STR):
                    continue

                item = {}
                item['columnName'] = column_name
                item['columnType'] = type(value).__name__
                item['value'] = value
                if record[RECORD_TYPE_STR] == 'changed' and value != record_dict[column_name + NEW_VALUE_COLUMN_SUFFIX]:
                    item['newValue'] = record_dict[column_name +
                                                   NEW_VALUE_COLUMN_SUFFIX]

                data.append(item)

            record['data'] = data
            page.append(record)
        return page
