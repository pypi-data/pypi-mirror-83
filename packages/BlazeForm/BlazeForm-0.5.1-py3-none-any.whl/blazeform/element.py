import html
import inspect
from os import path

import formencode
import formencode.validators as fev
from blazeutils.datastructures import LazyOrderedDict
from webhelpers2.html import HTML, tags, literal

from blazeform.exceptions import ElementInvalid, ProgrammingError
from blazeform.file_upload_translators import BaseTranslator
from blazeform.processors import Confirm, Select, MultiValues, Wrapper, Decimal
from blazeform.util import HtmlAttributeHolder, is_empty, multi_pop, NotGiven, \
    tolist, NotGivenIter, is_notgiven, is_iterable, ElementRegistrar, is_given

form_elements = {}


class MaxLengthMixin(object):

    def set_length(self, len):
        # if size is none, set it to None and return
        if len is None:
            return

        # make sure the size is an integer
        if not isinstance(1, type(len)):
            raise TypeError('maxlength should have been int but was %s' % type(len))

        self.set_attr('maxlength', len)

        # set a maxlength validator on this
        self.add_processor(fev.MaxLength(len))


class Label(object):
    """
    A class which represents the label associated with an element
    """

    def __init__(self, element, value):
        """
        @param element: the parent element of this label
        @type element: instantiated object that inherits pyHtmlQuickForm.element.ElementBase
        """

        if isinstance(element, ElementBase):
            #: the parent element this label is attached to
            self.element = element
        else:
            raise TypeError('Label expects pyHtmlQuickForm.element.ElementBase')

        #: the value of the label
        self.value = value

    def render(self, **kwargs):
        if isinstance(self.element, FormFieldElementBase):
            kwargs['for'] = self.element.getidattr()
        return HTML.label(self.value, **kwargs)

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def __str__(self):
        if self.value is NotGiven:
            return self.element.id
        return self.value


class ElementBase(HtmlAttributeHolder):
    """
    Base class for form elements.
    """

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, **kwargs):
        # settings to overide the form's settings
        self.settings = kwargs.pop('settings', {})
        self.label_after = kwargs.pop('label_after', False)

        HtmlAttributeHolder.__init__(self, **kwargs)

        self._defaultval = NotGiven
        self._displayval = NotGiven

        self.id = eid
        self.label = Label(self, label)
        self.form = form

        #: a list of user messages for this field (C{str})
        self.notes = []

        self.defaultval = defaultval
        self.set_attr('id', self.getidattr())

        # characteristics of this element
        self.is_defaultable = True
        self.is_renderable = True
        self.is_submittable = True
        self.is_returning = True
        self.renders_in_group = False

    @property
    def defaultval(self):
        return self._defaultval

    @defaultval.setter
    def defaultval(self, value):
        self._displayval = NotGiven
        self._defaultval = value

    @property
    def displayval(self):
        if self._displayval is NotGiven:
            self._from_python_processing()
        return self._displayval

    def _from_python_processing(self):
        self._displayval = self._defaultval

    def getidattr(self):
        return self.form._element_id_formatter % {'form_name': self.form._name,
                                                  'element_id': self.id}

    def add_note(self, note, escape=True):
        if escape:
            note = html.escape(note)
        self.notes.append(note)


class HasValueElement(ElementBase):

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, **kwargs):
        ElementBase.__init__(self, form, eid, label, defaultval, **kwargs)

        self.render_group = None

    @property
    def value(self):
        raise NotImplementedError('this method needs to be overriden')


