# Docker-compose로 로컬에 Orthanc 서버 구축


### dcmtk 설치 (window)
https://chocolatey.org/install

1. 관리자 권한으로 powershell 실행

2. 

```
Get-ExecutionPolicy

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

3. 설치 확인
<img src="./images/img2.JPG"/>