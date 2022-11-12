import whois as whoisservice
import re
import dns.resolver
import requests

DOMAIN_REGEX = "^(((?!\-))(xn\-\-)?[a-z0-9\-_]{0,61}[a-z0-9]{1,1}\.)*(xn\-\-)?([a-z0-9\-]{1,61}|[a-z0-9\-]{1,30})\.[a-z]{2,}$"

def whois(domain):

    whoisResult =  whoisservice.whois(domain)
    if "update_date" in whoisResult.keys(): whoisResult.pop("updated_date")
    if "creation_date" in whoisResult.keys(): whoisResult.pop('creation_date')
    if "expiration_date" in whoisResult.keys(): whoisResult.pop('expiration_date')
    
    return whoisResult
    
def validateDomain(domain):
    result = re.match(DOMAIN_REGEX, domain)
    if result == False:
        raise ValueError("Given string is not a valid domain")
    else: return True

def parseOutput(output):
    pass

def resolveRecords(domain):
    a_record = None
    aaaa_record = None
    cname_record = None
    mx_record = None
    ns_record = None
    txt_record = None

    try:
       a_record = dns.resolver.resolve(domain, 'A').target
       aaaa_record = dns.resolver.resolve(domain, 'AAAA').target
       cname_record = dns.resolver.resolve(domain, 'CNAME').target
       mx_record = dns.resolver.resolve(domain, 'MX').target
       ns_record = dns.resolver.resolve(domain, 'NS').target
       txt_record = dns.resolver.resolve(domain, 'TXT').target
    except:
        pass
    
    return {
        "a": a_record,
        "aaaa": aaaa_record,
        "cname": cname_record,
        "mx": mx_record,
        "ns": ns_record,
        "txt": txt_record
    }
    
    
def resolveRecords(domain):
    result = {"A": [], "NS": [], "CNAME": [], "MX": [], "TXT": [], "AAAA": []}
    
    ids = [
        'NONE',
        'A',
        'NS',
        'CNAME',
        'MX',
        'TXT',
        'AAAA',
    ]
    
    for a in ids:
        try:
            answers = dns.resolver.query(domain, a)
            for rdata in answers:
                if rdata.to_text() == "None":
                    result[a] = "'none'"

                else:
                    result[a].append(rdata.to_text())
    
        except Exception as e:
             pass
    
    return result

def resolveLocation(domain):
    ipaddr = resolveRecords(domain)["A"][0]
    response = requests.get(f'https://ipapi.co/{ipaddr}/json/').json()
    
    return {
        "country": response.get("country_name"),
        "region": response.get("region"),
        "city": response.get("city")
    }

def run(domain):
    validateDomain(domain)
    
    return {
        "whois": whois(domain),
        "records": resolveRecords(domain),
        "ipaddrs": { "location": resolveLocation(domain) } 
    }