import requests, os
from manga import MangaDownload
from bs4 import BeautifulSoup
from time import sleep

CLEAR_CMD = 'cls'

if os.name == 'posix':
    CLEAR_CMD = "clear"

def checkIfMangaExistst(url) -> bool:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find('title').text
    return True if not "404" in title else False

def clearCmd():
    os.system(CLEAR_CMD)


clearCmd()        

print("Welcome to the MangaNelo downloader !\n")

# main while true loop

while True:

    print("Please enter a valid MangaNelo manga url. (it must be the url that show all chapters, and should not contain the word chapter in it. Ex: https://m.manganelo.com/manga-hj91929)")
    mangaUrl = input("> ")

    downloader = MangaDownload(mangaUrl)

    clearCmd()

    downloader.displayChaptersNames()

    print("\nPlease enter the index of the chapter (index are the ones with the white background)")
    print(f"Keywords:\n")
    print("ALL > to download everything")
    print("STOP > to confirm your choice")
    print("You can also use ranges. Ex: 20-30 -> will select the chapter 20 to chapter 30\n")

    # 2nd while True loop
    while True:
    
        while True:
            userInput = str(input("> "))
            
            if userInput.upper() == "ALL":
                print("Sucessfully adding every chapters\n")
                downloader.requestedChapters = downloader.chaptersInfos
                break
            
            elif userInput.upper() == "STOP":
                print("STOPPING...")
                sleep(1.3)
                break
            
            elif '-' in userInput:
                nb1 = None
                nb2 = None
                try:
                    nb1, nb2 = [int(i) for i in userInput.split('-')]
                except:
                    print(f"Wrong indexes make sure to enter a valid number between 1 and {downloader.chaptersCount}.")
                    continue
                
                if nb1 > downloader.chaptersCount or nb2 > downloader.chaptersCount:
                    print(f"Wrong indexes make sure to enter a valid number between 1 and {downloader.chaptersCount}.")
                    continue
                
                for i in range(nb1, nb2+1):
                    if i in downloader.requestedChaptersIndexes:
                        print(f"Chapter {i} is already selected.")
                        continue
                    
                    # i-1 because to dislpay we use i+1 so i-1 is to get to the list
                    downloader.requestedChapters.append(downloader.chaptersInfos[i-1])
                    downloader.requestedChaptersIndexes.append(i)
                    print(f"Sucessfully added chapter {i}")
            else:
                try:
                    userInput = int(userInput)
                    if userInput in downloader.requestedChaptersIndexes:
                        print(f"Chapter {userInput} is already selected.")
                        continue
                    
                    downloader.requestedChapters.append(downloader.chaptersInfos[userInput-1])
                    downloader.requestedChaptersIndexes.append(userInput)
                    print(f"Sucessfully added chapter {userInput}.\n")
                except:
                    print(f"Wrong indexes make sure to enter a valid number between 1 and {downloader.chaptersCount}.")
                    continue


        clearCmd()

        print("Please confirm that you want to download all of theses chapters:\n")
        downloader.recapRequested()
        confirm = str(input('\nConfirm ? Y/N')).upper()

        if confirm == "N":
            continue
        break
    
    downloader.start()

    print("Would you like to download again ?")
    confirm = str(input('Confirm ? Y/N')).upper()
    if confirm == "Y":
        continue
    break
