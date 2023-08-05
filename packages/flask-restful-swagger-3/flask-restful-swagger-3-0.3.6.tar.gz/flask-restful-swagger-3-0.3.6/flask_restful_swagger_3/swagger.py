import collections
import re
import inspect
from functools import wraps

from flask import request
from flask_restful import Resource, reqparse, inputs


REGISTRY_SCHEMA = {}


class ValidationError(ValueError):
    pass


def auth(api_key, endpoint, method):
    """Override this function in your application.

    If this function returns False, 401 forbidden is raised and the documentation is not visible.
    """
    return True


def _auth(*args, **kwargs):
    return auth(*args, **kwargs)


def create_open_api_resource(swagger_object):
    """Creates a flask_restful api endpoint for the swagger spec"""

    class SwaggerEndpoint(Resource):
        def get(self):
            swagger_doc = {}
            # filter keys with empty values
            for k, v in swagger_object.items():
                if v or k == 'paths':
                    if k == 'paths':
                        paths = {}
                        for endpoint, view in v.items():
                            views = {}
                            for method, docs in view.items():
                                # check permissions. If a user has not access to an api, do not show the docs of it
                                if auth(request.args.get('api_key'), endpoint, method):
                                    views[method] = docs
                            if views:
                                paths[endpoint] = views
                        swagger_doc['paths'] = collections.OrderedDict(sorted(paths.items()))
                    else:
                        swagger_doc[k] = v

                if k == 'servers':
                    validate_servers_object(v)

                if k == 'info':
                    validate_info_object(v)
                    continue

            return swagger_doc

    return SwaggerEndpoint


class TypeSwagger:
    bool = "boolean"
    str = "string"
    float = "number"
    int = "integer"
    bin = "binary"
    list = "array"
    dict = "object"

    @classmethod
    def get_type(cls, _type):
        if _type in cls.__dict__:
            return cls.__dict__[_type]


def set_nested(d, key_spec, value):
    """
    Sets a value in a nested dictionary.
    :param d: The dictionary to set
    :param key_spec: The key specifier in dotted notation
    :param value: The value to set
    """
    keys = key_spec.split('.')

    for key in keys[:-1]:
        d = d.setdefault(key, {})

    d[keys[-1]] = value


def add_parameters(swagger_object, parameters):
    """
    Populates a swagger document with parameters.
    :param parameters: A collection of parameters to add
    :param swagger_object: The swagger document to add parameters to
    """
    # A list of accepted parameters.  The first item in the tuple is the
    # name of keyword argument, the second item is the default value,
    # and the third item is the key name in the swagger object.
    fields = [
        ('title', '', 'info.title'),
        ('description', '', 'info.description'),
        ('terms', '', 'info.termsOfService'),
        ('version', '', 'info.version'),
        ('contact', {}, 'info.contact'),
        ('license', {}, 'info.license'),
        ('servers', [], 'servers'),
        ('components', {}, 'components'),
        ('paths', {}, 'paths'),
        ('security', [], 'security'),
        ('tags', [], 'tags'),
        ('externalDocs', {}, 'externalDocs')
    ]

    for field in fields:
        value = parameters.pop(field[0], field[1])
        if value:
            set_nested(swagger_object, field[2], value)


def get_data_type(param):
    """
    Maps swagger data types to Python types.
    :param param: swagger parameter
    :return: Python type
    """
    if not param:
        return None
    try:
        param_type = param.get('type', None)
    except TypeError:
        param_type = param.__dict__.get('type', None)
    if param_type:
        if param_type == 'array':
            if 'items' in param:
                param = param['items']
            try:
                param_type = param.get('type', None)
            except TypeError:
                param_type = param.__dict__.get('type', None)
            if param_type == 'object':
                prop = param.__dict__.get('properties', None)
                for k in prop:
                    try:
                        param_type = prop[k].get('type', None)
                    except TypeError:
                        param_type = prop[k].__dict__.get('type', None)
        if param_type == 'string':
            try:
                param_format = param.get('format', None)
            except TypeError:
                param_format = param.__dict__.get('format', None)

            if param_format == 'date':
                return inputs.date

            elif param_format == 'date-time':
                return inputs.datetime_from_iso8601

            return str

        elif param_type == 'integer':
            return int

        elif param_type == 'boolean':
            return inputs.boolean

        elif param_type == 'number':
            param_format = param.get('format', None)

            if param_format == 'float' or param_format == 'double':
                return float

    return None


