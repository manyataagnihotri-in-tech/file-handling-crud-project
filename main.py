# CRUD - File handeling
# Create
# Read
# Update
# Delete
#Create
# import os
# from pathlib import Path

# def create_file():
#     filename = input("enter your filename: ")
#     path = Path(filename)
#     if path.exists():
#         print('file already exists')
#     else:
#         with open(filename,'w')as file:
#             content = input('enter your content')
#             file.write(content)
#             print('file created')

# def read_file():
#     filename = input('enter your filename: ')
#     path = Path(filename)

#     if path.exists():
#         with open(filename,'r')as file:
#             print(file.read())
#     else:
#         print("file does not exists")


# def update_file():
#     filename = input('enter your filename: ')
#     path = Path(filename)

#     if path.exists():
#         with open(filename,'a')as file:
#             content = input('enter new content: ')
#             file.write(content)
#             print('file updated sucessfully')
#     else:
#         print("file does not exist")


# def delete_file():
#     filename = input('enter your filename: ')
#     path = Path (filename)

#     if path.exists():
#         os.remove(filename)
#         print('file is deleted')
#     else:
#         print('file does not exist')



# def rename_file():
#     old_name = input("enter your old file name")
    
#     path = Path(old_name)
#     if path.exists():
#         new_name = input("enter new name: ")
#         os.rename(old_name,new_name)
#         print("file name changed")
#     else:
#         print("file does not exist")

# def create_folder():
#     foldername = input("enter the folder name")
#     path = Path(foldername)

#     if path.exists():
#         print("folder already exists")
#     else:
#         os.mkdir(foldername)
#         print("folder is created")



# def delete_folder():
#     foldername = input('Enter name of folder: ')
#     path = Path(foldername)

#     if path.exists():
#         os.rmdir(foldername)
#         print('Folder Deleted')
    
#     else:
#         print('folder does not exists')


# while True:
#     print("----menu-----")
#     print('press 0 for exiting...')
#     print("press 1 for creating a file")
#     print("press 2 for reading a file")
#     print("press 3 for updating a file")
#     print("press 4 for deleting a file")
#     print("press 5 for Rename a file")
#     print("press 6 for creating a folder")
#     print("press 7 for deleting a folder")
#     choice = int(input('enter your choice: '))

#     if choice == 0:
#         print('Exiting')
#         break

#     elif choice == 1:
#         create_file()

#     elif choice == 2:
#         read_file()

#     elif choice == 3:
#         update_file()

#     elif choice == 4:
#         delete_file()

#     elif choice == 5:
#         rename_file()

#     elif choice == 6:
#         create_folder()

#     elif choice == 7:
#         delete_folder()



# d ={}
# for i in nums:
#     if i not in d:
#         d[i] = 1
#     else:
#         d[i] += 1

# for i in d.values():
#     if  i % 2 != 0:
#         return False
#     else:
#         return True

