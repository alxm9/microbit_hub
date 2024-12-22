import os
import microfs

def create(connections_dict,givendir):
    current_dir = os.listdir(givendir)
    dir_num = 0
    for i in current_dir:
        if 'workspace_' in i:
            dir_num = int(i.split('_',1)[1])+1 if int(i.split('_',1)[1]) >= dir_num else dir_num
    for port, datalist in connections_dict.items():
        os.makedirs(f"{givendir}/workspace_{dir_num}/{datalist[1]}/", exist_ok=True)

    return f'workspace_{dir_num}'
    

def flash_all(connections_dict,workspace): 
    current_dir = os.listdir(workspace)
    current_ids = [datalist[1] for port, datalist in connections_dict.items()]
    id_serial_dict = {datalist[1]:datalist[2] for port, datalist in connections_dict.items()}

    # check if all ids match dirs
    for id in current_ids:
        if id not in current_dir:
            return ('missing_dir',id)
    
    # check if all dirs match ids
    for dir in current_dir:
        if dir not in current_ids:
            return ('missing_id',dir)
    
    # flash files on microbits
    for dir in current_dir:
        microbit_files = os.listdir(f'{workspace}/{dir}/')
        for file in microbit_files:
            print(f'{workspace}/{dir}/{file} to {id_serial_dict[dir]}')
            microfs.put(f'{workspace}/{dir}/{file}',serial=id_serial_dict[dir])

    return ('success',)