def get_data_action(param):
    if param:
        try:
            param_type = param.get('type', None)
        except TypeError:
            param_type = param.__dict__.get('type', None)

        if param_type == 'array':
            return 'append'
        return 'store'

    return None


def get_parser_from_schema(ref):
    if type(ref) == str:
        _schema = ref.split('/')[-1]
    else:
        _schema = ref
    if _schema in REGISTRY_SCHEMA:
        definitions_schema = REGISTRY_SCHEMA[_schema]
    else:
        definitions_schema = _schema
    _type = definitions_schema.__dict__.get('type', None)
    properties = definitions_schema.__dict__.get('properties', None)
    required = definitions_schema.__dict__.get('required', [])

    if _type == 'object':
        for prop in properties:
            try:
                _help = properties[prop].get('description', None)
            except TypeError:
                _help = properties[prop].__dict__.get('description', None)

            try:
                default = properties[prop].get('default', None)
            except TypeError:
                default = properties[prop].__dict__.get('default', None)
            name = prop
            second_part = {
                'dest': prop,
                'type': get_data_type(properties[prop]),
                'location': 'args',
                'help': _help,
                'required': prop in required,
                'default': default,
                'action': get_data_action(properties[prop])
            }
            yield name, second_part


def get_parser_arg(param):
    """
    Return an argument for the request parser.
    :param param: Swagger document parameter
    :return: Request parser argument
    """
    if 'schema' in param:
        if '$ref' in param['schema']:
            list_obj = [(name, sec) for name, sec in get_parser_from_schema(param['schema']['$ref'])]
            return list_obj

    obj = (
        param['name'],
        {
            'dest': param['name'],
            'type': get_data_type(param.get('schema', None)),
            'location': 'args',
            'help': param.get('description', None),
            'required': param.get('required', False),
            'default': param.get('default', None),
            'action': get_data_action(param['schema'])
        })
    return obj


def get_parser_args(params):
    """
    Return a list of arguments for the request parser.
    :param params: Swagger document parameters
    :return: Request parser arguments
    """
    return [get_parser_arg(p) for p in params if p['in'] == 'query']


def get_parser(params):
    """
    Returns a parser for query parameters from swagger document parameters.
    :param params: swagger doc parameters
    :return: Query parameter parser
    """
    parser = reqparse.RequestParser()

    for arg in get_parser_args(params):
        if type(arg) == list:
            for a in arg:
                parser.add_argument(a[0], **a[1])
        else:
            parser.add_argument(arg[0], **arg[1])

    return parser


def validate_info_object(info_object):
    for k, v in info_object.items():
        if k not in ['title', 'description', 'termsOfService', 'contact', 'license', 'version']:
            raise ValidationError('Invalid info object. Unknown field "{field}". See {url}'.format(
                field=k,
                url='http://swagger.io/specification/#infoObject'))

        if k == 'contact':
            validate_contact_object(v)
            continue

        if k == 'license':
            validate_license_object(v)
            continue

    if 'title' not in info_object:
        raise ValidationError('Invalid info object. Missing field "title"')

    if 'version' not in info_object:
        raise ValidationError('Invalid info object. Missing field "version"')


def validate_contact_object(contact_object):
    if contact_object:
        for k, v in contact_object.items():
            if k not in ['name', 'url', 'email']:
                raise ValidationError('Invalid contact object. Unknown field "{field}". See {url}'.format(
                    field=k,
                    url='http://swagger.io/specification/#contactObject'))

            if k == 'email':
                validate_email(v)
                continue


