import os
from pcloud import PyCloud

def go(dname):
    #print(dname)
    contents=os.listdir(dname)
    print("Directories")
    for i in contents:
        if os.path.isdir(dname+"\\"+i):
            print(i)
    print("Files")
    for i in contents:
        if not os.path.isdir(dname+"\\"+i):
            print(i)

      
def p():
    pc = PyCloud('grant@isijingi.co.za', 'SnUFuR6Uz54xssQMOEVr', endpoint="eapi")
  #  pc.renamefolder(folderid=5043748315, toname="JennyOne")
    documents=pc.listfolder(path="/Jenny/JennyOne/JennyOneOne", recursive=0)
    print(documents)
    folder_name=documents["metadata"]["name"]
    print(folder_name)
    folder_contents=[]
    folder_id=[]
    for i in documents["metadata"]["contents"]:
        folder_contents.append(i["name"])
        try:
            folder_id.append(i["folderid"])
        except:
            folder_id.append("file")
        print(i["name"]," ",folder_id[-1])
    pc.logout()

def test(dname):
    for (a,b,c) in os.walk(dname):
        print("a ",a)
        print("b ",b)
        print("c ",c)
    
def contribute(lpath, rpath):
    pc = PyCloud('grant@isijingi.co.za', 'SnUFuR6Uz54xssQMOEVr', endpoint="eapi")
    print ("PATHS")
    print (lpath)
    print (rpath)
    print ("=====")
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
            print("Processing file ",fname)
            if fname not in list_of_files:
                print("File not found on PCloud", fname)
                print("Checking path, filename", ppath+'/'+fname, curr+'\\'+fname)
                uf=pc.uploadfile(files=[curr+'\\'+fname], path=ppath)
                if uf["result"]!=0:
                    print(uf["result"], "File upload failed")
                
      
            
        
    pc.logout()
                             
       # for check_folder in sub:
            
    
    #read folders in lpath
    #check if folder exists in rpath #if no check for rename, if not rename copy
        #if exists read folders, repeat
    

    
