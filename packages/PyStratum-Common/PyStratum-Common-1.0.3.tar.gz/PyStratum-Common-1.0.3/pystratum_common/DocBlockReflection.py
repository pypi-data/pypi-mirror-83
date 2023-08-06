import os
import re
from typing import List, Tuple


class DocBlockReflection:
    """
    A simple DocBlock reflection.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, comment: List[str]):
        """
        Object constructor.

        :param list[str] comment: The comment as a list of strings.
        """
        self._comment: List[str] = comment
        """
        The DocBlock as a list of strings.
        """

        self._description: str = ''
        """
        The description.
        """

        self._tags: List[Tuple[str, str]] = list()
        """
        The tags in the DocBlock
        """

        self.__reflect()

    # ------------------------------------------------------------------------------------------------------------------
    def get_description(self) -> str:
        """
        Returns the description.

        :rtype: str
        """
        return self._description

    # ------------------------------------------------------------------------------------------------------------------
    def get_tag(self, name: str) -> str:
        """
        Returns a tag.

        @param str name: The name of the tag.

        :rtype: str
        """
        for tag in self._tags:
            if tag[0] == name:
                return tag[1]

        return ''

    # ------------------------------------------------------------------------------------------------------------------
    def get_tags(self, name: str) -> List[str]:
        """
        Returns a list of tags.

        @param str name: The name of the tag.

        :rtype: list[str]
        """
        tags = list()
        for tag in self._tags:
            if tag[0] == name:
                tags.append(tag[1])

        return tags

    # ------------------------------------------------------------------------------------------------------------------
    def __reflect(self) -> None:
        """
        Parses the DocBlock.
        """
        self.__clean_doc_block()
        self.__extract_description()
        self.__extract_tags()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __remove_leading_empty_lines(lines: List[str]) -> List[str]:
        """
        Removes leading empty lines from a list of lines.

        :param list[str] lines: The lines.
        """
        tmp = list()
        empty = True
        for i in range(0, len(lines)):
            empty = empty and lines[i] == ''
            if not empty:
                tmp.append(lines[i])

        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __remove_trailing_empty_lines(lines: List[str]) -> List[str]:
        """
        Removes leading empty lines from a list of lines.

        :param list[str] lines: The lines.
        """
        lines.reverse()
        tmp = DocBlockReflection.__remove_leading_empty_lines(lines)
        lines.reverse()
        tmp.reverse()

        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    def __clean_doc_block(self) -> None:
        """
        Cleans the DocBlock from leading and trailing white space and comment tokens.
        """
        # Return immediately if the DockBlock is empty.
        if not self._comment:
            return

        for i in range(1, len(self._comment) - 1):
            self._comment[i] = re.sub(r'^\s*\*', '', self._comment[i])

        self._comment[0] = re.sub(r'^\s*/\*\*', '', self._comment[0])

        self._comment[-1] = re.sub(r'\*/\s*$', '', self._comment[-1])

        for i, line in enumerate(self._comment):
            self._comment[i] = line.strip()

        self._comment = self.__remove_leading_empty_lines(self._comment)
        self._comment = self.__remove_trailing_empty_lines(self._comment)

    # ------------------------------------------------------------------------------------------------------------------
    def __extract_description(self) -> None:
        """
        Extracts the description from the DocBlock. The description start at the first line and stops at the first tag
        or the end of the DocBlock.
        """
        tmp = list()
        for line in self._comment:
            if len(line) >= 1 and line[0] == '@':
                break

            tmp.append(line)

        tmp = self.__remove_trailing_empty_lines(tmp)

        self._description = os.linesep.join(tmp)

    # ------------------------------------------------------------------------------------------------------------------
    def __extract_tags(self) -> None:
        """
        Extract tags from the DocBlock.
        """
        tags = list()
        current = None
        for line in self._comment:
            parts = re.match(r'^@(\w+)', line)
            if parts:
                current = (parts.group(1), list())
                tags.append(current)

            if current:
                if line == '':
                    current = None
                else:
                    current[1].append(line)

        for tag in tags:
            self._tags.append((tag[0], os.linesep.join(tag[1])))

# ----------------------------------------------------------------------------------------------------------------------
