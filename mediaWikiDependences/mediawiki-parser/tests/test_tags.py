# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class TagsTests(ParserTestCase):
    def test_basic_tag(self):
        source = '<a>'
        result = "[tag_name:'a']"
        self.parsed_equal_string(source, result, 'tag')

    def test_open_tag_with_standalone_attribute(self):
        # Not correct in XML but correct in HTML
        source = '<table noborder>'
        result = """tag_open:
   tag_name:table
   optional_attributes:
      optional_attribute:
         attribute_name:noborder"""
        self.parsed_equal_tree(source, result, 'tag')

    def test_open_tag_with_attribute(self):
        source = '<a style="color:red">'
        result = """tag_open:
   tag_name:a
   optional_attributes:
      optional_attribute:
         attribute_name:style
         value_quote:color:red"""
        self.parsed_equal_tree(source, result, 'tag')

    def test_autoclose_tag_with_attribute(self):
        source = '<img src="http://www.mozilla.org/test.png"/>'
        result = """tag_autoclose:
   tag_name:img
   optional_attributes:
      optional_attribute:
         attribute_name:src
         value_quote:http://www.mozilla.org/test.png"""
        self.parsed_equal_tree(source, result, 'tag')

    def test_url_in_tag_attribute(self):
        source = '<a href="http://www.mozilla.org" style="color:red">'
        result = """tag_open:
   tag_name:a
   optional_attributes:
      optional_attribute:
         attribute_name:href
         value_quote:http://www.mozilla.org
      optional_attribute:
         attribute_name:style
         value_quote:color:red"""
        self.parsed_equal_tree(source, result, 'tag')

    def test_multiple_tags(self):
        source = 'a <tag name="mytag" attribute=value /> and <span style=\'color: red\'>text</span>...'
        result = """@inline@:
   raw_text:a 
   tag_autoclose:
      tag_name:tag
      optional_attributes:
         optional_attribute:
            attribute_name:name
            value_quote:mytag
         optional_attribute:
            attribute_name:attribute
            value_noquote:value
   raw_text: and 
   tag_open:
      tag_name:span
      optional_attributes:
         optional_attribute:
            attribute_name:style
            value_apostrophe:color: red
   raw_text:text
   tag_close:
      tag_name:span
   raw_text:..."""
        self.parsed_equal_tree(source, result, 'inline')
