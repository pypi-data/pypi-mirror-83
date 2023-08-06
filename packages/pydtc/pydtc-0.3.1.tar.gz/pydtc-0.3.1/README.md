This pacakge provides various tools to perform task on data, in easy and efficient manner; more
modules could be added into the tools collection with development.

1. universal way to connect most database softwares via JDBC, using Fast/Batch load
technology to speed up the temporary table creation and query; as well as functions to convert clob 
into string or save the blob into specified file. 

2. add multiprocessing capablity to pandas dataframe when dealing with cpu intensive
operation on large volume data.

3. form based authentication module for requests package.

4. restapi client using aiohttp package with retry function.

sample usage:

    ## connect to mysql
        import pydtc

        conn = pydtc.connect('mysql', '127.0.0.1', 'user', 'pass')
        pydtc.read_sql(conn, 'select * from demo.sample')
        conn.close()
    
    ### or use with clause for auto close
        with pydtc.connect('mysql', '127.0.0.1', 'user', 'pass') as conn:
            conn.read_sql('select * from demo.sample')
            # pydtc.read_sql(conn, 'select * from demo.sample')

    ## pandas multiprocessing groupby then apply
        def func(df, key, value):
            dd = {key : value}
            dd['some_key'] = [len(df.other_key)]

            return pd.DataFrame(dd)

        new_df = pydtc.p_groupby_apply(func, df, 'group_key')

    ## access web page in website with form based authenticaion
        from pydtc import HttpFormAuth
        import requests

        r = requests.get('http://www.example.com/private_webpage.html', auth=HttpFormAuth('user', 'password'))

    ## restapi get and update
    # Fake Online REST API for Testing and Prototyping
    # https://jsonplaceholder.typicode.com/
        from pydtc import api_get, api_update

        api_get('https://jsonplaceholder.typicode.com/todos/1')
        # or
        api_update('https://jsonplaceholder.typicode.com/todos/1', data={'title': 'foo'}, method='patch')
