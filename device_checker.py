import csv

# ['serial number', 'assigned id']
def check_devices(connections_dict):
    for _, datalist in connections_dict.items():
        unique_id = csv_handler(datalist[0])
        datalist.append(unique_id)
    return connections_dict
    
def csv_handler(serial_number):
    with open('devices.csv', mode="a+",newline='') as csvfile:
        reader, writer = csv.reader(csvfile), csv.writer(csvfile)
        csvfile.seek(0)
        for row in reader:
            if serial_number == row[0]:
                return row[1] #return assigned id

        #if not found
        writer.writerow([serial_number,f"Rename_me_{serial_number[16:-26]}"])
        return f"Rename_me_{serial_number[16:-26]}"

def rename_device(serial_number, user_input):
    stored_rows = []
    with open('devices.csv', mode="r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for sn, id in reader:
            templist = [sn]
            templist.append(user_input if sn == serial_number else id)
            stored_rows.append(templist)
    with open('devices.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in stored_rows:
            writer.writerow(row)

# rename_device('ser1', '3')