import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from os import environ
import hashlib
import json
import gc
import copy
from workalendar.america import Brazil
from dateutil.relativedelta import relativedelta
import uuid

def console_log(decripion, alert_type):
    try:
        text = f"{alert_type}: {decripion}. - Time {str(datetime.now())} \n"
        print(text)
        try:
            if environ['log']:
                environ['log'] += text
            else:
                environ['log'] = text
        except:
            environ['log'] = text
    except Exception as error:
        print('Error during execute console_log:', str(error))


def console_tags(tag):
    try:
        if environ['tags']:
            environ['tags'] += f";{tag}"
        else:
            environ['tags'] = tag
    except:
        environ['tags'] = tag


def console_fields(field):
    try:
        environ['fields'] += f"{field},"
    except:
        environ['fields'] = f"{field},"


def console_status(status):
    environ['status'] = str(status)


def log():
    return str(environ['log']).split('\n')


def tags():
    return environ['tags'].split(';')


def fields():
    try:
        text = '{' + environ['fields'] + '}'
        text = json.dumps(eval(text))
    except:
        text = '{' + environ['fields'] + '}'
    finally:
        return text


def reset_log():
    environ['log'] = ''


def reset_tags():
    environ['tags'] = ''


def reset_fields():
    environ['fields'] = ''


def get_uuid():
    return str(uuid.uuid1())


def runtime(function):
    def wrap(*arg):
        start = datetime.now()
        result = function(*arg)
        text = f"Function: {function.__name__} - Runtime: {datetime.now() - start} "
        print(text)
        console_log(
            decripion=text, 
            alert_type='INFO'
        )
        return result
    return wrap


def runtime_2(function):
    def wrap(**kwargs):
        start = datetime.now()
        result = function(**kwargs)
        text = f"Function: {function.__name__} - Runtime: {datetime.now() - start} "
        print(text)
        console_log(
            decripion=text, 
            alert_type='INFO'
        )
        return result
    return wrap


def verify_message(message):
    try:
        id_msn = message.get('MessageId')
        return False
    except:
        return True


def get_bucket_in_message(message):
    try:
        bucket = eval(message.get('Body')) \
            .get('Records')[0] \
            .get('s3', {}) \
            .get('bucket', {}) \
            .get('name')
        return bucket
    except Exception as error:
        console_log(
            decripion=f"Error during execute get_bucket_in_message, error: {str(error)}", 
            alert_type='WARNING'
        )
        return None


def get_bucket_in_event(event):
    try:
        bucket = event['Records'][0] \
            .get('s3', {}) \
            .get('bucket', {}) \
            .get('name')
        return bucket
    except Exception as error:
        console_log(
            decripion=f"Error during execute get_bucket_in_event, error: {str(error)}", 
            alert_type='WARNING'
        )
        return None


def get_name_file_in_message(message):
    try:
        file_name = eval(message.get('Body')) \
            .get('Records')[0] \
            .get('s3', {}) \
            .get('object', {}) \
            .get('key')
        return file_name
    except Exception as error:
        console_log(
            decripion=f"Error during execute get_name_file_in_message, error: {str(error)}", 
            alert_type='WARNING'
        )
        return None

    
def get_name_file_in_event(event):
    try:
        file_name = event['Records'][0] \
            .get('s3', {}) \
            .get('object', {}) \
            .get('key')
        return file_name
    except Exception as error:
        console_log(
            decripion=f"Error during execute get_name_file_in_message, error: {str(error)}", 
            alert_type='WARNING'
        )
        return None


def get_size_in_message(message):
    try:
        size = eval(message.get('Body')) \
            .get('Records')[0] \
            .get('s3', {}) \
            .get('object', {}) \
            .get('size')
        return size
    except Exception as error:
        console_log(
            decripion=f"Error during execute get_size_in_message, error: {str(error)}", 
            alert_type='WARNING'
        )
        return None


def get_region_in_message(message):
    try:
        region = eval(message.get('Body')) \
            .get('Records')[0] \
            .get('awsRegion')
        return region
    except Exception as error:
        console_log(
            decripion=f"Error during execute get_region_in_message, error: {str(error)}", 
            alert_type='WARNING'
        )
        return None


def get_name_file_in_key(key):
    try:
        return key.split('/')[-1]
    except:
        return key


