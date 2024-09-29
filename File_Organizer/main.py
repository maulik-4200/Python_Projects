import os
import shutil

if __name__ == '__main__':
    print("------ Welcome to File Organizer by Maulik ------")
    while True:
        folder = input("Enter Folder Path (e to exit): ")
        
        if folder == 'e':
            print("File Organizer is closing...")
            break
        
        if os.path.exists(folder):
            if os.path.isdir(folder):
                print("Started organizing the folder...")
                
                files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
                        
                for file in files:
                    extension = os.path.splitext(file)[1]
                    if not os.path.exists(os.path.join(folder, f'{extension[1:]}')):
                        os.mkdir(os.path.join(folder, f'{extension[1:]}'))
                    
                    shutil.move(os.path.join(folder,file), os.path.join(folder, f'{extension[1:]}', file))
                print("All Files are organized")
            else:
                print("Provide Path of a Folder")
        else:
            print("Folder doesn't exists")
