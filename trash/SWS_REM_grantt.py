#! /usr/bin/env python
"""
StatisticsOSB


"""
# Authors: Jaime Bruno Cirne de Oliveira (jaime@neuro.ufrn.br)

from __future__ import division

from collections import Counter
import sys
import csv
import statistics
import numpy as np
import sys
import os
from scipy import stats
import chart_studio.plotly as py
import plotly.figure_factory as ff


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


if __name__ == '__main__':
    
    create_data_from_raw()
    
    with open('./data_processed/sws_before_rem.csv', mode='w', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for f in os.listdir("./data"):
            if f.endswith(".csv"):

                classStates = []
                state_intervals = {}
                counter = {}
                open_intervals = {}
                states = []
                
                with open("./data/"+f, 'r') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                    for row in spamreader:
                        states.append(row)

                s_t = []
                sws_last = False

                P = f.split('.')[0]
                D = f.split('.')[1]
                M = f.split('.')[2]
                Y = '20'+((f.split('.')[3]).split('-')[0])

                df = []

                result_file.writerow([f])

                for s in states:

                    if s[0] == 'SWS-like':
                        s_t = s
                        sws_last = True
                    elif s[0] == 'REM-like' and sws_last :
                        df.append(dict(Task='SWS', Start=Y+'-'+M+'-'+D+' '+s_t[1], Finish=Y+'-'+M+'-'+D+' '+s_t[2], Resource=P))
                        df.append(dict(Task='REM', Start=Y+'-'+M+'-'+D+' '+s[1], Finish=Y+'-'+M+'-'+D+' '+s[2], Resource=P))
                        result_file.writerow(s_t)
                        result_file.writerow(s)
                    else:
                        sws_last = False


    #            colors = dict(p1 = 'rgb(46, 137, 205)',
    #                        p2 = 'rgb(114, 44, 121)',
    #                        p3 = 'rgb(198, 47, 105)',
    #                        p4 = 'rgb(58, 149, 136)',
    #                        p5 = 'rgb(107, 127, 135)')

                colors = dict(SWS = 'rgb(46, 137, 205)',
                            REM = 'rgb(114, 44, 121)',
                            teste = 'rgb(107, 127, 135)')

                #fig = ff.create_gantt(df, colors=colors, index_col='Resource', title=f,
                #                    show_colorbar=True, bar_width=0.8, showgrid_x=True, showgrid_y=True)

                if df :
                    fig = ff.create_gantt(df, colors=colors, index_col='Task', title=f,
                                        show_colorbar=True, bar_width=0.8, showgrid_x=True, showgrid_y=True)
                    fig.write_image('./data_processed/sws_before_rem'+f+'.pdf')
                    #fig.show()
                    #fig.show(renderer="svg", width=1280, height=920)
            