#!/usr/bin/env python3
'''
Copyright (C) 2020, DomFu Contributors.
See the LICENSE.txt file for copying permission.
'''

import click
import requests
import time
import socket
from threading import *
import queue
from yaspin import yaspin, Spinner
from fake_useragent import UserAgent
from DomFu import fetchCrtSh, fetchBufferOverRun, fetchHackerTarget, fetchThreatCrowd, fetchVirusTotal, Probe


def version():
    return('''
⣤⣤⣤⡤⣤⣤⣀⠀⠀⠀⠀⣀⢤⣴⣴⣤⣀⠀⠀⣤⣤⣤⡄⢀⣤⣤⣀⠀⢀⣤⣤⣀⠀⢠⣤⣤⣤⠤⣤⣤⣤⢠⣤⣤⣤⠀⢠⣤⣤⣤⠀⠀⠀⠀
⣿⣿⣿⡇⠀⣿⣿⣿⡀⢠⣿⠀⢀⣿⣿⣿⣿⣷⠀⣿⣿⣿⡇⣿⣿⣿⣿⣆⣿⣿⣿⣿⣆⢸⣿⣿⡏⢾⣿⣿⣿⢸⣿⣿⣿⠀⢸⣿⣿⣿⠀⠀⠀⠀
⣿⣿⣿⡇⢀⣿⣿⣿⣷⣿⣿⣄⠀⠉⢻⣿⣿⣿⡇⣿⣿⣿⡟⠈⣿⣿⣿⣟⠈⣿⣿⣿⣇⢸⣿⣿⣿⣤⣭⣩⠉⢸⣿⣿⣿⠀⣸⣿⣿⣿⠀⠀⠀⠀
⣿⣿⣿⢿⣿⣿⣿⣿⠃⠹⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⡇⠀⣿⣿⣿⣇⠀⣿⣿⣿⡇⢸⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⢹⣿⣿⣿⠀⠀⠀⠀⠀
⠻⠻⠛⠸⠻⠻⠛⠁⠀⠀⠈⠛⠻⠿⠿⠛⠉⠀⠀⠻⠻⠻⠃⠀⠻⠻⠻⠓⠀⠻⠻⠻⠃⠸⠻⠻⠻⠀⠀⠀⠀⠀⠛⠻⠻⠋⠸⠻⠻⠻⠀⠀v1.2.3
by txsadhu⠀⠀⠀
------------------------------------------------------------⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''')


@click.command()
@click.version_option()
@click.option('--domain', '-d', prompt="Enter a domain name", help='Enter your domain name. (USAGE: --domain=domain.tld)')
@click.option('--output', '-o', help='Stores the output in a file. (USAGE: --output=domain.tld)',)
@click.option('--probe', '-p', default=False, help='Validates the output domains. (USAGE: --probe=True)')
def subdomain(domain, output, probe):
    click.echo(version())
    sp = Spinner(["[\]", "[|]", "[/]", "[-]"], 200)
    torthere = True

    if probe:
        with yaspin(sp, text="Checking if Tor is installed in your system"):
            try:
                headers = {'User-Agent': UserAgent().random}
                proxies = {
                    'http': 'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'
                }
                fetchURL = requests.get(
                    'https://check.torproject.org/api/ip', headers=headers, proxies=proxies).json()

                if fetchURL['IsTor'] == True:
                    torthere = True
                    yaspin().ok(
                        "[Done!] Checking if Tor is installed in your system")
                else:
                    torthere = False
                    yaspin().ok(
                        "[Eww...] Install and Connect to Tor to run prober")
            except:
                torthere = False
                yaspin().ok(
                    "[TPYL_DOMFU_TOR] There was a problem checking tor")

    with yaspin(sp, text="Checking if the domain is online or valid"):
        try:
            socket.gethostbyname(domain)
            dom_valid = True
            yaspin().ok("[Valid!] Looks like your domain is valid and online")
        except socket.gaierror:
            dom_valid = False
            yaspin().fail(
                "[Invalid!] Looks like your domain is offline or invalid")

    subdomain = []

    if dom_valid and torthere:
        timenow_start = time.perf_counter()

        with yaspin(sp, text="Asking ours spies about your subdomains"):

            que1 = queue.Queue()
            que2 = queue.Queue()
            que3 = queue.Queue()
            que4 = queue.Queue()
            que5 = queue.Queue()

            crt_thread = Thread(target=lambda q, arg1: q.put(
                fetchCrtSh(arg1)), args=(que1, domain))

            bufferoverrun_thread = Thread(target=lambda q, arg2: q.put(
                fetchBufferOverRun(arg2)), args=(que2, domain))

            hackertarget_thread = Thread(target=lambda q, arg3: q.put(
                fetchHackerTarget(arg3)), args=(que3, domain))

            threatcrowd_thread = Thread(target=lambda q, arg4: q.put(
                fetchThreatCrowd(arg4)), args=(que4, domain))

            vt_thread = Thread(target=lambda q, arg5: q.put(
                fetchVirusTotal(arg5)), args=(que5, domain))

            # INIT: Don't try to loop this threads, it slows down the process --->
            crt_thread.start()
            bufferoverrun_thread.start()
            hackertarget_thread.start()
            threatcrowd_thread.start()
            vt_thread.start()

            crt_thread.join()
            bufferoverrun_thread.join()
            hackertarget_thread.join()
            threatcrowd_thread.join()
            vt_thread.join()

            rcrt_thread = que1.get()
            rbufferoverrun_thread = que2.get()
            rhackertarget_thread = que3.get()
            rthreatcrowd_thread = que4.get()
            rvt_thread = que5.get()
            # End: Don't try to loop this threads, it slows down the process --->

            yaspin().ok("[Done!] Asking ours spies about your subdomains")

        with yaspin(sp, text="Processing the data recieved"):
            try:
                subdomain.extend(rcrt_thread)
            except:
                pass

            try:
                subdomain.extend(rbufferoverrun_thread)
            except:
                pass

            try:
                subdomain.extend(rhackertarget_thread)
            except:
                pass

            try:
                subdomain.extend(rthreatcrowd_thread)
            except:
                pass

            try:
                subdomain.extend(rvt_thread)
            except:
                pass

            yaspin().ok("[Done!] Processing the data recieved")

        if probe:
            with yaspin(sp, text="Validating your Domains on our Lab"):
                subdomain = Probe(subdomain)
                yaspin().ok("[Done!] Validating your Domains on our Lab")

        timenow_end = time.perf_counter()
        subdomain = sorted(set(subdomain))
        print('')
        print('-'*60)
        print('')

        if output != None:
            print('\n'.join(subdomain))
            print("")
            print('-'*60)
            fileoutput = open('%s' % output, 'w')
            towrite = '\n'.join(subdomain)
            fileoutput.write(towrite)
            fileoutput.close()
            print("")
            print(
                f"All Done! in {round(timenow_end-timenow_start, 2)} second(s). Check your output file")
            print("")
        else:
            print('\n'.join(subdomain))
            print("")
            print('-'*60)
            print("")
            print(
                f"All Done! in {round(timenow_end-timenow_start, 2)} second(s).")
            print("")

    else:
        print("Error (TPYL_DomFu_INVDOM): Enter a valid domain")
        print("\n")

    print('-'*60)


if __name__ == '__main__':
    subdomain()
