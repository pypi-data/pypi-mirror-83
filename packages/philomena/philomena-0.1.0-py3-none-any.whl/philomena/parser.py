# TODO: implement?
# from html.parser import HTMLParser
# import html.entities
#
# closable = []
#
# from bs4 import BeautifulSoup
# class Element:
#     unclosable = ["img", "input", "br", "hr", "meta", "etc"]
#
#     def __init__(self, html):
#         self.html
#
#
# class IncompleteElement:
#     def __init__(self, tag, attrs, data):
#         self.tag = tag
#         self.attrs = attrs
#         self.data = data
#
#     def __repr__(self):
#         return f"IncompleteElement(tag={self.tag}, attrs={self.attrs}"
#
#     def __str__(self):
#         return f"<{self._format_start_tag()}>{self.data}</{self.tag}>"
#
#     def _format_attrs(self):
#         return " ".join([f"{attr}='{value}'" for attr, value in self.attrs])
#
#     def _format_start_tag(self):
#         return " ".join([self.tag, self._format_attrs()])
#
#
# ls = [
#     "<html><body>"
#     "<div class='container'>"
#     "<p class='text-center p-0'>helllo<span>HELLO</span></p>"
#     "<img alt='hello' src='/hello.png'>"
#     "</div>"
#     "</body></html>"
# ]
#
#
# class Parser(HTMLParser):
#     STACK = []
#
#     # Overridable -- handle start tag
#     def handle_starttag(self, tag, attrs):
#         print(IncompleteElement(tag, attrs, ""))
#         # print("start_tag", tag)
#         # print("attrs", attrs)
#
#     # Overridable -- handle end tag
#     def handle_endtag(self, tag):
#         print("end_tag", tag)
#
#     # Overridable -- handle character reference
#     def handle_charref(self, name):
#         pass
#
#     # Overridable -- handle entity reference
#     def handle_entityref(self, name):
#         pass
#
#     # Overridable -- handle data
#     def handle_data(self, data):
#         print("data", data)
#
#     # Overridable -- handle comment
#     def handle_comment(self, data):
#         pass
#
#     # Overridable -- handle declaration
#     def handle_decl(self, decl):
#         pass
#
#     # Overridable -- handle processing instruction
#     def handle_pi(self, data):
#         pass
#
#     def handle_startendtag(self, tag, attrs):
#         pass
#
#
# parser = Parser()
# for i in ls:
#     parser.feed(i)
#
