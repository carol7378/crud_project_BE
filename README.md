# intern-crud-BE

### 📌 실행
- requirements 설치
    - requirements 수정 ("pip list --format=freeze > requirements.txt")
    <pre><code>pip install -r requirements.txt</code></pre>

- 8000 포트 사용, reload
    <pre><code>uvicorn main:app --port 8000 --reload</code></pre>

- 외부 접속 서버 : [ngrok](https://ngrok.com/) v3 사용
    - 회원 가입 후 [튜토리얼](https://dashboard.ngrok.com/get-started/setup/macos) 따라가기


***


### 📁 프로젝트 구조

    - main.py : FastAPI 애플리케이션 초기화
    
    - api/ : 라우터 및 엔드포인트 정의
    - controllers/ : 비즈니스 로직 처리
    - models/ : 데이터베이스 모델
    - schemas/ : 입출력 데이터 검증
    - helpers/ : JWT 토큰 생성/검증
    - constants/ : 상수 값 정의

    - database.py : DB 연동
    - requirements.txt : 필요한 라이브러리 설치 

***

### 📚 참고 자료
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/ko/)
- 
