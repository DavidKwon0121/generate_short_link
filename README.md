# Short Link Management

이 프로젝트는 사용자가 짧은 URL을 생성하고 관리할 수 있는 서비스를 제공합니다.


## 시작하기
이 프로젝트를 로컬 환경에서 실행하기 위해 Docker를 사용합니다.
```bash
docker-compose up --build
```

## 테스트 실행
1. 테스트용 데이터베이스 실행
```bash
docker-compose -f docker-compose.test_db.yml up --build -d
```
2. python 의존성 설치
```bash
python -m pip install --upgrade pip && \
python -m pip install setuptools && \
python -m pip install poetry && \
poetry config virtualenvs.create false 
```
3. poetry 실행
```bash
python -m poetry install --no-root
```

4. ENV 와 함께 pytest 실행
```bash
ENV=TEST python -m pytest -s -v 
```
