import os
import csv


class FileHelper:
    @staticmethod
    def get_file_name_and_extension(file_path):
        basename = os.path.basename(file_path)
        dn, dext = os.path.splitext(basename)
        return dn, dext[1:]

    @staticmethod
    def get_file_name(file_name):
        basename = os.path.basename(file_name)
        dn, dext = os.path.splitext(basename)
        return dn

    @staticmethod
    def get_file_extenstion(file_name):
        basename = os.path.basename(file_name)
        dn, dext = os.path.splitext(basename)
        return dext[1:]


    @staticmethod
    def read_file(file_name):
        with open(file_name, 'r') as document:
            return document.read()

    @staticmethod
    def write_to_file(file_name, content):
        with open(file_name, 'w') as document:
            document.write(content)

    @staticmethod
    def write_to_file_with_mode(file_name, content, mode):
        with open(file_name, mode) as document:
            document.write(content)
    @staticmethod
    def get_files_in_folder(path, file_types):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                ext = FileHelper.get_file_extenstion(file)
                if ext.lower() in file_types:
                    yield file

    @staticmethod
    def get_file_names(path, allowed_local_file_types):
        files = []
        for file in FileHelper.get_files_in_folder(path, allowed_local_file_types):
            files.append(path + file)
        return files

    @staticmethod
    def write_csv(file_name, field_names, csv_data):
        with open(file_name, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for item in csv_data:
                i = 0
                row = {}
                for value in item:
                    row[field_names[i]] = value
                    i = i + 1
                writer.writerow(row)

    @staticmethod
    def write_csv_raw(file_name, csv_data):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for item in csv_data:
                writer.writerow(item)
