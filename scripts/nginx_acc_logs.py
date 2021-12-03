#!/usr/bin/python3

import crossplane
import dns.resolver
import json
import re


def check_sname(d_f_check0):
    checker = 0
    s_names = ""
    for n in d_f_check0:
        if n["directive"] == "server_name":
            s_names = n["args"]
            checker = 1
    return checker, s_names


def check_acslog(d_f_check1):
    checker = 0
    a_logs_list = list()
    for n in d_f_check1:
        if n["directive"] == "access_log":
            log_data = n["args"]
            a_logs_list.append(log_data)
            checker = 1
    return checker, a_logs_list


def sort_logs(alogs_data):
    result = ""
    if len(alogs_data) > 1:
        for alogs_set in alogs_data:
            if "bytes" in alogs_set:
                alogs_data.remove(alogs_set)
    if len(alogs_data) > 1:
        for alogs_set in alogs_data:
            tlpath = alogs_set[0]
            if re.match(".+\.access\.log", tlpath):
                result = tlpath
    else:
        result = alogs_data[0][0]
    return result


def check_domain(domname):
    checker = 0
    try:
        my_resolver.resolve(domname, "A")
        checker = 1
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        pass
    except dns.resolver.NoNameservers:
        pass
    return checker


def verif_domains(dom_list):
    res_lst = list()
    for d_name in dom_list:
        if check_domain(d_name):
            res_lst.append(d_name)
    return res_lst


payload = crossplane.parse('/etc/nginx/nginx.conf')

my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

full_list = dict()
error_doms = list()
for i in payload["config"]:
    for j in i['parsed']:
        if j["directive"] == "server":
            s_data = j["block"]
            s_data_sncheck = list(check_sname(s_data))
            if s_data_sncheck[0]:
                sn_list = s_data_sncheck[1]
                sn_list = verif_domains(sn_list)
                if len(sn_list) > 0:
                    s_data_alcheck = list(check_acslog(s_data))
                    if s_data_alcheck[0]:
                        lp_name = sort_logs(s_data_alcheck[1])
                        if len(lp_name) > 0:
                            full_list[lp_name] = sn_list[0]
                        else:
                            for sn in sn_list:
                                error_doms.append(sn)

disc_log_list = {"data": []}
for l_name, d_name in list(full_list.items()):
    disc_log_list["data"].append({"{#NGACLOGPATH}": l_name, "{#NGDOMNAME}": d_name})

res_json = json.dumps(disc_log_list)

print(res_json)
