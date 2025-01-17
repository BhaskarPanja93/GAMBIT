def format_bytes(size_in_bytes):
    if size_in_bytes == 0:
        return "0B"

    units = ["B", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    power = 0
    while size_in_bytes >= 1024 and power < len(units) - 1:
        size_in_bytes /= 1024
        power += 1

    return f"{size_in_bytes:.2f}{units[power]}"

print(format_bytes(1215616142134))