import psycopg2

class PostgresHelper:
    def __init__(
            self,
            uri: str = None,
            host: str = None,
            port: str = None,
            user: str = None,
            database: str = None,
            password: str = None,
            table: str = None
    ):
        if uri:
            self.connection_mode = 'uri'
        else:
            self.connection_mode = 'log_pass'
        self.uri = uri
        self.host = host
        self.port = port
        self.user = user
        self.database = database
        self.password = password
        self.table = table
        self.connection = None
        self.cursor = None

    def _connect(self):
        if not self.connection:
            if self.connection_mode == 'uri':
                self.connection = psycopg2.connect(self.uri, sslmode='require')
            else:
                self.connection = psycopg2.connect(
                    user=self.user,
                    dbname=self.database,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )


    def _disconnect(self):
        self.connection.close()
        self.connection = None

    def _set_cursor(self):
        if self.connection:
            self.cursor = self.connection.cursor()
        else:
            self._connect()
            self.cursor = self.connection.cursor()

    def _unset_cursor(self):
        pass

    def setup_table(self, columns: dict):
        temp = []
        for key, value in columns.items():
            condition = f"{key}  {value}"
            temp.append(condition)
        columns = ',\n'.join(temp)
        sql = f"""
        CREATE TABLE {self.table} IF NOT EXISTS
        (
        {columns}
        )
        """
        self.cursor.execute(sql)

    @staticmethod
    def _parse_select_query(values):
        if type(values) == str:
            return values
        if type(values) == list:
            return f"({', '.join(values)}"
        else:
            return '*'

    @staticmethod
    def _parse_conditions(conditions):
        if type(conditions) != dict:
            return ''
        temp = []
        for key, value in conditions.items():
            condition = f"{key} = {value}"
            temp.append(condition)
        return f"WHERE {' AND '.join(temp)}"

    def _select(self, kwargs):
        values = self._parse_select_query(kwargs.get('values'))
        conditions = self._parse_conditions(kwargs.get('conditions'))
        sql = f"SELECT {values} FROM {kwargs.get('table')} {conditions}"
        self.cursor.execute(sql)

    def _alter(self, kwargs):
        sql = "ALTER TABLE IF EXISTS {table} "
        pass

    def _update(self, kwargs):
        pass

    def _delete(self, kwargs):
        pass

    def _check_state(self):
        if not self.cursor:
            if not self.connection:
                self._connect()
            self._set_cursor()

    def execute(self, **kwargs):
        self._check_state()
        with self.connection:
            if kwargs.get('action_type') == 'select':
                return self._select(kwargs)
            if kwargs.get('action_type') == 'alter':
                return self._alter(kwargs)
            if kwargs.get('action_type') == 'update':
                return self._update(kwargs)
            if kwargs.get('action_type') == 'delete':
                return self._delete(kwargs)
