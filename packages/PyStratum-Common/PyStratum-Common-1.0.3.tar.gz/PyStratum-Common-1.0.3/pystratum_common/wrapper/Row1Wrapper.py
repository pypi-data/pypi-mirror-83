from abc import ABC

from pystratum_common.wrapper.Wrapper import Wrapper


class Row1Wrapper(Wrapper, ABC):
    """
    Wrapper method generator for stored procedures that are selecting 1 row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _return_type_hint(self) -> str:
        """
        Returns the return type hint of the wrapper method.

        :rtype: str
        """
        return 'Any'

    # ------------------------------------------------------------------------------------------------------------------
    def _get_docstring_return_type(self) -> str:
        """
        Returns the return type of the wrapper methods the be used in the docstring.

        :rtype: str
        """
        return 'dict[str,*]'

# ----------------------------------------------------------------------------------------------------------------------
