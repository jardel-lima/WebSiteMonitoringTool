# #WEBSITE MONITORING TOOL#


# DESCRIPTION

This script will monitor Service Level Indicators (SLI) of a list of websites. Two SLIs will be monitored:
SUCCESSFUL RESPONSE and FAST RESPONSE.
    - SUCCESSFUL RESPONSE - Responses with HTTP status code >= 200 and <= 499;
    - FAST RESPONSE - HTTP requests that are responded in 100ms or less.

For a list of website url's a get request will be made every 5 seconds. Each SLI will compared with the given
Service Level Objective (SLO).


# REQUIREMENTS

    - Python 2.7


# INSTALLATION

    - Clone project or copy the  websitemonitor.py and website_monitoring_tool.py files to the same folder


# EXECUTION

    - First create a text file with website urls and their respective Service Level Objectives with the
    following format:
    <url>;<successful response SLO>;<fast response SLO>
        - url must be a string with a http format
        - the other 2 must be doubles >= 0.0 and <=100.0

    - Open the terminal and execute:
        python website_monitoring_tool.py <text file with website urls and SLOs>

    - If every thing went well you will see the message: 'Monitoring has started!'


# USAGE

When the script was executed you will see a simple option menu:
    Menu:
    s - Show Status
    r - Save Report
    q - Exit
    Choice:

    When you type and enter one of those options, the following will happen:

    s - Will be displayed on the terminal the current SLI the SLO and the STATUS
    (if SLI >= SLO GOOD will be displayed otherwise BAD);

    r - The same output seen on terminal when s is selected will be save on a text file called report.txt;

    q - The aplication will stop.


# DEVELOPMENT CONSIDERATIONS

This application was writen using Python for 3 reasons:
    1 - It is very simple and powerful programming language;
    2 - It is the programming language that lately I have used the most.
    3 - I had few time to concept and build the application.

Once I was asked to build a long-running application with user interaction and with some network tasks
I decided to use multithreading. It allows the user to get partial reports while the application keep making
requests and make HTTP requests over Internet without 'blocking' the application.

All threads was created as daemons, it allows the application to exit even if some threads still alive. The
necessary modules on this applications are only default modules that comes with Python 2.7, it is not
necessary to install any extra modules.

I decided to create a class called WebSiteMonitor because it helps to get reports to each monitored website.
I used a list of thread to each website because as every 5 second a new request has to be made
and even though the last request made cannot be a fast response anymore, once it has passed 5 seconds, it can be
a successful response still. So, I create a new thread to the new request and keep the old one in the list.
Not to keep finished threads in the list, I remove threads that are not alive anymore.

# IMPROVEMENTS AND ISSUES

The first improvement on this application was to create a better user interface, although it does what
it was asked for, this application is not user-friendly. A GUI to better user interaction and visualization
can be done. Another alternative would be use this script as content provider to a web application with a better
user interface.

Another improvement would be finding a better way to calculate the request response time. Doing some fast
research I found some modules that return the exactly response time to a request, I did not use this because
I did not have enough time and I wanted to keep this script simple. During tests I found out that the some
DNS servers can cause a 'Name or service not known' error when monitoring more than 15-20 websites.
Some forums said that this is error can be caused be the DNS server. I did not have time to better investigate
this error and find solutions, so I used a try catch as a workaround.

#CREDITS

This script was developed by Jardel Ribeiro de Lima (jardelribeiro.lima@gmail.com)





