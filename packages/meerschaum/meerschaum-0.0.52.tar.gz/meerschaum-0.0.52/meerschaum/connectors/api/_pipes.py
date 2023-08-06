#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Register or fetch Pipes from the API
"""

from meerschaum.utils.debug import dprint
from meerschaum.utils.warnings import error

def pipe_r_url(
        pipe : 'meerschaum.Pipe'
    ) -> str:
    """
    Generate a relative URL path from a Pipe's keys.
    """
    location_key = pipe.location_key
    if location_key is None: location_key = '[None]'
    return f'/mrsm/pipes/{pipe.connector_keys}/{pipe.metric_key}/{location_key}'

def register_pipe(
        self,
        pipe : 'meerschaum.Pipe',
        debug : bool = False
    ) -> tuple:
    """
    Submit a POST to the API to register a new Pipe object.
    Returns a tuple of (success_bool, response_dict)
    """

    ### NOTE: if `parameters` is supplied in the Pipe constructor,
    ###       then `pipe.parameters` will exist and not be fetched from the database.

    ### 1. Prioritize the Pipe object's `parameters` first.
    ###    E.g. if the user manually sets the `parameters` property
    ###    or if the Pipe already exists
    ###    (which shouldn't be able to be registered anyway but that's an issue for later).
    parameters = None
    try:
        parameters = pipe.parameters
    except Exception as e:
        if debug: dprint(str(e))
        parameters = None

    ### 2. If the parent pipe does not have `parameters` either manually set
    ###    or within the database, check the `meta.parameters` value (likely None as well)
    if parameters is None:
        try:
            parameters = pipe.meta.parameters
        except Exception as e:
            if debug: dprint(str(e))
            parameters = None

    ### ensure `parameters` is a dictionary
    if parameters is None:
        parameters = dict()

    ### override `meta.parameters` with parameters found from the above process
    pipe.meta.parameters = parameters

    response = self.post('/mrsm/pipes', json=pipe.meta.dict())
    if debug: dprint(response.text)
    return response.__bool__(), response.json()

def edit_pipe(
        self,
        pipe : 'meerschaum.Pipe',
        patch : bool = False,
        debug : bool = False
    ) -> tuple:
    """
    Submit a PATCH to the API to edit an existing Pipe.
    Returns a tuple of (success_bool, response_dict)
    """
    pipe.meta.parameters = pipe.parameters
    if pipe.meta.parameters is None: pipe.meta.parameters = dict()
    if debug:
        from meerschaum.utils.debug import dprint
        dprint(f"patch: {patch}")
    response = self.patch(
        '/mrsm/pipes',
        json = pipe.meta.dict(),
        params = {'patch' : patch}
    )
    return response.__bool__(), response.json()

def fetch_pipes_keys(
        self,
        connector_keys : list = [],
        metric_keys : list = [],
        location_keys : list = [],
        params : dict = dict(),
        mrsm_instance : str = 'api',
        debug : bool = False
    ) -> 'dict or list':
    """
    NOTE: This function no longer builds Pipes. Use the main `get_pipes()` function
          with the arguments `mrsm_instance = 'api' and `method = 'registered'` (default).

    Fetch registered Pipes' keys from the API.

    keys_only : bool : True
        If True, only return a list of tuples of the keys
        E.g. [ (connector_keys, metric_key, location_key) ]
        This is used by the main `get_pipes()` function for the 'api' method.
    """
    from meerschaum.utils.debug import dprint
    from meerschaum.utils.warnings import error
    import json

    r_url = '/mrsm/pipes/keys'
    try:
        j = self.get(
            r_url,
            params = {
                'connector_keys' : json.dumps(connector_keys),
                'metric_keys' : json.dumps(metric_keys),
                'location_keys' : json.dumps(location_keys),
                'params' : json.dumps(params),
                'debug' : debug,
            }
        ).json()
    except Exception as e:
        error(str(e))

    result = []
    for t in j:
        result.append( (t['connector_keys'], t['metric_key'], t['location_key']) )
    return result

def sync_pipe(
        self,
        pipe : 'meerschaum.Pipe' = None,
        df : 'pd.DataFrame' = None,
        debug : bool = False
    ) -> tuple:
    """
    Append a pandas DataFrame to a Pipe.
    If Pipe does not exist, it is registered with supplied metadata
        NOTE: columns['datetime'] must be set for new Pipes.
    """
    r_url = pipe_r_url(pipe) + '/data'
    if debug:
        from meerschaum.utils.debug import dprint
        dprint(r_url)
    try:
        response = self.post(
            r_url,
            data = df.to_json(date_format='iso')
        )
    except Exception as e:
        from meerschaum.utils.warnings import warn
        warn(e)
        return None

    return tuple(response.json())

def delete_pipe(
        self,
        pipe : 'mrsm.Pipe' = None,
        debug : bool = None,        
    ) -> tuple:
    """
    Delete a Pipe and drop its table.
    """
    return self.do_action(
        ['delete', 'pipes'],
        connector_keys = pipe.connector_keys,
        metric_keys = pipe.metric_key,
        location_keys = pipe.location_key,
        force = True,
        debug = debug
    )

def get_pipe_data(
        self,
        pipe : 'meerschaum.Pipe',
        begin : 'datetime.datetime' = None,
        end : 'datetime.datetime' = None,
        debug : bool = False
    ) -> 'pd.DataFrame':
    """
    Fetch data from the API
    """
    r_url = pipe_r_url(pipe)
    try:
        response = self.get(r_url + "/data", params={'begin': begin, 'end': end})
    except Exception as e:
        from meerschaum.utils.warnings import warn
        warn(e)
        return None
    from meerschaum.utils.misc import import_pandas, parse_df_datetimes
    pd = import_pandas()
    return parse_df_datetimes(pd.read_json(response.text))

def get_backtrack_data(
        self,
        pipe : 'meerschaum.Pipe',
        begin : 'datetime.datetime',
        backtrack_minutes : int = 0,
        debug : bool = False
    ) -> 'pd.DataFrame':
    """
    Get a Pipe's backtrack data from the API
    """
    r_url = pipe_r_url(pipe)
    try:
        response = self.get(
            r_url + "/backtrack_data",
            params = {
                'begin': begin,
                'backtrack_minutes': backtrack_minutes,
            }
        )
    except Exception as e:
        from meerschaum.utils.warnings import warn
        warn(e)
        return None
    from meerschaum.utils.misc import import_pandas, parse_df_datetimes
    pd = import_pandas()
    return parse_df_datetimes(pd.read_json(response.text))

