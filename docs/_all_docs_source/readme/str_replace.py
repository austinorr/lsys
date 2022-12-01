def str_replace(filepath, replace_content, replace_with):

    with open(filepath, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if replace_content in line:
            lines[i] = line.replace(replace_content, replace_with)

    with open(filepath, "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="String Replacer that works on files.")
    parser.add_argument("filename")
    parser.add_argument("-f", "--find")
    parser.add_argument("-r", "--replace")

    args = parser.parse_args()

    str_replace(args.filename, args.find, args.replace)

    print(args)
