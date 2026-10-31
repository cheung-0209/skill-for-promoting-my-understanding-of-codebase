from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'codebase-to-course-plus/scripts/course.py'
QA = None


def run(*args, ok=True):
    result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
    if ok and result.returncode != 0:
        raise AssertionError(result.stderr)
    if not ok and result.returncode == 0:
        raise AssertionError('Expected rejection: ' + ' '.join(map(str, args)))
    return result


def fixture(path):
    repo = path / 'repo'
    repo.mkdir(parents=True)
    (repo / 'toy.py').write_text('def distance(x, y):\n    """教学样例：绝对距离。"""\n    return abs(x - y) if x < y else x - y\n', encoding='utf-8')
    course = path / 'course'
    run('init', '--out', course, '--title', '源码跟敲 · QA', '--lang', 'zh-CN')
    run('extract', '--repo', repo, '--file', 'toy.py', '--start', 1, '--end', 3,
        '--id', 'distance-core', '--course', course)
    snippet = (course / 'snippets/distance-core.html').read_text()
    (course / 'source-map.md').write_text('QA synthetic fixture; non-Git; no paper/model claims.\n')
    (course / 'modules/01-start.html').write_text('''
<section class="module" id="module-1" data-title="读代码并预测">
<div class="module-content">
<p class="module-number">01 · SOURCE</p><h1 class="module-title">读代码并预测</h1>
<p>这是用于验证课程引擎的微型样例。先观察输入，再预测输出。</p>
''' + snippet + '''
<div class="explanation">比较两点的位置，再返回它们之间的非负距离。</div>
<p><span class="term" data-definition="程序接受的值，例如 x=2、y=5。">输入</span>改变时，结果会怎样？</p>
<div class="quiz-container" id="quiz-one"><div class="quiz-question-block" data-correct="b" data-explanation-right="两点的距离是 3。" data-explanation-wrong="代入 x=2、y=5，检查 abs 的含义。">
<h3 class="quiz-question">输入 2 和 5，输出是什么？</h3>
<div class="quiz-options"><button class="quiz-option" data-value="a" onclick="selectOption(this)">-3</button><button class="quiz-option" data-value="b" onclick="selectOption(this)">3</button></div>
<div class="quiz-feedback" aria-live="polite"></div></div>
<button class="quiz-check-btn" onclick="checkQuiz('quiz-one')">检查答案</button>
<button class="quiz-reset-btn" onclick="resetQuiz('quiz-one')">重试</button></div>
<details><summary>参考答案与下一步</summary><p>distance(2,5) 返回 3。交换输入后应保持一致。</p></details>
<div class="chat-window" id="chat-qa">
<div class="chat-messages">
<div class="chat-message" data-sender="Input" style="display:none"><div class="chat-avatar">I</div><div class="chat-bubble">读取输入。</div></div>
<div class="chat-message" data-sender="Output" style="display:none"><div class="chat-avatar">O</div><div class="chat-bubble">返回结果。</div></div>
</div><p class="chat-progress"></p>
<button class="chat-next-btn">下一条</button><button class="chat-all-btn">全部播放</button><button class="chat-reset-btn">重置消息</button>
</div></div></section>''', encoding='utf-8')
    (course / 'modules/02-flow.html').write_text('''
<section class="module" id="module-2" data-title="跟踪数据流"><div class="module-content">
<p class="module-number">02 · FLOW</p><h2 class="module-title">跟踪数据流</h2>
<p>逐步观察两个数如何得到一个非负距离。</p>
<div class="flow-animation" data-steps='[{"label":"读取两个输入","highlight":"input","from":"input","to":"output","packet":true},{"label":"比较后返回距离","highlight":"output"}]'>
<div class="flow-actors"><div class="flow-actor" id="flow-input">输入 2、5</div><div class="flow-actor" id="flow-output">距离 3</div></div>
<div class="flow-packet"></div><p class="flow-step-label">点击下一步开始</p><p class="flow-progress"></p>
<button class="flow-next-btn">下一步</button><button class="flow-reset-btn">重置</button></div>
<details><summary>跟敲任务</summary><p>实现两点距离，并检查交换两点位置后结果保持不变。</p></details>
</div></section>''', encoding='utf-8')
    run('build', '--course', course)
    return repo, course


class Checks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global QA
        cls.tempdir = tempfile.TemporaryDirectory(prefix='course-skill-tests-')
        cls.addClassCleanup(cls.tempdir.cleanup)
        QA = Path(cls.tempdir.name)
        cls.repo, cls.course = fixture(QA / 'good')

    def case(self, name):
        target = QA / name
        shutil.copytree(QA / 'good', target)
        return target / 'repo', target / 'course'

    def test_good_offline_artifact_and_unicode(self):
        run('check', '--course', self.course, '--repo', self.repo)
        text = (self.course / 'index.html').read_text()
        self.assertIn('x &lt; y', text)
        self.assertIn('教学样例', text)
        self.assertNotIn('fonts.googleapis.com', text)

    def test_modified_displayed_source_rejected(self):
        repo, course = self.case('altered-display')
        p = course / 'index.html'
        p.write_text(p.read_text().replace('abs(x - y)', 'abs(x + y)'))
        self.assertIn('Rendered source differs', run('check', '--course', course, '--repo', repo, ok=False).stderr)

    def test_modified_source_checkout_rejected(self):
        repo, course = self.case('altered-repo')
        p = repo / 'toy.py'
        p.write_text(p.read_text() + '# changed\n')
        self.assertIn('changed since extraction', run('check', '--course', course, '--repo', repo, ok=False).stderr)

    def test_traversal_rejected(self):
        run('extract', '--repo', self.repo, '--file', '../course/index.html', '--start', 1, '--end', 1,
            '--id', 'escape', '--course', self.course, ok=False)

    def test_invalid_ranges_rejected(self):
        run('extract', '--repo', self.repo, '--file', 'toy.py', '--start', 0, '--end', 99,
            '--id', 'invalid', '--course', self.course, ok=False)

    def test_duplicate_module_id_rejected(self):
        _, course = self.case('duplicate-module')
        p = course / 'modules/02-flow.html'
        p.write_text(p.read_text().replace('module-2', 'module-1'))
        run('build', '--course', course, ok=False)

    def test_remote_runtime_asset_rejected(self):
        _, course = self.case('remote-asset')
        p = course / 'index.html'
        p.write_text(p.read_text().replace('src="main.js"', 'src="https://example.com/main.js"'))
        self.assertIn('Remote runtime asset', run('check', '--course', course, ok=False).stderr)

    def test_broken_flow_endpoint_rejected(self):
        _, course = self.case('broken-flow')
        p = course / 'index.html'
        p.write_text(p.read_text().replace('"to":"output"', '"to":"unknown"'))
        self.assertIn('unknown flow endpoint', run('check', '--course', course, ok=False).stderr)

    def test_missing_local_file_rejected(self):
        _, course = self.case('missing-file')
        (course / 'main.js').unlink()
        self.assertIn('Missing local file', run('check', '--course', course, ok=False).stderr)

    def test_existing_course_not_overwritten(self):
        run('init', '--out', self.course, '--title', 'Overwrite?', ok=False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
