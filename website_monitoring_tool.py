#Author: Jardel Ribeiro de Lima
#Date: 07/20/2017
#Local: Juazeiro-BA, Brazil

import sys
import threading
import time
import re

from websitemonitor import WebSiteMonitor

sites = []
begin_time = None

#Verify if Exist any thread alive
def has_alive_thread(threads):
    for thread in threads:
        if thread.is_alive():
            return True
    return False

#Validate inputs with regular expressions
def validate_input(input):

    match = re.search(r'^\d{1,2}(\.\d+){0,1}$',input[1].replace(',','.'))
    if not match or not (float(input[1].replace(',','.')) >= 0 and float(input[1].replace(',','.')) <= 100 ):
        return False

    match = re.search(r'^\d{1,2}(\.\d+){0,1}$', input[2].replace(',','.'))
    if not match or not (float(input[2].replace(',','.')) >= 0 and float(input[2].replace(',','.')) <= 100 ):
        return False


    match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                      input[0])
    if not match:
        return False

    return True

#Read input file with URL's and SLO's
def read_file(file):

    sites=[]
    try:
        with open(file,'r') as file:
            for line in file:
                info = line.split(';')

                if len(info) < 3:
                    print('\nError on line - {}.\n'
                          'Correct format is: <url>;<successful response SLO>;<fast response SLO>'.format(line.strip()))
                else:
                    if not validate_input(info):
                        print('\nError with url format or double values on line - {}.\n'
                          'Correct format is: <url>;<double>;<double>'.format(line.strip()))
                        continue

                    url = info[0].strip()

                    if url[-1] == '/':
                        url = url[:-1]

                    site = WebSiteMonitor(url,float(info[1]),float(info[2]))
                    sites.append(site)
    except IOError:
        print('Could not open file {}.'.format(file))
        exit()

    return sites

#Thread responsable for making requests every 5 seconds
def make_requests_thread():
    while True:
        for site in sites:
            site.make_request()
        time.sleep(5)

#Mount string with websites status info
def get_status_info():

    info = 'SHOW WEBSITE STATUS\n'
    info += 'BEGIN TIME {}\n'.format(time.strftime('%d/%m/%Y -- %H:%M:%S', begin_time))
    info += 'NOW {}\n'.format(time.strftime('%d/%m/%Y -- %H:%M:%S'))
    info += '{0:40s}\t{1:40s}\t{2:30s}\n'.format('', 'SUCCESSFUL RESPONSE', 'FAST RESPONSE')
    info += '{0:40s}\t{1:10s}\t{2:10s}\t{3:10s}\t{4:10s}\t{5:10s}\t{6:10s}  {7}\n' \
        .format('URL', 'SLI', 'SLO', 'STATUS', 'SLI', 'SLO', 'STATUS','OBS')

    for site in sites:

        if site.req_n == 0:
            info += '{0:30s}\t{1}\n'.format(site.url, 'NO REQUESTS')
            continue

        sli_succ_resp = float(site.succ_res_n / float(site.req_n)) * 100
        sli_fast_resp = float(site.fast_res_n / float(site.req_n)) * 100

        if sli_fast_resp < site.fast_res_slo:
            fast_sli_status = 'BAD'
        else:
            fast_sli_status = 'GOOD'

        if sli_succ_resp < site.succ_res_slo:
            succ_sli_status = 'BAD'
        else:
            succ_sli_status = 'GOOD'

        if has_alive_thread(site.threads):
            alive_threads = '*'
        else:
            alive_threads = ''

        if site.dns_error:
            dns_error = '+'
        else:
            dns_error = ''

        info += '{0:40s}\t{1:10.2f}%\t{2:10.2f}%\t{3:10s}\t{4:10.2f}%\t{5:10.2f}%\t{6:10s}  {7}{8}\n'.format(
            site.url,
            sli_succ_resp,
            site.succ_res_slo,
            succ_sli_status,
            sli_fast_resp,
            site.fast_res_slo,
            fast_sli_status,
            alive_threads,
            dns_error)
    info += 'Legend:\n* - Waiting for succesful responses\n+ - DNS Error'

    return info

#Save report with websites' status
def save_report():
    print('Save status to report.txt')
    try:
        with open('report.txt','w') as file:
            file.write(get_status_info())
    except IOError:
        print('Could not save file report.txt!')

#Display website's status on terminal
def show_status():
    print(get_status_info())


#Main
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('usage: python website_monitoring_tool.py <file_with_sites_urls_and_slos>')

    else:
        print('Web Site SLO Monitor')
        print('\nReading file with URL\'s and SLO\'s')

        sites = read_file(sys.argv[1])
        thread = threading.Thread(target=make_requests_thread)
        thread.daemon = True
        thread.start()
        begin_time = time.localtime()

        print('\nMonitoring has started!')

        while True:
            print('\nMonitoring...')
            print('Menu:\ns - Show Status\nr - Save Report\nq - Exit')
            input = raw_input('Choice:')

            if input == 'q':
                exit(0)
            elif input == 's':
                show_status()
            elif input == 'r':
                save_report()
