import re
import pandas as pd
import csv

input_file = "ancom_cluj.csv"
regex_loc = re.compile('.* - ')

def main():
    rec = []
    df = pd.read_csv(input_file)
    for index, row in df.iterrows():
        localitate = re.findall('.* - ', row['localitate'])[0].split(' - ')[0]
        uat = re.findall('\(.* - ', row['localitate'])[0].strip('(').strip(' - ')
        rec.append([localitate, uat, row['companie'], row['telefonie_fixa'], row['internet_fix'], row['TV_cablu']])

    df_out = pd.DataFrame(rec, columns = ['localitate', 'uat', 'companie', 'telefonie_fixa', 'internet_fix', 'TV_cablu'])
    df_out.to_csv('ancom_cluj_proc.csv', index = False)

if __name__ == "__main__":
    main()