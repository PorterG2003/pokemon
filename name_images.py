import os

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        new_filename = filename.split('.')[0]
        new_filename = new_filename.capitalize()
        new_filename = new_filename.split('-')[0]
        new_filename += '.' + filename.split('.')[1]

        # Rename the file
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

images_directory = './images'
rename_files_in_directory(images_directory)