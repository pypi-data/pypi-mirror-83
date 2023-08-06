# %load helpers.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



def summary(df):
    """Takes a DataFrame and creates a summary, does different things if object or numeric features.  """
    summary_list = []
    print('SHAPE', df.shape)

    for i in df.columns:
        vals = df[i]
        if df[i].dtype == 'O':
            try:
                most_frequent = Counter(df[i].tolist()).most_common(1)
                uniq = vals.nunique()
            except TypeError:
                most_frequent = 'NA'
                uniq = 'NA'
            summary_list.append([i,
                                 vals.dtype,
                                 'NA',
                                 'NA',
                                 most_frequent,
                                 uniq,
                                 sum(pd.isnull(vals)),
                                 sum(pd.isnull(vals)) / (1.0 * len(df))])
        elif df[i].dtype == '<M8[ns]':
            most_frequent = Counter(df[i].tolist()).most_common(1)
            summary_list.append([i,
                                 vals.dtype,
                                 vals.min(),
                                 vals.max(),
                                 most_frequent,
                                 vals.nunique(),
                                 sum(pd.isnull(vals)),
                                 sum(pd.isnull(vals)) / (1.0 * len(df))])
        else:
            summary_list.append([i,
                                 vals.dtype,
                                 vals.min(),
                                 vals.max(),
                                 vals.mean(),
                                 vals.nunique(),
                                 sum(pd.isnull(vals)),
                                 sum(pd.isnull(vals)) / (1.0 * len(df))])
    return pd.DataFrame(summary_list,
                        columns=['col', 'datatype', 'min', 'max', 'mean_or_most_common', 'num_uniq', 'null_count',
                                 'null_pct'])


def color_obeject(val):
    """
    Color the "Object" rows in red - just to help in looking at those fields
    """
    if val == 'O':
        color = 'red'
    elif val == '<M8[ns]':
        color = 'blue'
    else:
        color = 'black'
    return 'color: %s' % color


def highlight_max(s, threshold=.5):
    '''
    highlight the maximum in a Series yellow.
    '''

    def color_translate(x):
        out = 'background-color: white' if x <= .02 else \
            'background-color: yellow' if x <= .25 else \
                'background-color: orange' if x <= .5 else \
                    'background-color: red'
        return out

    return [color_translate(v) for v in s]


def color_code_summary(df):
    """Then apply the color to the DateFrame"""
    s = summary(df)
    style_s = s.style.applymap(color_obeject).apply(highlight_max, subset=['null_pct'])

    return s, style_s


def summary_hist(df, field, label, color='blue', bins=None, dplot_args={}):
    fig, ax = plt.subplots(figsize=(14, 5))  # Sample figsize in inches
    if pd.notnull(bins):
        _ = sns.distplot(df[field], bins=bins, color=color, **dplot_args)
    else:
        _ = sns.distplot(df[field], color=color, **dplot_args)

    ax.set_ylabel('Density')

    ## Get some Bounds
    xx = _.patches
    xx = np.max([z.properties()['bbox'].bounds[-1] for z in xx]) * (1.3)
    adjustment_val = xx * .1
    color_dict = {'mean': 'blue', 'mode': 'red', 'median': 'purple'}
    ## Text of summary metrics
    base_val = xx - adjustment_val
    for m in [('mean', np.mean), ('median', np.median), ('mode', pd.Series.mode)]:
        if m[0] == 'mode':
            text = m[0] + ': ' + str(m[1](df[field])[0])
        else:
            text = m[0] + ': ' + str(round(m[1](df[field]), 2))

        ax.text(max(df[field]) * .75,
                base_val,
                text,
                fontdict={'fontsize': 15, 'color': color_dict[m[0]]}
                )
        base_val -= adjustment_val
        ax.vlines(m[1](df[field]), 0, xx, color_dict[m[0]])
    ax.set_ylim(0, xx)
    ax.set_title(label)


def shared_fields(data_files, do_print = False):
    """
    Just looking at shared fields.
    """
    
    record = []
    df_data = []
    for d1 in data_files:
        for d2 in data_files:
            record_file = sorted([d1,d2])
            if (d1 != d2) and record_file not in record:
                d1_cols = set(data_files[d1].columns.tolist())
                d2_cols = set(data_files[d2].columns.tolist())
                shared_cols = list(d1_cols & d2_cols)
                if do_print:
                    print(f"{d1} <--> {d2}")
                    print(shared_cols)
                    print('\n')
                df_data += list(zip([d1 for i in range(len(shared_cols))],shared_cols))
                df_data += list(zip([d2 for i in range(len(shared_cols))],shared_cols))

            record.append(record_file)
            
    df = pd.DataFrame(df_data)
    df.columns = ['table', 'col']
    df = df.drop_duplicates()

    
    grp = df.groupby('col').agg({'table': ['count', list]})
    grp = grp.droplevel(1,axis=1).reset_index()
    grp.columns = ['col', 'col_count', 'tables']
    return grp.sort_values('col_count', ascending=False)

def clean_cols(cols: list, replaces=None):
    """
    Removes special characters and lowercases things. 
    """
    cols = [i.lower().replace(' ', '_') for i in cols]
    clean_cols = []
    for c in cols:
        clean_cols.append(c.translate ({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}))
    return clean_cols


def get_gsheet(SPREADSHEET_ID, RANGE_NAME, CREDS_PATH):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # https://docs.google.com/spreadsheets/d/1pdQIU5mtziHRVd1rkPqZP9n-md4p3zm2YMdkeYXa_ec/edit#gid=2049809256
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    return values