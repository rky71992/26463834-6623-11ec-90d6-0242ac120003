import hashlib
import logging
from constants import *

def md5_hash(string_to_hash):
    string_to_hash = string_to_hash + HASH_SALT
    return hashlib.md5(string_to_hash.encode("utf-8")).hexdigest()

def format_mail_services_opted(services_list):
    services_opted = []
    new_services_requested = []
    
    if not type(services_list,list):
        logging.debug("Services is not list. returning empty list")
        return services_opted, new_services_requested
    
    for service in services_list:
        temp_dict = {}
        service_id = str(service.get("service_id","")).strip()
        service_key = str(service.get("service_key","")).strip()
        
        if (not service_id) or (not service_key):
            logging.debug("Empty service_id/service_key. Skipping this key")
            continue
        
        if service_id in SUPPORTED_MAIL_SERVICES_IDS:
            temp_dict["service_id"] = service_id
            temp_dict["service_key"] = service_key
            services_opted.append(temp_dict)
        else:
            new_services_requested.append(service_id)
    
    return services_opted, new_services_requested
            
            
        
            