import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# 크롬 드라이버 연결
driver = webdriver.Chrome()
# 멜론 웹 페이지 접근
driver.get('https://www.melon.com/chart/index.htm')
driver.implicitly_wait(10)

# 각종 리스트
titles = []  # 제목
artists = [] # 아티스트
lyrics = [] # 가사
genres = [] # 장르

#  음악 정보 크롤링 함수
def craw_lyrics(n):
    # 가사 크롤링
    lyric = driver.find_elements_by_class_name('lyric')
    driver.implicitly_wait(10)
    tmp = []
    # 가사 없는 노래 제거
    if lyric:
        tmp = lyric[0].text.split('\n')
        # 공백 제거
        tmp = list(filter(None, tmp))
        # 영어 제거
        tmp = list(filter(lambda i: i.upper() == i.lower(), tmp))

        lyrics.append(' '.join(tmp)) # 다시 합침
    else:
        return

    # 제목 크롤링
    title = driver.find_element_by_class_name('song_name')
    titles.append(title.text)


    # 아티스트 크롤링
    artist = driver.find_element_by_class_name('artist_name')
    artists.append(artist.get_attribute('title'))

    # 장르 크롤링
    genre = driver.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]')
    genres.append(genre.text)

    print(titles)
    print(artists)
    print(lyrics)
    print(genres)


# data-song-no를 모으는 함수
# 크롤링하는 동안 로딩이 안되는 오류 현상 제거
def collect_no():
    song_num = []
    try:
        tr = driver.find_elements_by_xpath('//tbody/tr//input')
        for i in tr:
            song_num.append(i.get_attribute('value'))
        return song_num
    except StaleElementReferenceException:
        driver.refresh()
        tr = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//tbody/tr//input'))
        )
        tr = driver.find_elements_by_xpath('//tbody/tr//input')
        for i in tr:
            song_num.append(i.get_attribute('value'))
        return song_num


# 곡 상세 페이지 접근 함수
def access_detail(song_num, n):
    for i in range(50):
        driver.get('https://www.melon.com/song/lyrics.htm?songId={song_num}'.format(song_num=song_num[i]))

        craw_lyrics(n)



# 장르별 차트 접근
# 장르별 2000곡 추출
num =1 
while num < 2000:
    driver.get("https://www.melon.com/genre/song_list.htm?gnrCode=GN0800#params%5BgnrCode%5D=GN0800&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=NEW&params%5BsteadyYn%5D=N&po=pageObj&startIndex="+str(num))
    num = num + 50
    song_num = collect_no()
    access_detail(song_num, 8)



# 데이터 프레임 생성
df = pd.DataFrame({"title": titles, "artist": artists, "lyric": lyrics, "genre": genres})



# csv 파일로 저장
df.to_csv("music_info8.csv",  encoding='utf-8-sig')
