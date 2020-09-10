# AVAS

##### Automated Vulnerability Analysis System

## 시작하기

> 인프라 진단 시 일일이 비교하여 수행하는 자들이 많아  
 
> 업무의 고충은 날로 늘어 제 능력을 충분히 발휘하지 못 하니   

> 이런 까닭으로 능력있는 사람 조차 번번이 실수를 하는 사람이 많다.   

> 이를 안타깝게 여겨 새로이 자동화 무른모를 만드니   

> 그대들에게 하여금 업무의 효율성을 증대시키고자 할 따름이다.   

#### 시작하기에 앞서
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
#### 설치하기
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
<br/><img src="https://user-images.githubusercontent.com/62414986/92617619-71032a00-f2fa-11ea-82f8-d58d5b44472d.png" width=90%></img><br />

- 다운로드한 zip 파일 압축 해제 후 필요한 Python 모듈 설치(CMD 창)
  * CMD 창에서 압축 해제한 경로로 이동 후 아래와 같이 실행
```
python -m pip install -r requirements.txt
```

## 사용법
#### Usage
```
usage: python avas.py [ AVAS MOD ]

Automated Vulnerability Analysis System

positional arguments:
  AVAS MOD    collect  (수집 스크립트 생성 옵션)
              analysis (수집 스크립트 결과 분석 옵션)

optional arguments:
  -h, --help  show this help message and exit
```
#### Demo
[![asciicast](https://asciinema.org/a/o6k7G6yunupSy2ZVwFOI7eyWt.svg)](https://asciinema.org/a/o6k7G6yunupSy2ZVwFOI7eyWt)

## 설정파일
- AVAS.yaml   
**assetType** : 진단하고자 하는 대상의 운영체제   
**assetSubType** : 진단하고자 하는 대상의 종류   
**assetCode** : 진단하고자 하는 대상의 항목 코드   
  * U-ALL(all, All) : 해당 항목 코드에 관련된 모든 코드
  * U-10 ~ U-20 : 가져오고자 하는 항목 코드 범위 지정
  * U-01 : 항목 코드 하나씩 지정
```
assetInfo:
    assetType:
        - LINUX
    assetSubType:
        - OS
    assetCode:
        - U-All
        - U-10 ~ U-20
        - U-01
```

## 주의사항
- 반드시 수집 스크립트 결과 파일은 **InputResult 디렉터리**에 있어야 합니다.
- 분석이 완료된 후 최종 결과 엑셀 파일은 **ExcelDir 디렉터리에 위치**합니다.
- 새로운 항목 생성 시 **plugins 디렉터리 안에 생성**하셔야 하며, 기본 구조를 반드시 지켜주셔야 합니다.
  * 항목 생성 시 부수적으로 공통적인 코드 추가 시에는 **LibScript 디렉터리**에서 각 확장자에 맞게 추가하시면 됩니다.
- DRM 솔루션에 의한 엑셀 파일 잠금으로 인해 기본 엑셀 템플릿 파일은 소스코드안에 존재합니다.
  * 이 방법이 해당 솔루션을 우회하는지는 확인이 필요한 상태입니다.

## 라이센스
이 프로젝트는 **KISEC** 에서 진행 중으로 추후 공개 예정입니다.

## 교육
> 해당 프로젝트는 **KISEC 단기 교육 과정** 중 하나의 교육 컨텐츠로도 사용 중 입니다.
>    - 교육 링크 : [KISEC 사이트](https://www.kisec.com/service/edu_sbj_002_det.do?subjectNum=22)

## 감사 인사

-  이 프로젝트 진행에 많은 도움을 주신 [madwind76](https://github.com/madwind76) 님께 경의를 표합니다.

---

