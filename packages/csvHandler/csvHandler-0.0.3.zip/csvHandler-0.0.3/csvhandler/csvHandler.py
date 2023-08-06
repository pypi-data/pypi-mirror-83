import pandas as pd

NEW_VALUE_COLUMN_SUFFIX = '_new'

def combine(added_path, deleted_path, changed_original_path, changed_new_path, result_path):
    added = pd.read_csv(added_path)
    deleted = pd.read_csv(deleted_path)
    changed_original = pd.read_csv(changed_original_path)
    changed = pd.read_csv(changed_new_path)

    added['recordType'] = 'added'
    deleted['recordType'] = 'deleted'

    changed_merge = changed_original.merge(
        changed, on='Id', suffixes=('', NEW_VALUE_COLUMN_SUFFIX))
    changed_merge['recordType'] = 'changed'

    result = pd.concat([added, deleted, changed_merge])
    result.to_csv(result_path, index=False)

class CsvHandler():
    def __init__(self, path):
        self.file_path = path
        self.page_number = 0
        self.page_size = 0

    def get_metadata(self):
        data_frame = pd.read_csv(self.file_path)
        return {'total_rows': data_frame.shape[0],
                'file_path': self.file_path,
                'columns': data_frame.columns.tolist(),
                'page_size': self.page_size,
                'current_page_number': self.page_number}

    def get_page(self, page_number, page_size):
        data_frame = pd.read_csv(self.file_path, skiprows=(
            page_number-1)*page_size, nrows=page_size)
        self.page_number = page_number
        self.page_size = page_size
        return self.__page_format(data_frame)

    def __page_format(self, data_frame):
        records = data_frame.to_dict('records')
        page = []
        for record_dict in records:
            record = {}
            record['id'] = record_dict['Id']
            record['recordType'] = record_dict['recordType']
            data = []
            for column_name, value in record_dict.iteritems():
                if (column_name.find(NEW_VALUE_COLUMN_SUFFIX, len(column_name)-len(NEW_VALUE_COLUMN_SUFFIX), len(column_name)) > -1 or
                    column_name == 'recordType' or
                        column_name == 'Id'):
                    continue

                item = {}
                item['column_name'] = column_name
                item['column_type'] = type(value).__name__
                item['value'] = value
                if record['recordType'] == 'changed' and value != record_dict[column_name + NEW_VALUE_COLUMN_SUFFIX]:
                    item['new_value'] = record_dict[column_name +
                                                    NEW_VALUE_COLUMN_SUFFIX]

                data.append(item)

            record['data'] = data
            page.append(record)
        return page
