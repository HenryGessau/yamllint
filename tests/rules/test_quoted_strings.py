# Copyright (C) 2018 ClearScore
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tests.common import RuleTestCase

from yamllint import config


class QuotedTestCase(RuleTestCase):
    rule_id = 'quoted-strings'

    def test_disabled(self):
        conf = 'quoted-strings: disable'

        self.check('---\n'
                   'foo: bar\n', conf)
        self.check('---\n'
                   'foo: "bar"\n', conf)
        self.check('---\n'
                   'foo: \'bar\'\n', conf)
        self.check('---\n'
                   'bar: 123\n', conf)
        self.check('---\n'
                   'bar: "123"\n', conf)

    def test_quote_type_any(self):
        conf = 'quoted-strings: {quote-type: any}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'                          # fails
                   'string2: "foo"\n'
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar", "foo[bar]", "foo{bar}"]\n'
                   'flow-map2: {a: foo, b: "foo,bar"}\n'
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf, problem1=(4, 10), problem2=(17, 5), problem3=(19, 12),
                   problem4=(20, 15), problem5=(21, 13), problem6=(22, 16),
                   problem7=(23, 19), problem8=(23, 28), problem9=(24, 20))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'               # fails
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3))

    def test_quote_type_single(self):
        conf = 'quoted-strings: {quote-type: single}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'                          # fails
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'                       # fails
                   'string4: "123"\n'                        # fails
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'                             # fails
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar", "foo[bar]", "foo{bar}"]\n'
                   'flow-map2: {a: foo, b: "foo,bar"}\n'
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf, problem1=(4, 10), problem2=(5, 10), problem3=(6, 10),
                   problem4=(7, 10), problem5=(17, 5), problem6=(18, 5),
                   problem7=(19, 12), problem8=(19, 17), problem9=(20, 15),
                   problem10=(20, 23), problem11=(21, 13), problem12=(21, 18),
                   problem13=(21, 29), problem14=(21, 41), problem15=(22, 16),
                   problem16=(22, 24), problem17=(23, 19), problem18=(23, 28),
                   problem19=(23, 33), problem20=(24, 20), problem21=(24, 30),
                   problem22=(24, 45))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'               # fails
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3), problem2=(12, 3))

    def test_quote_type_double(self):
        conf = 'quoted-strings: {quote-type: double}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'                          # fails
                   'string2: "foo"\n'
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'                      # fails
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar", "foo[bar]", "foo{bar}"]\n'
                   'flow-map2: {a: foo, b: "foo,bar"}\n'
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf, problem1=(4, 10), problem2=(8, 10), problem3=(17, 5),
                   problem4=(19, 12), problem5=(20, 15), problem6=(21, 13),
                   problem7=(22, 16), problem8=(23, 19), problem9=(23, 28),
                   problem10=(24, 20))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'               # fails
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf, problem1=(9, 3))

    def test_any_quotes_not_required(self):
        conf = 'quoted-strings: {quote-type: any, required: false}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar", "foo[bar]", "foo{bar}"]\n'
                   'flow-map2: {a: foo, b: "foo,bar"}\n'
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf)
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'
                   '   word 2"\n',
                   conf)

    def test_single_quotes_not_required(self):
        conf = 'quoted-strings: {quote-type: single, required: false}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'                       # fails
                   'string4: "123"\n'                        # fails
                   'string5: \'bar\'\n'
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'                               # fails
                   '  - "foo"\n'
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar", "foo[bar]", "foo{bar}"]\n'
                   'flow-map2: {a: foo, b: "foo,bar"}\n'
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf, problem1=(5, 10), problem2=(6, 10), problem3=(7, 10),
                   problem4=(18, 5), problem5=(19, 17), problem6=(20, 23),
                   problem7=(21, 18), problem8=(21, 29), problem9=(21, 41),
                   problem10=(22, 24), problem11=(23, 33), problem12=(24, 30),
                   problem13=(24, 45))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'            # fails
                   '   word 2"\n',
                   conf, problem1=(12, 3))

    def test_only_when_needed(self):
        conf = 'quoted-strings: {required: only-when-needed}\n'

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'
                   'string4: "123"\n'
                   'string5: \'bar\'\n'                      # fails
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'
                   '  - "foo"\n'                             # fails
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar", "foo[bar]", "foo{bar}"]\n'
                   'flow-map2: {a: foo, b: "foo,bar"}\n'
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf, problem1=(5, 10), problem2=(8, 10), problem3=(18, 5),
                   problem4=(19, 17), problem5=(20, 23))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'            # fails
                   '   word 2"\n',
                   conf, problem1=(12, 3))

    def test_only_when_needed_single_quotes(self):
        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: only-when-needed}\n')

        self.check('---\n'
                   'boolean1: true\n'
                   'number1: 123\n'
                   'string1: foo\n'
                   'string2: "foo"\n'                        # fails
                   'string3: "true"\n'                       # fails
                   'string4: "123"\n'                        # fails
                   'string5: \'bar\'\n'                      # fails
                   'string6: !!str genericstring\n'
                   'string7: !!str 456\n'
                   'string8: !!str "quotedgenericstring"\n'
                   'binary: !!binary binstring\n'
                   'integer: !!int intstring\n'
                   'boolean2: !!bool boolstring\n'
                   'boolean3: !!bool "quotedboolstring"\n'
                   'block-seq:\n'
                   '  - foo\n'
                   '  - "foo"\n'                             # fails
                   'flow-seq: [foo, "foo"]\n'                # fails
                   'flow-map: {a: foo, b: "foo"}\n'          # fails
                   'flow-seq2: [foo, "foo,bar"]\n'           # fails
                   'flow-map2: {a: foo, b: "foo,bar"}\n'     # fails
                   'nested-flow1: {a: foo, b: [foo, "foo,bar"]}\n'
                   'nested-flow2: [{a: foo}, {b: "foo,bar", c: ["d[e]"]}]\n',
                   conf, problem1=(5, 10), problem2=(6, 10), problem3=(7, 10),
                   problem4=(8, 10), problem5=(18, 5), problem6=(19, 17),
                   problem7=(20, 23), problem8=(21, 18), problem9=(22, 24),
                   problem10=(23, 33), problem11=(24, 30), problem12=(24, 45))
        self.check('---\n'
                   'multiline string 1: |\n'
                   '  line 1\n'
                   '  line 2\n'
                   'multiline string 2: >\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 3:\n'
                   '  word 1\n'
                   '  word 2\n'
                   'multiline string 4:\n'
                   '  "word 1\\\n'            # fails
                   '   word 2"\n',
                   conf, problem1=(12, 3))

    def test_only_when_needed_corner_cases(self):
        conf = 'quoted-strings: {required: only-when-needed}\n'

        self.check('---\n'
                   '- ""\n'
                   '- "- item"\n'
                   '- "key: value"\n'
                   '- "%H:%M:%S"\n'
                   '- "%wheel ALL=(ALL) NOPASSWD: ALL"\n'
                   '- \'"quoted"\'\n'
                   '- "\'foo\' == \'bar\'"\n'
                   '- "\'Mac\' in ansible_facts.product_name"\n'
                   '- \'foo # bar\'\n',
                   conf)
        self.check('---\n'
                   'k1: ""\n'
                   'k2: "- item"\n'
                   'k3: "key: value"\n'
                   'k4: "%H:%M:%S"\n'
                   'k5: "%wheel ALL=(ALL) NOPASSWD: ALL"\n'
                   'k6: \'"quoted"\'\n'
                   'k7: "\'foo\' == \'bar\'"\n'
                   'k8: "\'Mac\' in ansible_facts.product_name"\n',
                   conf)

        self.check('---\n'
                   '- ---\n'
                   '- "---"\n'                     # fails
                   '- ----------\n'
                   '- "----------"\n'              # fails
                   '- :wq\n'
                   '- ":wq"\n',                    # fails
                   conf, problem1=(3, 3), problem2=(5, 3), problem3=(7, 3))
        self.check('---\n'
                   'k1: ---\n'
                   'k2: "---"\n'                   # fails
                   'k3: ----------\n'
                   'k4: "----------"\n'            # fails
                   'k5: :wq\n'
                   'k6: ":wq"\n',                  # fails
                   conf, problem1=(3, 5), problem2=(5, 5), problem3=(7, 5))

    def test_only_when_needed_extras(self):
        conf = ('quoted-strings:\n'
                '  required: true\n'
                '  extra-allowed: [^http://]\n')
        self.assertRaises(config.YamlLintConfigError, self.check, '', conf)

        conf = ('quoted-strings:\n'
                '  required: true\n'
                '  extra-required: [^http://]\n')
        self.assertRaises(config.YamlLintConfigError, self.check, '', conf)

        conf = ('quoted-strings:\n'
                '  required: false\n'
                '  extra-allowed: [^http://]\n')
        self.assertRaises(config.YamlLintConfigError, self.check, '', conf)

        conf = ('quoted-strings:\n'
                '  required: true\n')
        self.check('---\n'
                   '- 123\n'
                   '- "123"\n'
                   '- localhost\n'                  # fails
                   '- "localhost"\n'
                   '- http://localhost\n'           # fails
                   '- "http://localhost"\n'
                   '- ftp://localhost\n'            # fails
                   '- "ftp://localhost"\n',
                   conf, problem1=(4, 3), problem2=(6, 3), problem3=(8, 3))

        conf = ('quoted-strings:\n'
                '  required: only-when-needed\n'
                '  extra-allowed: [^ftp://]\n'
                '  extra-required: [^http://]\n')
        self.check('---\n'
                   '- 123\n'
                   '- "123"\n'
                   '- localhost\n'
                   '- "localhost"\n'                # fails
                   '- http://localhost\n'           # fails
                   '- "http://localhost"\n'
                   '- ftp://localhost\n'
                   '- "ftp://localhost"\n',
                   conf, problem1=(5, 3), problem2=(6, 3))

        conf = ('quoted-strings:\n'
                '  required: false\n'
                '  extra-required: [^http://, ^ftp://]\n')
        self.check('---\n'
                   '- 123\n'
                   '- "123"\n'
                   '- localhost\n'
                   '- "localhost"\n'
                   '- http://localhost\n'           # fails
                   '- "http://localhost"\n'
                   '- ftp://localhost\n'            # fails
                   '- "ftp://localhost"\n',
                   conf, problem1=(6, 3), problem2=(8, 3))

        conf = ('quoted-strings:\n'
                '  required: only-when-needed\n'
                '  extra-allowed: [^ftp://, ";$", " "]\n')
        self.check('---\n'
                   '- localhost\n'
                   '- "localhost"\n'                # fails
                   '- ftp://localhost\n'
                   '- "ftp://localhost"\n'
                   '- i=i+1\n'
                   '- "i=i+1"\n'                # fails
                   '- i=i+2;\n'
                   '- "i=i+2;"\n'
                   '- foo\n'
                   '- "foo"\n'                      # fails
                   '- foo bar\n'
                   '- "foo bar"\n',
                   conf, problem1=(3, 3), problem2=(7, 3), problem3=(11, 3))

    def test_octal_values(self):
        conf = 'quoted-strings: {required: true}\n'

        self.check('---\n'
                   '- 100\n'
                   '- 0100\n'
                   '- 0o100\n'
                   '- 777\n'
                   '- 0777\n'
                   '- 0o777\n'
                   '- 800\n'
                   '- 0800\n'
                   '- 0o800\n'
                   '- "0800"\n'
                   '- "0o800"\n',
                   conf,
                   problem1=(9, 3), problem2=(10, 3))

    def test_allow_quoted_quotes(self):
        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: false,\n'
                '                 allow-quoted-quotes: false}\n')
        self.check('---\n'
                   'foo1: "[barbaz]"\n'          # fails
                   'foo2: "[bar\'baz]"\n',       # fails
                   conf, problem1=(2, 7), problem2=(3, 7))

        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: false,\n'
                '                 allow-quoted-quotes: true}\n')
        self.check('---\n'
                   'foo1: "[barbaz]"\n'          # fails
                   'foo2: "[bar\'baz]"\n',
                   conf, problem1=(2, 7))

        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: true,\n'
                '                 allow-quoted-quotes: false}\n')
        self.check('---\n'
                   'foo1: "[barbaz]"\n'          # fails
                   'foo2: "[bar\'baz]"\n',       # fails
                   conf, problem1=(2, 7), problem2=(3, 7))

        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: true,\n'
                '                 allow-quoted-quotes: true}\n')
        self.check('---\n'
                   'foo1: "[barbaz]"\n'          # fails
                   'foo2: "[bar\'baz]"\n',
                   conf, problem1=(2, 7))

        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: only-when-needed,\n'
                '                 allow-quoted-quotes: false}\n')
        self.check('---\n'
                   'foo1: "[barbaz]"\n'          # fails
                   'foo2: "[bar\'baz]"\n',       # fails
                   conf, problem1=(2, 7), problem2=(3, 7))

        conf = ('quoted-strings: {quote-type: single,\n'
                '                 required: only-when-needed,\n'
                '                 allow-quoted-quotes: true}\n')
        self.check('---\n'
                   'foo1: "[barbaz]"\n'          # fails
                   'foo2: "[bar\'baz]"\n',
                   conf, problem1=(2, 7))

        conf = ('quoted-strings: {quote-type: double,\n'
                '                 required: false,\n'
                '                 allow-quoted-quotes: false}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"          # fails
                   "foo2: '[bar\"baz]'\n",       # fails
                   conf, problem1=(2, 7), problem2=(3, 7))

        conf = ('quoted-strings: {quote-type: double,\n'
                '                 required: false,\n'
                '                 allow-quoted-quotes: true}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"          # fails
                   "foo2: '[bar\"baz]'\n",
                   conf, problem1=(2, 7))

        conf = ('quoted-strings: {quote-type: double,\n'
                '                 required: true,\n'
                '                 allow-quoted-quotes: false}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"          # fails
                   "foo2: '[bar\"baz]'\n",       # fails
                   conf, problem1=(2, 7), problem2=(3, 7))

        conf = ('quoted-strings: {quote-type: double,\n'
                '                 required: true,\n'
                '                 allow-quoted-quotes: true}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"          # fails
                   "foo2: '[bar\"baz]'\n",
                   conf, problem1=(2, 7))

        conf = ('quoted-strings: {quote-type: double,\n'
                '                 required: only-when-needed,\n'
                '                 allow-quoted-quotes: false}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"          # fails
                   "foo2: '[bar\"baz]'\n",       # fails
                   conf, problem1=(2, 7), problem2=(3, 7))

        conf = ('quoted-strings: {quote-type: double,\n'
                '                 required: only-when-needed,\n'
                '                 allow-quoted-quotes: true}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"          # fails
                   "foo2: '[bar\"baz]'\n",
                   conf, problem1=(2, 7))

        conf = ('quoted-strings: {quote-type: any}\n')
        self.check("---\n"
                   "foo1: '[barbaz]'\n"
                   "foo2: '[bar\"baz]'\n",
                   conf)
