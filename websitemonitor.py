#Author: Jardel Ribeiro de Lima
#Date: 07/20/2017
#Local: Juazeiro-BA, Brazil

import httplib
import threading
import time
import numpy as np

class WebSiteMonitor:

    #Class constructor.
    def __init__(self, url, succ_res_slo, fast_res_slo, perc_slo):
        self.url = url
        self.succ_res_slo = succ_res_slo
        self.fast_res_slo = fast_res_slo
        self.perc_slo = perc_slo
        self.req_n = 0
        self.succ_res_n = 0
        self.fast_res_n = 0
        self.dns_error = False
        self.threads = []
        self.req_time = []
        self.perc_ok_n = 0

    #Thread responsable for making requests
    def __make_request_thread(self, show=False):
        try:
            self.req_n += 1
            req_nn = self.req_n

            conn = httplib.HTTPConnection(host=self.url.replace('http://',''), timeout=30)
            begin_time = time.time()
            conn.request("GET", "/")
            end_time = time.time()

            req_time_value = end_time - begin_time

            self.req_time.append(req_time_value)

            resp = conn.getresponse()

            if resp.status in range(200, 500):
                self.succ_res_n += 1

            if (end_time - begin_time) <= 0.1:
                self.fast_res_n += 1

            #For Debugging
            if show:
                print('\nWeb Site: {}'.format(self.url))
                print('Request - {}/{}'.format(req_nn,self.req_n))
                print('Time: {}s'.format((end_time-begin_time)))
                print('Status: {}'.format(resp.status))

        except Exception as e:
            if 'Name or service not known' in e:
                self.dns_error = True
                print('\nError: Name or service not known({}). Verify your DNS Server!'.format(self.url))
                print('\nMonitoring...')
                print('Menu:\nr - Report\ns - Show status\nq - Exit')
                print('Choice:')

    def calc_percentil(self):
        percentil = np.percentile(self.req_time, 90)
        if percentil <= 1:
            self.perc_ok_n += 1
        del self.req_time[:]

    def make_request(self):

        thread = threading.Thread(name=self.url+'-'+str(len(self.threads)), target=self.__make_request_thread)
        thread.daemon = True
        thread.start()

        #Insert thread in threads list
        self.threads.append(thread)

        #Remove threads that are not alive
        for thread in self.threads:
            if not thread.is_alive():
                self.threads.remove(thread)
