import pytest
from typing import List, Optional
from pytest_mock import MockerFixture
from pygls.workspace import Document, Position

from ...services.context import (
    XmlContextService,
    XmlContext,
    XmlContextParser,
    ContextTokenType,
    XsdTree,
    XsdNode,
    Range,
)


# The content starts at line 1 for convenience
FAKE_CONTENT = """
<tool id="test">
    <description/>
    <test value="0"/>
    <help><![CDATA[
        Sample text
    ]]></help>
    <inputs></inputs>
</tool>'
"""
FAKE_DOC_URI = "file://fake_doc.xml"
FAKE_DOCUMENT = Document(FAKE_DOC_URI, FAKE_CONTENT)


def get_fake_document(content: str) -> Document:
    return Document(FAKE_DOC_URI, content)


def print_context_params(document: Document, position: Position) -> None:
    print(f"Test context at position [line={position.line}, char={position.character}]")
    print(f"Document:\n{document.source}")


def get_mock_xsd_tree(mocker: MockerFixture) -> XsdTree:
    root = XsdNode(name="root", element=mocker.Mock())
    child = XsdNode(name="child", parent=root, element=mocker.Mock())
    XsdNode(name="sibling", parent=root, element=mocker.Mock())
    XsdNode(name="subchild", parent=child, element=mocker.Mock())
    return XsdTree(root)


class TestXmlContextClass:
    def test_init_sets_properties(self) -> None:
        expected_line_content = "test"
        expected_position = Position()

        context = XmlContext(document_line=expected_line_content, position=expected_position)

        assert context.document_line == expected_line_content
        assert context.target_position == expected_position
        assert not context.is_empty

    def test_context_with_unknown_token_type_returns_all_false(self) -> None:
        context = XmlContext(token_type=ContextTokenType.UNKNOWN)

        assert not context.is_tag()
        assert not context.is_attribute_key()
        assert not context.is_attribute_value()

    def test_context_with_tag_token_type_returns_is_tag(self) -> None:
        context = XmlContext(token_type=ContextTokenType.TAG)

        assert context.is_tag()
        assert not context.is_attribute_key()
        assert not context.is_attribute_value()

    def test_context_with_attr_key_token_type_returns_is_attr_key(self) -> None:
        context = XmlContext(token_type=ContextTokenType.ATTRIBUTE_KEY)

        assert not context.is_tag()
        assert context.is_attribute_key()
        assert not context.is_attribute_value()

    def test_context_with_attr_value_token_type_returns_is_attr_value(self) -> None:
        context = XmlContext(token_type=ContextTokenType.ATTRIBUTE_VALUE)

        assert not context.is_tag()
        assert not context.is_attribute_key()
        assert context.is_attribute_value()


class TestXmlContextServiceClass:
    def test_init_sets_properties(self, mocker: MockerFixture) -> None:
        expected = mocker.Mock()

        service = XmlContextService(expected)

        assert service.xsd_tree

    def test_get_xml_context_returns_empty_document_context(self, mocker: MockerFixture) -> None:
        xml_content = ""
        position = Position()
        xsd_tree_mock = mocker.Mock()
        service = XmlContextService(xsd_tree_mock)

        context = service.get_xml_context(Document(FAKE_DOC_URI, xml_content), position)

        assert context.is_empty

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (get_fake_document("<root><child"), Position(line=0, character=0), "root",),
            (get_fake_document("<root><child"), Position(line=0, character=6), "root",),
            (get_fake_document("<root><child"), Position(line=0, character=7), "child",),
            (get_fake_document("<root><child"), Position(line=0, character=12), "child",),
            (get_fake_document("<root><child "), Position(line=0, character=13), "child",),
            (get_fake_document('<root attr="4"><child '), Position(line=0, character=14), "root",),
            (get_fake_document('<root attr="4"><child '), Position(line=0, character=16), "child",),
            (get_fake_document('<root attr="4">\n<child/><other'), Position(line=1, character=7), "child",),
            (get_fake_document('<root attr="4">\n<child/><other'), Position(line=1, character=8), "root",),
            (get_fake_document('<root attr="4">\n<child/><other'), Position(line=1, character=9), "root",),
            (get_fake_document('<root attr="4">\n<child/><sibling'), Position(line=1, character=9), "sibling",),
            (get_fake_document('<root attr="4">\n    <\n<child'), Position(line=1, character=5), "root",),
        ],
    )
    def test_get_xml_context_returns_context_with_expected_node(
        self, mocker: MockerFixture, document, position, expected
    ) -> None:
        xsd_tree_mock = get_mock_xsd_tree(mocker)
        service = XmlContextService(xsd_tree_mock)
        print(xsd_tree_mock.render())
        print_context_params(document, position)

        context = service.get_xml_context(document, position)

        assert context
        assert context.node
        assert context.node.name == expected


