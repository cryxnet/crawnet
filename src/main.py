from database import Database
import os
from dotenv import load_dotenv
import recon as Recon
import json

header = """
 ██████╗██████╗  █████╗ ██╗    ██╗███╗   ██╗███████╗████████╗
██╔════╝██╔══██╗██╔══██╗██║    ██║████╗  ██║██╔════╝╚══██╔══╝
██║     ██████╔╝███████║██║ █╗ ██║██╔██╗ ██║█████╗     ██║   
██║     ██╔══██╗██╔══██║██║███╗██║██║╚██╗██║██╔══╝     ██║   
╚██████╗██║  ██║██║  ██║╚███╔███╔╝██║ ╚████║███████╗   ██║   
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   
 
                    >> by cryxnet <<  
           $~ 𝙂𝙧𝙖𝙥𝙝 𝙗𝙖𝙨𝙚𝙙 Domain 𝘿𝙞𝙨𝙘𝙤𝙫𝙚𝙧𝙮 𝙏𝙤𝙤𝙡𝙠𝙞𝙩 ~$
           
         __________________________________________                                                                                                                                                                                                                                                                                                                             
"""

load_dotenv()

db = Database(os.environ.get("DB_URI"), os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"))

ip_node_create_query = "CREATE (n:IP {address:'IP_HOLDER'})"
domain_node_create_query = "CREATE (n:DOMAIN {name: 'NAME_HOLDER', a: 'A_HOLDER', aaaa: AAAAT_HOLDER, cname: CNME_HOLDER, mx: MX_HOLDER, ns: NS_HOLDER, txt: TXT_HOLDER })"
port_node_create_query = "CREATE (n:PORT {number: 'PORTNUMBER_HOLDER', name: 'DESCRIPTION_HOLDER'})"
location_node_create_query = "CREATE (n:LOCATION {country:'COUNTRY_HOLDER', region:'REGION_HOLDER', city:'CITY_HOLDER'})"
service_node_create_query = "CREATE (n:SERVICE {name:'NAME_HOLDER', version:'VERSION_HOLDER', vendor:'VENDOR_HOLDER'})"

service_to_port_match_query = "MATCH (a:SERVICE), (b:PORT) WHERE a.name = 'SERVICE_HOLDER' AND b.port = 'PORTNUMBER_HOLDER' AND b.belongs = 'BELONGS_HOLDER' CREATE (a)-[r:running_on]->(b)"
ip_to_port_match_query = "MATCH (a:IP), (b:PORT) WHERE a.address = 'IP_HOLDER' AND b.number = 'PORTNUMBER_HOLDER' CREATE (b)-[r:open_on]->(a)"
ip_to_location_match_query = "MATCH (a:IP), (b:LOCATION) WHERE a.address = 'IP_HOLDER' AND b.country = 'COUNTRY_HOLDER' AND b.region = 'REGION_HOLDER' and b.city = 'CITY_HOLDER' CREATE (a)-[r:located_in]->(b)"
domain_to_ip_match_query = "MATCH (a:DOMAIN), (b:IP) WHERE a.name = 'DOMAIN_HOLDER' AND b.address = 'IP_HOLDER' CREATE (a)-[r:belongs_to]->(b)"

ip_exists_query = "OPTIONAL MATCH (n:IP{address:'IP_HOLDER'})RETURN n IS NOT NULL AS Predicate"
location_exists_query = "OPTIONAL MATCH (n:LOCATION{country:'COUNTRY_HOLDER', region:'REGION_HOLDER', city:'CITY_HOLDER'})RETURN n IS NOT NULL AS Predicate"
port_exists_query = "OPTIONAL MATCH (n:PORT{number:'PORTNUMBER_HOLDER', name: 'DESCRIPTION_HOLDER'})RETURN n IS NOT NULL AS Predicate"

def buildDomainNode(name, context):
    create_domain_query = domain_node_create_query.replace('NAME_HOLDER', name).replace('A_HOLDER', str(context["records"]["A"][0])).replace('AAAAT_HOLDER', str(context["records"]["AAAA"])).replace('CNME_HOLDER', str(context["records"]["CNAME"])).replace('MX_HOLDER', str(context["records"]["MX"])).replace('NS_HOLDER', str(context["records"]["NS"])).replace('TXT_HOLDER', str(context["records"]["TXT"]))
    create_ip_query = ip_node_create_query.replace('IP_HOLDER', context["records"]["A"][0])
    create_location_query = location_node_create_query.replace('COUNTRY_HOLDER', str(context["ipaddrs"]["location"]["country"])).replace('REGION_HOLDER', str(context["ipaddrs"]["location"]["region"])).replace('CITY_HOLDER', str(context["ipaddrs"]["location"]["city"]))
    create_port_query = port_node_create_query.replace('PORTNUMBER_HOLDER', "443").replace('DESCRIPTION_HOLDER', 'HTTPS')
    
    match_domain_with_ip_query = domain_to_ip_match_query.replace('DOMAIN_HOLDER', name).replace('IP_HOLDER', context["records"]["A"][0])
    match_ip_with_location_query = ip_to_location_match_query.replace('IP_HOLDER', context["records"]["A"][0]).replace('COUNTRY_HOLDER', str(context["ipaddrs"]["location"]["country"])).replace('REGION_HOLDER', str(context["ipaddrs"]["location"]["region"])).replace('CITY_HOLDER', str(context["ipaddrs"]["location"]["city"]))
    match_ip_with_port_query = ip_to_port_match_query.replace('IP_HOLDER', context["records"]["A"][0]).replace("PORTNUMBER_HOLDER", "443")
    
    check_ip_exists_query = ip_exists_query.replace('IP_HOLDER', context["records"]["A"][0])
    check_location_exists_query = location_exists_query.replace('COUNTRY_HOLDER', str(context["ipaddrs"]["location"]["country"])).replace('REGION_HOLDER', str(context["ipaddrs"]["location"]["region"])).replace('CITY_HOLDER', str(context["ipaddrs"]["location"]["city"]))
    check_port_exists_query = port_exists_query.replace('PORTNUMBER_HOLDER', "443").replace('DESCRIPTION_HOLDER', 'HTTPS')
    
    print("[+] Query Created: " + create_domain_query)
    print("[+] Query Created: " + create_ip_query)
    print("[+] Query Created: " + create_location_query)
    print("[+] Query Created: " + create_port_query)
    print("[+] Query Created: " + match_domain_with_ip_query)
    print("[+] Query Created: " + match_ip_with_location_query)
    print("[+] Query Created: " + match_ip_with_port_query)
    print("[+] Query Created: " + check_ip_exists_query)
    print("[+] Query Created: " + check_location_exists_query)
    print("[+] Query Created: " + check_port_exists_query)
    
    result_location_check = db.query(check_location_exists_query)
    result_ip_check = db.query(check_ip_exists_query)
    result_port_check = db.query(check_port_exists_query)
    
    if "False" in str(result_ip_check):
        db.query(create_ip_query)
    
    if "False" in str(result_location_check):
        db.query(create_location_query)
        
    if "False" in str(result_port_check):
        db.query(create_port_query)
    
    db.query(create_domain_query)
    
    db.query(match_domain_with_ip_query)
    db.query(match_ip_with_location_query)
    db.query(match_ip_with_port_query)

    return "Done!"

if __name__ == "__main__":
    print(header + "\n")
    
    while True:
        print("""
              [1] Discover new Domain
              """)
        
        menuID = int(input("$~ Enter Number >> "))
        
        if menuID == 1:
            domain = input("$~ Enter Domain >> ")
            reconResult = Recon.run(domain)
            queryResult = buildDomainNode(name=domain, context=reconResult)
            print(queryResult)
                  
        else:
            print("[-] Non existing menu option.")