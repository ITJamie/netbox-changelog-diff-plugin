# modified from https://github.com/wagoodman/diff2HtmlCompare
import difflib
import io
import json
import yaml
import pygments
from pygments.lexers import guess_lexer_for_filename
from pygments.lexer import RegexLexer
from pygments.formatters import HtmlFormatter
from pygments.token import *
import pprint
from ..utils import get_plugin_setting


class DefaultLexer(RegexLexer):
    """
    Simply lex each line as a token.
    """

    name = 'Default'
    aliases = ['default']
    filenames = ['*']

    tokens = {
        'root': [
            (r'.*\n', Text),
        ]
    }


class DiffHtmlFormatter(HtmlFormatter):
    """
    Formats a single source file with pygments and adds diff highlights based on the 
    diff details given.
    """
    isLeft = False
    diffs = None

    def __init__(self, isLeft, diffs, *args, **kwargs):
        self.isLeft = isLeft
        self.diffs = diffs
        super(DiffHtmlFormatter, self).__init__(*args, **kwargs)

    def wrap(self, source):
        return self._wrap_code(source)

    def getDiffLineNos(self):
        retlinenos = []
        for idx, ((left_no, left_line), (right_no, right_line), change) in enumerate(self.diffs):
            no = None
            if self.isLeft:
                if change:
                    if isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_leftchange">' + \
                            str(left_no) + "</span>"
                    elif isinstance(left_no, int) and not isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_leftdel">' + \
                            str(left_no) + "</span>"
                    elif not isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_leftadd">  </span>'
                else:
                    no = '<span class="lineno_q">' + str(left_no) + "</span>"
            else:
                if change:
                    if isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_rightchange">' + \
                            str(right_no) + "</span>"
                    elif isinstance(left_no, int) and not isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_rightdel">  </span>'
                    elif not isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_rightadd">' + \
                            str(right_no) + "</span>"
                else:
                    no = '<span class="lineno_q">' + str(right_no) + "</span>"

            retlinenos.append(no)

        return retlinenos

    def _wrap_code(self, source):
        source = list(source)
        yield 0, ''

        for idx, ((left_no, left_line), (right_no, right_line), change) in enumerate(self.diffs):
            # print idx, ((left_no, left_line),(right_no, right_line),change)
            try:
                if self.isLeft:
                    if change:
                        if isinstance(left_no, int) and isinstance(right_no, int) and left_no <= len(source):
                            i, t = source[left_no - 1]
                            t = '<span class="left_diff_change">' + t + "</span>"
                            # t = '<pre class="change-data"><span class="removed">' + t + "</span></pre>"
                        elif isinstance(left_no, int) and not isinstance(right_no, int) and left_no <= len(source):
                            i, t = source[left_no - 1]
                            t = '<span class="left_diff_del">' + t + "</span>"
                            # t = '<pre class="change-data"><span class="removed">' + t + "</span></pre>"
                        elif not isinstance(left_no, int) and isinstance(right_no, int):
                            i, t = 1, left_line
                            t = '<span class="left_diff_add">' + t + "</span>"
                            # t = '<pre class="change-data"><span class="removed">' + t + "</span></pre>"
                        else:
                            raise
                    else:
                        if left_no <= len(source):
                            i, t = source[left_no - 1]
                        else:
                            i = 1
                            t = left_line
                else:
                    if change:
                        if isinstance(left_no, int) and isinstance(right_no, int) and right_no <= len(source):
                            i, t = source[right_no - 1]
                            t = '<span class="right_diff_change">' + t + "</span>"
                            # t = '<pre class="change-data"><span class="added">' + t + "</span></pre>"
                        elif isinstance(left_no, int) and not isinstance(right_no, int):
                            i, t = 1, right_line
                            t = '<span class="right_diff_del">' + t + "</span>"
                            # t = '<pre class="change-data"><span class="removed">' + t + "</span></pre>"
                        elif not isinstance(left_no, int) and isinstance(right_no, int) and right_no <= len(source):
                            i, t = source[right_no - 1]
                            t = '<span class="right_diff_add">' + t + "</span>"
                            # t = '<pre class="change-data"><span class="added">' + t + "</span></pre>"
                        else:
                            raise
                    else:
                        if right_no <= len(source):
                            i, t = source[right_no - 1]
                        else:
                            i = 1
                            t = right_line
                yield i, t
            except:
                # print "WARNING! failed to enumerate diffs fully!"
                pass  # this is expected sometimes
        yield 0, '\n'

    def _wrap_tablelinenos(self, inner):
        dummyoutfile = io.StringIO()
        lncount = 0
        for t, line in inner:
            if t:
                lncount += 1

            dummyoutfile.write(line)
        fl = self.linenostart
        mw = len(str(lncount + fl - 1))
        sp = self.linenospecial
        st = self.linenostep
        la = self.lineanchors
        aln = self.anchorlinenos
        nocls = self.noclasses



        yield 0, (f'<table width="100%" class="{self.cssclass}"><tr></div></td><td class="code">')
        yield 0, dummyoutfile.getvalue()
        yield 0, '</td></tr></table>'


