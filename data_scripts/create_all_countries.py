#!/usr/bin/python3
from __future__ import division,print_function
import json
from subprocess import call
import os
import json
script_path = os.path.dirname(os.path.realpath(__file__))


def do_fig(country_name):
    call(["python3", os.path.join(script_path, "caide_country_colored.py"), country_name])
    call(["python3", os.path.join(script_path, "caide_lcolor_colored.py"), country_name])


if __name__ == '__main__':
    from sys import argv
    country_list = [
 'Japan',
 'Romania',
 'Myanmar',
 'Algeria',
 'Serbia and Montenegro',
 'Portugal',
 'Viet Nam',
 'Bulgaria',
 'United Kingdom',
 'Canada',
 'Slovakia',
 'Greece',
 'Laos',
 'Denmark',
 'Spain',
 'Bolivia',
 'Netherlands',
 'Tunisia',
 'Turkmenistan',
 'Serbia',
 'Sweden',
 'Malaysia',
 'Iceland',
 'Estonia',
 'New Zealand',
 'Croatia',
 'Republic of Korea',
 'Venezuela',
 'Slovenia',
 'Latvia',
 'Indonesia',
 'Hungary',
 'Pakistan',
 'Germany',
 'Chile',
 'Israel',
 'Thailand',
 'Finland',
 'United States',
 'Philippines',
 'Kuwait',
 'Cambodia',
 'Honduras',
 'Nicaragua',
 'Austria',
 'Ecuador',
 'South Africa',
 'Italy',
 'Cameroon',
 'Bangladesh',
 'West Bank',
 'Norway',
 'Peru',
 'Ukraine',
 'India',
 'Argentina',
 'Taiwan',
 'Costa Rica',
 'Turkey',
 'Brazil',
 'Australia',
 'Azerbaijan',
 'El Salvador',
 'Cyprus',
 'Russian Federation',
 'Syria',
 'Poland',
 'Belarus',
 'United Arab Emirates',
 'Uruguay',
 'Bosnia and Herzegovina',
 'Singapore',
 'Guatemala',
 'Albania',
 'Armenia',
 'Ghana',
 'Ethiopia',
 'Czech Republic',
 'Botswana',
 'Iran',
 'Sri Lanka',
 'Uganda',
 'Belgium',
 'Lithuania',
 'Switzerland',
 'Iraq',
 'Paraguay',
 'Bahrain',
 'Nigeria',
 'Equatorial Guinea',
 'France',
 'Guadeloupe',
 'Egypt',
 'Trinidad and Tobago',
 'Congo (Brazzaville)',
 'Saudi Arabia',
 'Niger',
 'Lebanon',
 'Morocco',
 'Dominica',
 'Congo (Kinshasa)',
 'Ireland',
 'Oman',
 'Mexico',
 'China']


    #cdict = json.load(open(script_path, "../real_data/country_locations.json"))
    #country_list = [cdict.keys() if i not in bad_country_list]
    try:
        from multiprocessing import Process, Pool, cpu_count
        pool = Pool(processes=int(argv[1]))
        res = pool.map_async(do_fig, country_list)
        print(res.get())
    except ImportError:
        print ("Not utilizing multiprocessing")
        map(do_fig, country_list)