def validate_license_object(license_object):
    if license_object:
        for k, v in license_object.items():
            if k not in ['name', 'url']:
                raise ValidationError('Invalid license object. Unknown field "{field}". See {url}'.format(
                    field=k,
                    url='http://swagger.io/specification/#licenseObject'))

            if k ==  'url':
                validate_url(v)
                continue

        if 'name' not in license_object:
            raise ValidationError('Invalid license object. Missing field "name"')


def validate_path_item_object(path_item_object):
    """Checks if the passed object is valid according to http://swagger.io/specification/#pathItemObject"""

    for k, v in path_item_object.items():
        if k == '$ref':
            continue
        if k in ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']:
            validate_operation_object(v)
            continue
        if k == 'servers':
            validate_servers_object(v)
            continue
        if k == 'parameters':
            for parameter in v:
                try:
                    validate_reference_object(parameter)
                except ValidationError:
                    validate_parameter_object(parameter)
            continue
        if k == "summary":
            continue
        if k == "description":
            continue
        raise ValidationError('Invalid path item object. Unknown field "{field}". See {url}'.format(
                field=k,
                url='http://swagger.io/specification/#pathItemObject'))


def validate_operation_object(operation_object):
    for k, v in operation_object.items():
        if k in ['tags']:
            if isinstance(v, list):
                continue
            raise ValidationError('Invalid operation object. "{0}" must be a list but was "{1}"', k, type(v))
        if k in ['summary', 'description', 'operationId']:
            if isinstance(v, str):
                continue
            raise ValidationError('Invalid operation object. "{0}" must be a string but was "{1}"', k, type(v))
        if k in ['requestBody']:
            validate_request_body_object(v)
            continue
        if k in ['deprecated']:
            if isinstance(v, bool):
                continue
            raise ValidationError('Invalid operation object. "{0}" must be a bool but was "{1}"', k, type(v))
        if k in ['externalDocs']:
            validate_external_documentation_object(v) # to check
            continue
        if k in ['parameters']:
            for parameter in v:
                validate_parameter_object(parameter)
            continue
        if k in ['responses']:
            validate_responses_object(v)
            continue
        if k in ['security']:
            validate_security_requirement_object(v)
            continue
        raise ValidationError('Invalid operation object. Unknown field "{field}". See {url}'.format(
                field=k,
                url='http://swagger.io/specification/#pathItemObject'))
    if 'responses' not in operation_object:
        raise ValidationError('Invalid operation object. Missing field "responses"')


def validate_parameter_object(parameter_object):
    for k, v in parameter_object.items():
        if k not in ['name', 'in', 'description', 'required', 'deprecated', 'allowEmptyValue', 'style', 'explode',
                     'allowReserved', 'schema', 'example', 'examples', 'content', 'matrix', 'label', 'form',
                     'simple', 'spaceDelimited', 'pipeDelimited', 'deepObject', 'reqparser']:
            raise ValidationError('Invalid parameter object. Unknown field "{field}". See {url}'.format(
                    field=k,
                    url='http://swagger.io/specification/#parameterObject'))
    if 'reqparser' in parameter_object:
        if 'name' not in parameter_object['reqparser']:
            raise ValidationError('name for request parser not specified')
        if 'parser' not in parameter_object['reqparser'] or not isinstance(parameter_object['reqparser']['parser'], reqparse.RequestParser):
            raise ValidationError('RequestParser object not specified')
        return
    if 'name' not in parameter_object:
        raise ValidationError('Invalid parameter object. Missing field "name"')
    if 'in' not in parameter_object:
        raise ValidationError('Invalid parameter object. Missing field "in"')
    else:
        if parameter_object['in'] not in ['path', 'query', 'header', 'cookie']:
            raise ValidationError(
                    'Invalid parameter object. Value of field "in" must be path, query, header, cookie was "{0}"'.format(
                            parameter_object['in']))
    if 'schema' in parameter_object:
        validate_schema_object(parameter_object['schema'])


def validate_reference_object(parameter_object):
    if len(parameter_object.keys()) > 1 or '$ref' not in parameter_object:
        raise ValidationError('Invalid reference object. It may only contain key "$ref"')