def get_path_in_key(key):
    try:
        return key.split('/')[0]
    except:
        return key


def get_relative_path_in_key(key):
    try:
        return key.replace(key.split('/')[-1], '')
    except:
        return key

        
def Decimal(number):
    try:
        if '.' in number:
            return float(number)
        else:
            return int(number)
    except:
        return number


def identifier_row_in_layout(row, line):
    
    """
        Functionality: identify layout of file row.
        Parameters:
            row: file line (string).
            line: acquirer layout row (dictionary).
        Return: file line parameterization.
    """

    try:
        for key in line.get('columns').keys():
            if line.get('columns').get(key).get('identifier') == 'Y':
                value = row[
                    line.get('columns').get(key).get('start'): 
                    line.get('columns').get(key).get('end')
                ]
                if value == line.get('columns').get(key).get('value'):
                    return line.get('columns')
        return None
    except Exception as error:
        console_log(
            decripion=f"Error during execute identifier_row_in_layout, error: {str(error)}", 
            alert_type='WARNING'
        )


def split_row_in_dict(row, column):
    
    """
        Functionality: transform file row into a dictionary according to layout.
        Parameters:
            row: file line (string).
            column: row layout (dictionary).
        Return: file line dictionary. 
    """

    try:
        if column:
            row_in_dict = {}
            for key in column.keys():
                row_in_dict[key] = row[
                    column.get(key).get('start'): 
                    column.get(key).get('end')
                ].strip()
                try:
                    if column.get('type') == 'date':
                        row_in_dict[key] = datetime.strptime(row_in_dict[key],  column.get('format'))
                    elif column.get('type') == 'int':
                        row_in_dict[key] = int(row_in_dict[key])
                    elif column.get('type') == 'float':
                        row_in_dict[key] = float(row_in_dict[key])
                    else:
                        row_in_dict[key] = str(row_in_dict[key])
                except:
                    row_in_dict[key] = str(row_in_dict[key])
            return row_in_dict
    except Exception as error:
        console_log(
            decripion=f"Error during execute split_row_in_dict, error: {str(error)}", 
            alert_type='WARNING'
        )


def apply(dataframe, execution):
    try:
        for execute in execution:
            try:
                dataframe = execute['function'](
                    df=dataframe,
                    args=execute['fields']
                )
            except Exception as error:
                console_log(
                    decripion=f"Error during execute Adiq.apply.for: error: {str(error)}", 
                    alert_type='ERROR'
                )
    except Exception as error:
        console_log(
            decripion=f"Error during execute apply: , error: {str(error)}", 
            alert_type='WARNING'
        )
    finally:
        return dataframe