class FormFieldElementBase(HasValueElement):
    """
    Base class for form elements that represent form fields (input, select, etc.)
    as opposed to Elements that are only for display (i.e. static, headers).
    """

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        # if this field was not submitted, we can substitute
        self.if_missing = kwargs.pop('if_missing', NotGiven)
        # if the field was submitted, but is an empty value
        self.if_empty = kwargs.pop('if_empty', NotGiven)
        # if the field is invalid, return this value
        self.if_invalid = kwargs.pop('if_invalid', NotGiven)
        #: is this field required in order for the form submission to be valid?
        self.required = kwargs.pop('required', False)
        #: name attribute
        self.nameattr = kwargs.pop('name', None)
        HasValueElement.__init__(self, form, eid, label, defaultval, **kwargs)

        self._submittedval = NotGiven
        self._safeval = NotGiven
        #: a list of error messages for this field (C{str})
        self.errors = []
        #: validators/converters
        self.processors = []
        #: whether or not this field is valid, None means the field has not been processed yet
        self._valid = None
        #: allows a form/element to "expect" an exception and handle gracefully
        self.exception_handlers = []
        #: strip string submitted values?
        self.strip = strip

        # types
        vtypes = ('boolean', 'bool', 'int', 'integer', 'number', 'num',
                  'str', 'string', 'unicode', 'uni', 'float', 'decimal')
        if vtype is not NotGiven:
            try:
                vtype = vtype.lower()
                if vtype not in vtypes:
                    raise ValueError('invalid vtype "%s"' % vtype)
            except AttributeError:
                raise TypeError('vtype should have been a string, got %s instead' % type(vtype))
        self.vtype = vtype

    def set_attrs(self, **kwargs):
        name = kwargs.pop('name', None)
        if not name:
            name = self.nameattr or self.id
        kwargs['name'] = name
        HasValueElement.set_attrs(self, **kwargs)

    @property
    def submittedval(self):
        return self._submittedval

    @submittedval.setter
    def submittedval(self, value):
        self._valid = None
        self.errors = []
        self._submittedval = value

    @property
    def displayval(self):
        if is_notgiven(self.submittedval):
            return super(FormFieldElementBase, self).displayval
        return self.submittedval

    @property
    def value(self):
        self._to_python_processing()
        if not self._valid:
            raise ElementInvalid(self.label)
        return self._safeval

    def _from_python_processing(self):
        # process processors
        value = self.defaultval

        # If its empty, there is no reason to run the converters.  By default,
        # the validators don't do anything if the value is empty and they WILL
        # try to convert our NotGiven value, which we want to avoid.  Therefore,
        # just skip the conversion.
        if not is_empty(value):
            for processor, msg in self.processors:
                value = processor.from_python(value)
        self._displayval = value

    def required_empty_test(self, value):
        return is_empty(value)

    def _to_python_processing(self):  # noqa
        """
        filters, validates, and converts the submitted value based on
        element settings and processors
        """

        # if the value has already been processed, don't process it again
        if self._valid is not None:
            return

        valid = True
        value = self.submittedval

        # strip if necessary
        if self.strip and isinstance(value, str):
            value = value.strip()
        elif self.strip and is_iterable(value):
            newvalue = []
            for item in value:
                if isinstance(item, str):
                    newvalue.append(item.strip())
                else:
                    newvalue.append(item)
            if newvalue:
                value = newvalue

        # if nothing was submitted, but we have an if_missing, substitute
        if is_notgiven(value) and self.if_missing is not NotGiven:
            value = self.if_missing

        # handle empty or missing submit value with if_empty
        if is_empty(value) and self.if_empty is not NotGiven:
            value = self.if_empty
        # standardize all empty values as None if if_empty not given
        elif is_empty(value) and not is_notgiven(value):
            value = None

        # process required
        if self.required and self.required_empty_test(value):
            valid = False
            self.add_error('field is required')

        # process processors
        for processor, msg in self.processors:
            try:
                processor = MultiValues(processor)
                ap_value = processor.to_python(value, self)

                # FormEncode takes "empty" values and returns None
                # Since NotGiven == '', FormEncode thinks its empty
                # and returns None on us.  We override that here.
                if ap_value is not None or value is not NotGiven:
                    value = ap_value
            except formencode.Invalid as e:
                valid = False
                self.add_error((msg or str(e)))
        else:
            # we rely on MultiValues for this, but if no processor,
            # it doesn't get called
            if getattr(self, 'multiple', False) and not is_iterable(value):
                value = tolist(value)

        ###
        # Doing these again in case the processors changed the value
        ###
        # handle empty or missing submit value with if_empty
        if is_empty(value) and self.if_empty is not NotGiven:
            value = self.if_empty
        # standardize all empty values as None if if_empty not given
        elif is_empty(value) and not is_notgiven(value):
            value = None

        # process required
        if self.required and self.required_empty_test(value) and \
                'field is required' not in self.errors:
            valid = False
            self.add_error('field is required')

        # If its empty, there is no reason to run the converters.  By default,
        # the validators don't do anything if the value is empty and they WILL
        # try to convert our NotGiven value, which we want to avoid.  Therefore,
        # just skip the conversion.
        if not is_empty(value):
            # process type conversion
            if self.vtype is not NotGiven:
                if self.vtype in ('boolean', 'bool'):
                    tvalidator = formencode.compound.Any(fev.Bool(), fev.StringBool())
                elif self.vtype in ('integer', 'int'):
                    tvalidator = fev.Int
                elif self.vtype in ('number', 'num', 'float'):
                    tvalidator = fev.Number
                elif self.vtype in ('decimal'):
                    tvalidator = Decimal
                elif self.vtype in ('str', 'string'):
                    tvalidator = fev.String
                elif self.vtype in ('unicode', 'uni'):
                    tvalidator = fev.UnicodeString
                try:
                    tvalidator = MultiValues(tvalidator, multi_check=False)
                    value = tvalidator.to_python(value, self)
                except formencode.Invalid as e:
                    valid = False
                    self.add_error(str(e))

        # save
        if valid:
            self._safeval = value
            self._valid = True
        else:
            # is if_invalid if applicable
            if self.if_invalid is not NotGiven:
                # we might want to clear error messages too, but the extra
                # detail probably won't hurt (for now)
                self._safeval = self.if_invalid
                self._valid = True
            else:
                self._valid = False

    def is_submitted(self):
        return self.submittedval is not NotGiven

    def is_valid(self):
        self._to_python_processing()
        return self._valid

    def add_error(self, error):
        self.errors.append(error)

    def add_processor(self, processor, msg=None):
        if not formencode.is_validator(processor):
            if callable(processor):
                processor = Wrapper(to_python=processor)
            else:
                raise TypeError('processor must be a Formencode validator or a callable')
        else:
            # FE validators may be passed as the class or an instance
            #   if class, then make it an instance
            if inspect.isclass(processor):
                processor = processor()

        self.processors.append((processor, msg))

    def add_handler(self, exception_txt=NotGiven, error_msg=NotGiven, exc_type=NotGiven,
                    callback=NotGiven):
        self.exception_handlers.append((exception_txt, error_msg, exc_type, callback))

    def handle_exception(self, exc):
        def can_handle(error_msg):
            self._valid = False
            if is_notgiven(error_msg):
                error_msg = str(exc)
            self.add_error(error_msg)
            return True

        for looking_for, error_msg, exc_type, callback in self.exception_handlers:
            if is_notgiven(callback):
                if not is_notgiven(exc_type):
                    if isinstance(exc_type, str):
                        if exc.__class__.__name__ != exc_type:
                            continue
                    else:
                        if not isinstance(exc, exc_type):
                            continue
                if is_notgiven(looking_for):
                    return can_handle(error_msg)
                elif looking_for in str(exc):
                    return can_handle(error_msg)
            else:
                if callback(exc):
                    return can_handle(error_msg)
        return False


