# "Bugs"
If a file is deleted after the program starts, but before the file is processed, the program crashes:
```
Processing file  dripping tap v3.m2t.aix2 142477
Traceback (most recent call last):
  File "C:\Users\g.hillebrand\Documents\Programming\Python\Contribute\ContributeV0.1.py", line 85, in <module>
    contribute(left,right)
  File "C:\Users\g.hillebrand\Documents\Programming\Python\Contribute\ContributeV0.1.py", line 48, in contribute
    fsize=os.path.getsize(curr+"\\"+fname)
  File "C:\Program Files\Python38\lib\genericpath.py", line 50, in getsize
    return os.stat(filename).st_size
FileNotFoundError: [WinError 2] The system cannot find the file specified: 'C:\\Users\\g.hillebrand\\Videos\\Editted Clips\\dripping tap v3.m2t.vix'
```
# Feature Requests
- preserve the local file metadata on the pCloud copy - particularly creation and modification date


# Security
- don't include pswd on the public repo? (I don't mind pasting it in after download)

# Info Stuff
- print file size in MiB (with bytes in brackets - it's nice for comparisons)
- print out the estimated time left for the copy (Based on average upload speed so far)
- print a copied/ already present message on upload
