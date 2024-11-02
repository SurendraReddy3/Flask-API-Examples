#reading an JSON file

import json
import os 
def read_json(file):
    #if path not exists it will create an path
    dir_name=os.path.dirname(file)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


    """  Reading an JSON file
    """
    try:              #opening file in read format
        with open(file,'r') as Json: 
            data=json.load(Json)
        return data

    except Exception as e:
        print("please upload valid JSON file")

def write_json(file,data):

    """  Writing an JSON file
    """
    with open(file,"w") as wr:
        json.dump(data,wr,indent=4)
    return file

# error was raising
def append_data(file,new_data):
    """  Appending New data into an Existing file
    """
    existing_file=read_json(file)
    if existing_file is not None and isinstance(existing_file,dict):
        existing_file.update(new_data)
        write_json(file,existing_file)
    elif existing_file is not None and isinstance(existing_file,list):
        existing_file.append(new_data)
        write_json(file,existing_file)
        
    else:
        write_json(file,new_data)
        
def main():
    
    print("Writing data in JSON file")
    data={"Company":"G_Creations","MNC or Start_UP":"Start_UP","Branches":("Vijayawada","Guntur"),
          "Year of Establishment":2024,
          "Contact_Details":{"VIjayawada":100,
                             "Guntur":200}}
    write_json("C:\Tech_job\student1.json",data)


    data={"name":"Voonna Gowri Ganesh",
          "age":21}
    append_data("C:\Tech_job\student1.json",data)
    path="C:\Tech_job\student1.json"
    data=read_json(path)
    print(data)
     

    # data={"Name":"Gannu",
    #       "Age":20,
    #       "Gender":"Male"}
    # append_data(path,data)

    # print("After appending the data :")

    # print(read_json(path))
    # print("Again")
    # data={"Name1":"Gannu",
    #       "Age 1":20,
    #       "Gender":"Male"}
    # append_data(path,data)
    # print(read_json(path))
 

if __name__=="__main__":
    main()
    