class InputElementBase(FormFieldElementBase):
    """
    Base class for input form elements.

    Since <input> elements have very similar HTML representations, they have
    this common base class. You don't need to instantiate it directly,
    use one of the child classes.
    """

    def __init__(self, etype, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven,
                 strip=True, **kwargs):
        FormFieldElementBase.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        # use to override using the id as the default "name" attribute
        self.add_attr('class', etype)
        self.etype = etype

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def render(self, **kwargs):
        self.set_attrs(**kwargs)
        if self.form._static:
            return self.render_static()
        else:
            return self.render_html()

    def render_html(self):
        if (self.displayval or self.displayval == 0) and self.displayval is not NotGiven:
            self.set_attr('value', self.displayval)
        return HTML.input(type=self.etype, **self.attributes)

    def _static_attributes(self):
        attrs = self.attributes.copy()

        try:
            del attrs['name']
        except KeyError:
            pass
        try:
            del attrs['maxlength']
        except KeyError:
            pass
        try:
            del attrs['checked']
        except KeyError:
            pass
        attrs['class'] = attrs['class'] + ' static'
        return attrs

    def render_static(self):
        if self.etype in ('button', 'file', 'hidden', 'image', 'submit',
                          'reset', 'password'):
            return ''
        if self.displayval == '':
            todisplay = literal('&nbsp;')
        else:
            todisplay = self.displayval
        return HTML.span(todisplay, **self._static_attributes())


class ButtonElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        InputElementBase.__init__(self, 'button', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)


form_elements['button'] = ButtonElement


class CheckboxElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        checked = kwargs.pop('checked', NotGiven)
        InputElementBase.__init__(self, 'checkbox', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)

        # some sane defaults for a checkbox IMO
        if self.vtype is NotGiven:
            self.vtype = 'bool'
        if self.if_empty is NotGiven:
            self.if_empty = False
        if self.defaultval is NotGiven:
            self.defaultval = bool(checked)

    @property
    def submittedval(self):
        return self._submittedval

    @submittedval.setter
    def submittedval(self, value):
        self._valid = None
        self.errors = []

        # this is really not correct, submitted values should be strings only.  But the library
        # was built this way to begin with and for BC reasons, I'm keeping it for now.
        #
        # We do however need to handle the empty string as a special case since it's bool value
        # is False, but for checkboxes, any value sent over should be considered "on."  Most
        # browsers send the string "on" including compliant browsers and IE 8.  However, IE 9 and
        # 10 proved to send the name of the field with an empty value to indicate "on".
        if value == '':
            self._submittedval = True
        else:
            self._submittedval = bool(value)

    def required_empty_test(self, value):
        return not bool(value)

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def render(self, **kwargs):
        self.set_attrs(**kwargs)
        if self.form._static:
            return self.render_static()
        else:
            return self.render_html()

    def render_html(self):
        # have to override InputBase.render or it will put a value attribute
        # for a checkbox
        if self.displayval and self.displayval is not NotGiven:
            self.set_attr('checked', 'checked')
        else:
            try:
                self.del_attr('checked')
            except KeyError:
                pass
        return HTML.input(type=self.etype, **self.attributes)

    def render_static(self):
        return HTML.span('yes' if self.displayval else 'no', **self._static_attributes())


