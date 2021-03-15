# LearnUs Downloader

## 소개
LearnUs Downloader는 LearnUs 내 강의 동영상을 다운로드할 수 있도록 도와주는 프로그램입니다.

<center><img src="/guide/main_screenshot_mac.png" width="90%" alt="메인 화면 (맥)"></center>
<center><img src="/guide/main_screenshot_windows.png" width="80%" alt="메인 화면 (윈도우)"></center>

## 주의사항
- 본 프로그램의 목적은 강의 오프라인 재생 및 수업 복습 용 영상 확인입니다.
- 강의 영상 공유, 영리 행위를 포함한 모든 불법 행위는 엄격히 금지됩니다.

## 다운로드
1. Release 폴더에서 현재 사용하는 OS에 맞는 압축파일을 찾고 Download를 클릭합니다.
2. 압축을 풀고 실행파일 (.app 또는 .exe)을 실행합니다.

## 설치 중 문제가 생기다면 (macOS)
<center><img src="/guide/warning_mac.png" width="50%" alt="오류 (맥)"></center>

위 사진과 같이 보안 경고가 뜬다면 '설정' > '보안 및 개인 정보 보호'에서 '확인 없이 열기'를 클릭합니다.
소스 코드도 같이 공개하였기때문에 바이러스 걱정은 전혀 안 해도 됩니다!

## 설치 중 문제가 생기다면 (Windows)
<center><img src="/guide/warning_windows.png" width="40%" alt="오류 (윈도우)"></center>

위 사진과 같이 PC 보호 경고가 뜬다면 '추가 정보' > '실행'을 클릭합니다.
소스 코드도 같이 공개하였기때문에 바이러스 걱정은 전혀 안 해도 됩니다!

## 사용 방법
1. LearnUs에서 다운로드 받을 강의에 접속합니다. (크롬 추천)
2. 마우스 우클릭 후 '페이지 소스 보기'를 클릭합니다. (크롬 기준)
3. Ctrl(Cmd) + A와 Ctrl(Cmd) + C 로 전체 HTML 소스를 복사합니다.
4. LearnUs Downloader를 실행하고 복사한 소스는 강의 소스에 붙여넣습니다.
5. 저장 이름 및 저장 위치를 지정한 후 다운로드를 눌러 영상을 다운로드 받습니다.

## 버그
- 스크립트 실행파일화가 서투른 탓에 빌드 중 불필요한 라이브러리까지 포함되어 용량이 큽니다.. (macOS 한정)
- 다운로드 받은 영상 파일이 깨질 수 있으므로 기본 프로그램으로 열리지 않는다면 서드파티 프로그램 (IINA 등)으로 재생시켜야합니다.
