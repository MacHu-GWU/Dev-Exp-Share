#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Sanhe Hu
CopyRight: MIT 2017

Allow user to read sublime snippet, and transform into Atom/PyCharm snippet.

Where to put snippet:

Sublime Text
------------
MacOS:

put this ``MySnippets`` folder under:

``/Users/<your-username>/Library/Application Support/Sublime Text 3/Packages/User/``


Atom
----
Open ``Atom`` -> ``Snippet``, edit this file.

Ref: https://github.com/atom/snippets


PyCharm
-------
MacOS:

create a xml file ``<Template-Group-Name>.xml``, let's say ``User.xml``, edit
this file and put it under 
``/Users/<your-username>/Library/Preferences/PyCharmCE2<version>/templates``.

"""

from __future__ import (
    print_function, unicode_literals, absolute_import,
    division, generators,
)
import re
import lxml.etree as ET
from pathlib_mate import Path
from bs4 import BeautifulSoup, Comment


def read(path):
    """
    Read utf-8 pure text file.
    """
    with open(path, "rb") as f:
        return f.read().decode("utf-8").replace("\r\n", "\n")


def write(content, path):
    """
    Write string to utf-8 pure text file
    """
    with open(path, "wb") as f:
        return f.write(content.encode("utf-8"))


snippet_dir = Path(__file__).parent


def reset_test_file():
    """
    Delete content of all test file
    """
    for p in snippet_dir.select_file(lambda p: p.fname == "test"):
        write(" ", p.abspath)

reset_test_file()


def extract_by_prefix_surfix(text, prefix, surfix, minlen=None, maxlen=None,
                             include=False):
    """Extract the text in between a prefix and surfix. It use non-greedy match.

    :param text: text body
    :type text: str

    :param prefix: the prefix
    :type prefix: str

    :param surfix: the surfix
    :type surfix: str

    :param minlen: the min matched string length
    :type minlen: int

    :param maxlen: the max matched string length
    :type maxlen: int

    :param include: whether if include prefix and surfix
    :type include: bool
    """
    if minlen is None:
        minlen = 0
    if maxlen is None:
        maxlen = 2 ** 30
    pattern = r"""(?<=%s)[\s\S]{%s,%s}?(?=%s)""" % (
        prefix, minlen, maxlen, surfix)
    if include:
        return [prefix + s + surfix for s in re.findall(pattern, text)]
    else:
        return re.findall(pattern, text)


sublime_tpl = \
    '''
<snippet>
    <scope>{scope}</scope>
    <description>{description}</description>
    <tabTrigger>{trigger}</tabTrigger>
    <content><![CDATA[
{content}
]]></content>
</snippet>
'''.strip()

atom_snippet_tpl = \
    '''
'{description}':
  'prefix': '{trigger}'
  'body': """
{body}
  """
'''.replace('"', "'").strip()

atom_tpl = \
    """
