import os
from pcloud import PyCloud
  
def contributeold(lpath, rpath):
    pc = PyCloud('grant@isijingi.co.za', 'SnUFuR6Uz54xssQMOEVr', endpoint="eapi")
    print ("PATHS")
    print ("Local path: ",lpath)
    print ("PCloud path: ",rpath)
    print ("====================")
    for(curr, sub, file) in os.walk(lpath):
        print("processing ", curr)
        ppath_=curr.replace(lpath,"")
        ppath=ppath_.replace("\\","/")
        ppath=rpath+ppath
 #       print("ppath",ppath)
        lf=pc.listfolder(path=ppath)
        if lf["result"]==0:
            pass
  #          print ("Folder found on PCloud", ppath)
        else:
            print (lf["result"], "Folder not found on PCloud", ppath)
            folder_name=ppath[ppath.rfind("/")+1:]
 #           print ("folder name", folder_name)
            cf=pc.createfolder(path=ppath, name=folder_name)
            if cf["result"]==0:
                print("folder created", ppath)
                lf=pc.listfolder(path=ppath)
            else:
                print(cf["result"], " unable to create folder ",ppath)
        list_of_files=[]
        for i in lf["metadata"]["contents"]:
            if not i["isfolder"]:
                list_of_files.append(i["name"])
        
        for fname in file:
    #        print("Processing file ",fname)
            if fname not in list_of_files:
    #            print("File not found on PCloud", fname)
    #            print("Checking path, filename", ppath+'/'+fname, curr+'\\'+fname)
                uf=pc.uploadfile(files=[curr+'\\'+fname], path=ppath)
                if uf["result"]!=0:
                    print(uf["result"], "File upload failed")
                
          
        
    pc.logout()

   # import os
#gh 
import time
#from pcloud import PyCloud
  
def contribute(lpath, rpath):
    tstart: float = time.perf_counter()
    if ":" in rpath:
        rpath=rpath[rpath.find(":")+1:]
    if "\\" in rpath:
        rpath=rpath.replace("\\","/")
    
    pc = PyCloud('grant@isijingi.co.za', 'SnUFuR6Uz54xssQMOEVr', endpoint="eapi")
    print ("PATHS")
    print ("Local path: ",lpath)
    print ("PCloud path: ",rpath)
    print ("*")
    for(curr, sub, file) in os.walk(lpath):
        print("processing ", curr)
        ppath_=curr.replace(lpath,"")
        ppath=ppath_.replace("\\","/")
        ppath=rpath+ppath
 #       print("ppath",ppath)
        lf=pc.listfolder(path=ppath)
        if lf["result"]==0:
            pass
  #          print ("Folder found on PCloud", ppath)
        else:
            print (lf["result"], "Folder not found on PCloud", ppath)
            folder_name=ppath[ppath.rfind("/")+1:]
 #           print ("folder name", folder_name)
            cf=pc.createfolder(path=ppath, name=folder_name)
            if cf["result"]==0:
                print("folder created", ppath)
                lf=pc.listfolder(path=ppath)
            else:
                print(cf["result"], " unable to create folder ",ppath)
        list_of_files=[]
        dic_of_sizes={}
        for i in lf["metadata"]["contents"]:
            if not i["isfolder"]:
                list_of_files.append(i["name"])
                dic_of_sizes[i["name"]]=i["size"]
        
        #gh
        tcopyStart:float = time.perf_counter()
        for fname in file:   
            fsize=os.path.getsize(curr+"\\"+fname)
            print("Processing file ",fname, fsize)
            if fname in list_of_files and fsize!=dic_of_sizes[fname]:
                counter=1
                fnameold=fname[:fname.rfind(".")]+"old ("+str(counter)+")"+fname[fname.rfind("."):]
                while fnameold in list_of_files:
                    counter+=1
                 #   fnameold=fname+"old ("+str(counter)+")"
                    fnameold=fname[:fname.rfind(".")]+"old ("+str(counter)+")"+fname[fname.rfind("."):]
                rf=pc.renamefile(path=ppath+"/"+fname, toname=fnameold)
                if rf["result"]==0:
                    print(fname, " already exists. Renamed to ", fnameold)
                else:
                    print(rf["result"], "Unable to rename ",fname, " to ", fnameold)
            if fname not in list_of_files or fsize!=dic_of_sizes[fname]:
    #            print("File not found on PCloud", fname)
    #            print("Checking path, filename", ppath+'/'+fname, curr+'\\'+fname)
                uf=pc.uploadfile(files=[curr+'\\'+fname], path=ppath, nopartial="1", renameifexists="1")
                if uf["result"]!=0:
                    print(uf["result"], "File upload failed", fname)
                #GH progress trail
           #     else:
           #         print(".",end="")
       #     else:
       #         print("P size: ", dic_of_sizes[fname])
        #gh
        print()
        tcopyEnd:float = time.perf_counter()
        
        print(f"Total time: {tcopyEnd - tstart:0.4f}, copying time = {tcopyEnd - tcopyStart:0.4f}")
                
        
    pc.logout()
                             
   

    
