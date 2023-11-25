# -*- coding: utf-8 -*-
"""Convert SRT file (a subtitle file) to a CSV file
The CSV file follows the Davinci Resolve Fairlight page ADR csv template.
As the time of writting (Resolve 18.6) there is no way to directly import a SRT into the ADR workflow
as it requires a CSV.
With this script, you can easily convert your SRT to the CSV file.
The script does not set any characters, you have to do that manually in resolve

To call the script: python srt_to_adr_convert.py my_srt_file.srt

@author Felipe Caldas
@email caldas@gmail.com
@youtube https://www.youtube.com/channel/UCg-m_QZxNCqsDdNPCaYB7xg

"""


import re
import sys
import os

def convert_srt_to_csv(srt_filename):
    # Check if the file has a .srt extension
    if not srt_filename.lower().endswith('.srt'):
        raise ValueError("The file must have a .srt extension")

    # Check if the file exists
    if not os.path.exists(srt_filename):
        raise FileNotFoundError(f"The file '{srt_filename}' does not exist")

    csv_filename = srt_filename.rsplit('.', 1)[0] + '.csv'
    with open(srt_filename, 'r', encoding='utf-8') as srt_file, open(csv_filename, 'w', encoding='utf-8') as csv_file:
        subtitle_text = ''
        for line in srt_file:
            if re.match(r'\d+\n', line):
                number = line.strip()
            elif '-->' in line:
                start_time, end_time = line.replace(',', ':').split(' --> ')
                end_time = end_time.strip()
                subtitle_text = ''
            elif line.strip() == '':
                csv_line = f'"{number}","{start_time}","{end_time}","","{subtitle_text.strip()}","False"\n'
                csv_file.write(csv_line)
            else:
                subtitle_text += line.strip() + ' '

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py your_srt_file.srt")
        sys.exit(1)

    try:
        srt_filename = sys.argv[1]
        convert_srt_to_csv(srt_filename)
        print(f"Conversion successful. Output saved to '{srt_filename.rsplit('.', 1)[0]}.csv'")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