'{scope}':
{list_of_snippet_cson}
""".strip()


def indent_n_space(text, n):
    """
    Add indent for each line.
    """
    indent = " " * n
    return "\n".join([indent + line for line in text.split("\n")])


pycharm_scope_mapper = {
    "source.python": "Python",
    "source.shell": "Bash",
    "text.restructuredtext": "OTHER",
    "text": "OTHER",
}


class Snippet(object):
    """
    Represent a Snippet

    :param scope: available for which type of file.
    :param description: help message to descript this snippet.
    :param trigger: text to trigger this snippet.
    :param content: content of this snippet, written in CoffeeScript.
    :param fname: filename of this snippet.
    """
    sublime_tpl = sublime_tpl
    atom_tpl = atom_tpl

    def __init__(self, scope, description, trigger, content, args, fname=None):
        self.scope = scope
        self.description = description
        self.trigger = trigger
        self.content = content
        self.args = args

        if fname is None:
            self.fname = self.description.replace(" ", "-")

    @property
    def sublime_scope(self):
        """
        Return its Sublime scope.
        """
        return self.scope

    @property
    def atom_scope(self):
        """
        Return its Atom scope.
        """
        return "." + self.scope

    @property
    def pycharm_scope(self):
        """
        Return its PyCharm scope.
        """
        return pycharm_scope_mapper[self.scope]

    def to_sublime_snippet(self):
        """
        Export as sublime snippet xml format.
        """
        xml = self.sublime_tpl.format(
            scope=self.sublime_scope,
            description=self.description,
            trigger=self.trigger,
            content=self.content,
        )

        return xml

    def to_atom_cson(self):
        """
        Export as atom cson snippet format.

        Example:

        .. code-block: CoffeeScript

            'Footer':
              'prefix': 'footer'
              'body': '''
                .. footer::

              '''
        """
        cson = atom_snippet_tpl.format(
            description=self.description,
            trigger=self.trigger,
            body=indent_n_space(self.content, 4)
        )
        cson = indent_n_space(cson, 2)
        return cson

    @classmethod
    def to_atom_snippet(cls, snippet_list):
        """
        Export to atom snippet cson file.
        """
        snippet_by_scope = dict()

        # group by scope
        for snippet in snippet_list:
            try:
                snippet_by_scope[snippet.atom_scope].append(snippet)
            except:
                snippet_by_scope[snippet.atom_scope] = [snippet, ]

        l = list()
        for scope, snippet_list in snippet_by_scope.items():
            scope_snippet = atom_tpl.format(
                scope=scope,
                list_of_snippet_cson="\n\n".join(
                    [snippet.to_atom_cson() for snippet in snippet_list]
                )
            )
            l.append(scope_snippet)
        return "\n".join(l)

    @property
    def pycharm_content(self):
        """
        Convert CoffeeScript snippet language to PyCharm snippet language.

        - in CoffeeScript: [${1:item} for $1 in ${2:iterable}]
        - in PyCharm: [$item$ for $item$ in $iterable$]
        """
        content = self.content
        for i, arg in enumerate(self.args):
            i += 1
            content = content.replace(
                "$%s" % i,
                "${%s:%s}" % (i, arg),
            )
        for i, arg in enumerate(self.args):
            i += 1
            content = content.replace(
                "${%s:%s}" % (i, arg),
                "$%s$" % arg.replace(" ", "_").replace("-", "_"),
            )
        return content

    @classmethod
    def to_pycharm_snippet(cls, snippet_list, group_name="User"):
        """

        Example:

        .. code-block: xml

            <templateSet group="PythonUser">
              <template name="class" value="class $class$($object$):&#10;    &quot;&quot;&quot;$cls_doc$&quot;&quot;&quot;&#10;&#10;    def __init__(self,$args$):&#10;        &quot;&quot;&quot;Constructor for $class$&quot;&quot;&quot;&#10;        $END$" description="" toReformat="false" toShortenFQNames="true">
                <variable name="class" expression="" defaultValue="" alwaysStopAt="true" />
                <variable name="object" expression="" defaultValue="" alwaysStopAt="true" />
                <variable name="cls_doc" expression="" defaultValue="" alwaysStopAt="true" />
                <variable name="args" expression="" defaultValue="" alwaysStopAt="true" />
                <context>
                  <option name="Python" value="true" />
                </context>
              </template>
              ...
            </templateSet>
        """
        templateSet = ET.Element("templateSet", group=group_name)
        # template = ET.SubElement(templateSet, "template")
        for snippet in snippet_list:
            if snippet.scope not in pycharm_scope_mapper:
                continue

            template = ET.SubElement(
                templateSet, "template",
                name=snippet.trigger,
                description=snippet.description,
                value=snippet.pycharm_content,
                toReformat="false",
                toShortenFQNames="true",
            )
            for arg in snippet.args:
                variable = ET.SubElement(
                    template, "variable",
                    name=arg.replace(" ", "_").replace("-", "_"),
                    expression="",
                    defaultValue='"%s"' % arg,
                    alwaysStopAt="true",
                )
            context = ET.SubElement(template, "context")
            option = ET.SubElement(
                context, "option",
                name=snippet.pycharm_scope,
                value="true",
            )

        xml = ET.tostring(templateSet, pretty_print=True)
        return xml

    @classmethod
    def from_sublime_snippet_xml(cls, xml, fname):
        """
        Read snippet from sublime snippet xml.
        """
        soup = BeautifulSoup(xml, "xml")

        scope = soup.snippet.scope.text
        description = soup.snippet.description.text
        trigger = soup.snippet.tabTrigger.text
        content = extract_by_prefix_surfix(
            xml, prefix="<!\[CDATA\[\n", surfix="\n\]\]>", include=False)[0]
        args = list()
        for place_holder in re.findall("\$\{\d*:[\s\S]+?\}", content):
            arg = place_holder[:-1].split(":", 1)[1]
            args.append(arg)

        snippet = cls(
            scope=scope,
            description=description,
            trigger=trigger,
            content=content,
            args=args,
            fname=p.fname,
        )
        return snippet


if __name__ == "__main__":
    snippet_list = list()
    for p in snippet_dir.select_by_ext(".sublime-snippet"):
        xml = read(p.abspath)
        snippet = Snippet.from_sublime_snippet_xml(xml, p.fname)
        snippet_list.append(snippet)

    cson = Snippet.to_atom_snippet(snippet_list)
    print(cson)

    xml = Snippet.to_pycharm_snippet(snippet_list)
    # print(xml)
