import requests
import urllib3
import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


target =input("pe or cvm ip: ")
username = input("username: ")
password = getpass.getpass("password: ")

payload = {}
headers = {'Content-Type': "application/json" }
auth = (username, password)

#get hosts uuid/ip
hosts_url = f'https://{target}:9440/PrismGateway/services/rest/v2.0/hosts/'
hosts_response = requests.get(hosts_url, json=payload, headers=headers, auth=auth,verify=False)
hosts_data = hosts_response.json()
entities=hosts_data["entities"]
hosts={}
for entity in entities:
    hosts[entity["uuid"]]=entity["hypervisor_address"]
    
#nic to switch port mapp

for uuid, ip in hosts.items():
    
    url=f'https://{target}:9440/PrismGateway/services/rest/v2.0/hosts/{uuid}/host_nics'
    response = requests.get(url, json=payload, headers=headers, auth=auth,verify=False)
    nics = response.json()

    print(f"==================[ {ip} ]==================")

    for nic in nics:
        nic_name=str(nic["name"])
        TOR_sw_name=str(nic["switch_device_id"])
        TOR_sw_port=str(nic["switch_port_id"])
        print(f"{nic_name.ljust(10)}{TOR_sw_name.ljust(25)}{TOR_sw_port}")
        
    
    