def validate_external_documentation_object(external_documentation_object):
    pass


def validate_responses_object(responses_object):
    for k, v in responses_object.items():
        if k in ["1XX", "2XX", "3XX", "4XX", "5XX", "default"]:
            try:
                validate_reference_object(v)
            except ValidationError:
                validate_response_object(v)
            continue
        if 99 < int(k) < 600:
            try:
                validate_reference_object(v)
            except ValidationError:
                validate_response_object(v)
                continue


def validate_response_object(response_object):
    for k, v in response_object.items():
        if k == 'description':
            continue
        if k == 'headers':
            try:
                validate_reference_object(v)
            except ValidationError:
                validate_headers_object(v)
            continue
        if k == 'content':
            validate_content_object(v)
            continue
        if k == "links":
            validate_link_object(v)
            continue
        raise ValidationError('Invalid response object. Unknown field "{field}". See {url}'.format(
                field=k,
                url='http://swagger.io/specification/#responseObject'))
    if 'description' not in response_object:
        raise ValidationError('Invalid response object. Missing field "description"')


def validate_request_body_object(request_body_object):
    for k, v in request_body_object.items():
        if k in ['description']:
            continue
        if k in ['required']:
            if isinstance(v, bool):
                continue
        if k in ['content']:
            validate_content_object(v)
            continue

    if 'content' not in request_body_object:
        raise ValidationError('Invalid request body object. Missing field "content"')


def validate_content_object(content_object):
    for k, v in content_object.items():
        if re.match(r'(.*)/(.*)', k):
            validate_media_type_object(v)
            continue
        raise ValidationError(
            'Invalid content object, the field must match the following patter ("application/json", "*/*" ...").'
            '. See http://swagger.io/specification/#mediaObject'
        )


def validate_media_type_object(media_type_object):
    for k, v in media_type_object.items():
        if k == "schema":
            validate_schema_object(v)
            continue
        if k == "examples":
            validate_example_object(v)
            continue


def validate_security_requirement_object(security_requirement_object):
    pass


def validate_components_object(definition_object):
    for k, v in definition_object.items():
        if k == "schemas":
            validate_schema_object(v)
            continue


def validate_schema_object(schema_object):
    for k, v in schema_object.items():
        try:
            validate_reference_object(v)
            continue
        except AttributeError:
            if k == 'required' and not isinstance(v, list):
                raise ValidationError('Invalid schema object. "{0}" must be a list but was {1}'.format(k, type(v)))


def validate_headers_object(headers_object):
    for k, v in headers_object.items():
        if k not in ['name', 'in', 'description', 'required', 'deprecated', 'allowEmptyValue', 'style', 'explode',
                     'allowReserved', 'schema', 'example', 'examples', 'content', 'matrix', 'label', 'form',
                     'simple', 'spaceDelimited', 'pipeDelimited', 'deepObject']:
            raise ValidationError('Invalid headers object. Unknown field "{field}". See {url}'.format(
                    field=k,
                    url='http://swagger.io/specification/#headerObject'))
        if k == 'name':
            raise ValidationError('"name" must not be specified. See http://swagger.io/specification/#headerObject')
        if k == 'in':
            raise ValidationError('"in" must not be specified. See http://swagger.io/specification/#headerObject')

        if k == 'schema':
            validate_schema_object(headers_object['schema'])
            continue


def validate_link_object(link_object):
    for k, v in link_object.items():
        if k in ['operationRef', 'operationId', 'parameters', 'requestBody', 'description']:
            continue
        if k == 'server':
            validate_servers_object(v)


def validate_servers_object(server_object):
    if isinstance(server_object, list):
        for server in server_object:
            validate_server_object(server)

    else:
        validate_server_object(server_object)


