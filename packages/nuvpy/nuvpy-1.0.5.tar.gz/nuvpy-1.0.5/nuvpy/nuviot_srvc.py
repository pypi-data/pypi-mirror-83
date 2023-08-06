import urllib3.request
import urllib.parse
import certifi
import requests
from requests.exceptions import HTTPError
       
class NuvIoTResponse:
    def __init__(self, result):
        self.rows = result['model']
        self.nextParititonKey = result['nextPartitionKey']
        self.nextRowKey = result['nextRowKey']
        self.pageSize = result['pageSize']
        self.hasMoreRecords = result['hasMoreRecords']

class NuvIoTRequest:
    def __init__(self, path):
        self.path = path
        self.pageSize = 50
        self.nextRowKey = None
        self.nextPartitionKey = None
        self.startDate = None
        self.endDate = None
                                      
def get(ctx, path, content_type = "", pageSize=50):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token, 'x-pagesize' : str(pageSize)}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token, 'x-pagesize' : str(pageSize)}
       
    if(content_type != ""):
        headers['Accept'] = content_type
   
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = ctx.url + path
    r = http.request("GET", url, headers=headers, preload_content=False)
    
    responseJSON = ''
    for chunk in r.stream(32):
        responseJSON += chunk.decode("utf-8")
        
    r.release_conn()
    
    if r.status > 299:
        print('Failed http call, response code: ' + str(r.status))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print(responseJSON)
        print('--------------------------------------------------------------------------------')
        print()
        return None
    
    return responseJSON

def post_file(ctx, path, file_name):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token}
    
    print(file_name)
    
    url = ctx.url + path
    
    print(file_name)
    
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
  
    
    with open(file_name, 'rb') as fp:
        file_data = fp.read()
        r = http.request( 'POST',url,
        fields={
           'filefield': ('model.bin', file_data),
        })
        
        responseJSON = ''
        for chunk in r.stream(32):
            responseJSON += chunk.decode("utf-8")
       
        r.release_conn()
         
        if r.status > 299:
            print('Failed http call, response code: ' + str(r.status))
            print('Url: ' + url)
            print('Headers: ' + str(headers))
            print(responseJSON)
            print('--------------------------------------------------------------------------------')
            print()
            return None

        return responseJSON


def download_file(ctx, path, dest, accept = ""):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token}
       
    if(accept != ""):
        headers['Accept'] = accept
    
    url = ctx.url + path
    
    chunk_size = 65536
        
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request("GET", url, headers=headers, preload_content=False)
 
    with open(dest, 'wb') as out:
        while True:
            data = r.read(65535)
            if not data:
                break
            
            out.write(data)

    r.release_conn()
 
    if r.status > 299:
        print('Failed http call, response code: ' + str(r.status))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print('--------------------------------------------------------------------------------')
        print()
        return None
   
def get_paged(ctx, rqst):
    if ctx.auth_type == 'user':
        headers={'Authorization': 'Bearer ' + ctx.auth_token, 'x-pagesize' : rqst.pageSize}
    else:
        headers={'Authorization': 'APIKey ' + ctx.client_id + ':' + ctx.client_token, 'x-pagesize' : rqst.pageSize}    

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = ctx.url + rqst.path;
    r = http.request("GET", url, headers=headers, preload_content=False)
    responseJSON = ''
    for chunk in r.stream(32):
        responseJSON += chunk.decode("utf-8")

    r.release_conn()
    
    if r.status > 299:
        print('Failed http call, response code: ' + str(r.status))
        print('Url: ' + url)
        print('Headers: ' + str(headers))
        print(responseJSON)
        print('--------------------------------------------------------------------------------')
        print()
        return None
      

    return responseJSON