form_elements['checkbox'] = CheckboxElement


class FileElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        InputElementBase.__init__(self, 'file', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)

        # validation related
        self._allowed_exts = []
        self._allowed_types = []
        self._denied_exts = []
        self._denied_types = []
        self._maxsize = NotGiven

        # characterstics of this element
        self.is_defaultable = False

    @property
    def defaultval(self):
        return NotGiven

    @defaultval.setter
    def defaultval(self, value):
        if is_given(value):
            raise NotImplementedError('FileElement doesn\'t support default values')

    @property
    def submittedval(self):
        return self._submittedval

    @submittedval.setter
    def submittedval(self, value):
        self._valid = None
        self.errors = []
        if isinstance(value, BaseTranslator):
            self._submittedval = value
        elif isinstance(value, str):
            self._submittedval = NotGiven
        else:
            self._submittedval = self.form._fu_translator(value)

    def maxsize(self, size):
        "set the maximum allowed file upload size"
        self._maxsize = size

    def allow_extension(self, *args):
        "allowed extensions, (with or without dots)"
        self._allowed_exts.extend([('.%s' % a.lstrip('.').lower()) for a in args])

    def deny_extension(self, *args):
        "denied extensions, (with or without dots)"
        self._denied_exts.extend([('.%s' % a.lstrip('.').lower()) for a in args])

    def allow_type(self, *args):
        "allowed mime type strings"
        self._allowed_types.extend(args)

    def deny_type(self, *args):
        "denied mime type strings"
        self._denied_types.extend(args)

    def _to_python_processing(self):
        # if the value has already been processed, don't process it again
        if self._valid is not None:
            return

        valid = True
        value = self.submittedval

        if is_notgiven(value):
            value = BaseTranslator(None, None, 0)

        if value.is_uploaded:
            _, ext = path.splitext(value.file_name)
            ext = ext.lower()
            if not ext and (self._allowed_exts or self._denied_exts):
                valid = False
                self.add_error('extension requirement exists, but submitted file had no extension')

            if self._allowed_exts and ext not in self._allowed_exts:
                valid = False
                self.add_error('extension "%s" not allowed' % ext)

            if self._denied_exts and ext in self._denied_exts:
                valid = False
                self.add_error('extension "%s" not permitted' % ext)

            if value.content_type:
                if self._allowed_types and value.content_type not in self._allowed_types:
                    valid = False
                    self.add_error('content type "%s" not allowed' % value.content_type)

                if self._denied_types and value.content_type in self._denied_types:
                    valid = False
                    self.add_error('content type "%s" not permitted' % value.content_type)
            elif value.content_type is not None and (self._allowed_types or self._denied_types):
                valid = False
                self.add_error('content-type requirements exist, but submitted file had '
                               'no content-type')

            if self._maxsize:
                if not value.content_length:
                    valid = False
                    self.add_error('maximum size requirement exists, but submitted file had '
                                   'no content length')
                elif value.content_length > self._maxsize:
                    valid = False
                    self.add_error('file too big (%s), max size %s' %
                                   (value.content_length, self._maxsize))
        elif self.required:
            valid = False
            self.add_error('field is required')

        self._valid = valid
        if valid:
            self._safeval = self.submittedval

    def add_processor(self, processor, msg=None):
        """ NotImplementedError: FileElement does not support add_processor() """
        raise NotImplementedError('FileElement does not support add_processor()')


form_elements['file'] = FileElement


class HiddenElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        InputElementBase.__init__(self, 'hidden', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)


form_elements['hidden'] = HiddenElement


class ImageElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        InputElementBase.__init__(self, 'image', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)


form_elements['image'] = ImageElement


class ResetElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        InputElementBase.__init__(self, 'reset', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)
        if self.defaultval is NotGiven:
            self.defaultval = 'Reset'


form_elements['reset'] = ResetElement


class SubmitElement(InputElementBase):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven,
                 defaultval=NotGiven, strip=True, fixed=True, **kwargs):
        InputElementBase.__init__(self, 'submit', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)
        if self.defaultval is NotGiven:
            self.defaultval = 'Submit'
        self.fixed = fixed

    @property
    def displayval(self):
        if is_notgiven(self.submittedval) or self.fixed:
            return HasValueElement.displayval.fget(self)
        return self.submittedval


form_elements['submit'] = SubmitElement


