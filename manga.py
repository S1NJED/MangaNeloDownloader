import requests
import os
import re
from bs4 import BeautifulSoup
from bs4.element import Tag
from colorama import Fore, Style, Back, init
from typing import Union
from time import time, sleep
from global_vars import *

init(autoreset=True)


if not os.path.isabs(DOWNLOAD_PATH):
    DOWNLOAD_PATH = os.path.join(os.getcwd(), DOWNLOAD_PATH)

if not os.path.exists(DOWNLOAD_PATH):
    raise OSError("Your DOWNLOAD_PATH is incorrect. Make sure to enter a valid one")


class MangaDownload:
    
    def __init__(self, mangaUrl):
        self.mangaUrl = mangaUrl
        self.HOST = ''
        self.chaptersCount = 0
        self.mangaName = ""
        self.chaptersInfos = []
        self.requestedChapters = []
        self.requestedChaptersIndexes = []
        self.hostUrl = ""
        self.HEADERS = {
            'Host': None,
            'User-Agent': USER_AGENT,
            'Accept': 'image/avif,image/webp,*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://chapmanganelo.com/'
        }
        
        self.createChaptersList()
        self.getHostUrl()
        

    def getAllChapterImagesUrls(self, chapter: Union[str, int]) -> list:
        chapterUrl = chapter
        if isinstance(chapter, int):
            if chapter > self.chaptersCount-1 or chapter < 0:
                raise ValueError(f"chapter index must be between 1 and {self.chaptersCount-1}")
            chapterUrl = self.chaptersInfos[chapter-1].get('url')
        
        
        req = requests.get(chapterUrl)
        soup = BeautifulSoup(req.text, 'html.parser')
        img_elems = soup.find_all('img', class_="reader-content")
        return [elem.attrs.get('src') for elem in img_elems]
            
        
    def downloadImage(self, imageUrl, imagePath) -> bool:
        if self.HEADERS.get('Host') is None:
            return print("The 'Host' header is set to `None` make sure to call getHostUrl() method before")
        
        while True:
            
            try:
                req = requests.get(imageUrl, headers=self.HEADERS, timeout=(5, 30))
                
                if req.status_code != 200:
                    print("Couldn't retrieve image.")
                    return False

                with open(imagePath, 'wb') as image:
                    image.write(req.content)
                
                return True
            except:
                print("Cannot download images, trying again in 2 seconds...")
                sleep(2)
    
    
    def createChaptersList(self) -> None:
        req = requests.get(self.mangaUrl)
        soup = BeautifulSoup(req.text, 'html.parser')
        chapters = soup.find('ul', id="row-content-chapter").find_all('li')
        self.chaptersCount = len(chapters)
        
        # setting mangaName
        self.mangaName = soup.find('div', class_="story-info-right").find('h1').text
        
        chapter: Tag
        for chapter in chapters[::-1]:
            obj = {
                "name": re.sub(r'[\\/:*?"<>|]', '', chapter.find('a').text).rstrip('.'),
                "url": chapter.find('a').attrs.get('href')
            }
            self.chaptersInfos.append( obj )
    
    
    def displayChaptersNames(self) -> None:
        for i, chapter in enumerate(self.chaptersInfos):
            print(f"[{Back.LIGHTWHITE_EX}{Fore.BLACK}{i+1}{Style.RESET_ALL}] {chapter.get('name')}")


    def checkMangaUrl(self) -> bool:
        return False if "chapter" in self.mangaUrl else True


    def getHostUrl(self):
        # https://m.manganelo.com/manga-hj91929
        # https://chapmanganelo.com/manga-hj91929/chapter-1
        
        url = self.mangaUrl
        if 'm.' in self.mangaUrl:
            url = self.mangaUrl.replace("m.manganelo", "chapmanganelo") 
     
        req = requests.get(url + "/chapter-1")
        soup = BeautifulSoup(req.text, 'html.parser')
        url = soup.find('img', class_="reader-content").attrs.get('src')
        self.hostUrl = url.replace('https://', '').split('/')[0]
        self.HEADERS['Host'] = self.hostUrl
    

    def recapRequested(self):
        for i, chapter in enumerate(self.requestedChapters):
            print(f"[{Back.LIGHTWHITE_EX}{Fore.BLACK}{i+1}{Style.RESET_ALL}] {chapter.get('name')}")
    

    def start(self) -> None:
        startTime = time()
        imagesUrlLenght = 0
        downloadedChaptersCount = 0
        downloadedImagesCount = 0
        
        for chapterIndex, chapter in enumerate(self.requestedChapters):

            chapterFolderPath = os.path.join(DOWNLOAD_PATH, self.mangaName, chapter.get('name'))
            
            if not os.path.exists(chapterFolderPath):
                os.makedirs(chapterFolderPath, exist_ok=True)
            
            
            url = chapter.get('url')
            imagesUrls = self.getAllChapterImagesUrls(url)       
            imagesUrlLenght = len(imagesUrls)
            
            print(f"\n========= {self.mangaName}: CHAPTER {Style.BRIGHT}{chapterIndex+1}{Style.RESET_ALL} / {Back.YELLOW}{Fore.BLACK}{len(self.requestedChapters)}{Style.RESET_ALL} ===================")
            
            print(f'Starting to download {len(imagesUrls)} images ...\n')
            
            for imageIndex, imageUrl in enumerate(imagesUrls):
                imagePath = os.path.join(chapterFolderPath, f"{imageIndex+1}.jpg")
                res = self.downloadImage(imageUrl, imagePath)

                if not res:
                    print("Couldn't download image ...")
                    continue
                
                print(f"[Chapter {Back.WHITE}{Fore.BLACK}{chapterIndex}{Style.RESET_ALL}] Sucessfully downloaded {Style.BRIGHT}{imageIndex+1}.jpg {Style.RESET_ALL} / {imagesUrlLenght}")

                sleep(MS)
                downloadedImagesCount += 1
            
            downloadedChaptersCount += 1
        
        # substract waiting time caused by the sleep method
        endTime = (time() - startTime) - (imagesUrlLenght * MS)
        
        print(f"\n{Back.RED}{Style.BRIGHT}{Fore.WHITE} ===== DOWNLOAD HAS ENDED IN {endTime} seconds ====== {Style.RESET_ALL}\n\n".center(50))
        print(f"-> {downloadedChaptersCount} chapters downloaded.")
        print(f"-> {downloadedImagesCount} images downloaded.")
        print(f"\nYour downloaded images are here --> {os.path.join(os.getcwd(), DOWNLOAD_PATH, self.mangaName)}")



if __name__ == '__main__':
    dl = MangaDownload("https://chapmanganelo.com/manga-ad115397")
    print(dl.hostUrl)