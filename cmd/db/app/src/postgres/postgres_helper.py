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
    def __parse_array(input_array: list):
        return "{values}".format(values=','.join(input_array))
    @staticmethod
    def __parse_select_query(values):
        if type(values) == str:
            return values
        if type(values) == list:
            return f"({', '.join(values)}"
        else:
            return '*'

    @staticmethod
    def __parse_values(values):
        return f"({', '.join(values)})"

    @staticmethod
    def __parse_fields(fields):
        return f"({', '.join(fields)})"

    @staticmethod
    def __parse_conditions(conditions):
        if type(conditions) != dict:
            return ''
        temp = []
        for key, value in conditions.items():
            condition = f"{key} = {value}"
            temp.append(condition)
        return f"WHERE {' AND '.join(temp)}"

    @staticmethod
    def __parse_target(target):
        return f"{target.get('field')} = {target.get('value')}"

    def __generate_select_sql(self, kwargs):
        values = self.__parse_select_query(kwargs.get('values'))
        conditions = self.__parse_conditions(kwargs.get('conditions'))
        return f"SELECT {values} FROM {kwargs.get('table')} {conditions}"

    def __generate_insert_sql(self, kwargs):
        fields = self.__parse_fields(kwargs.get('fields'))
        values = self.__parse_values(kwargs.get('values'))
        return f"INSERT INTO {kwargs.get('table')} {fields} VALUES {values}"

    def __generate_update_sql(self, kwargs):
        if self._select_one(kwargs):
            conditions = self.__parse_conditions(kwargs.get('conditions'))
            target = self.__parse_target(kwargs.get('target'))
            return f"UPDATE {kwargs.get('table')} SET {target} {conditions}"

    def __generate_delete_sql(self, kwargs):
        if self._select_one(kwargs):
            conditions = self.__parse_conditions(kwargs.get('conditions'))
            return f"DELETE FROM {kwargs.get('table')} {conditions}"
        return None

    def _select_one(self, kwargs):
        with self.connection:
            self.cursor.execute(self.__generate_select_sql(kwargs))
            return self.cursor.fetchone()

    def _select_all(self, kwargs):
        with self.connection:
            self.cursor.execute(self.__generate_select_sql(kwargs))
            return self.cursor.fetchall()

    def _insert(self, kwargs):
        with self.connection:
            sql = self.__generate_insert_sql(kwargs)
            print(sql)
            self.cursor.execute(sql)
            return self.connection.commit()

    def _delete(self, kwargs):
        sql = self.__generate_delete_sql(kwargs)
        if sql:
            with self.connection:
                self.cursor.execute(sql)
                return self.connection.commit()

    def _update(self, kwargs):
        sql = self.__generate_update_sql(kwargs)
        if sql:
            with self.connection:
                self.cursor.execute(sql)
                return self.connection.commit()


    def _check_state(self):
        if not self.cursor:
            if not self.connection:
                self._connect()
            self._set_cursor()

    def execute(self, **kwargs):
        self._check_state()
        if kwargs.get('action_type') == 'select_one':
            return self._select_one(kwargs)
        if kwargs.get('action_type') == 'select_all':
            return self._select_all(kwargs)
        if kwargs.get('action_type') == 'alter':
            return self._insert(kwargs)
        if kwargs.get('action_type') == 'update':
            return self._update(kwargs)
        if kwargs.get('action_type') == 'delete':
            return self._delete(kwargs)