class CancelElement(SubmitElement):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 fixed=True, **kwargs):
        InputElementBase.__init__(self, 'submit', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)
        if self.defaultval is NotGiven:
            self.defaultval = 'Cancel'
        self.fixed = fixed

    @property
    def displayval(self):
        if is_notgiven(self.submittedval) or self.fixed:
            return HasValueElement.displayval.fget(self)
        return self.submittedval


form_elements['cancel'] = CancelElement


class TextElement(InputElementBase, MaxLengthMixin):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        maxlength = kwargs.pop('maxlength', None)
        InputElementBase.__init__(self, 'text', form, eid, label, vtype, defaultval, strip,
                                  **kwargs)

        self.set_length(maxlength)


form_elements['text'] = TextElement


class ConfirmElement(TextElement):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        match = kwargs.pop('match', None)
        TextElement.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        if not match:
            raise ProgrammingError('match argument is required for Confirm elements')
        elif isinstance(match, str):
            try:
                self.mel = self.form.els[match]
            except KeyError as e:
                if match not in str(e):
                    raise
                raise ProgrammingError('match element "%s" does not exist' % match)
        else:
            self.mel = match
        if not isinstance(self.mel, HasValueElement):
            raise ProgrammingError('match element was not of type HasValueElement')
        # do we need to act like a password element?
        if isinstance(self.mel, PasswordElement):
            # override the type
            self.etype = 'password'
            # class attribute set already, override that too
            self.set_attr('class_', 'password')

        self.add_processor(Confirm(self.mel))

    @property
    def displayval(self):
        if isinstance(self.mel, PasswordElement) and not self.mel.default_ok:
            return None
        return super(ConfirmElement, self).displayval

    def render_static(self):
        return ''


form_elements['confirm'] = ConfirmElement


class DateElement(TextElement):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        vargs = multi_pop(kwargs, 'accept_day', 'month_style', 'datetime_module')
        TextElement.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        self.add_processor(fev.DateConverter(**vargs))


form_elements['date'] = DateElement


class EmailElement(TextElement):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        vargs = multi_pop(kwargs, 'resolve_domain')
        TextElement.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        self.add_processor(fev.Email(**vargs))


form_elements['email'] = EmailElement


class PasswordElement(TextElement):
    """
    Techincally, password is on the same level as text as both are types
    of input elements, but I want to inherit the text maxlength validator
    """

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        self.default_ok = kwargs.pop('default_ok', False)
        TextElement.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        # override the type
        self.etype = 'password'
        # class attribute set already, override that too
        self.set_attr('class_', 'password')

    @property
    def displayval(self):
        if self.default_ok:
            return super(PasswordElement, self).displayval
        return None


form_elements['password'] = PasswordElement


class TimeElement(TextElement):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        vargs = multi_pop(kwargs, 'use_ampm', 'prefer_ampm', 'use_seconds',
                          'use_datetime', 'datetime_module')
        TextElement.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        self.add_processor(fev.TimeConverter(**vargs))


form_elements['time'] = TimeElement


class URLElement(TextElement):

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        vargs = multi_pop(kwargs, 'check_exists', 'add_http', 'require_tld')
        TextElement.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)
        self.add_processor(fev.URL(**vargs))

    def render_static(self):
        if self.displayval == '':
            todisplay = literal('&nbsp;')
        else:
            if self.displayval.startswith('http:') or self.displayval.startswith('https:'):
                todisplay = tags.link_to(self.displayval, self.displayval)
            else:
                todisplay = self.displayval
        return HTML.span(todisplay, **self._static_attributes())


form_elements['url'] = URLElement


