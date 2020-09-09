# AVAS

##### Automated Vulnerability Analysis System

## 시작하기

인프라 진단 시 일일이 비교하여 수행하는 자들이 많아   
업무의 고충은 날로 늘어 제 능력을 충분히 발휘하지 못 하니   
이런 까닭으로 능력있는 사람 조차 번번이 실수를 하는 사람이 많다.   
이를 안타깝게 여겨 새로이 자동화 무른모를 만드니   
그대들에게 하여금 업무의 효율성을 증대시키고자 할 따름이다.   

### 시작하기에 앞서
- 설치 및 실행 테스트 환경
```
OS : Windows10, Ubuntu 18.04
Version : Python 3.8
```
- 스크립트 실행 테스트 환경
```
Windows Server 2008 R2
Windows Server 2012
CentOS 7
Ubuntu 16.04
Ubuntu 18.04
```
### 설치하기
##### Ubuntu

- Python 및 git 설치

```
sudo apt-get install python3.* git
```
- git 저장소에서 Pull
```
git clone https://github.com/GGC-Github/AVAS.git
```
- 필요한 Python 모듈 설치
```
cd AVAS
python3 -m pip install -r requirements.txt
```

##### Windows
- Python 설치(아래 사이트에서 3.8 버전 다운로드 및 설치)
```
https://www.python.org/downloads/
```
- AVAS Github 에서 Download Zip   
<img src="https://user-images.githubusercontent.com/62414986/92617619-71032a00-f2fa-11ea-82f8-d58d5b44472d.png" width=90%></img><br />

마무리로 시스템에서 데이터를 추출하는 방법이나 데모를 실행하는 방법을 설명해 주세요.

## 테스트 실행하기

이 시스템을 위한 자동화된 테스트를 실행하는 방법을 적어주세요.

### End-to-End 테스트

이 단위 테스트가 테스트하는 항목을 설명하고 테스트를 하는 이유를 적어주세요.

```
예시도 재공하세요
```

### 코딩 스타일 테스트

이 단위 테스트가 테스트하는 항목을 설명하고 테스트를 하는 이유를 적어주세요.

```
예시도 재공하세요
```


## 배포

추가로 실제 시스템에 배포하는 방법을 노트해 두세요.

## 사용된 도구

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - 웹 프레임워크
* [Maven](https://maven.apache.org/) - 의존성 관리 프로그램
* [ROME](https://rometools.github.io/rome/) - RSS 피드 생성기

## 기여하기

[CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) 를 읽으신 후 기여를 해주십시오. 자세한 Pull Request 절차와 행동 규칙을 확인하실 수 있습니다.

## 버전 관리

[SemVer](http://semver.org/) (을)를 사용하여 버전을 관리합니다. 자세한 방법은 레포지토리의 [테그(tags)](https://github.com/your/project/tags)를 확인해 주십시오.

## 저자

* **Billie Thompson** - *초기작* - [PurpleBooth](https://github.com/PurpleBooth)
* **Taeuk Kang** - *한국어 번역* - [GitHub](https://github.com/taeukme) / [Keybase](https://keybase.io/taeuk)


[기여자 목록](https://github.com/your/project/contributors)을 확인하여 이 프로젝트에 참가하신 분들을 보실 수 있습니다.

## 라이센스

이 프로젝트는 MIT 허가서를 사용합니다 - [LICENSE.md](LICENSE.md) 파일에서 자세히 알아보세요.

## 감사 인사

* 본인의 코드가 사용된 분께 경의를 표합니다
* 영감
* 기타 등등...

---

위 템플렛의 영문 원본은 [여기](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)에서 확인하실 수 있습니다.
오타는 Comment (댓글) 로 남겨주시면 수정해드리겠습니다.

- 
