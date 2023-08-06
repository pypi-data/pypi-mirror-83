import pandas as pd

def path_all(df:pd.DataFrame.astype) -> None:
    """ Append FileName (i.e. name of text) column's values on new line. """
    return '\n'.join(df.FileName)


def merge_edges(df:pd.DataFrame.astype) -> pd.DataFrame.astype:
    """ 
    Merge redundant edges from trains of transmission to single edge connecting nodes.
    If file doesn't provide FileName (i.e. name of text), return input dataframe.
    """
    try:
        df_paths = df.merge(
                            pd.DataFrame(df.groupby(['From', 'To']).apply(path_all)),
                            on=['From', 'To']).rename(columns={0:'paths'})
        return df_paths[~df_paths.duplicated(['From', 'To'])]
    except AttributeError:
        return df
