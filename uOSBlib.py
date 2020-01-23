import os
import csv

relabel_states ={
    'Alerta': 'Alert',
    'Ativo': 'Active',
    'Quieto': 'QOP',
    'AMMD': 'QHH',
    'AMME': 'QHH',
    'QMMD': 'QHH',
    'QMME': 'QHH',
    'QPC': 'SWS-like',
    'REM': 'REM-like',
    'REMD': 'OEM',
    'REME': 'OEM',
}

def get_interval_in_seconds(time_s, time_e):
    return get_duration_in_seconds(time_s, time_e)

def get_duration_in_seconds(time_s, time_e):
    hour_s = int(time_s.split(':')[0])
    minutes_s = int(time_s.split(':')[1])
    seconds_s = int(time_s.split(':')[2])
    hour_e = int(time_e.split(':')[0])
    minutes_e = int(time_e.split(':')[1])
    seconds_e = int(time_e.split(':')[2])

    return (hour_e-hour_s)*3600  + (minutes_e-minutes_s)*60 + seconds_e-seconds_s

def str_time_to_int_seconds(time):
    hour = int(time.split(':')[0])
    minutes = int(time.split(':')[1])
    seconds = int(time.split(':')[2])
    return hour*3600  + minutes*60 + seconds

def create_data_from_raw():
    for f in os.listdir("./data_raw"):
        if f.endswith(".csv"):
            cleaning_states = []
            states_raw = []
            with open("./data_raw/"+f, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    if any(row):
                        states_raw.append(row)

            #cleaning empty and duration columns
            for i, r in enumerate(states_raw):
                r = list(filter(lambda a: a != '', r))
                if len(r) > 3:
                    r.pop(1)
                states_raw[i] = r

            # removing consecutive equals states
            for s in states_raw:
                if len(cleaning_states) > 0 and s[0] == cleaning_states[-1][0]:
                    cleaning_states[-1][2] = s[2]
                else:
                    cleaning_states.append(s)
            
            # change old names states to new names
            for i in range(len(cleaning_states)):
                cleaning_states[i][0] = relabel_states.get(cleaning_states[i][0], cleaning_states[i][0])

            # save new csv to work
            with open('./data/'+f, mode='w', newline='') as csvfile:
                result_file = csv.writer(csvfile, delimiter=';', quotechar='|')
                for cs in cleaning_states:
                    result_file.writerow(cs)