def validate_server_object(server_object):
    if isinstance(server_object, dict):
        for k, v in server_object.items():
            if k not in ['url', 'description', 'variables']:
                raise ValidationError('Invalid server object. Unknown field "{field}". See {url}'.format(
                    field=k,
                    url='http://swagger.io/specification/#serverObject'))

            if k == 'variables':
                validate_server_variables_object(v)
                continue

            if k == 'url':
                if not validate_url(v):
                    raise ValidationError('Invalid url. See {url}'.format(
                        url='http://swagger.io/specification/#serverObject'))

        if "url" not in server_object:
            raise ValidationError('Invalid server object. Missing field "url"')
    else:
        raise ValidationError('Invalid server object. See {url}'.format(
            url='http://swagger.io/specification/#serverObject'
        ))


def validate_url(url):
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_regex, url) is not None


def validate_email(email):
    email_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

    return re.match(email_regex, email) is not None


def validate_server_variables_object(server_variables_object):
    for k, v in server_variables_object.items():
        if k not in ['enum', 'default', 'description']:
            raise ValidationError('Invalid server variables object. Unknown field "{field}". See {url}'.format(
                field=k,
                url='http://swagger.io/specification/#headerObject'))

        if k == 'enum':
            if isinstance(v, list):
                if not all(isinstance(x, str) for x in v):
                    raise ValidationError(
                        'Invalid server variables object object. Each item of enum must be string'
                        'See http://swagger.io/specification/#serverVariablesObject'
                    )
            else:
                raise ValidationError(
                    'Invalid server variables object object. Enum must be a list of strings'
                    'See http://swagger.io/specification/#serverVariablesObject'
                )

    if 'default' not in server_variables_object:
        raise ValidationError(
            'Invalid server variables object object. Missing field "url"'
            'See http://swagger.io/specification/#serverVariablesObject'
        )


def validate_example_object(example_object):
    pass


def extract_swagger_path(path):
    """
    Extracts a swagger type path from the given flask style path.
    This /path/<parameter> turns into this /path/{parameter}
    And this /<string(length=2):lang_code>/<string:id>/<float:probability>
    to this: /{lang_code}/{id}/{probability}
    """
    return re.sub("<(?:[^:]+:)?([^>]+)>", "{\\1}", path), re.findall("<(.*?)>", path)


def sanitize_doc(comment):
    """
    Substitute HTML breaks for new lines in comment text.
    :param comment: The comment text
    :return: Sanitized comment text
    """
    if isinstance(comment, list):
        return sanitize_doc('\n'.join(filter(None, comment)))
    else:
        return comment.replace('\n', '<br/>') if comment else comment


def expected(schema, required=False):
    """
    decorator to add request body in method
    :param schema:
    :param required:
    :return:
    """

    def decorated(func):
        func.__request_body = {"schema": schema, "required": required}

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return wrapper

    return decorated


def parameters(params=[]):
    """
    decorator to add multiple parameters to url

    Example usage:
        @parameters([
            {
                'in': 'query',
                'name': 'test',
                'schema': {type: integer},
                'description': 'a description'
            }])
        def get():
            ...


        @parameters(_in='query', name='test')
        def get():
            ...

    :param params:
    :return:
    """
    if not type(params) == list:
        raise ValidationError("decorator 'parameters' accept only list argument")

    for param in params:
        if param and param['in'] == 'path':
            raise ValidationError("""
            parameter with path must be set automlatically when added variable in url path
            example: api.add_resource(/user/<int:user_id>)
            """)

    def decorated(func):
        func_args = inspect.getfullargspec(func).args
        if "__params" in func.__dict__:
            for param in params:
                func.__params.append({k: v for k, v in dict(param).items()})

        else:
            func.__params = params

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if '_parser' in func_args:
                kwargs.update({'_parser': get_parser(params)})
            return func(self, *args, **kwargs)

        return wrapper

    return decorated


def parameter(param={}, **kwargs):
    """
    decorator to add one parameter to url

    Example usage:
        @parameter(_in='query', name='test', schema={type: integer}, description='a description')
        def get():
            ...

        @parameter({
                'in': 'query',
                'name': 'test',
                'schema': {type: integer},
                'description': 'a description'
            })
        def get():
            ...
    :param param
    :param kwargs:
    :return:
    """
    params = []
    if "_in" in kwargs:
        kwargs["in"] = kwargs.pop("_in")

    if not type(param) == dict:
        raise ValueError(f"'param' {param} must be of type 'dict'")

    if kwargs:
        params.append(dict(kwargs))

    if param:
        params.append(param)

    return parameters(params)


