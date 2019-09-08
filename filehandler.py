import os

def make_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)

def make_file(folder, file_name):
    if file_name not in os.listdir(folder):
        with open(folder+"/"+file_name, 'w') as file:
            file.write('')

def write_to_file(filepath, data):
    try:
        with open(filepath, 'w') as file_opened:
            try:
                    for link in data:
                            file_opened.write(link+"\n")
            except:
                    pass
            file_opened.close()
    except:
        pass

def read_from_file(filepath):
    result = set()
    with open(filepath,'r') as file_opened:
        for link in file_opened:
            result.add(link.replace("\n",''))
        return (result)

# def delete_from_file(filepath, data):
#     file_data = open(filepath,'r')
#     with open(filepath, 'w') as file_opened:
#         for link in file_data:
#             if(link != data):
#                 file_opened.write(link)
#         file_opened.close()

def queue_to_file(filepath, queue):
    write_to_file(filepath, set(queue.queue))

