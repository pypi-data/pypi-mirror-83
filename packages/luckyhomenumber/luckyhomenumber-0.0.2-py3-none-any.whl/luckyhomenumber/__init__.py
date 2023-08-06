from luckyhomenumber.homenumber import Homenumber

print(f"Please try to create your home number object e.g. hm = Homenumber('1488/186')")
print('Then you can use hm.is_good_address() to check if your home address number is lucky')

x = input('Please input your homenumber e.g. 1488/186: ')
x = str(x)
hm = Homenumber(x)
hm.is_good_address()