def response(response_code, description=None, schema=None, no_content=False):
    """
    Decorator to add a response to the url
    :param response_code:
    :param description:
    :param schema:
    :param no_content:
    :return:
    """
    def decorated(func):
        if "__response_code" in func.__dict__:
            func.__response_code.append(response_code)
        else:
            func.__response_code = [response_code]

        _description = description
        if not _description:
            _description = sanitize_doc(func.__doc__.split('\n'))
        if "__description" in func.__dict__:
            func.__description.append(sanitize_doc(_description.split('\n')))
        else:
            func.__description = [sanitize_doc(_description.split('\n'))]

        if "__schema" in func.__dict__:
            func.__schema.append(schema)
        else:
            func.__schema = [schema]

        if "__no_content" in func.__dict__:
            func.__no_content.append(no_content)
        else:
            func.__no_content = [no_content]

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return wrapper

    return decorated


def reorder_with(schema, as_list: bool = False, response_code=200, description=None):
    """
    Decorator to apply a schema to a response
    :param schema:
    :param as_list:
    :param response_code:
    :param description:
    :return:
    """
    def decorated(func):
        _schema = [schema] if as_list else schema
        if "__schema" in func.__dict__:
            func.__schema.append(_schema)
        else:
            func.__schema = [_schema]

        if "__response_code" in func.__dict__:
            func.__response_code.append(response_code)
        else:
            func.__response_code = [response_code]

        _description = description
        if not _description:
            _description = sanitize_doc(func.__doc__.split('\n'))
        if "__description" in func.__dict__:
            func.__description.append(_description)
        else:
            func.__description = [_description]

        if "__no_content" in func.__dict__:
            func.__no_content.append(False)
        else:
            func.__no_content = [False]

        @wraps(func)
        def wrapper(self, *args, **kwargs):

            return func(self, *args, **kwargs)

        return wrapper

    return decorated


def reorder_list_with(schema, response_code=200, description=None):
    """
    Same as reoder_with with as_list = True
    :param schema:
    :param response_code:
    :param description
    :return:
    """
    return reorder_with(schema, True, response_code, description)


def __tags_method(func, *_tags):
    """
    Decorate method
    :param func:
    :param _tags:
    :return:
    """
    func.__tags = list(_tags)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper


def __tags_decorated_class(cls, *_tags):
    """
    Decorate each method of Resource class
    :param cls:
    :param _tags:
    :return:
    """
    for name, m in inspect.getmembers(cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
        if name in ['get', 'post', 'patch', 'put', 'delete']:
            setattr(cls, name, __tags_method(m, *_tags))
    return cls


def tags(*_tags):
    """
    add tags to operation object
    :param _tags:
    :return:
    """
    def decorated(func_or_class):
        klass = None
        function = None

        if inspect.isclass(func_or_class):
            klass = func_or_class

        if inspect.ismethod(func_or_class) or inspect.isfunction(func_or_class):
            function = func_or_class

        if klass:
            return __tags_decorated_class(klass, *_tags)

        if function:
            return __tags_method(function, *_tags)

    return decorated


def reqparser(name, parser):
    """
    get reparser
    :param name:
    :param parser:
    :return:
    """

    def decorated(func):

        func.__reqparser = {"name": name, "parser": parser}

        @wraps(func)
        def wrapper(self, *args, **kwargs):

            return func(self, *args, **kwargs)

        return wrapper

    return decorated


def slash_join(*args):
    """
    Function to join several parts of url
    :param args:
    :return:
    """
    return "/".join([url[:-1] if url.endswith("/") else url for url in args]).replace('//', '/')


def payload():
    """
    Return the request response
    :return:
    """
    return request.get_json()

