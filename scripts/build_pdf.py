"""Create the submission PDF. Requires reportlab; --font accepts a Korean TTF."""
import argparse
import json
from html import escape
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font', default='/System/Library/Fonts/Supplemental/AppleGothic.ttf')
args = parser.parse_args()
pdfmetrics.registerFont(TTFont('Korean', args.font))
DATA = json.loads((ROOT / 'content/projects.json').read_text())
OUT = ROOT / 'output/pdf/김민준_개발자_포트폴리오.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
W, H = 595.276, 841.89
M, CW = 44, W - 88
GREEN, INK, SOFT = '#183e2e', '#171b16', '#50594e'
c = Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
c.setTitle('김민준 | Backend Developer Portfolio')
c.setAuthor('김민준')
c.setSubject('프로젝트별 역할, 문제 해결 과정과 검증 기록')
page_no = 0
y = 0


def clean(text):
    return text.replace('–', '-').replace('—', '-').replace('‑', '-')


def para(text, size=10.5, color=INK, space=9, x=M, width=CW, markup=False):
    global y
    style = ParagraphStyle('body', fontName='Korean', fontSize=size,
                           leading=size * 1.58, textColor=HexColor(color), wordWrap='CJK')
    p = Paragraph(clean(text) if markup else escape(clean(text)), style)
    _, height = p.wrap(width, H)
    if y - height < 49:
        raise ValueError(f'Page {page_no} overflow at {text[:65]} (y={y}, h={height})')
    p.drawOn(c, x, y - height)
    y -= height + space


