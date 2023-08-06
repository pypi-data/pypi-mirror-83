import abc
import configparser
import json
import os
from typing import Dict, List, Optional

from pystratum_backend.RoutineLoaderWorker import RoutineLoaderWorker
from pystratum_backend.StratumStyle import StratumStyle
from pystratum_common.ConstantClass import ConstantClass
from pystratum_common.helper.RoutineLoaderHelper import RoutineLoaderHelper


class CommonRoutineLoaderWorker(RoutineLoaderWorker):
    """
    Class for loading stored routines into a RDBMS instance from (pseudo) SQL files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle, config: configparser.ConfigParser):
        """
        Object constructor.

        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        self.error_file_names = set()
        """
        A set with source names that are not loaded into RDBMS instance.

        :type: set
        """

        self._pystratum_metadata: Dict = {}
        """
        The meta data of all stored routines.
        """

        self._pystratum_metadata_filename: Optional[str] = None
        """
        The filename of the file with the metadata of all stored routines.
        """

        self._rdbms_old_metadata: Dict = {}
        """
        Old metadata about all stored routines.
        """

        self._replace_pairs: Dict = {}
        """
        A map from placeholders to their actual values.
        """

        self._source_file_encoding: Optional[str] = None
        """
        The character set of the source files.
        """

        self._source_directory: Optional[str] = None
        """
        Path where source files can be found.
        """

        self._source_file_extension: Optional[str] = None
        """
        The extension of the source files.
        """

        self._source_file_names: Dict = {}
        """
        All found source files.
        """

        self._constants_class_name: str = ''
        """
        The name of the class that acts like a namespace for constants.
        """

        self.__shadow_directory: Optional[str] = None
        """
        The name of the directory were copies with pure SQL of the stored routine sources must be stored.
        """

        self._io: StratumStyle = io
        """
        The output decorator.
        """

        self._config = config
        """
        The configuration object.

        :type: ConfigParser 
        """

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, file_names: Optional[List[str]] = None) -> int:
        """
        Loads stored routines into the current schema.

        :param list[str] file_names: The sources that must be loaded. If empty all sources (if required) will loaded.

        :rtype: int The status of exit.
        """
        self._io.title('Loader')

        self._read_configuration_file()

        if file_names:
            self.__load_list(file_names)
        else:
            self.__load_all()

        if self.error_file_names:
            self.__log_overview_errors()

        self._io.writeln('')

        return 1 if self.error_file_names else 0

    # ------------------------------------------------------------------------------------------------------------------
    def __log_overview_errors(self) -> None:
        """
        Show info about sources files of stored routines that were not loaded successfully.
        """
        if self.error_file_names:
            self._io.warning('Routines in the files below are not loaded:')
            self._io.listing(sorted(self.error_file_names))

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def connect(self) -> None:
        """
        Connects to the RDBMS instance.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def disconnect(self) -> None:
        """
        Disconnects from the RDBMS instance.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _add_replace_pair(self, name: str, value: str, quote: bool):
        """
        Adds a replace part to the map of replace pairs.

        :param name: The name of the replace pair.
        :param value: The value of value of the replace pair.
        """
        key = '@' + name + '@'
        key = key.lower()

        class_name = value.__class__.__name__

        if class_name in ['int', 'float']:
            value = str(value)
        elif class_name in ['bool']:
            value = '1' if value else '0'
        elif class_name in ['str']:
            if quote:
                value = "'" + value + "'"
        else:
            self._io.log_verbose("Ignoring constant {} which is an instance of {}".format(name, class_name))

        self._replace_pairs[key] = value

    # ------------------------------------------------------------------------------------------------------------------
    def __load_list(self, file_names: Optional[List[str]]) -> None:
        """
        Loads all stored routines in a list into the RDBMS instance.
        :param list[str] file_names: The list of files to be loaded.
        """
        self.connect()
        self.find_source_files_from_list(file_names)
        self._get_column_type()
        self.__read_stored_routine_metadata()
        self.__get_constants()
        self._get_old_stored_routine_info()
        self._get_correct_sql_mode()
        self.__load_stored_routines()
        self.__write_stored_routine_metadata()
        self.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def __load_all(self) -> None:
        """
        Loads all stored routines into the RDBMS instance.
        """
        self.connect()
        self.__find_source_files()
        self._get_column_type()
        self.__read_stored_routine_metadata()
        self.__get_constants()
        self._get_old_stored_routine_info()
        self._get_correct_sql_mode()
        self.__load_stored_routines()
        self._drop_obsolete_routines()
        self.__remove_obsolete_metadata()
        self.__write_stored_routine_metadata()
        self.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self) -> None:
        """
        Reads parameters from the configuration file.
        """
        self._source_directory = self._config.get('loader', 'source_directory')
        self._source_file_extension = self._config.get('loader', 'extension')
        self._source_file_encoding = self._config.get('loader', 'encoding')
        self.__shadow_directory = self._config.get('loader', 'shadow_directory', fallback=None)

        self._pystratum_metadata_filename = self._config.get('wrapper', 'metadata')

        self._constants_class_name = self._config.get('constants', 'class')

    # ------------------------------------------------------------------------------------------------------------------
    def __find_source_files(self) -> None:
        """
        Searches recursively for all source files in a directory.
        """
        for dir_path, _, files in os.walk(self._source_directory):
            for name in files:
                if name.lower().endswith(self._source_file_extension):
                    basename = os.path.splitext(os.path.basename(name))[0]
                    relative_path = os.path.relpath(os.path.join(dir_path, name))

                    if basename in self._source_file_names:
                        self._io.error("Files '{0}' and '{1}' have the same basename.".
                                       format(self._source_file_names[basename], relative_path))
                        self.error_file_names.add(relative_path)
                    else:
                        self._source_file_names[basename] = relative_path

    # ------------------------------------------------------------------------------------------------------------------
    def __read_stored_routine_metadata(self) -> None:
        """
        Reads the metadata of stored routines from the metadata file.
        """
        if os.path.isfile(self._pystratum_metadata_filename):
            with open(self._pystratum_metadata_filename, 'r') as file:
                self._pystratum_metadata = json.load(file)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_column_type(self) -> None:
        """
        Selects schema, table, column names and the column type from the RDBMS instance and saves them as replace pairs.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def create_routine_loader_helper(self,
                                     routine_name: str,
                                     pystratum_old_metadata: Dict,
                                     rdbms_old_metadata: Dict) -> RoutineLoaderHelper:
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from database instance.

        :rtype: RoutineLoaderHelper
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __load_stored_routines(self) -> None:
        """
        Loads all stored routines into the RDBMS instance.
        """
        self._io.writeln('')

        for routine_name in sorted(self._source_file_names):
            if routine_name in self._pystratum_metadata:
                old_metadata = self._pystratum_metadata[routine_name]
            else:
                old_metadata = None

            if routine_name in self._rdbms_old_metadata:
                old_routine_info = self._rdbms_old_metadata[routine_name]
            else:
                old_routine_info = None

            routine_loader_helper = self.create_routine_loader_helper(routine_name, old_metadata, old_routine_info)
            routine_loader_helper.shadow_directory = self.__shadow_directory

            metadata = routine_loader_helper.load_stored_routine()

            if not metadata:
                self.error_file_names.add(self._source_file_names[routine_name])
                if routine_name in self._pystratum_metadata:
                    del self._pystratum_metadata[routine_name]
            else:
                self._pystratum_metadata[routine_name] = metadata

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _get_old_stored_routine_info(self) -> None:
        """
        Retrieves information about all stored routines in the current schema.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_correct_sql_mode(self) -> None:
        """
        Gets the SQL mode in the order as preferred by MySQL. This method is specific for MySQL.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _drop_obsolete_routines(self) -> None:
        """
        Drops obsolete stored routines (i.e. stored routines that exits in the current schema but for
        which we don't have a source file).
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def __remove_obsolete_metadata(self) -> None:
        """
        Removes obsolete entries from the metadata of all stored routines.
        """
        clean = {}
        for key, _ in self._source_file_names.items():
            if key in self._pystratum_metadata:
                clean[key] = self._pystratum_metadata[key]

        self._pystratum_metadata = clean

    # ------------------------------------------------------------------------------------------------------------------
    def __write_stored_routine_metadata(self) -> None:
        """
        Writes the metadata of all stored routines to the metadata file.
        """
        with open(self._pystratum_metadata_filename, 'w') as stream:
            json.dump(self._pystratum_metadata, stream, indent=4, sort_keys=True)

    # ------------------------------------------------------------------------------------------------------------------
    def find_source_files_from_list(self, file_names) -> None:
        """
        Finds all source files that actually exists from a list of file names.

        :param list[str] file_names: The list of file names.
        """
        for file_name in file_names:
            if os.path.exists(file_name):
                routine_name = os.path.splitext(os.path.basename(file_name))[0]
                if routine_name not in self._source_file_names:
                    self._source_file_names[routine_name] = file_name
                else:
                    self._io.error("Files '{0}' and '{1}' have the same basename.".
                                   format(self._source_file_names[routine_name], file_name))
                    self.error_file_names.add(file_name)
            else:
                self._io.error("File not exists: '{0}'".format(file_name))
                self.error_file_names.add(file_name)

    # ------------------------------------------------------------------------------------------------------------------
    def __get_constants(self) -> None:
        """
        Gets the constants from the class that acts like a namespace for constants and adds them to the replace pairs.
        """
        helper = ConstantClass(self._constants_class_name, self._io)
        helper.reload()
        constants = helper.constants()

        for name, value in constants.items():
            self._add_replace_pair(name, value, True)

        self._io.text('Read {0} constants for substitution from <fso>{1}</fso>'.
                      format(len(constants), helper.file_name()))

# ----------------------------------------------------------------------------------------------------------------------