class SelectElement(FormFieldElementBase):
    """
    Class to dynamically create an HTML select.  Includes methods for working
    with the select's options.
    """

    def __init__(self, form, eid, options, label=NotGiven, vtype=NotGiven,
                 defaultval=NotGiven, strip=True, choose='Choose:',
                 auto_validate=True, invalid=[], error_msg=None,
                 required=False, **kwargs):
        self.multiple = bool(kwargs.pop('multiple', False))
        FormFieldElementBase.__init__(self, form, eid, label,
                                      vtype, defaultval, strip, required=required, **kwargs)

        self.options = options
        self.choose = None
        if choose:
            if isinstance(choose, list):
                self.choose = choose
            else:
                self.choose = [(-2, choose), (-1, '-' * 25)]
                if required:
                    invalid = [-2, -1] + tolist(invalid)

            self.options = self.choose + options

        if auto_validate:
            choose_as_none = [cv[0] for cv in tolist(self.choose)]
            if required:
                self.add_processor(Select(self.options, invalid, choose_as_none), error_msg)
            else:
                # NotGiven is a valid option as long as a value isn't required
                ok_values = self.options + [(NotGiven, 0)] + [(NotGivenIter, 0)]
                self.add_processor(Select(ok_values, invalid, choose_as_none), error_msg)

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def _to_python_processing(self):
        """
            if "choose" value was chosen, we need to return an emtpy
            value appropriate to `multi`
        """
        FormFieldElementBase._to_python_processing(self)
        # multiple select fields should always return a list
        if self.multiple and not is_notgiven(self._safeval):
            self._safeval = tolist(self._safeval)

    def set_attrs(self, **kwargs):
        """ no name attribute b/c select tag takes it directly """
        HasValueElement.set_attrs(self, **kwargs)

    def _static_attributes(self):
        attrs = self.attributes.copy()
        try:
            del attrs['name']
        except KeyError:
            pass
        try:
            del attrs['multiple']
        except KeyError:
            pass
        return attrs

    def render(self, **kwargs):
        if self.multiple:
            self.set_attr('multiple', 'multiple')
        self.set_attrs(**kwargs)
        if self.form._static:
            return self.render_static()
        else:
            return self.render_html()

    def render_html(self):
        def option_tag(opt):
            if isinstance(opt, (list, tuple)):
                value, label = opt
            else:
                value = label = opt
            return tags.Option(label, str(value))

        displayval = self.displayval if self.displayval or self.displayval == 0 else None
        displayval = [str(val) for val in tolist(displayval)]
        options = [option_tag(opt) for opt in self.options]
        return tags.select(self.nameattr or self.id, displayval, options, **self.attributes)

    def render_static(self):
        if self.displayval == '':
            todisplay = literal('&nbsp;')
        else:
            values = []

            def mapf(option):
                if isinstance(option, tuple):
                    return str(option[0]), option[1]
                else:
                    return str(option), option
            lookup = dict(map(mapf, self.options))
            for key in tolist(self.displayval):
                try:
                    values.append(lookup[str(key)])
                except KeyError:
                    pass
            todisplay = ', '.join(values)

        self.add_attr('class', 'select')
        return HTML.span(todisplay, **self._static_attributes())


form_elements['select'] = SelectElement


class MultiSelectElement(SelectElement):

    def __init__(self, form, eid, options, label=NotGiven, vtype=NotGiven,
                 defaultval=NotGiven, strip=True, choose='Choose:',
                 auto_validate=True, invalid=[], error_msg=None,
                 required=False, **kwargs):
        kwargs['multiple'] = True
        SelectElement.__init__(self, form, eid, options, label, vtype,
                               defaultval, strip, choose,
                               auto_validate, invalid, error_msg,
                               required, **kwargs)
        self.submittedval = NotGivenIter


form_elements['mselect'] = MultiSelectElement


class TextAreaElement(FormFieldElementBase, MaxLengthMixin):
    """
    HTML class for a textarea type field
    """

    def __init__(self, form, eid, label=NotGiven, vtype=NotGiven, defaultval=NotGiven, strip=True,
                 **kwargs):
        # set default values
        kwargs['rows'] = kwargs.pop('rows', 7)
        kwargs['cols'] = kwargs.pop('cols', 40)
        maxlength = kwargs.pop('maxlength', None)
        FormFieldElementBase.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)

        self.set_length(maxlength)

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def set_attrs(self, **kwargs):
        """ no name attribute b/c textarea tag takes it directly """
        HasValueElement.set_attrs(self, **kwargs)

    def _static_attributes(self):
        attrs = self.attributes.copy()
        try:
            del attrs['rows']
        except KeyError:
            pass
        try:
            del attrs['cols']
        except KeyError:
            pass
        try:
            del attrs['maxlength']
        except KeyError:
            pass
        return attrs

    def render(self, **kwargs):
        self.set_attrs(**kwargs)
        if self.form._static:
            return self.render_static()
        else:
            return self.render_html()

    def render_html(self):
        displayval = self.displayval if self.displayval or self.displayval == 0 else ''
        return tags.textarea(self.nameattr or self.id, displayval, **self.attributes)

    def render_static(self):
        self.add_attr('class', 'textarea')
        if self.displayval == '':
            todisplay = literal('&nbsp;')
        else:
            todisplay = self.displayval
        return HTML.span(todisplay, **self._static_attributes())


form_elements['textarea'] = TextAreaElement


