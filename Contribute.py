import time
import os
from pcloud import PyCloud

  
def contribute(lpath, rpath, password):
    tstart: float = time.perf_counter()
    if ":" in rpath:
        rpath=rpath[rpath.find(":")+1:]
    if "\\" in rpath:
        rpath=rpath.replace("\\","/")
    
    pc = PyCloud('grant@isijingi.co.za', password, endpoint="eapi")
    print ("PATHS")
    print ("Local path: ",lpath)
    print ("PCloud path: ",rpath)
    print ("*")
    # get size of stuff to be potentially uploaded
    total_size=0
    for(a,b,c) in os.walk(lpath):
        for d in c:
            total_size+=os.path.getsize(a+"\\"+d)
    print(f"Size of source {total_size/1048576:0.4f} MiB")
            
    tcopyActualStart:float = time.perf_counter()
    size_processed=0
    for(curr, sub, file) in os.walk(lpath):
        print("Processing folder ", curr)
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
        for i in lf["metadata"]["contents"]: # pcloud folder
            if not i["isfolder"]:
                list_of_files.append(i["name"])
                dic_of_sizes[i["name"]]=i["size"]
        
        
        tcopyStart:float = time.perf_counter()
        

        for fname in file: # windows machine
            try:
                fsize=os.path.getsize(curr+"\\"+fname) # in case the file was deleted since starting os.walk
            except:
                print("Unable to access file ", fname, "file not processed.")
            else:
                print(f"  Processing file {fname} Size {fsize/1048576:0.4f} MiB ({fsize} bytes)", end="")
                if fname in list_of_files and fsize!=dic_of_sizes[fname]:  # if file has changed size rename file on pcloud
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
                if fname not in list_of_files or fsize!=dic_of_sizes[fname]: # if file not on pcloud upload
                    create_time = str(int(os.path.getctime(curr+"\\"+fname)))
                    modify_time = str(int(os.path.getmtime(curr+"\\"+fname)))
                    uf=pc.uploadfile(files=[curr+'\\'+fname], path=ppath, nopartial="1", renameifexists="1", ctime=create_time, mtime=modify_time)
                    if uf["result"]!=0:
                        print(uf["result"], "File upload failed", fname)
                    print("  -- uploaded successfully.", end="")
                else:
                    print("  -- already on PCloud, not copied.", end="")
                size_processed+=fsize
            tcopyInterim:float = time.perf_counter()
            time_sofar=tcopyInterim-tcopyActualStart
            file_size_remaining=total_size-size_processed
            if size_processed !=0:
                upload_speed=time_sofar/size_processed
                print(f" Time remaining {(upload_speed*file_size_remaining)/60:0.4f} minutes.")
               # print(f"{   size_processed/1048576:0.4f} MiB processed in {time_sofar/60:0.4f} minutes. {file_size_remaining/1048576:0.4f} MiB left. Anticipated time to go {(upload_speed*file_size_remaining)/60:0.4f} minutes.")
            else:
               # print(f"{   size_processed/1048576:0.4f} MiB processed in {time_sofar/60:0.4f} minutes. {file_size_remaining/1048576:0.4f} MiB left. Anticipated time to go * unknown * minutes.")
                print(" Unknown time remaining.")
        print()
        tcopyEnd:float = time.perf_counter()
        
    print(f"Total time: {tcopyEnd - tstart:0.4f}, copying time = {tcopyEnd - tcopyStart:0.4f}")
                
        
    pc.logout()
                             
   

    
