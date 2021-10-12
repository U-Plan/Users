# Users
---

## 사용기술
Django, DRF, JWT


## 프로젝트 내용
Dango 프레임워크 위에서 DRF를 통해 API를 구현하였으며,<br>
Token(jwt)을 통해 인증을 관리한다.<br>
<br>
기본적인 유효성 검사를 제공하며  => email 형식, phone 형식, password 형식(^[A-Za-z0-9!@#$%^&+=]{8,100}$)<br>
API 호출시 잘못된 호출에 대한 HTTP코드와 에러 내용을 출력한다.<br>
<br>
회원정보는 이메일(unique),전화번호(unique),닉네임,이름,비밀번호로 구성되어있으며,<br>
저장시에는 id를 발행하나 이는 내부 관리용으로 로그인에는 사용되지 않는다.<br>
<br>
SMS인증은 실제 발송하지 않으며 테스트를 위해 인증번호는 "0000" 고정값을 사용하였다.<br>
단, 인증번호는 고정값이지만 인증 API 호출 후 3분이내에 인증값을 입력하지 않으면 인증에 실패한다.<br>
또한 인증에 성공시 발행 된 auth_key는 10분간만 유효하다.<br>
<br>
로그인은 기본적으로 이메일 혹은 전화번호 + 비밀번호로 가능하며<br>
로그인 후에 발급받은 Token을 통해 로그인을 유지할 수 있다. (테스트 용도로 발행 된 token으로 30일의 유효기간을 가지며, refresh를 사용하지 않는다.)<br>
<br>


## 로컬에서 프로젝트 실행하기
### 저장소 복제
> git clone https://github.com/U-Plan/Users.git
<br/>

### 구성요소 설치
추천 버전 :
<br/>
Python 3.9.4, django-3.2.8, djangorestframework-3.12.4, djangorestframework-jwt-1.11.0, django-model-utils-4.1.1
> pip install -r requirments.txt
<br/>

### 마이그레이션 적용 (필요시)
> python manage.py migrate
<br/>

### 개발서버 실행
> python manage.py runserver

---
## API 문서

### SMS 인증
인증번호 발송 

- 실제 SMS는 발송하지 않으며, 테스트를 위해 발송되는 인증번호는 0000으로 고정
- HTTP Method : POST
- URL : http://127.0.0.1:8000/user/auth
- Parameters : phone


호출 예제
~~~
curl -H "Content-Type: application/json" -d  '{"phone":"01011112222"}' -X POST http://127.0.0.1:8000/user/auth
~~~

응답값
~~~
{"message":"SUCCESS"}
~~~

인증번호 확인
- 인증번호 발송 후 3분간만 인증이 가능하며, 인증 성공시 발급된 auth_key는 10분간 유효하다.
- HTTP Method : POST
- URL : http://127.0.0.1:8000/user/auth/certificate
- Parameters : phone, auth

호출 예제
~~~
curl -H "Content-Type: application/json" -d  '{"phone":"01011112222","auth":"0000"}' -X POST http://127.0.0.1:8000/user/auth/certificate
~~~

응답값
~~~
{"auth_key":"6008"}
~~~

### 회원가입
- SMS 인증키 (/user/auth/certificate) 값이 필요하며 이메일(unique), 닉네임, 비밀번호, 이름, 전화번호(unique)를 입력받는다.
- HTTP Method : POST
- URL : http://127.0.0.1:8000/user/signup
- Parameters : phone, nickname, email, name, password, auth

호출 예제
~~~
curl -H "Content-Type: application/json" -d  '{
	"phone" : "01011112222",
	"nickname" : "john",
	"email": "test@ably.com",
	"name": "James",
	"password": "12345678",
	"auth": "6008"
}' -X POST http://127.0.0.1:8000/user/signup
~~~

응답값
~~~
{"id": 1} # 실제 유저에게 제공하는 값이 아닌 내부 보관용 아이디로 설계하였으나 테스트 용도로 출력
~~~


### 로그인
- 이메일 혹은 전화번호 + 비밀번호를 입력하면 로그인이 가능합니다.
- HTTP Method : POST
- URL : http://127.0.0.1:8000/user/login
- Parameters : id (email or phone), password

호출 예제
~~~
curl -H "Content-Type: application/json" -d  '{
	"id" : "01011112222",
	"password": "12345678"
}' -X POST http://127.0.0.1:8000/user/login

curl -H "Content-Type: application/json" -d  '{
	"id" : "test@ably.com",
	"password": "12345678"
}' -X POST http://127.0.0.1:8000/user/login
~~~

응답값
~~~
{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IjAxMDExMTEyMjIyIiwiZXhwIjoxNjM2NjQwNjk4LCJlbWFpbCI6InRlc3RAYWJseS5jb20iLCJwaG9uZSI6IjAxMDExMTEyMjIyIn0.CJbTHHyolkLQsw7afz-nI3KX-rVKPl7CkIkrKVbCG8s"}
~~~


### 내 정보 보기 기능
- 로그인을 통해 획득한 token을 header에 추가하여 호출 ex)Authorization : jwt {token}
- HTTP Method : GET
- URL : http://127.0.0.1:8000/user/info

호출 예제
~~~
curl -H "Content-Type: application/json" -H "Authorization:jwt  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IjAxMDExMTEyMjIyIiwiZXhwIjoxNjM2NjQwNzMzLCJlbWFpbCI6InRlc3RAYWJseS5jb20iLCJwaG9uZSI6IjAxMDExMTEyMjIyIn0.OL6qoTFQLUEMFz78LgPH9J24-xWtKYXuAQbvCbbjuYI"  http://127.0.0.1:8000/user/info
~~~

응답값
~~~
{"info":{"nickname":"john","email":"test@ably.com","name":"James","phone":"01011112222"}}
~~~


### 비밀번호 재설정 기능
- SMS 인증키 (/user/auth/certificate) 값이 필요하며 비밀번호, 전화번호를 입력받는다.
- HTTP Method : PATCH
- URL : http://127.0.0.1:8000/user/password
- Parameters : phone, assword, auth

호출 예제
~~~
curl -H "Content-Type: application/json" -d  '{
  "phone":"01011112222",
	"password": "09876543",
  "auth": "1088"
}' -X PATCH http://127.0.0.1:8000/user/password
~~~

응답값
~~~
{"message":"SUCCESS"}
~~~
