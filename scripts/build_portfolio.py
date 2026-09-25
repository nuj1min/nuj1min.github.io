"""Generate static project cards and detail pages from one content source."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / 'content/projects.json').read_text())
START = '<!-- selected-projects:start -->'
END = '<!-- selected-projects:end -->'


def e(value):
    return escape(str(value), quote=True)


def links(items):
    return '<div class="evidence-links">' + ''.join(
        f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a>'
        for label, url in items) + '</div>'


def tags(project):
    return '<ul class="tag-list" aria-label="기술 스택">' + ''.join(
        f'<li>{e(tag)}</li>' for tag in project['tags']) + '</ul>'


def card(project, index):
    return f'''<article class="case-preview" {'id="featured-project"' if index == 0 else ''}>
      <div class="case-preview-heading">
        <p class="eyebrow">Selected work / 0{index + 1}</p>
        <h3>{e(project['name'])}<span>{e(project['english'])}</span></h3>
        <p class="case-headline">{e(project['headline'])}</p>
        <p class="project-summary">{e(project['summary'])}</p>
        <p class="case-period">{e(project['period'])}</p>
        {tags(project)}
      </div>
      <div class="case-preview-body">
        <p class="role-label">{e(project['role'])}</p>
        <p class="ownership">{e(project['ownership'])}</p>
        <dl class="case-summary">
          <div><dt>문제</dt><dd>{e(project['problem'])}</dd></div>
          <div><dt>선택</dt><dd>{e(project['decision'])}</dd></div>
          <div><dt>결과</dt><dd>{e(project['result'])}</dd></div>
        </dl>
        <div class="case-actions"><a class="button button-primary" href="projects/{e(project['slug'])}.html">문제 해결 과정 읽기 <span aria-hidden="true">↗</span></a>
        <a class="text-link" href="{e(project['cases'][0]['links'][0][1])}" target="_blank" rel="noopener noreferrer">대표 PR ↗</a></div>
      </div>
    </article>'''


def detail(project):
    scope = ''.join(f'<article><h3>{e(title)}</h3><p>{e(body)}</p></article>' for title, body in project['scope'])
    flow = ''.join(f'<li>{e(step)}</li>' for step in project['flow'])
    cases = ''
    for index, case in enumerate(project['cases'], 1):
        cases += f'''<article class="case-study" id="case-{index}">
          <p class="eyebrow">Case 0{index}</p><h3>{e(case['title'])}</h3>
          <dl class="case-breakdown">
            <div><dt>문제</dt><dd>{e(case['problem'])}</dd></div>
            <div><dt>변경</dt><dd>{e(case['solution'])}</dd></div>
            <div><dt>판단</dt><dd>{e(case['reason'])}</dd></div>
            <div class="verified"><dt>검증</dt><dd>{e(case['verification'])}</dd></div>
          </dl>{links(case['links'])}</article>'''
    results = ''.join(f'<li>{e(result)}</li>' for result in project['results'])
    visual = ''
    if project['slug'] == 'yeogido':
        visual = '''<figure class="service-figure"><img src="../images/yeogido-preview.jpg" width="1600" height="1512" alt="여기도 소상공인 홍보 기능 와이어프레임" loading="lazy"><figcaption>서비스 소개용 와이어프레임 · 소상공인 홍보 화면. 제 담당 영역은 인증·회원입니다.</figcaption></figure>'''
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(project['name'])} | 김민준 프로젝트 사례</title>
  <meta name="description" content="{e(project['headline'])}. {e(project['ownership'])}">
  <meta name="theme-color" content="#183e2e">
  <link rel="canonical" href="https://nuj1min.github.io/projects/{e(project['slug'])}.html">
  <link rel="stylesheet" href="../css/portfolio.css">
</head>
<body class="detail-page">
  <a class="skip-link" href="#main">본문으로 바로가기</a>
  <header class="site-header"><div class="container header-inner">
    <a class="brand" href="../index.html"><strong>BEYOND CODE</strong><span>김민준 · 프로젝트 사례</span></a>
    <a class="header-cta" href="../index.html#projects">프로젝트 목록</a>
  </div></header>
  <main id="main">
    <div class="container detail-hero">
      <p class="eyebrow">{e(project['role'])}</p>
      <h1>{e(project['name'])}</h1><p class="detail-subtitle">{e(project['headline'])}</p>
      <p class="case-period">{e(project['period'])}</p>{tags(project)}
    </div>
    <div class="container detail-layout">
      <nav class="case-toc" aria-label="프로젝트 목차">
        <a href="#overview">01 프로젝트 소개</a><a href="#ownership">02 담당 범위</a>
        <a href="#cases">03 문제 해결 과정</a><a href="#results">04 결과와 검증</a><a href="#resources">05 관련 자료</a>
      </nav>
      <div class="detail-content">
        <section id="overview"><p class="eyebrow">Overview</p><h2>어떤 서비스인가요?</h2>
          <p class="lead">{e(project['summary'])}</p>{visual}</section>
        <section id="ownership"><p class="eyebrow">My contribution</p><h2>제가 맡은 범위</h2>
          <p class="lead">{e(project['ownership'])}</p><div class="scope-grid">{scope}</div>
          <p class="scope-note">{e(project['boundary'])}</p>
          <figure class="flow-figure"><figcaption>{e(project['flowTitle'])}</figcaption><ol>{flow}</ol><p>구현 구조 요약</p></figure>
        </section>
        <section id="cases"><p class="eyebrow">Problem → Decision → Evidence</p><h2>문제와 해결 과정</h2>{cases}</section>
        <section id="results"><p class="eyebrow">Results</p><h2>변경한 동작과 검증 근거</h2>
          <ul class="result-list">{results}</ul><p class="scope-note">{e(project['note'])}</p>
        </section>
        <section id="resources"><p class="eyebrow">References</p><h2>코드와 변경 기록</h2>{links(project['links'])}
          <p class="source-date">작성 기준 · 2026.09.25 / 제공된 프로젝트 복원 자료와 PR 검증 기록</p>
        </section>
      </div>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>© 2026 Minjun Kim</span><a href="mailto:minjun0123@naver.com">minjun0123@naver.com</a><a href="../index.html#projects">프로젝트 목록</a></div></footer>
</body>
</html>
'''


home = ROOT / 'index.html'
html = home.read_text()
if START not in html or END not in html:
    raise SystemExit('Missing generated-content markers in index.html')
before, rest = html.split(START, 1)
_, after = rest.split(END, 1)
home.write_text(before + START + '\n' + '\n'.join(card(p, i) for i, p in enumerate(PROJECTS)) + '\n' + END + after)
for project in PROJECTS:
    (ROOT / 'projects' / (project['slug'] + '.html')).write_text(detail(project))
print('Generated home project cards and 2 detail pages.')
