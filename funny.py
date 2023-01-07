import random
import colorama

errors = ["Memory Full", "Invalid Syntax", "API request aborted", "API not found", "Session server not found"]
colorama.init(autoreset=True)
while True:
    print(f'{colorama.Fore.RED}ERROR: {errors[random.randint(0, 4)]}')