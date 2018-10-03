def parse(file):
    file_contents_by_row = []
    last_line = None
    with open(file) as sample_file:
        for line in sample_file:
            if not last_line:
                row = line.split(",")
                file_contents_by_row.append(row)

    print(file_contents_by_row)
    return file_contents_by_row
