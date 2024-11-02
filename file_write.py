import os 
def file_write(file_name):
    #create the parent directories if they dont exist
    dir_name=os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(file_name, 'a') as f:
        while True:
            text = input("Enter an text to overwrite the file or enter Exit:")
            if text.lower() == "exit":
                break
            print("Added Text:",text)
            f.write(text+"\n")

file_write("D:/python/file_write.txt")

