import os
import shutil

copied_files = {}

def file_name_filter(source_folder, filter_list, filter_type):
    if not os.path.exists(source_folder):
        raise ValueError("Source folder does not exist")

    if filter_type not in ['in', 'out']:
        raise ValueError("Invalid filter type")
    
    copied_files.clear()

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.startswith('.') or file.startswith('_'):
                continue

            filename_matches = any(file == filename for filename in filter_list)
            should_remove = (filter_type == 'in' and not filename_matches) \
                    or (filter_type == 'out' and filename_matches)

            if should_remove:
                os.remove(file_path)
            else:
                if file in copied_files:
                    copied_files[file] += 1
                else:
                    copied_files[file] = 1
    return copied_files


def file_ext_filter(source_folder, filter_list, filter_type, dest_folder):
    if not os.path.exists(source_folder):
        raise ValueError("Source folder does not exist")

    if filter_type not in ['in', 'out']:
        raise ValueError("Invalid filter type")
    
    copied_files.clear()

    for root, dirs, files in os.walk(source_folder):
        rel_path = os.path.relpath(root, source_folder)
        dest_path = os.path.join(dest_folder, rel_path)

        for file in files:
            file_path = os.path.join(root, file)

            extension_matches = any(file.endswith(ext) for ext in filter_list)
            if file.startswith('.') or file.startswith('_'):
                continue
            should_copy = (filter_type == 'in' and extension_matches) \
                          or (filter_type == 'out' and not extension_matches)

            if should_copy:
                os.makedirs(dest_path, exist_ok=True)
                dest_file_path = os.path.join(dest_path, file)
                if file in copied_files:
                    copied_files[file] += 1
                else:
                    copied_files[file] = 1
                shutil.copy(file_path, dest_file_path)
    return copied_files
