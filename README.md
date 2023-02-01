# S3-RestAPI
AWS S3버킷과 RestAPI를 진행하는 서버입니다.  
-> *Restful한 서버를 위해 CRUD를 지원합니다.*

> Django의 MTV 구조에 맞게 프로젝트를 구성하였으며, DRF(Django RestFramework)를 이용한 서버를 구축하였습니다.  

Viewset을 이용해 미리 설정된 class와 Method를 활용해 백엔드를 구성하였습니다.  
유저 접근 및 보안을 위해 JWT 토큰을 사용한 검증 진행

### a. 메소드 설명
1. retrieve(get) : S3 버킷에 있는 파일을 불러와 웹서비스를 제공하기 위해 렌더링을 해주는 작업을 수행
2. create(post) : 업로드할 파일을 S3 버킷에 올리는 작업을 수행
3. destroy(delete) : S3 버킷에 해당 파일과 관련 내용을 삭제하는 작업을 수행
4. update(put) : 웹서비스를 통해 작업하였던 파일을 다시 S3 버킷에 올려 저장(업데이트) 해주는 작업을 수행
5. list(get) : 유저 정보(UID)를 확인해 S3 버킷에 해당 유저가 올린 데이터를 확인해 조회해주는 작업을 수행

### b. MSA 아키텍처를 위해 각 서비스별로 세분화시켜 작업을 진행하였고, 객체 지향을 목표로 프로젝트를 구성
### c. 서버에 업로드를 위해 Github Action과 연동해 CF(CloudFoundry)를 통한 CI/CD 연결 진행
