import re

types = '.ico, .jpg, .jpeg, .png, .gif, .svg'
file_extentions = re.findall(r'[\w\.-]+.[\w\.-]+', types)
for fe in file_extentions:
    print(fe)
