import pandas as pd
import csv
import os
import zipfile
from api import download_hist_data


def mkdir_p(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def download_all():
    with open('pairs.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # skip the headers
        frames = {}
        for row in reader:
            currency_pair_name, pair, history_first_trading_month = row
            year = int(history_first_trading_month[0:4])
            print(currency_pair_name)
            frames[currency_pair_name.replace('/', '')] = []
            output_folder = os.path.join('output', pair)
            mkdir_p(output_folder)
            try:
                while True:
                    could_download_full_year = False
                    try:
                        print('-', download_hist_data(year=year,
                                                      pair=pair,
                                                      output_directory=output_folder,
                                                      verbose=False))
                        could_download_full_year = True
                    except AssertionError:
                        pass  # lets download it month by month.
                    month = 1
                    while not could_download_full_year and month <= 12:
                        print('-', download_hist_data(year=str(year),
                                                      month=str(month),
                                                      pair=pair,
                                                      output_directory=output_folder,
                                                      verbose=False))
                        month += 1
                    year += 1
            except Exception:
                print('Unzip files for {pair}'.format(pair=pair))
                current_dir = os.getcwd()
                currency_output = os.path.join(current_dir, output_folder)
                os.chdir(currency_output)
                for item in os.listdir(currency_output):
                    if item.endswith(".zip"):
                        file_name = os.path.abspath(item)
                        zip_ref = zipfile.ZipFile(file_name)
                        zip_ref.extractall(currency_output)
                        zip_ref.close()
                        os.remove(file_name)

                print('Remove txt files for {pair}'.format(pair=pair))
                files_in_directory = os.listdir(currency_output)
                filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
                for file in filtered_files:
                    path_to_file = os.path.join(currency_output, file)
                    os.remove(path_to_file)

                #Convert csv files: add header, join date and time, add 0 columns
                os.chdir(currency_output)
                for item in os.listdir(currency_output):
                    if item.endswith(".csv"):
                        file_name = os.path.abspath(item)
                        header_list = ["<DTYYYYMMDD>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>", "<VOL>"]
                        historic_info = pd.read_csv(file_name, sep=',', names=header_list)
                        historic_info['<TICKVOL>'] = 0
                        historic_info['<SPREAD>'] = 2
                        # Convert columns of date and time to datetime index
                        historic_info.index = pd.to_datetime(historic_info['<DTYYYYMMDD>'].map(str) + ' ' + historic_info['<TIME>'].map(str), format='%Y.%m.%d %H:%M:%S')
                        historic_info = historic_info.drop(['<TIME>', '<DTYYYYMMDD>'], axis=1)
                        historic_info.index.name = '<DATETIME>'
                        frames[currency_pair_name.replace('/', '')].append(historic_info)
                final = pd.concat(frames[currency_pair_name.replace('/', '')])
                final.to_csv('{}-1min-backtrader.csv'.format(currency_pair_name.replace('/', '')), float_format='%.4f', index=True)

                os.chdir(current_dir)
                print('[DONE] for currency', currency_pair_name)

if __name__ == '__main__':
    download_all()