def substr_inside_data_frame(df, args):
    for arg in args:
        try:
            df[arg['new_key']] = df[arg['key']].str[arg['start']: arg['end']]
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute substr_inside_data_frame, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def lstrip_inside_data_frame(df, args):
    for arg in args:
        try:
            df[arg['new_key']] = df[arg['key']].astype(str).str.lstrip(arg['character'])
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute lstrip_inside_data_frame, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_decimal_places(df, args):
    for arg in args:
        try:
            df[arg['key']] = pd.to_numeric(df[arg['key']]) / arg['decimal']
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_decimal_places, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_sinal(df, args):
    for arg in args:
        try:
            df[arg['key_value']] = np.where(
                (
                    (df[arg['key_sinal']] == '-') &
                    (df[arg['key_sinal']] != '') &
                    (df[arg['key_sinal']].notnull())
                ),
                df[arg['key_value']] * -1,
                df[arg['key_value']]
            )
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_sinal, key: {arg['key_value']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_default_value(df, args):
    for arg in args:
        try:
            df[arg['key']] = np.where(
                df[arg['key']] == arg['when'],
                arg['defalt'],
                df[arg['key']]
            )
        except KeyError as error:
            df[arg['key']] = arg['defalt']
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_default_value, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def from_line_to_column(df, args):
    for arg in args:
        try:
            df[arg['key_dest']] = df.loc[
                arg['line'], 
                arg['key']
            ]
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute from_line_to_column, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_toggle_value_when_is_same(df, args):
    for arg in args:
        try:
            df[arg['key_origin']] = np.where(
                df[arg['key_when']] == arg['when'],
                df[arg['key_dest']],
                df[arg['key_origin']]
            )
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_toggle_value_when_is_same, key: {arg['key_origin']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_toggle_value_when_is_different(df, args):
    for arg in args:
        try:
            for index, row in df.iterrows():
                if row[arg['key_when']] != arg['when']:
                    df.at[index, arg['key_origin']] = row[arg['key_dest']]
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_toggle_value_when_is_different, key: {arg['key_origin']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_toggle_value_when_is_different_2(df, args):
    for arg in args:
        try:
            for row in df.itertuples():
                if eval(f"row.{arg['key_when']}") != arg['when']:
                    df.at[row.Index, arg['key_origin']] = eval(f"row.{arg['key_dest']}")
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_toggle_value_when_is_different_2, key: {arg['key_origin']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_toggle_value_when_is_same_with_value_defalut(df, args):
    for arg in args:
        try:
            df[arg['key_origin']] = np.where(
                df[arg['key_origin']]  == arg['when'], 
                arg['default'] + df[arg['key_default']], 
                df[arg['key_origin']]
            )
        except KeyError as error:
            pass
        except Exception as error:   
            console_log(
                decripion=f"Error during execute adjust_toggle_value_when_is_same_with_value_defalut, key: {arg['key_origin']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def set_index(df, args):
    for arg in args:
        try:
            df[arg['key']] = df.index.values
        except KeyError as error:
            pass
        except Exception as error:   
            console_log(
                decripion=f"Error during execute set_index, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def set_index_plus_one(df, args):
    for arg in args:
        try:
            df[arg['key']] = df.index.values + 1
        except KeyError as error:
            pass
        except Exception as error:   
            console_log(
                decripion=f"Error during execute set_index_plus_one, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def calculate_net_amount(df, args):
    for arg in args:
        try:
            df[arg['key_net_amount']] = round(
                df[arg['key_gloss_amount']].astype(float) - (df[arg['key_gloss_amount']].astype(float) * (df[arg['key_fee']].astype(float) / 100)), 
                2
            )
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute calculate_net_amount, key: {arg['key_gloss_amount']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def calculate_fee_amount(df, args):
    for arg in args:
        try: 
            df[arg['key_fee_amount']] = round(
                df[arg['key_gloss_amount']] * (df[arg['key_fee']] / 100), 
                2
            )
        except Exception as error:
            console_log(
                decripion=f"Error during execute calculate_fee_amount, key: {arg['key_fee']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def calculate_fee(df, args):
    for arg in args:
        try: 
            df[arg['key_fee']] = round(  
                (1 - (df[arg['key_net_amount']] / df[arg['key_gloss_amount']])) * 100 , 
                arg['places']
            )
        except Exception as error:
            console_log(
                decripion=f"Error during execute calculate_fee, key: {arg['key_gloss_amount']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def format_datetime(df, args):
    for arg in args:
        try:
            df[arg['key_dest']] = pd.to_datetime(df[arg['key']], format=arg['format_in'])
            df[arg['key_dest']] = df[arg['key_dest']].dt.strftime(arg['format_out'])
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute format_datetime, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def to_datetime(df, args):
    for arg in args:
        try:
            df[arg['key_result']] = pd.to_datetime(
                df[arg['key']], 
                format=arg['format'],
                errors='ignore',
            )
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute to_datetime, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def generate_new_column_with_same_value(df, args):
    for arg in args:
        try:
            df[arg['key_dest']] = df[arg['key']]
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute generate_new_column_with_same_value, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def generate_same_new_columns_with_same_value(df, args):
    for arg in args:
        try:
            for fild in arg['key_dest']:
                try:
                    df[fild] = df[arg['key']]
                except KeyError as error:
                    pass
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute generate_same_new_columns_with_same_value, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def change_type_column(df, args):
    for arg in args:
        try:
            df[arg['key_dest']] = df[arg['key']].astype(arg['type'])
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute change_type_column, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def change_type_column_for(df, args):
    for arg in args:
        try:
            for index, row in df.iterrows():
                if row[arg['key']]:
                    df.at[index, arg['key_dest']] = arg['type'](row[arg['key']])
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute change_type_column_for, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def change_type_column_for_2(df, args):
    for arg in args:
        try:
            for row in df.itertuples():
                if eval(f"row.{arg['key']}"):
                    df.at[row.Index, arg['key_dest']] = arg['type'](eval(f"row.{arg['key']}"))
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute change_type_column_for_2, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def change_type_column_if(df, args):
    for arg in args:
        try:
            if str(df.dtypes[arg['key_if']]) == arg['value_if']:
                df[arg['key_dest']] = df[arg['key_change']].astype(arg['type'])
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute change_type_column_if, key: {arg['key_if']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


@runtime_2
def write_csv_file_buffer(df, name, args):
    try:
        buff = StringIO()                 
        df.to_csv(
            buff,
            index=args['index'],
            sep=args['delimiter'],
            quotechar=args['quotechar'],
            chunksize=args['chunksize'],
            quoting=args['quoting'],
            decimal=args['decimal']
        )
        return buff
    except Exception as error:
        console_log(
            decripion=f"Error during execute write_csv_file_buffer, error: {str(error)}", 
            alert_type='WARNING'
        )


def write_csv_file_buffer_binary(df, name, args):
    try:
        buff = StringIO()                
        df.to_csv(
            buff,
            index=args['index'],
            sep=args['delimiter'],
            quotechar=args['quotechar'],
            chunksize=args['chunksize'],
            quoting=args['quoting'],
            decimal=args['decimal']
        )
        buff = BytesIO(bytes(buff.getvalue(), encoding='utf-8'))
        return buff
    except Exception as error:
        console_log(
            decripion=f"Error during execute write_csv_file_buffer_binary, error: {str(error)}", 
            alert_type='WARNING'
        )


def write_csv_file_local(df, name, args):
    try:               
        df.to_csv(
            name,
            index=args['index'],
            sep=args['delimiter'],
            quotechar=args['quotechar'],
            chunksize=args['chunksize'],
            quoting=args['quoting'],
            decimal=args['decimal']
        )
        return 'Success'
    except Exception as error:
        console_log(
            decripion=f"Error during execute write_csv_file_local, error: {str(error)}", 
            alert_type='WARNING'
        )


@runtime_2
def write_parquet_file_buffer(df, name, args):
    try:
        buff = BytesIO() 
        df.to_parquet(
            buff, 
            engine=args['engine'],
            compression=args['compression'],
            index=args['index']
        )
        return buff
    except Exception as error:
        console_log(
            decripion=f"Error during execute write_parquet_file_buffer, error: {str(error)}", 
            alert_type='WARNING'
        )


def write_parquet_file_local(df, name, args):
    try:
        df.to_parquet(
            name, 
            engine=args['engine'],
            compression=args['compression'],
            index=args['index']
        )
        return 'Success'
    except Exception as error:
        console_log(
            decripion=f"Error during execute write_parquet_file_local, error: {str(error)}", 
            alert_type='WARNING'
        )


@runtime_2
def write_database(df, name, args):
    try:
        df_sql = df[args['df']] 

        if args['from']:
            df_sql.columns = args['from'] 
            try:
                df_sql = df_sql.reindex()
            except:
                pass

        if args['apply']:  
            df_sql= apply(
                dataframe=df_sql, 
                execution=args['apply']
            )  

        df_sql.to_sql(
            name=args['table'],
            con=args['engine'],
            if_exists=args['if_exists'],
            index=args['index'],
            chunksize=args['chunksize'],
            dtype=args['dtype'],
            method=args['method']
        )
        return 'Success'

    except Exception as error:
        console_log(
            decripion=f"Error during execute write_database, error: {str(error)}", 
            alert_type='WARNING'
        )


@runtime_2
def read_database(query, engine):
    try:

        df_sql = pd.read_sql(
            sql=query,
            con=engine
        )

    except Exception as error:
        console_log(
            decripion=f"Error during execute read_database, error: {str(error)}", 
            alert_type='WARNING'
        )

        df_sql = pd.DataFrame()
    finally:
        return df_sql


def link_record(df, args):
    for arg in args:
        try: 
            link = None
            for index, row in df.iterrows():
                if row[arg['key']] == arg['key_value']:
                    link = row[arg['key_link']]
                if link:
                    if row[arg['key_son']] in arg['key_son_value']:
                        df.at[index, arg['key_link_result']] = link

                    if row[arg['key_son']] in arg['break']:
                        link = None

        except KeyError as error:
            pass
            
        except Exception as error:
            console_log(
                decripion=f"Error during execute link_record, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def link_record_2(df, args):
    for arg in args:
        try: 
            link = None
            for row in df.itertuples():
                
                if eval(f"row.{arg['key']}") == arg['key_value']:
                    link = eval(f"row.{arg['key_link']}")
                if link:
                    son = eval(f"row.{arg['key_son']}")
                    if son in arg['key_son_value']:
                        df.at[row.Index, arg['key_link_result']] = link

                    if son in arg['break']:
                        link = None

        except KeyError as error:
            pass
            
        except Exception as error:
            console_log(
                decripion=f"Error during execute link_record_2, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def multiply_values(df, args):
    for arg in args:
        try: 
            df[arg['result']] = df[arg['multiplied']].astype(float) * df[arg['multiplier']].astype(float)
        except KeyError as error:
            pass
            
        except Exception as error:
            console_log(
                decripion=f"Error during execute multiply_values, key: {arg['multiplied']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def subtraction_values(df, args):
    for arg in args:
        try: 
            df[arg['result']] = round(df[arg['minuendo']].astype(float) - df[arg['subtrahend']].astype(float), arg['round'] )
        except KeyError as error:
            pass
            
        except Exception as error:
            console_log(
                decripion=f"Error during execute subtraction_values, key: {arg['minuendo']}, {arg['subtrahend']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def sum_values(df, args):
    for arg in args:
        try: 
            df[arg['result']] = round(df[arg['value1']].astype(float) + df[arg['value2']].astype(float), arg['round'] )
        except KeyError as error:
            pass
            
        except Exception as error:
            console_log(
                decripion=f"Error during execute sum_values, key: {arg['value1']}, {arg['value2']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def mask(df, args):
    for arg in args:
        try:
            df[arg['card']] = df[arg['card']].astype(str)
            for index, row in df.iterrows():
                if row[arg['card']] and row[arg['card']] != np.nan and row[arg['card']] != '' and row[arg['card']] != 'nan':
                    row[arg['card']] = row[arg['card']].strip()
                    card = ''
                    for i in range(0, len(arg['format'])):
                        if arg['format'][i] != '_':
                            card += arg['format'][i]
                        else:
                            card += row[arg['card']][i]

                    df.at[index, arg['card']] = card
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute mask, key: {arg['card']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def mask_2(df, args):
    for arg in args:
        try:
            for row in df.query(f"{arg['card']}.notnull()").itertuples():
                card = ''
                for i in range(0, len(arg['format'])):
                    if arg['format'][i] != '_':
                        card += arg['format'][i]
                    else:
                        card += eval(f"row.{arg['card']}")[i]
                df.at[row.Index, arg['card']] = card
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute mask, key: {arg['card']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def line_hash(df, args):
    for arg in args:
        try:
            for index, row in df.iterrows():
                if row[arg['key_when']] == arg['when']:
                    df.at[index, arg['key_hash']] = hashlib.md5(
                        bytes(
                            str(row), 
                            encoding ='utf-8'
                        )
                    ).hexdigest()
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute line_hash, key: {arg['key_hash']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def line_hash_2(df, args):
    for arg in args:
        try:
            for row in df.itertuples():
                if eval(f"row.{arg['key_when']}") == arg['when']:
                    df.at[row.Index, arg['key_hash']] = hashlib.md5(
                        bytes(
                            str(row), 
                            encoding ='utf-8'
                        )
                    ).hexdigest()
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute line_hash_2, key: {arg['key_hash']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def sniffer(name, logs):
    try:
        
        for log in logs:
            if log['write']:

                log_file = fields()

                if log['place'] == 's3':
        
                    response = log['class'].put_object(
                        p_bucket=log['bucket'], 
                        p_key= f"{log['prefix']}{name}{log['sufix']}{str(datetime.now().strftime('%Y%m%d%H%M%S%f'))}{log['extension']}", 
                        p_file=log_file
                    )

                    if response != 'Success':
                        console_log(
                            decripion=f"Error during execute sniffer.s3, error: {str(response)}", 
                            alert_type='WARNING'
                        )
                
                if log['place'] == 'database':

                    df_log = pd.DataFrame(
                        [
                            json.loads(log_file)
                        ]
                    )

                    buff = log['function'](
                        df=df_log, 
                        name="log_database", 
                        args=log
                    )

    except Exception as error:
        console_log(
            decripion=f"Error during execute sniffer, error: {str(error)}", 
            alert_type='WARNING'
        )


def finder_duplicate_file(duplicate, hash):
    try:
        response = False
        list_of_file = duplicate['class'].list_like_objects(
            p_bucket=duplicate['bucket'], 
            p_like=hash
        )
        for file in list_of_file:
            h = file.split('.')[0].split('_')[-1]
            if hash == h:
                response = duplicate['response']
            
    except Exception as error:
        console_log(
            decripion=f"Error during execute finder_duplicate_file, error: {str(error)}", 
            alert_type='WARNING'
        )

    finally:
        return response


def clean_up_memory(object):
    try:
        del(object)
        gc.collect()
    except Exception as error:
        console_log(
            decripion=f"Error during execute clean_up_memory, error: {str(error)}", 
            alert_type='WARNING'
        )


def abs_value(df, args):
    for arg in args:
        try:
            df[arg['key']] = df[arg['key']].abs()
        except Exception as error:
            console_log(
                decripion=f"Error during execute abs_value,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def days_sum(df, args):
    for arg in args:
        try:
            for index, row in df.iterrows():
                dt_previsao = datetime.strptime(row[arg['key_date']], arg['format_in']).date() + timedelta(days=arg['key_sum'])
                df.at[index, arg['key_dest']] = dt_previsao.strftime(arg['format_out'])
        except Exception as error:
            console_log(
                decripion=f"Error during execute days_sum,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def days_sum_2(df, args):
    for arg in args:
        try:
            for row in df.itertuples():
                dt_previsao = datetime.strptime(eval(f"row.{arg['key_date']}"), arg['format_in']).date() + timedelta(days=int(eval(f"row.{arg['key_sum']}")))
                df.at[row.Index, arg['key_dest']] = dt_previsao.strftime(arg['format_out'])
        except Exception as error:
            console_log(
                decripion=f"Error during execute days_sum_2,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def amounts_sum(df, args):
    for arg in args:
        try:
            df[arg['key_result']] = df[arg['key_val']] + df[arg['key_val2']]
        except Exception as error:
            console_log(
                decripion=f"Error during execute amounts_sum,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_toggle_default_value_when_is_same(df, args):
    for arg in args:
        try:
            for index, row in df.iterrows():
                if row[arg['key_when']] == arg['when']:
                    df.at[index, arg['key']] = arg['value']
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_toggle_default_value_when_is_same, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def adjust_toggle_default_value_when_is_same_2(df, args):
    for arg in args:
        try:
            for row in df.itertuples():
                if eval(f"row.{arg['key_when']}") == arg['when']:
                    df.at[row.Index, arg['key']] = arg['value']
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute adjust_toggle_default_value_when_is_same_2, key: {arg['key']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def replace_value(df, args):
    for arg in args:
        try:
            df[arg['new_key']] = df[arg['key']].str.replace(arg['old'], arg['new'])
        except KeyError as error:
            pass
        except Exception as error:
            console_log(
                decripion=f"Error during execute replace_value, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def nvl(df, args):
    for arg in args:
        try:
            df[arg['key_result']] = df[arg['key_none']].fillna(df[arg['key_value']])
        except KeyError as error:
            pass 
        except Exception as error:
            console_log(
                decripion=f"Error during execute nvl,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


@runtime_2
def get_detail(df, args):
    for arg in args:
        try:
            if arg['query']:
                df_sql = pd.DataFrame()
                for index, row in df.query(arg['df'], engine='python').iterrows():
                    query = arg['query']
                    for key in arg['bind']:
                        query = query.replace(key, str(row[arg['bind'][key]]))

                    df_sql = pd.concat(
                        [
                            df_sql,
                            pd.read_sql(
                                sql=query,
                                con=arg['engine']
                            )
                        ]
                    )
                
                if arg['duplicate']:
                    df_sql = df_sql.drop_duplicates()

                df_sql= apply(
                    dataframe=df_sql, 
                    execution=arg['apply']
                )

                if arg['join']:
                    if isinstance(arg['join'], list):  
                        df = pd.merge(
                            df, 
                            df_sql, 
                            how=arg['join_type'],
                            on=arg['join']
                        )
                    else:
                        df = pd.merge(
                            df, 
                            df_sql,
                            how=arg['join_type'],
                            left_on=arg['join']['left_on'], 
                            right_on=arg['join']['right_on']
                        )
                    
                if arg['concat']:
                    df = pd.concat(
                        [
                            df,
                            df_sql
                        ]
                    )

                clean_up_memory(
                    object=df_sql
                )
                
        except Exception as error:
            print(arg['query'])
            console_log(
                decripion=f"Error during execute get_detail,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


@runtime_2
def get_detail_2(df, args):
    for arg in args:
        try:
            if arg['query']:

                df_sql = pd.DataFrame()

                query = arg['query']

                for key in arg['bind']:

                    if arg['bind'][key] in df.columns:

                        value = None

                        value = arg['str_join'].join( 
                            list(df.query(f"{arg['df']} & {arg['bind'][key]}.notnull()")[arg['bind'][key]].unique())
                        )

                        query = query.replace(key, str(value))

                if ':bind' not in query:
                    df_sql = pd.read_sql(
                        sql=query,
                        con=arg['engine']
                    )
                
                if arg['duplicate']:
                    df_sql = df_sql.drop_duplicates()

                df_sql= apply(
                    dataframe=df_sql, 
                    execution=arg['apply']
                )

                if arg['join']:
                    if isinstance(arg['join'], list):  
                        df = pd.merge(
                            df, 
                            df_sql, 
                            how=arg['join_type'],
                            on=arg['join']
                        )
                    else:
                        df = pd.merge(
                            df, 
                            df_sql,
                            how=arg['join_type'],
                            left_on=arg['join']['left_on'], 
                            right_on=arg['join']['right_on']
                        )
                    
                if arg['concat']:
                    df = pd.concat(
                        [
                            df,
                            df_sql
                        ]
                    )

                clean_up_memory(
                    object=df_sql
                )
                
        except Exception as error:
            print(arg['query'])
            console_log(
                decripion=f"Error during execute get_detail_2,  error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def unique_hash(df, args):
    for arg in args:
        try:
            for index, row in df.iterrows():
                unique = None
                for fild in arg['filds']:
                    if not unique:
                        unique = str(row[fild])
                    else:
                        unique += str(row[fild])
                df.at[index, arg['key_hash']] = hashlib.md5(
                    bytes(
                        str(unique), 
                        encoding ='utf-8'
                    )
                ).hexdigest()
        except Exception as error:
            console_log(
                decripion=f"Error during execute unique_hash, key: {arg['key_hash']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def unique_hash_2(df, args):
    for arg in args:
        try:
            for row in df.itertuples():
                unique = None
                for fild in arg['filds']:
                    if not unique:
                        unique = str(eval(f"row.{fild}"))
                    else:
                        unique += str(eval(f"row.{fild}"))
                df.at[row.Index, arg['key_hash']] = hashlib.md5(
                    bytes(
                        str(unique), 
                        encoding ='utf-8'
                    )
                ).hexdigest()
        except Exception as error:
            console_log(
                decripion=f"Error during execute unique_hash_2, key: {arg['key_hash']}, error: {str(error)}", 
                alert_type='WARNING'
            )
    return df


def due_date(sale_date, brand, product, installment):
    try:
        if product == 'DEBITO':
            payment_date = sale_date + tumedelta(days = 2) 
        else:
            if brand in ('MASTERCARD','DISCOVER','DINERSCLUB'):
                payment_date = sale_date + timedelta(days = 30 * installment) 
            else:
                payment_date = sale_date + relativedelta(months=installment) 
                
        cal = Brazil()
        if not cal.is_working_day(data_pagamento):
            payment_date = cal.add_working_days(payment_date, 1)
                
        return payment_date
    except:
        return sale_date
    
    
def due_date_starting_first(forecast_date_par_1, brand, product, installment):
    try:
        if product == 'DEBITO':
            payment_date = forecast_date_par_1 + tumedelta(days = 2) 
        else:
            if brand in ('MASTERCARD','DISCOVER','DINERSCLUB'):
                payment_date = forecast_date_par_1 + timedelta(days = 30 * installment -1) 
            else:
                payment_date = forecast_date_par_1 + relativedelta(months=installment - 1) 
                
        cal = Brazil()
        if not cal.is_working_day(payment_date):
            payment_date = cal.add_working_days(payment_date, 1)
                
        return payment_date
    except:
        return forecast_date_par_1


@runtime_2
def adjust_sales_recovered_file_cielo(df, args):
    try:
        if df.loc[0,'identificacao'] == 'sales' and int(df.loc[0,'sequencia']) == 9999999:
            df_2 = df.query("tipo_registro == '1' &  tipo_transacao_codigo == 'venda' &  filler == '/' & plano_parcela != '1' & plano_parcela.notnull()")
            list_of_reg = []
            aux = None
            for index, row in df_2.iterrows():
                if aux is None:
                    aux = copy.deepcopy(row)
                else:
                    if int(aux['parcela']) == 1 and aux['parcela'] == row['parcela'] and aux['resumo_unico_15_posicoes'] != row['resumo_unico_15_posicoes']:
                        for par in range (2, int(aux['plano_parcela']) + 1):
                            aux2 = copy.deepcopy(aux)
                            aux2['parcela'] =  str(par).rjust(2, '0')
                            aux2['data_prev_pg'] = due_date_starting_first(
                                forecast_date_par_1=datetime.strptime(str(int(aux['data_prev_pg'])),'%y%m%d'), 
                                brand=aux['bandeira'], 
                                product=aux['produto'], 
                                installment=par
                            ).strftime('%y%m%d')

                            aux2['line_hash'] = hashlib.md5(
                                bytes(
                                    str(dict(aux2)), 
                                    encoding ='utf-8'
                                )
                            ).hexdigest()

                            list_of_reg.append(aux2)
                    aux = copy.deepcopy(row)
            df_3 = pd.DataFrame(list_of_reg)
            df = pd.concat([df, df_3])
            df = df.reset_index(drop=True)
    except Exception as error:
        console_log(
                decripion=f"Error during execute adjust_sales_recovered_file_cielo, error: {str(error)}", 
                alert_type='WARNING'
            )

    return df


@runtime_2
def adjust_sales_recovered_file_cielo_2(df, args):
    try:
        if df.loc[0,'identificacao'] == 'sales' and int(df.loc[0,'sequencia']) == 9999999:
            aux = None
            for row in df.query("tipo_registro == '1' &  tipo_transacao_codigo == 'venda' &  filler == '/' & plano_parcela != '1' & plano_parcela.notnull()").itertuples():
                if aux is None:
                    aux = copy.deepcopy(row)
                else:
                    if int(aux.parcela) == 1 and aux.parcela == row.parcela and aux.resumo_unico_15_posicoes != row.resumo_unico_15_posicoes:
                        for par in range (2, int(aux.plano_parcela) + 1):

                            df_2 = pd.DataFrame([aux])
                            df_2['parcela'] =  str(par).rjust(2, '0')
                            df_2['data_prev_pg'] = due_date_starting_first(
                                forecast_date_par_1=datetime.strptime(str(int(aux.data_prev_pg)),'%y%m%d'), 
                                brand=aux.bandeira, 
                                product=aux.produto, 
                                installment=par
                            ).strftime('%y%m%d')

                            df_2['line_hash'] = hashlib.md5(
                                bytes(
                                    str(df_2), 
                                    encoding ='utf-8'
                                )
                            ).hexdigest()

                            df = pd.concat([df, df_2])

                            clean_up_memory(
                                object=df_2
                            )

                    aux = copy.deepcopy(row)
                    
            df = df.reset_index(drop=True)
            
    except Exception as error:
        console_log(
                decripion=f"Error during execute adjust_sales_recovered_file_cielo_2, error: {str(error)}", 
                alert_type='WARNING'
            )

    return df


def empty(df, args):
    try:
        for arg in args:
            val = False
            if df.query(arg['query']).shape[0] == 0:
                val = True
            if val:
                df[arg['field']] = arg['value']
            else:
                df[arg['field']] = np.nan

    except Exception as error:
        console_log(
                decripion=f"Error during execute empty, error: {str(error)}", 
                alert_type='WARNING'
            )

    return df