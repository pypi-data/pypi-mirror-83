import os

from typing import Any, Dict, Generator, List, Union


class Datasource(object):
    name = ""

    client = None

    query_builder = None

    @classmethod
    def create_client(cls, *args, **kwargs):
        connection_dict = cls._get_connection_dict()
        cls.client = cls._get_connector(connection_dict, *args, **kwargs)
        return cls

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """
            FUNCTION TO CREATE A NEW COLLECTION IN DATASOURCE

            params:
                name: str, Name of the collection
        """
        raise NotImplementedError("Base datastore can not create a collection.")

    @classmethod
    def insert(cls, name: str,
               documents: Union[str, Dict[str, Any], List[Dict[str, Any]]],
               *args, **kwargs):
        """
            FUCNTION TO INGEST ENTRIES INTO THE DATASTORE

            params:
                name      : str, Name of the collection in which to ingest.
                documents : dict, Object containing all the info for entries.
        """
        if isinstance(documents, str):
            if (os.path.isfile(documents) and documents.endswith(".json")) or\
                    os.path.isdir(documents):
                return cls._insert_from_io(name, documents, *args, **kwargs)
            err = ("Only json files allowed as string in insert. "
                   "%s is not a valid JSON file." % documents)
            raise ValueError()
            
        if not isinstance(documents, list):
            documents = [documents]
        return cls._insert(name, documents, *args, **kwargs)

    @classmethod
    def read(cls, name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """
            FUNCTION TO READ DATA FROM DATASTORE

            params:
                name  : str, Name of the collection in which to ingest.
                query : dict, Object containing projections, filters to
                        get data from the datastore.

            return: JSON object containing all the records matching the
                    query.
        """
        raise NotImplementedError("Base datastore can not read an entry.")

    @classmethod
    def update(cls, document: Dict[str, Any]):
        """
            FUCNTION TO UPDATE AN ENTRY INTO THE DATASTORE

            params:
                document: dict, Object containing all the info for the entry.
        """
        raise NotImplementedError("Base datastore can not update an entry.")

    @classmethod
    def delete(cls, document_id: str):
        """
            FUNCTION TO DELETE AN ENTRY FROM THE DATASTORE

            params:
                document_id: str, Id of the document to be deleted
        """
        raise NotImplementedError("Base datastore can not delete an entry.")

    @classmethod
    def _get_connector(cls, connection_dict: Dict[str, Any], *args, **kwargs):
        """
            FUNCTION TO GET DATASOURCE CLIENT

            params:
                connection_string: dict, Connection details to connect
                                   with the datasource client.

            return: connection object of the datasource client
        """
        raise NotImplementedError("Can not get connector for base datastore.")

    @classmethod
    def _get_connection_dict(cls):
        """
            FUNCTION TO GET CONNECTION DETAILS FOR THE DATASTORE
        """
        connection_dict = {}
        for detail in ("host", "port", "user", "pass", "auth", "db", "timeout"):
            key = "{}_{}".format(cls.name.upper(), detail.upper())
            connection_dict[detail] = os.environ.get(key)
        return connection_dict

    @classmethod
    def _insert(cls, name: str, documents: List[Dict[str, Any]], *args, **kwargs):
        raise NotImplementedError("Base datastore can not create entries.")

    @classmethod
    def _read_file(cls, name: str, filename: str, *args, **kwargs
                  ) -> Generator[List[Dict[str, Any]], None, None]:
        raise NotImplementedError("Base datastore can not read from file.")

    @classmethod
    def _insert_from_io(cls, name: str, filename: str, *args, **kwargs):
        """
            FUNCTION TO INGEST ENTRIES INTO DATASOURCE USING FILE
        """
        if os.path.isfile(filename):
            document_batches = cls._read_file(name, filename)
        else:
            document_batches = cls._read_dir(name, filename)
        for i, documents in enumerate(document_batches):
            cls._insert(name, documents, *args, **kwargs)