class TestXmlContextParserClass:
    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (FAKE_DOCUMENT, Position(line=1, character=0), "tool"),
            (FAKE_DOCUMENT, Position(line=1, character=1), "tool"),
            (FAKE_DOCUMENT, Position(line=1, character=5), None),
            (FAKE_DOCUMENT, Position(line=1, character=6), "id"),
            (FAKE_DOCUMENT, Position(line=1, character=8), "id"),
            (FAKE_DOCUMENT, Position(line=1, character=9), None),
            (FAKE_DOCUMENT, Position(line=1, character=10), "test"),
            (FAKE_DOCUMENT, Position(line=1, character=14), "test"),
            (FAKE_DOCUMENT, Position(line=1, character=15), None),
            (FAKE_DOCUMENT, Position(line=2, character=5), "description"),
            (FAKE_DOCUMENT, Position(line=2, character=15), "description"),
            (FAKE_DOCUMENT, Position(line=2, character=17), None),
            (FAKE_DOCUMENT, Position(line=3, character=4), None),
            (FAKE_DOCUMENT, Position(line=3, character=5), "test"),
            (FAKE_DOCUMENT, Position(line=3, character=8), "test"),
            (FAKE_DOCUMENT, Position(line=3, character=9), None),
            (FAKE_DOCUMENT, Position(line=3, character=10), "value"),
            (FAKE_DOCUMENT, Position(line=3, character=15), "value"),
            (FAKE_DOCUMENT, Position(line=3, character=16), None),
            (FAKE_DOCUMENT, Position(line=3, character=17), "0"),
            (FAKE_DOCUMENT, Position(line=3, character=18), "0"),
            (FAKE_DOCUMENT, Position(line=3, character=19), None),
        ],
    )
    def test_parse_well_formed_xml_return_expected_context_token_name(
        self, document: Document, position: Position, expected: Optional[str]
    ) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.token_name == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (get_fake_document('<other id="1"'), Position(line=0, character=0), None),
            (get_fake_document('<other id="1"'), Position(line=0, character=1), "other"),
            (get_fake_document('<other id="1"'), Position(line=0, character=6), "other"),
            (get_fake_document('<other id="1"'), Position(line=0, character=7), "id"),
            (get_fake_document('<other id="1"'), Position(line=0, character=9), "id"),
            (get_fake_document('<other id="1"'), Position(line=0, character=11), "1"),
            (get_fake_document('<other id="1"'), Position(line=0, character=12), "1"),
            (get_fake_document('<other id="1"'), Position(line=0, character=13), None),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=2), "first",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=8), "id",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=11), "1",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=12), "1",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=14), "test",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=20), "value",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=0, character=25), "value",),
            (get_fake_document('<first id="1" test="value">\n    <second'), Position(line=1, character=5), "second",),
            (get_fake_document('<first id="one_test">\n    <second'), Position(line=0, character=11), "one_test",),
            (get_fake_document('<first id="one_test">\n    <second'), Position(line=0, character=19), "one_test",),
            (get_fake_document('<first id="one test">\n    <second'), Position(line=0, character=11), "one test",),
            (get_fake_document('<first id="one test">\n    <second'), Position(line=0, character=19), "one test",),
            (get_fake_document('<first id="one test'), Position(line=0, character=19), "one test",),
            (get_fake_document('<first id="value"><second/></first>'), Position(line=0, character=19), "second",),
            (get_fake_document('<first id="value"><second/></first>'), Position(line=0, character=29), "first",),
        ],
    )
    def test_parse_incomplete_xml_return_expected_context_token_name(
        self, document: Document, position: Position, expected: str
    ) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.token_name == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (
                get_fake_document('<first id="1" test="value">\n    <second'),
                Position(line=0, character=0),
                ContextTokenType.TAG,
            ),
            (
                get_fake_document('<first id="1" test="value">\n    <second'),
                Position(line=0, character=2),
                ContextTokenType.TAG,
            ),
            (
                get_fake_document('<first id="1" test="value">\n    <second'),
                Position(line=0, character=8),
                ContextTokenType.ATTRIBUTE_KEY,
            ),
            (
                get_fake_document('<first id="1" test="value">\n    <second'),
                Position(line=0, character=11),
                ContextTokenType.ATTRIBUTE_VALUE,
            ),
            (
                get_fake_document('<first id="one_test">\n    <second'),
                Position(line=0, character=19),
                ContextTokenType.ATTRIBUTE_VALUE,
            ),
            (
                get_fake_document('<first id="1" test="value">\n    <second'),
                Position(line=1, character=0),
                ContextTokenType.UNKNOWN,
            ),
            (
                get_fake_document('<first id="1" test="value">\n    <second'),
                Position(line=1, character=4),
                ContextTokenType.UNKNOWN,
            ),
            (get_fake_document('<first id="one test'), Position(line=0, character=19), ContextTokenType.ATTRIBUTE_VALUE,),
            (get_fake_document('<first id="1">value</first>'), Position(line=0, character=14), ContextTokenType.UNKNOWN,),
            (get_fake_document('<first id="value"><second/></first>'), Position(line=0, character=19), ContextTokenType.TAG,),
            (get_fake_document('<first id="value"><second/></first>'), Position(line=0, character=29), ContextTokenType.TAG,),
            (get_fake_document('<first id="value"><second/></first'), Position(line=0, character=29), ContextTokenType.TAG,),
        ],
    )
    def test_parse_incomplete_xml_return_expected_context_token_type(
        self, document: Document, position: Position, expected: ContextTokenType
    ) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.token_type == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (get_fake_document(""), Position(line=0, character=0), True),
            (get_fake_document(""), Position(line=0, character=10), True),
            (get_fake_document("<"), Position(line=0, character=0), True),
            (get_fake_document("   "), Position(line=0, character=0), True),
            (get_fake_document("\n\n"), Position(line=0, character=0), True),
            (get_fake_document("\n\n"), Position(line=1, character=0), True),
        ],
    )
    def test_parse_empty_xml_return_empty_context(self, document: Document, position: Position, expected: bool) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.is_empty == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (get_fake_document("<first><second><third>"), Position(line=0, character=1), ["first"],),
            (get_fake_document("<first><second><third>"), Position(line=0, character=8), ["first", "second"],),
            (get_fake_document("<first><second><third>"), Position(line=0, character=16), ["first", "second", "third"],),
            (get_fake_document("<first><second/><third>"), Position(line=0, character=8), ["first", "second"],),
            (get_fake_document("<first><second/><third>"), Position(line=0, character=17), ["first", "third"],),
            (get_fake_document("<first><second></second><third"), Position(line=0, character=25), ["first", "third"],),
            (get_fake_document("<first><second></second><third"), Position(line=0, character=18), ["first", "second"],),
            (get_fake_document("<first><second\n<third/></first>"), Position(line=1, character=10), ["first"],),
            (get_fake_document("<first><second/></first>"), Position(line=0, character=18), ["first"],),
            (get_fake_document("<first><second/>\n</first>"), Position(line=1, character=2), ["first"],),
            (get_fake_document('<first><second attr="value"/><third'), Position(line=0, character=29), ["first"],),
            (get_fake_document('<first><second attr="value"/><third'), Position(line=0, character=30), ["first", "third"],),
            (get_fake_document('<first attr="value"><third>\n'), Position(line=0, character=26), ["first", "third"],),
            (get_fake_document("<first>\n    <second>  \n</first>"), Position(line=1, character=11), ["first", "second"],),
            (FAKE_DOCUMENT, Position(line=4, character=10), ["tool", "help"]),
            (FAKE_DOCUMENT, Position(line=4, character=18), ["tool", "help"]),
            (FAKE_DOCUMENT, Position(line=6, character=5), ["tool", "help"]),
            (FAKE_DOCUMENT, Position(line=6, character=7), ["tool", "help"]),
            (
                get_fake_document('<first>\n<second attr="value"\n</second>'),
                Position(line=2, character=2),
                ["first", "second"],
            ),
        ],
    )
    def test_parse_return_expected_tag_stack_context(
        self, document: Document, position: Position, expected: List[str]
    ) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.node_stack == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (
                get_fake_document("<first><second><third>"),
                Position(line=0, character=1),
                Range(start=Position(line=0, character=1), end=Position(line=0, character=6)),
            ),
            (
                get_fake_document("<first><second><third>"),
                Position(line=0, character=8),
                Range(start=Position(line=0, character=8), end=Position(line=0, character=14)),
            ),
            (
                get_fake_document("<first><second/><third>"),
                Position(line=0, character=8),
                Range(start=Position(line=0, character=8), end=Position(line=0, character=14)),
            ),
            (
                get_fake_document("<first><second/><third>"),
                Position(line=0, character=17),
                Range(start=Position(line=0, character=17), end=Position(line=0, character=22)),
            ),
            (
                get_fake_document("<first><second></second><third>"),
                Position(line=0, character=25),
                Range(start=Position(line=0, character=25), end=Position(line=0, character=30)),
            ),
            (
                get_fake_document("<first><second/>\n</first>"),
                Position(line=1, character=2),
                Range(start=Position(line=1, character=0), end=Position(line=1, character=8)),
            ),
            (
                get_fake_document('<first attr="value"/><third'),
                Position(line=0, character=8),
                Range(start=Position(line=0, character=7), end=Position(line=0, character=11)),
            ),
            (
                get_fake_document('<first>\n<second attr="value"/>\n<third'),
                Position(line=1, character=15),
                Range(start=Position(line=1, character=14), end=Position(line=1, character=19)),
            ),
            (
                get_fake_document('<first attr1="value1" attr2="value2">'),
                Position(line=0, character=24),
                Range(start=Position(line=0, character=22), end=Position(line=0, character=27)),
            ),
            (
                get_fake_document('<first attr1="value1" attr2="value2">'),
                Position(line=0, character=30),
                Range(start=Position(line=0, character=29), end=Position(line=0, character=35)),
            ),
        ],
    )
    def test_parse_return_expected_tag_range_context(self, document: Document, position: Position, expected: Range) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.token_range == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=0, character=1),
                False,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=0, character=8),
                False,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=0, character=14),
                True,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=0),
                True,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=4),
                True,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=5),
                False,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=6),
                False,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=24),
                False,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=25),
                True,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=29),
                True,
            ),
            (
                get_fake_document('<first id="1">\n    <second attr="value">test</second>\n<third'),
                Position(line=1, character=30),
                False,
            ),
            (FAKE_DOCUMENT, Position(line=4, character=10), True),
            (FAKE_DOCUMENT, Position(line=4, character=18), True),
            (FAKE_DOCUMENT, Position(line=6, character=5), True),
            (FAKE_DOCUMENT, Position(line=6, character=7), True),
        ],
    )
    def test_parse_returns_context_with_expected_is_node_content(
        self, document: Document, position: Position, expected: bool
    ) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.is_node_content == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (get_fake_document('<first id="1" test="2"'), Position(line=0, character=2), ["id", "test"],),
            (get_fake_document('<first id="1" test="2"'), Position(line=0, character=14), ["id", "test"],),
            (get_fake_document('<first id="1" test="2"'), Position(line=0, character=22), ["id", "test"],),
            (get_fake_document('<first id="1" test="2"/>'), Position(line=0, character=2), ["id", "test"],),
            (get_fake_document('<first id="1" test="2">\n</first>'), Position(line=0, character=10), ["id", "test"],),
        ],
    )
    def test_parse_return_expected_attributes_at_node(
        self, document: Document, position: Position, expected: List[str]
    ) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.attr_list == expected

    @pytest.mark.parametrize(
        "document, position, expected",
        [
            (get_fake_document("<first> </first>"), Position(line=0, character=7), False,),
            (get_fake_document("<first></first>"), Position(line=0, character=8), True,),
            (get_fake_document("<first></first>"), Position(line=0, character=14), True,),
            (get_fake_document("<first></first >"), Position(line=0, character=14), True,),
            (get_fake_document("<first></first"), Position(line=0, character=10), True,),
            (get_fake_document("<first/>"), Position(line=0, character=7), True,),
            (get_fake_document("<first/ >"), Position(line=0, character=7), True,),
            (get_fake_document('<first attr="1"/>'), Position(line=0, character=15), False,),
            (get_fake_document('<first attr="1" />'), Position(line=0, character=15), False,),
            (get_fake_document('<first attr="1"/'), Position(line=0, character=15), False,),
        ],
    )
    def test_parse_return_expected_is_closin_tag(self, document: Document, position: Position, expected: bool) -> None:
        print_context_params(document, position)
        parser = XmlContextParser()

        context = parser.parse(document, position)

        assert context.is_closing_tag == expected
