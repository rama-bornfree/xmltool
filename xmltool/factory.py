#!/usr/bin/env python

import os
from lxml import etree
from StringIO import StringIO
import dtd_parser
import utils
import elements


def create(root_tag, dtd_url=None, dtd_str=None):
    """Create a python object for the given root_tag

    :param root_tag: The root tag to create
    :param dtd_url: The dtd url
    :param dtd_str: The dtd as string
    """
    dic = dtd_parser.parse(dtd_url=dtd_url, dtd_str=dtd_str)
    if root_tag not in dic:
        raise Exception('Bad root_tag %s, '
                        'it\'s not supported by the dtd' % root_tag)
    return dic[root_tag]()


def load(filename, validate=True):
    """Generate a python object

    :param filename: the XML filename we should load
    :param validate: validate the XML before generating the python object.
    :type filename: str
    :type validate: bool
    :return: the generated python object
    :rtype: :class:`Element`
    """
    tree = etree.parse(filename)
    dtd_url = tree.docinfo.system_url
    path = isinstance(filename, basestring) and os.path.dirname(filename) or None
    dtd_str = utils.get_dtd_content(dtd_url, path)
    if validate:
        utils.validate_xml(tree, dtd_str)

    dic = dtd_parser.parse(dtd_str=dtd_str,
                           cache_key='xmltool.parse.%s' % dtd_url)
    root = tree.getroot()
    obj = dic[root.tag]()
    obj.load_from_xml(root)
    obj._xml_filename = filename
    obj._xml_dtd_url = dtd_url
    obj._xml_encoding = tree.docinfo.encoding
    return obj


def load_string(xml_str, validate=True):
    """Generate a python object

    :param xml_str: the XML file as string
    :type xml_str: str
    :param validate: validate the XML before generating the python object.
    :type validate: bool
    :return: the generated python object
    :rtype: :class:`Element`
    """
    if type(xml_str) == unicode:
        xml_str = xml_str.encode('utf-8')
    return load(StringIO(xml_str), validate)


def generate_form(filename, form_action=None, form_filename=None, validate=True):
    """Generate the HTML form for the given filename.

    :param filename: the XML filename we should load
    :type filename: str
    :param form_action: the action to put on the HTML form
    :type form_action: str
    :param validate: validate the XML before generating the form.
    :type validate: bool
    :return: the generated HTML form
    :rtype: str
    """
    if not form_filename:
        form_filename = filename
    obj = load(filename, validate)
    return generate_form_from_obj(obj, form_action, form_filename, validate)


def generate_form_from_obj(obj, form_action=None, form_filename=None,
                           validate=True, form_attrs=None):
    hidden_inputs = (
        '<input type="hidden" name="_xml_filename" '
        'id="_xml_filename" value="%s" />'
        '<input type="hidden" name="_xml_dtd_url" '
        'id="_xml_dtd_url" value="%s" />'
        '<input type="hidden" name="_xml_encoding" '
        'id="_xml_encoding" value="%s" />'
    ) % (
        form_filename or '',
        obj._xml_dtd_url,
        obj._xml_encoding or elements.DEFAULT_ENCODING,
    )
    attrs = {}
    if form_attrs:
        attrs = form_attrs.copy()
    if 'id' not in attrs:
        attrs['id'] = 'xmltool-form'
    if form_action:
        attrs['action'] = form_action

    attrs_str = ' '.join(['%s="%s"' % tple for tple in attrs.items()])
    html = ['<form method="POST" %s>' % attrs_str]
    html += [hidden_inputs]
    html += [obj._to_html()]
    html += ['</form>']
    return ''.join(html)


def update(filename, data, validate=True, transform=None):
    """Update the file named filename with data.

    :param filename: the XML filename we should update
    :param data: the result of the submitted data.
    :param validate: validate the updated XML before writing it.
    :type filename: str
    :type data: dict style like: dict, webob.MultiDict, ...
    :type validate: bool
    :param transform: function to transform the XML string just before
        writing it.
    :type transform: function
    :return: the object generated from the data
    :rtype: :class:`Element`
    """
    data = utils.unflatten_params(data)
    encoding = data.pop('_xml_encoding')
    dtd_url = data.pop('_xml_dtd_url')

    if len(data) != 1:
        raise Exception('Bad data')

    root_tag = data.keys()[0]
    dic = dtd_parser.parse(dtd_url=dtd_url, path=os.path.dirname(filename))
    obj = dic[root_tag]()

    obj.load_from_dict(data)
    obj.write(filename, encoding, dtd_url, validate, transform)
    return obj


def new(dtd_url, root_tag, form_action=None, form_attrs=None):
    dic = dtd_parser.parse(dtd_url=dtd_url)
    obj = dic[root_tag]()

    # Merge the following line with the function which generate the form!
    hidden_inputs = (
        '<input type="hidden" name="_xml_filename" '
        'id="_xml_filename" value="" />'
        '<input type="hidden" name="_xml_dtd_url" '
        'id="_xml_dtd_url" value="%s" />'
        '<input type="hidden" name="_xml_encoding" '
        'id="_xml_encoding" value="%s" />'
    ) % (
        dtd_url,
        elements.DEFAULT_ENCODING,
    )

    attrs = {}
    if form_attrs:
        attrs = form_attrs.copy()
    if 'id' not in attrs:
        attrs['id'] = 'xmltool-form'
    if form_action:
        attrs['action'] = form_action

    attrs_str = ' '.join(['%s="%s"' % tple for tple in attrs.items()])
    html = ['<form method="POST" %s>' % attrs_str]
    html += [hidden_inputs]
    html += [obj._to_html()]
    html += ['</form>']
    return ''.join(html)


def getElementData(elt_id, data):
    """Get the dic from data to load last element of elt_id
    """
    data = utils.unflatten_params(data)
    lis = elt_id.split(':')
    tagname = lis[-1]
    for v in lis:
        try:
            if isinstance(data, list):
                v = int(v)
            data = data[v]
        except (KeyError, IndexError):
            data = {}
            break
    return {tagname: data}
