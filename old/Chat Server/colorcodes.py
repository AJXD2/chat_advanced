import colorama
colorama.init()
string=input()
print(string)
color_codes = {'&a': colorama.Fore.LIGHTGREEN_EX, '&4': colorama.Fore.RED}

for char in color_codes:
    string = string.replace(char, color_codes[char])
print(string)