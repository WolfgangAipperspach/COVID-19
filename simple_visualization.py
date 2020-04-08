#!/usr/bin python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pprint import pprint
import pandas as pd
import numpy as np

class Covid(object):
    def __init__(self):
        self.data = {}

        dat = pd.read_csv('csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        self.data.update({'confirmed':dat})

        dat = pd.read_csv('csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        self.data.update({'deaths':dat})

        #dat = pd.read_csv('../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
        #self.data.update({'recovered':dat})

        POP_DATA_SOURCE_EUROPE = 'https://en.wikipedia.org/wiki/List_of_European_countries_by_population'

        spain = {'data_type':'confirmed', 'data_line':self.data_line('Spain', ''), 'population':46767543, 'population_source':POP_DATA_SOURCE_EUROPE}
        germany = {'data_type':'confirmed', 'data_line':self.data_line('Germany', ''), 'population':83792987, 'population_source':POP_DATA_SOURCE_EUROPE}
        italy = {'data_type':'confirmed', 'data_line':self.data_line('Italy', ''), 'population':60496082, 'population_source':POP_DATA_SOURCE_EUROPE}
        france = {'data_type':'confirmed', 'data_line':self.data_line('France', ''), 'population':65227357, 'population_source':POP_DATA_SOURCE_EUROPE}
        switzerland = {'data_type':'confirmed', 'data_line':self.data_line('Switzerland', ''), 'population':8637694, 'population_source':POP_DATA_SOURCE_EUROPE}
        norway = {'data_type':'confirmed', 'data_line':self.data_line('Norway', ''), 'population':5407670, 'population_source':POP_DATA_SOURCE_EUROPE}
        sweden = {'data_type':'confirmed', 'data_line':self.data_line('Sweden', ''), 'population':10081948, 'population_source':POP_DATA_SOURCE_EUROPE}
        denmark = {'data_type':'confirmed', 'data_line':self.data_line('Denmark', ''), 'population':5785741, 'population_source':POP_DATA_SOURCE_EUROPE}
        netherlands = {'data_type':'confirmed', 'data_line':self.data_line('Netherlands', ''), 'population':17123478, 'population_source':POP_DATA_SOURCE_EUROPE}
        belgium = {'data_type':'confirmed', 'data_line':self.data_line('Belgium', ''), 'population':11579502, 'population_source':POP_DATA_SOURCE_EUROPE}
        austria = {'data_type':'confirmed', 'data_line':self.data_line('Austria', ''), 'population':8999973, 'population_source':POP_DATA_SOURCE_EUROPE}
        uk = {'data_type':'confirmed', 'data_line':self.data_line('United Kingdom', ''), 'population': 	67803450, 'population_source':POP_DATA_SOURCE_EUROPE}

        us = {'data_type':'confirmed', 'data_line':self.data_line('US', ''), 'population': 329.45e9 , 'population_source':'https://worldpopulationreview.com/countries/united-states-population/'}
        iran = {'data_type':'confirmed', 'data_line':self.data_line('Iran', ''), 'population':82913906, 'population_source':'https://en.wikipedia.org/wiki/Demographics_of_Iran'}
        south_korea = {'data_type':'confirmed', 'data_line':self.data_line('Korea, South', ''), 'population':51635256 , 'population_source':''}


        country_list = [spain, italy, switzerland, norway, denmark, sweden, austria, uk, germany, france, netherlands, belgium, us, iran, south_korea]
        filename = 'relative_cases.png'
        title = "relative COVID-19 confirmed cases \n cases data from https://github.com/CSSEGISandData/COVID-19 \n population data from https://en.wikipedia.org/wiki/List_of_European_countries_by_population"
        self.plot_graph_relative(country_list, title, filename)

        filename = 'absolute_cases.png'
        title = "COVID-19 confirmed cases \n data from https://github.com/CSSEGISandData/COVID-19"
        self.plot_graph_absolute(country_list, title, filename)

        filename = 'absolute_deaths.png'
        title = "COVID-19 deaths \n data from https://github.com/CSSEGISandData/COVID-19"
        for c in country_list:
            c['data_type'] = 'deaths'
        self.plot_graph_absolute(country_list, title, filename)



    def data_line(self, country, province):
        n_lines = self.data['confirmed'].shape[0]
        if province == '':
            province = 'nan'
        for data_line in range(n_lines):
            _country = str(self.data['confirmed'].iloc[data_line,1])
            _province = str(self.data['confirmed'].iloc[data_line,0])
            #print(country, _country, str(type(_country)))
            if country == _country and province == _province:
                print('found', country, province, 'data line =', str(data_line))
                return data_line
        print(country, province, ' not found')
        return -1

    def get_data(self, data_type, data_line):
        tl = self.data[data_type].iloc[data_line,4:]
        tld = [datetime.strptime(date, '%m/%d/%y') for date in tl.index]
        tlv = [tl.loc[i] for i in tl.index]
        country = self.data[data_type].iloc[data_line,1]
        province = self.data[data_type].iloc[data_line,0]
        #print(country)
        #print(province)

        if type(province) != str:
        #if np.isnan(province) == True:
            province = ''
        label = country + ' ' + province + ', ' + data_type + ' cases'
        return (tld, tlv, label)

    def abs_to_rel(self, cases, population):
        relative_cases = [case/population*1000.0 for case in cases]
        return relative_cases


    def plot_graph_relative(self, country_list, title, filename):
            fig = plt.figure()
            scale_factor = 1.0
            fig.set_size_inches(14.1*scale_factor,10*scale_factor)
            ax = fig.add_subplot(1, 1, 1)

            for country in country_list:
                data_type = country['data_type']
                data_line = country['data_line']
                population = country['population']
                population_source = country['population_source']

                (dates, cases, label) = self.get_data(data_type, data_line)
                label += ', population=' + str(population)
                relative_cases = self.abs_to_rel(cases, population)
                ax.plot(dates, relative_cases, label = label)

            ax.set_title(title)
            ax.set_ylabel('relative cases per country population in ‰')
            ax.grid(True)
            #plt.yscale('log')
            plt.legend(loc='upper left')
            plt.savefig('output/' + filename)
            plt.close('all')
            #plt.show()

    def plot_graph_absolute(self, country_list, title, filename):
            fig = plt.figure()
            scale_factor = 1.0
            fig.set_size_inches(14.1*scale_factor,10*scale_factor)
            ax = fig.add_subplot(1, 1, 1)

            for country in country_list:
                data_type = country['data_type']
                data_line = country['data_line']
                population = country['population']
                population_source = country['population_source']

                (dates, cases, label) = self.get_data(data_type, data_line)
                label += ', population=' + str(population)
                #relative_cases = self.abs_to_rel(cases, population)
                ax.plot(dates, cases, label = label)

            ax.set_title(title)
            ax.set_ylabel('absolute cases')
            ax.grid(True)
            #plt.yscale('log')

            plt.legend(loc='upper left')
            plt.savefig('output/' + filename)
            plt.close('all')
            #plt.show()



if __name__ == "__main__":
    covid = Covid()