class CodeDiff(object):
    """
    Manages a pair of source files and generates a single html diff page comparing
    the contents.
    """

    def __init__(self, fromtxt, totxt, name=None):

        self.fromlines = [n + "\n" for n in fromtxt.split("\n")]
        self.leftcode = "".join(self.fromlines)


        self.tolines = [n + "\n" for n in totxt.split("\n")]
        self.rightcode = "".join(self.tolines)

    def getDiffDetails(self, fromdesc='', todesc='', context=False, numlines=5, tabSize=8):
        # change tabs to spaces before it gets more difficult after we insert
        # markkup
        def expand_tabs(line):
            # hide real spaces
            line = line.replace(' ', '\0')
            # expand tabs into spaces
            line = line.expandtabs(tabSize)
            # replace spaces from expanded tabs back into tab characters
            # (we'll replace them with markup after we do differencing)
            line = line.replace(' ', '\t')
            return line.replace('\0', ' ').rstrip('\n')

        self.fromlines = [expand_tabs(line) for line in self.fromlines]
        self.tolines = [expand_tabs(line) for line in self.tolines]

        # create diffs iterator which generates side by side from/to data
        if context:
            context_lines = numlines
        else:
            context_lines = None

        diffs = difflib._mdiff(self.fromlines, self.tolines, context_lines,
                               linejunk=None, charjunk=difflib.IS_CHARACTER_JUNK)
        return list(diffs)

    def format(self, verbose=False):
        self.diffs = self.getDiffDetails('a', 'b')

        if verbose:
            for diff in self.diffs:
                print("%-6s %-80s %-80s" % (diff[2], diff[0], diff[1]))

        fields = ((self.leftcode, True),
                  (self.rightcode, False))

        codeContents = []
        for (code, isLeft) in fields:

            inst = DiffHtmlFormatter(isLeft,
                                     self.diffs,
                                     nobackground=False,
                                     linenos=True,
                                     #style=options.syntax_css
                                     )

            self.lexer = DefaultLexer()

            formatted = pygments.highlight(code, self.lexer, inst)

            codeContents.append(formatted)

        answers = {
            "left":  codeContents[0],
            "right":  codeContents[1],
        }

        return answers

def styled_diff(old, new):
    """
    returns styled output
    """

    if "last_updated" in old:
        old.pop("last_updated") 
    if "last_updated" in new:
        new.pop("last_updated")

    if get_plugin_setting('change_log_format') == 'yaml':
        # old['output_format'] = 'yaml'
        old = yaml.dump(old, sort_keys=False)
        new = yaml.dump(new, sort_keys=False)
    elif get_plugin_setting('change_log_format') == 'json':
        # old['output_format'] = 'json'
        old = json.dumps(old, indent=2)
        new = json.dumps(new, indent=2)
    else:
        # old['output_format'] = 'unknown_yaml-fallback'
        old = yaml.dump(old, sort_keys=False)
        new = yaml.dump(new, sort_keys=False)

    codeDiff = CodeDiff(old, new)
    return codeDiff.format()