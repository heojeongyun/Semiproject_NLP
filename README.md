# 감성분석 기반의 노래 추천 서비스
사용자가 오늘 있었던 일이나 느꼈던 감정을 문장으로 입력하면, 인공지능 모델이 글에서 감정을 읽어내고 알맞은 가사의 노래들을 추천해줍니다.
멀티캠퍼스에서 진행했던 세미프로젝트입니다. kimwoonggon 님의 [케라스로 버트 빠르게 돌려보기 With 네이버 영화 평가 감성분석](https://github.com/kimwoonggon/publicservant_AI/blob/master/03_%EC%BC%80%EB%9D%BC%EC%8A%A4%EB%A1%9C_%EB%B2%84%ED%8A%B8_%EB%B9%A0%EB%A5%B4%EA%B2%8C_%EB%8F%8C%EB%A0%A4%EB%B3%B4%EA%B8%B0_With_%EB%84%A4%EC%9D%B4%EB%B2%84_%EC%98%81%ED%99%94_%EA%B0%90%EC%84%B1%EB%B6%84%EC%84%9D_TUTORIAL.ipynb)을 많이 참고해서 만들었습니다.

사전 학습된 multilingual bert 모델을 사용하여 파인튜닝 진행하였고, 학습 데이터로는 AIhub의 [감성대화말뭉치 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100)를 사용했습니다. 학습된 모델은 멜론에서 크롤링해온 데이터에서 알맞은 감성의 가사를 분류하고, 스트림릿 상에서 사용자가 문장을 입력하면 알맞은 가사의 노래 데이터들을 차트(df)형태로 보여줍니다.

# 코드 실행
```streamlit_musicrecommend.py``` 실행