def start(kicker, title, subtitle=''):
    global page_no, y
    if page_no:
        c.showPage()
    page_no += 1
    c.setFillColor(HexColor('#f4f3ed'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor(GREEN))
    c.rect(0, H - 12, W, 12, fill=1, stroke=0)
    c.setFont('Korean', 8)
    c.drawString(M, 29, '김민준 · Backend Developer / 2026.09.25')
    c.drawRightString(W - M, 29, f'{page_no:02d} / 09')
    y = H - 46
    para(kicker, 10, GREEN, 12)
    para(title, 27, GREEN, 9)
    if subtitle:
        para(subtitle, 11, SOFT, 18)
    else:
        y -= 10


def label(text):
    para(text, 12, GREEN, 7)


def rule():
    global y
    y -= 4
    c.setStrokeColor(HexColor('#cbd2c7'))
    c.line(M, y, W - M, y)
    y -= 19


def link(label_text, url, compact=False):
    short = url.replace('https://', '')
    text = f'{escape(label_text)}' + ('' if compact else f' · {escape(short)}')
    para(f'<link href="{escape(url, quote=True)}" color="{GREEN}"><u>{text}</u></link>',
         9, GREEN, 6, markup=True)


def case(item, number):
    label(f'CASE {number:02d} / {item["title"]}')
    for name, key in [('문제', 'problem'), ('변경', 'solution'), ('판단', 'reason'), ('검증', 'verification')]:
        para(f'<font color="{GREEN}">{name}</font>  {escape(item[key])}', 10.5, space=8, markup=True)
    for title, url in item['links']:
        link(title, url)
    rule()


def overview(project):
    para(project['summary'], 12, space=14)
    label('직접 맡은 역할')
    para(project['ownership'], 11)
    for name, body in project['scope']:
        para(f'<font color="{GREEN}">{escape(name)}</font>  {escape(body)}', markup=True)
    para(project['boundary'], 9, SOFT, 16)
    label(project['flowTitle'])
    for n, step in enumerate(project['flow'], 1):
        para(f'{n:02d}  {step}', 10.5, space=6)
    rule()
    label('변경 결과')
    for result in project['results']:
        para('· ' + result, 10.5, space=7)


yeogido, dasi = DATA
start('PORTFOLIO / BACKEND & FULL-STACK', '김민준', '인증의 실패 조건과 AI 연동 흐름을 설계하는 개발자')
para('화면부터 API·배포까지 연결하며,\n변경의 이유를 코드와 검증 기록으로 남깁니다.'.replace('\n', '<br/>'), 20, GREEN, 22, markup=True)
para('낯선 요구사항을 작은 문제로 나누고 실패 조건을 먼저 정의합니다. PR 리뷰와 API 명세로 결정의 이유를 공유하고, 팀원이 다음 작업을 이어갈 수 있는 구조를 지향합니다.', 11, space=20)
label('대표 프로젝트')
for project, pages in [(yeogido, '02-04'), (dasi, '05-07')]:
    para(f'{project["name"]}  /  {project["role"]}', 17, GREEN, 5)
    para(project['headline'], 12, space=5)
    para(project['result'], 10.5, SOFT, 7)
    para(f'상세 사례 {pages}쪽', 9, SOFT, 15)
rule()
label('추가 프로젝트 · 역량')
para('바비든든 · Whatshu · Crossy HUFS  /  08쪽\n기술 적용 경험 · 활동 이력 · 자격  /  09쪽'.replace('\n', '<br/>'), 11, space=18, markup=True)
label('연락처와 자료')
link('이메일', 'mailto:minjun0123@naver.com')
link('GitHub', 'https://github.com/nuj1min')
link('웹 포트폴리오', 'https://nuj1min.github.io')
para('한국외국어대학교 글로벌캠퍼스 · 컴퓨터공학부', 10, SOFT)

start('01 / YEOGIDO · OVERVIEW', '여기도', yeogido['role'] + ' / ' + yeogido['period'])
overview(yeogido)
para('기술 · ' + ' / '.join(yeogido['tags']), 9, SOFT, 10)
link(*yeogido['links'][0])

start('01 / YEOGIDO · CASE STUDIES', '동시 요청과 세션의 경계', '인증 상태가 바뀌는 순간의 실패 조건을 다뤘습니다.')
case(yeogido['cases'][0], 1)
case(yeogido['cases'][1], 2)

start('01 / YEOGIDO · POLICY & EVIDENCE', '탈퇴 상태를 인증 정책에 반영', '로그인 방식이 달라도 회원 상태 검증은 일관되게 적용합니다.')
case(yeogido['cases'][2], 3)
label('협업 / Provider별 로그인 계약')
para('카카오는 authorizationCode와 redirectUri를 받아 백엔드에서 토큰을 교환하고, 네이버는 프론트엔드에서 받은 accessToken을 사용하는 흐름으로 구분했습니다. Provider별 필수값과 프로필 성별 미선택 값 NONE, Swagger 계약을 함께 맞췄습니다.')
para('PR #246의 API 테스트 완료 여부는 확인되지 않아 테스트 성과로 인용하지 않았습니다.', 9, SOFT)
rule()
label('검증 범위')
para(yeogido['note'], 10.5)
label('관련 코드와 변경 기록')
for item in yeogido['links']:
    link(*item)

start('02 / DASI FIND · OVERVIEW', '다시찾음', dasi['role'] + ' / ' + dasi['period'])
overview(dasi)
para('기술 · ' + ' / '.join(dasi['tags']), 9, SOFT, 8)
link('프론트엔드 · github.com/dasi-find/FE', 'https://github.com/dasi-find/FE', True)
link('백엔드 · github.com/dasi-find/BE', 'https://github.com/dasi-find/BE', True)

start('02 / DASI FIND · FRONTEND', '입력의 정확성과 초기 로딩', '화면과 서버의 계약을 맞추고, 첫 화면에 필요한 코드부터 불러옵니다.')
case(dasi['cases'][0], 1)
case(dasi['cases'][1], 2)

start('02 / DASI FIND · BACKEND', 'AI 연동과 상태 경계', '인증·소유권·저장은 BE에, 모델 실행은 AI 영역에 분리했습니다.')
case(dasi['cases'][2], 3)
case(dasi['cases'][3], 4)
para('검증 수치는 각 PR 당시 기록입니다. 최신 테스트 수나 AI 정확도 평가 수로 합산하지 않았습니다.', 9, SOFT, 0)
para('사진 누락 시 가중치 재분배와 후보 적합도 정책은 설계 영역이며, 매칭 엔진의 구현·평가 완료와 구분합니다.', 9, SOFT, 7)
for item in dasi['links'][2:]:
    link(*item)

start('03 / MORE PROJECTS', '다른 도메인에서 쌓은 경험', '주문 흐름, 행사 출석, 게임 개발에서 맡은 역할')
others = [
 ('바비든든', '2026.07부터 개발 / Backend · 메뉴·주문·관리자 인증',
  '교내 식당에서 QR로 메뉴를 확인하고 주문·결제·픽업 현황을 연결하는 서비스입니다.',
  '메뉴·주문 API, 관리자 JWT 인증과 판매 상태 관리를 담당했습니다. 품절·중복 옵션·최대 수량을 검증하고 PREPARING → READY → COMPLETED 상태 전이를 제한했습니다. 주문 이벤트는 트랜잭션 커밋 이후에만 발행하도록 보완했습니다.',
  'Spring Boot / MySQL / Docker / JWT / JUnit 5', 'https://github.com/GDGOC-babidundeun/BE'),
 ('Whatshu', '2025.09 - 2026.02 / Backend Lead',
  'Google Form으로 분산되던 GDG 행사 출결을 세션·멤버 단위로 관리하는 모바일 출석 서비스입니다.',
  '백엔드 리드로 Spring Boot API·인증 구조와 배포 환경을 설계했습니다. Swagger로 프론트엔드와 요청·응답 계약을 공유하고, Docker·AWS EC2·GitHub Actions 배포 환경을 구성했습니다.',
  'Java / Spring Boot / MySQL / Docker / AWS', 'https://github.com/GDG-whatshu/BE'),
 ('Crossy HUFS', '2025.03 - 2025.05 / Project Lead · Unity',
  '한국외대 글로벌캠퍼스를 배경으로 재해석한 3D 아케이드 게임입니다.',
  '팀장으로 기획·일정·통합을 맡고 랜덤 장애물 생성 로직을 구현했습니다. 장애물 중복 배치를 방지하고 차량·통나무 생성 및 충돌 처리를 개선했습니다. 팀원 PR 통합과 빌드 안정화, 데모 일정을 관리했습니다.',
  'C# / Unity / OOP / GitHub Projects', 'https://github.com/nuj1min/Crossy_HUFS')]
for name, period, intro, work, tech, url in others:
    para(name, 17, GREEN, 4)
    para(period, 9, SOFT, 7)
    para(intro, 10.5, space=7)
    para(work, 10.5, space=7)
    para(tech, 9, SOFT, 4)
    link('Repository', url)
    rule()

start('04 / SKILLS & JOURNEY', '기술과 협업 경험', '한국외국어대학교 글로벌캠퍼스 · 컴퓨터공학부')
skills = [
 ('Java · Spring Boot · JPA · MySQL', '인증·회원·메뉴·주문 API, 도메인 관계와 트랜잭션 경계, UNIQUE 충돌 및 데이터 정합성 처리'),
 ('Spring Security · JWT · Redis', '이메일·OAuth 인증, 역할별 인가, 세션별 Refresh Token과 TTL, Lua 원자적 교체'),
 ('React · TypeScript', '모바일 웹 화면, 입력 계약과 좌표 정합성, 동적 import 기반 페이지별 코드 분할'),
 ('Docker · AWS · GitHub Actions', 'EC2·Docker Compose, OIDC·SSM 배포, CloudFront HTTPS와 Vercel API rewrite'),
 ('Test · API Documentation', '토큰 교체·분석 소유권·수색 만료 경계 테스트, Swagger 및 API 계약 공유')]
for name, body in skills:
    label(name)
    para(body, 10, space=10)
rule()
label('활동 이력')
for date, body in [
 ('2022', '컴퓨터공학부 1학년 과대표 · 보안 학회 PNP / 의견 조율과 Linux·TCP/IP 학습'),
 ('2025', '학생회 집행부장 / 행사 기획과 구성원 커뮤니케이션'),
 ('2025.09 - 2026.02', 'GDG 7기 Core Member · Whatshu 백엔드 리드'),
 ('2026.02 - 08', '학생회 기획부장 · UMC 10기 / 조직 운영과 Spring 백엔드 심화'),
 ('2026.07부터', '여기도·바비든든 백엔드 / 인증·회원·메뉴·주문·관리자'),
 ('2026.08 - 09 기록', '다시찾음 풀스택 / 모바일 웹·AI 분석 연동·배포')]:
    para(f'{date}  |  {body}', 9.5, space=7)
rule()
label('자격')
para('리눅스마스터 2급 · 2025.08  /  네트워크관리사 2급 · 2025.07', 10, space=9)
para('본 문서는 2026.09.25 기준 제공된 프로젝트 자료와 PR 기록으로 작성했습니다. 개발 기록이 확인된 기간을 표기했으며, 확인되지 않은 팀 인원이나 운영 성과는 포함하지 않았습니다.', 9, SOFT, 0)
assert page_no == 9
c.save()
print(f'{OUT} ({OUT.stat().st_size:,} bytes, {page_no} pages)')