class LogicalGroupElement(FormFieldElementBase):
    """
        Used to support MultiCheckboxElement and RadioElement
    """

    def __init__(self, is_multiple, form, eid, label=NotGiven, vtype=NotGiven,
                 defaultval=NotGiven, strip=True, **kwargs):
        self.auto_validate = kwargs.pop('auto_validate', True)
        self.error_msg = kwargs.pop('error_msg', None)
        self.invalid = kwargs.pop('invalid', [])
        self.submittedval = NotGivenIter
        self.members = {}
        FormFieldElementBase.__init__(self, form, eid, label, vtype, defaultval, strip, **kwargs)

        self.multiple = is_multiple
        self.mbrs = self.members
        self.to_python_first = True

        # characterstics of this element
        self.is_renderable = False

    @property
    def defaultval(self):
        return self._defaultval

    @defaultval.setter
    def defaultval(self, value):
        self._displayval = NotGiven
        self._defaultval = value

        # if you do this every time, then ElementBase ends up
        # setting this value in it's __init__, but that happens before
        # _submittedval is created in FormFieldElementBase, and we get an error
        if value:
            # call displayval to make sure any _from_python processing gets done
            displayval = super(LogicalGroupElement, self).defaultval
            self._set_members(displayval)

    @property
    def submittedval(self):
        return self._submittedval

    @submittedval.setter
    def submittedval(self, value):
        self._valid = None
        self.errors = []
        self._submittedval = value

        # use self.value to make sure processing gets done
        if is_given(value) and self.is_valid():
            self._set_members(self.value)

    def _to_python_processing(self):
        """
            we may need to add a processor, but this can't happen in init
            because we want to allow more members to be added
        """
        if self.to_python_first:
            self.to_python_first = False
            if self.auto_validate:
                options = list(self.members.items())
                if self.required:
                    self.add_processor(Select(options, self.invalid), self.error_msg)
                else:
                    # NotGiven is a valid option as long as a value isn't required
                    self.add_processor(Select(options + [(NotGivenIter, 0)], self.invalid),
                                       self.error_msg)
        FormFieldElementBase._to_python_processing(self)

    def _set_members(self, values):
        # convert to dict with unicode keys so our comparisons are always
        # the same type
        values = dict([(str(v), 1) for v in tolist(values)])

        # based on our values, set our members to chosen or not chosen
        for key, el in self.members.items():
            if str(key) in values:
                el.chosen = True
            else:
                el.chosen = False

    def add_member(self, el):
        if el.displayval in self.members:
            raise ValueError(
                'a member of this group already exists with value "%s"' % el.displayval
            )
        self.members[el.displayval] = el


class PassThruElement(HasValueElement):
    """
    This element is a non-rendering element that simply allows you to set
    a value and get that same value as .value.  It is impossible
    for this field to be set by submitted values, so .value is safe as long
    as your original was correct.
    """

    def __init__(self, form, eid, defaultval=NotGiven, label=NotGiven, **kwargs):
        HasValueElement.__init__(self, form, eid, label, defaultval, **kwargs)

        # characterstics of this element
        self.is_submittable = False
        self.is_renderable = False

    @property
    def submittedval(self):
        raise NotImplementedError('element does not allow submitted values')

    @submittedval.setter
    def submittedval(self, value):
        raise NotImplementedError('element does not allow submitted values')

    @property
    def value(self):
        return self.defaultval


form_elements['passthru'] = PassThruElement


class FixedElement(PassThruElement):
    """
    Like PassThruElement, but renders like a StaticElement
    """

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, **kwargs):
        PassThruElement.__init__(self, form, eid, defaultval, label, **kwargs)

        # characterstics of this element
        self.is_submittable = False
        self.is_renderable = True

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def render(self, **kwargs):
        self.set_attrs(**kwargs)
        return HTML.tag('div', self.value, **self.attributes)


form_elements['fixed'] = FixedElement


class StaticElement(ElementBase):
    """
    This element renders, but does not take submitted values or return values.
    It is for display/rendering purposes only.
    """

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, **kwargs):
        ElementBase.__init__(self, form, eid, label, defaultval, **kwargs)

        # characterstics of this element
        self.is_submittable = False
        self.is_returning = False

    @property
    def submittedval(self):
        raise NotImplementedError('element does not allow submitted values')

    @submittedval.setter
    def submittedval(self, value):
        raise NotImplementedError('element does not allow submitted values')

    @property
    def value(self):
        raise NotImplementedError('element does not have a value')

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def render(self, **kwargs):
        self.set_attrs(**kwargs)
        displayval = self.displayval if self.displayval or self.displayval == 0 else None
        return HTML.tag('span', displayval, **self.attributes)


form_elements['static'] = StaticElement


class GroupElement(StaticElement, ElementRegistrar):
    """
    HTML class for a form element group

    Groups can be used both for visual grouping of the elements (e.g. putting
    "Submit" and "Reset" buttons in one row or two text fields for first and
    last name in one row).
    """

    def __init__(self, form, eid, label=NotGiven, **kwargs):
        StaticElement.__init__(self, form, eid, label, NotGiven, **kwargs)
        ElementRegistrar.__init__(self, form, True)
        self.elements = LazyOrderedDict()
        self.els = self.elements

    @property
    def renderable_els(self):
        for el in self.els.values():
            if el.is_renderable:
                yield el


