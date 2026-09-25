# 김민준 Backend Portfolio

인증의 실패 조건과 AI 연동 흐름을 설계하고 구현하는 백엔드 개발자 김민준의 포트폴리오입니다.

## Website

[https://nuj1min.github.io](https://nuj1min.github.io)

## Featured work

- **여기도** — 지역 문화 아카이빙 플랫폼. 인증·회원 도메인 담당. Redis 원자적 토큰 교체, 세션별 로그인 관리, 탈퇴 회원 인증 정책 구현
- **다시찾음** — 분실물 탐색 모바일 웹. React·Spring Boot·배포 담당, 입력·좌표 정합성 및 AI 분석 계약 구현
- **바비든든** — 교내 식당 주문 서비스. 메뉴·주문·관리자 인증, 주문 상태 전이와 이벤트 발행 흐름 구현
- **Whatshu** — GDG 행사 출석 관리 서비스. 백엔드 구조와 배포 환경 설계
- **Crossy HUFS** — 한국외대 캠퍼스 기반 3D 아케이드 게임. 프로젝트 리드 및 장애물 로직 구현

## Focus

Java, Spring Boot, Spring Security, JPA, MySQL, Redis, Docker, AWS, JUnit 5

## Contact

- Email: [minjun0123@naver.com](mailto:minjun0123@naver.com)
- GitHub: [github.com/nuj1min](https://github.com/nuj1min)

## 콘텐츠 수정

대표 프로젝트의 원본은 `content/projects.json`입니다. 원본 수정 후 아래 명령으로 홈 요약과 상세 페이지를 함께 갱신합니다. 생성된 카드 구간과 `projects/*.html`은 직접 수정하지 않습니다.

```sh
python3 scripts/build_portfolio.py
```

- 홈: `index.html`
- 사례 상세: `projects/yeogido.html`, `projects/dasi-find.html`
- 공통 스타일: `css/portfolio.css`
- 내용 검토 사항: `docs/content-review.md`

별도 프레임워크나 설치 과정 없이 정적 HTML로 GitHub Pages에서 제공됩니다. PDF도 같은 대표 프로젝트 콘텐츠 원본을 사용합니다. 제출용 PDF는 `output/pdf/김민준_개발자_포트폴리오.pdf`에 있습니다.

PDF 재생성 (Python `reportlab` 필요):

```sh
python3 scripts/build_pdf.py --font /path/to/korean-font.ttf
```

기본 글꼴 경로는 macOS의 AppleGothic입니다. 다른 환경에서는 한글을 지원하는 TrueType 글꼴을 지정하세요. PDF는 9쪽이며 한글 글꼴과 클릭 가능한 자료 링크를 포함합니다.
