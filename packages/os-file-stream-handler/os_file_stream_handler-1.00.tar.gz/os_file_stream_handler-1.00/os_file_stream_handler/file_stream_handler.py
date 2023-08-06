####################################################
# this is just a simple file stream handling script#
####################################################


# will read a file from a path
def read_file(file_path, drop_new_lines=False):
    with open(file_path, 'r') as fd:
        reader = fd.readlines()
    lines = list(reader)
    if drop_new_lines:
        for i in range(0, len(lines)):
            lines[i] = lines[i].replace('\n', '')
    return lines


# will write a content to a file (str or array of strings)
def write_file(file_path, content):
    with open(file_path, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_path)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        if isinstance(content, str):
            f.write(content)
        if isinstance(content, list):
            for line in content:
                if not str(line).endswith('\n'):
                    line += '\n'
                f.write(line)


# will replace a bunch of chars in a file
def replace_text_in_file(file_src, file_dst, old_expression, new_expression):
    lines = read_file(file_src, drop_new_lines=True)

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for line in lines:
            if old_expression in line:
                line = line.replace(old_expression, new_expression)
            f.write(f'{line}\n')


# will add text below some other text in a file
def append_text_below_line_in_file(file_src, file_dst, below_line, new_expression):
    lines = read_file(file_src, drop_new_lines=True)

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for i in range(0, len(lines)):
            f.write(f'{lines[i]}\n')
            if below_line in lines[i]:
                f.write(f'{new_expression}\n')


# will add text above some other text in a file
def append_text_above_line_in_file(file_src, file_dst, above_line, new_expression):
    lines = read_file(file_src, drop_new_lines=True)

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for i in range(0, len(lines)):
            if above_line in lines[i]:
                f.write(f'{new_expression}\n')
            f.write(f'{lines[i]}\n')