form_elements['elgroup'] = GroupElement


class HeaderElement(StaticElement):
    """
    A rendering element used for adding headers to a form.  It can also be used,
    depending on the renderer, to group together field elements into sections.

    Headers will normally be rendered differently than other static elements,
    hence they have their own class.
    """

    def __init__(self, form, eid, defaultval=NotGiven, level='h3', **kwargs):
        StaticElement.__init__(self, form, eid, label=NotGiven, defaultval=defaultval, **kwargs)
        self.level = level

    def render(self, **kwargs):
        self.set_attrs(**kwargs)
        displayval = self.displayval if self.displayval or self.displayval == 0 else None
        return HTML.tag(self.level, displayval, **self.attributes)


form_elements['header'] = HeaderElement


class LogicalSupportElement(ElementBase):
    """
        A checkbox for "group" use.  `Defaultval` is what goes in the "value"
        attribute.  `Chosen` is set by the parent LogicalGroupElement when
        it's submitval is set.

        These elements are used to support LogicalGroupElement
    """

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, group=NotGiven, **kwargs):
        if 'required' in kwargs:
            raise ProgrammingError(
                'Required is not allowed on this element. Set it for the logical group.'
            )

        ElementBase.__init__(self, form, eid, label, defaultval, **kwargs)
        if isinstance(group, str):
            self.lgroup = form.elements.get(group, None)
            if not self.lgroup:
                group_label = kwargs.get('group_label', group)
                self.lgroup = LogicalGroupElement(self.is_multiple, form, group, label=group_label)
                form.els[group] = self.lgroup
        elif not isinstance(group, LogicalGroupElement):
            raise TypeError('lgroup should be a string or LogicalGroupElement')
        else:
            self.lgroup = group
        self.lgroup.add_member(self)
        self.chosen = False
        self.chosen_attr = 'checked'

        # characterstics of this element
        self.is_submittable = False
        self.is_returning = False

    @property
    def submittedval(self):
        raise NotImplementedError('element does not allow submitted values')

    @submittedval.setter
    def submittedval(self, value):
        raise NotImplementedError('element does not allow submitted values')

    @property
    def value(self):
        raise NotImplementedError('element does not have a value')

    def __call__(self, **kwargs):
        return self.render(**kwargs)

    def render(self, **kwargs):
        self.set_attr('class_', self.etype)
        if self.form._static:
            return self.render_static(**kwargs)
        else:
            return self.render_html(**kwargs)

    def render_html(self, **kwargs):
        if self.displayval or self.displayval == 0:
            self.set_attr('value', self.displayval)
        if self.chosen:
            self.set_attr(self.chosen_attr, self.chosen_attr)
        else:
            try:
                self.del_attr(self.chosen_attr)
            except KeyError:
                pass
        self.set_attrs(**kwargs)
        self.set_attr('name', self.lgroup.id)
        return HTML.input(type=self.etype, **self.attributes)

    def _static_attributes(self):
        attrs = self.attributes.copy()
        for attr in ('checked', 'name', 'type', 'selected'):
            try:
                del attrs[attr]
            except KeyError:
                pass

            # Add static class to the HTML output of static elements, if it is not already there
            if 'class' in attrs:
                if 'static' not in attrs['class']:
                    attrs['class'] += ' static'
            else:
                attrs['class'] = 'static'
        return attrs

    def render_static(self, **kwargs):
        self.set_attrs(**kwargs)
        if self.chosen or self.get_attr(self.chosen_attr, None):
            if self.displayval or self.displayval == 0:
                todisplay = self.displayval
            else:
                todisplay = literal('&nbsp;')
        else:
            todisplay = literal('&nbsp;')
        return HTML.span(todisplay, **self._static_attributes())


class MultiCheckboxElement(LogicalSupportElement):

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, group=NotGiven,
                 checked=False, **kwargs):
        chosen = bool(checked)
        self.is_multiple = True
        LogicalSupportElement.__init__(self, form, eid, label, defaultval, group, **kwargs)
        self.chosen = chosen
        self.chosen_attr = 'checked'
        self.etype = 'checkbox'


form_elements['mcheckbox'] = MultiCheckboxElement


class RadioElement(LogicalSupportElement):

    def __init__(self, form, eid, label=NotGiven, defaultval=NotGiven, group=NotGiven,
                 selected=False, **kwargs):
        chosen = bool(selected)
        self.is_multiple = False
        LogicalSupportElement.__init__(self, form, eid, label, defaultval, group, **kwargs)
        self.chosen = chosen
        self.chosen_attr = 'checked'
        self.etype = 'radio'


form_elements['radio'] = RadioElement
