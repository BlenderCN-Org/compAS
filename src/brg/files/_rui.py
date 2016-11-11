# -*- coding: utf-8 -*-
# @Date    : 2016-03-12 12:11:03
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


import os
import uuid
import inspect

from xml.etree import ElementTree as ET
from xml.dom import minidom

# from xml.etree.SimpleXMLTreeBuilder import TreeBuilder

# ET.XMLTreeBuilder = TreeBuilder


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2016-03-12 12:11:03'


TPL_RUI = '''<?xml version="1.0" encoding="utf-8"?>
<RhinoUI major_ver="2"
         minor_ver="0"
         guid="{0}"
         localize="False"
         default_language_id="1033">
    <extend_rhino_menus>
        <menu guid="{1}">
          <text>
            <locale_1033>Extend Rhino Menus</locale_1033>
          </text>
        </menu>
    </extend_rhino_menus>
    <menus />
    <tool_bar_groups />
    <tool_bars />
    <macros />
    <bitmaps>
        <small_bitmap item_width="16" item_height="16">
          <bitmap>iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6Q
AAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAATSURBVDhPYxgFo2AUjAIwYGAAAA
QQAAGnRHxjAAAAAElFTkSuQmCCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==</bitmap>
        </small_bitmap>
        <normal_bitmap item_width="24" item_height="24">
          <bitmap>iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6Q
AAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYSURBVEhL7cEBAQAAAIIg/6+uIU
AAAFwNCRgAAdACW14AAAAASUVORK5CYIIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==</bitmap>
        </normal_bitmap>
        <large_bitmap item_width="32" item_height="32">
          <bitmap>iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6Q
AAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAaSURBVFhH7cEBAQAAAIIg/69uSE
AAAADAuRoQIAABnXhJQwAAAABJRU5ErkJgggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==</bitmap>
        </large_bitmap>
    </bitmaps>
    <scripts />
</RhinoUI>
'''

TPL_MENUITEM = '''
<menu_item guid="{0}" item_type="normal">
    <text>
        <locale_1033>{1}</locale_1033>
    </text>
    <macro_id>{2}</macro_id>
</menu_item>
'''

TPL_MENUSEPARATOR = '''
<menu_item guid="{0}" item_type="separator">
    <text />
</menu_item>
'''

TPL_MACRO = '''
<macro_item guid="{0}">
    <text>
        <locale_1033>{1}</locale_1033>
    </text>
    <tooltip>
        <locale_1033>{3}</locale_1033>
    </tooltip>
    <help_text>
        <locale_1033>{4}</locale_1033>
    </help_text>
    <button_text>
        <locale_1033>{5}</locale_1033>
    </button_text>
    <menu_text>
        <locale_1033>{6}</locale_1033>
    </menu_text>
    <script>{2}</script>
</macro_item>
'''

TPL_TOOLBARGROUP = '''
<tool_bar_group guid="{0}"
                dock_bar_guid32=""
                dock_bar_guid64=""
                active_tool_bar_group=""
                single_file="{2[single_file]}"
                hide_single_tab="{2[hide_single_tab]}"
                point_floating="0,0">
    <text>
        <locale_1033>{1}</locale_1033>
    </text>
</tool_bar_group>
'''

TPL_TOOLBARGROUPITEM = '''
<tool_bar_group_item guid="{0}"
                     major_version="1"
                     minor_version="1">
    <text>
        <locale_1033>{1}</locale_1033>
    </text>
    <tool_bar_id>{2}</tool_bar_id>
</tool_bar_group_item>
'''

TPL_TOOLBAR = '''
<tool_bar guid="{0}"
          item_display_style="{2[item_display_style]}">
    <text>
        <locale_1033>{1}</locale_1033>
    </text>
</tool_bar>
'''

TPL_TOOLBARITEM = '''
<tool_bar_item guid="{0}"
               button_display_mode="control_only"
               button_style="normal">
    <text>
        <locale_1033>{1}</locale_1033>
    </text>
    <left_macro_id>{2}</left_macro_id>
    <right_macro_id></right_macro_id>
</tool_bar_item>
'''

TPL_TOOLBARSEPARATOR = '''
<tool_bar_item guid="{0}"
               button_display_mode="control_only"
               button_style="spacer">
    <text />
</tool_bar_item>
'''


class Rui(object):
    """
    This class provides the required functionality to make *.rui files

    Parameters:
        filepath (str): The path to the rui file.

    Attributes:
        filepath (str) : The path to the rui file.
        clear_file_contents (bool) : If `True`, clear the contents of the rui file
            before writing. Default is `True`.
        separator (str) : The token used as a separator between names and values
            in the comments. Default is `'=>'`.

    >>> rui = Rui('path/to/file.rui')
    >>> rui.add_macrocontroller()
    """
    def __init__(self, filepath, **config):
        self.filepath = filepath
        self.clear_file_contents = config.get('clear_file_contents', True)
        self.separator = config.get('separator', '=>')
        self.xml = None
        self.root = None
        self.root_macros = None
        self.root_menus = None
        self.root_toolbargroups = None
        self.root_toolbars = None
        self.macros = {}
        self.menus = {}
        self.menuitems = {}
        self.toolbars = {}
        self.toolbaritems = {}
        self.toolbargroups = {}
        self.default_macro_options = {}
        self.default_toolbargroup_options = {
            'single_file'     : 'False',
            'hide_single_tab' : 'False',
        }
        self.default_toolbar_options = {
            'item_display_style' : 'text_only',
        }
        self.parse()

    def check_filepath(self):
        if not os.path.exists(os.path.dirname(self.filepath)):
            try:
                os.makedirs(os.path.dirname(self.filepath))
            except OSError as e:
                if e.errno != os.errno.EEXIST:
                    raise e
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'wb+'):
                pass

    def clear(self):
        with open(self.filepath, 'wb+') as f:
            f.write(TPL_RUI.format(uuid.uuid4(), uuid.uuid4()))

    def parse(self):
        self.check_filepath()
        if self.clear_file_contents:
            self.clear()
        self.xml                = ET.parse(self.filepath)
        self.root               = self.xml.getroot()
        self.root_macros        = self.root.find('macros')
        self.root_menus         = self.root.find('menus')
        self.root_toolbargroups = self.root.find('tool_bar_groups')
        self.root_toolbars      = self.root.find('tool_bars')

    def write(self):
        xml = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="    ")
        xml = '\n'.join([line for line in xml.split('\n') if line.strip()])
        with open(self.filepath, 'wb+') as fh:
            fh.write(xml.encode('utf-8'))

    # ==========================================================================
    # comments
    # ==========================================================================

    def get_object_comments(self, obj):
        return inspect.getcomments(obj)

    def get_parsed_object_comments(self, obj):
        options = self.default_macro_options.copy()
        comments = self.get_object_comments(obj)
        if comments:
            comments = [comment.strip('#').strip() for comment in comments.split('\n')]
            comments = [comment.split(self.separator) for comment in comments]
            comments = [comment for comment in comments if len(comment) == 2]
            comments = dict((key.strip(), value.strip()) for key, value in comments)
            options.update(comments)
        return options

    # ==========================================================================
    # class methods
    # ==========================================================================

    def get_class_methods(self, cls):
        methods = inspect.getmembers(cls, inspect.ismethod)
        linenumbers = dict((name, self.get_method_linenumber(obj)) for name, obj in methods)
        return sorted(methods, key=lambda x: linenumbers[x[0]])

    def get_public_class_methods(self, cls):
        methods = self.get_class_methods(cls)
        return [method for method in methods if not method[0].startswith('_')]

    def get_protected_class_methods(self, cls):
        methods = self.get_class_methods(cls)
        return [method for method in methods if method[0].startswith('_') and not method[0].startswith('__')]

    def get_private_class_methods(self, cls):
        methods = self.get_class_methods(cls)
        return [method for method in methods if method[0].startswith('__')]

    def get_class_methods_docstrings(self, cls):
        pass

    def get_class_methods_comments(self, cls):
        methods = self.get_class_methods(cls)
        comments = dict((name, self.get_parsed_object_comments(obj)) for name, obj in methods)
        return comments

    def get_class_methods_linenumbers(self, cls):
        methods = self.get_class_methods(cls)
        numbering = dict((name, inspect.getsourcelines(obj)[1]) for name, obj in methods)
        return numbering

    # --------------------------------------------------------------------------

    def sort_methods(self, methods):
        comments = dict((name, self.get_method_comments(obj)) for name, obj in methods)
        linenumbers = dict((name, self.get_method_linenumber(obj)) for name, obj in methods)
        # the key-function
        def sortfunc(method):
            name, obj = method
            # menu = comments[name].get('menu', '')
            line = linenumbers[name]
            # pos  = int(comments[name].get('menu_pos', 0))
            menu = 0
            pos = 0
            return menu, line, pos
        return sorted(methods, key=sortfunc)

    # ==========================================================================
    # method properties
    # ==========================================================================

    def get_method_comments(self, obj):
        return self.get_parsed_object_comments(obj)

    def get_method_linenumber(self, obj):
        return inspect.getsourcelines(obj)[1]

    def get_method_docstring(self, obj):
        return inspect.getdoc(obj)

    def get_method_oneliner(self, obj):
        docstring = self.get_method_docstring(obj)
        if not docstring:
            return
        parts = docstring.trim().split('\n')
        return parts[0]

    # ==========================================================================
    # miscellaneous
    # ==========================================================================

    def set_default_macro_options(self, options):
        options.update(self.default_macro_options)

    # ==========================================================================
    # Add stuff
    # ==========================================================================

    def add_macrocontroller(self, controller, tool=None):
        if tool:
            instancename = tool.instancename + '.' + controller.instancename
        else:
            instancename = controller.instancename
        methods = self.get_public_class_methods(controller)
        self.add_macros(methods, instancename)
        self.add_menuitems(methods)
        self.add_toolbaritems(methods)

    # --------------------------------------------------------------------------
    # add macros
    # --------------------------------------------------------------------------

    def add_macros(self, members, prefix):
        for name, obj in members:
            guid        = str(uuid.uuid4())
            options     = self.get_parsed_object_comments(obj)
            funcname    = '{0}.{1}'.format(prefix, name)
            script      = '-_RunPythonScript ({0}())'.format(funcname)
            text        = options.get('text', funcname)
            script      = options.get('script', script)
            tooltip     = options.get('tooltip')
            help_text   = options.get('help_text')
            button_text = options.get('button_text', name)
            menu_text   = options.get('menu_text', ' '.join(name.split('_')))
            self.add_macro(name, guid, text, script, tooltip, help_text, button_text, menu_text)

    def add_macro(self, name, guid, text, script, tooltip='', help_text='', button_text='', menu_text=''):
        s_macro = TPL_MACRO.format(guid, text, script, tooltip, help_text, button_text, menu_text)
        e_macro = ET.fromstring(s_macro)
        self.root_macros.append(e_macro)
        self.macros[name] = e_macro
        return e_macro

    # --------------------------------------------------------------------------
    # add menus
    # --------------------------------------------------------------------------

    def add_menus(self, menus, root=None):
        for menu in menus:
            e_menu   = self.add_menu(menu, root=root)
            submenus = menu.get('menus', [])
            if submenus:
                self.add_menus(submenus, root=e_menu)

    def add_menu(self, menu, root=None):
        if root is None:
            root = self.root_menus
        if menu.get('separator', False):
            self.add_menuseparator(root)
        name   = menu['name']
        e_menu = ET.SubElement(root, 'menu')
        e_menu.set('guid', str(uuid.uuid4()))
        e_text           = ET.SubElement(e_menu, 'text')
        e_locale         = ET.SubElement(e_text, 'locale_1033')
        e_locale.text    = name
        self.menus[name] = e_menu
        return e_menu

    def add_menuitems(self, members):
        pos = 1
        for name, obj in members:
            if name not in self.macros:
                continue
            e_macro = self.macros[name]
            macro_guid = e_macro.attrib['guid']
            macro_options = self.get_parsed_object_comments(obj)
            if 'menu' in macro_options:
                menu = macro_options['menu']
                if menu in self.menus:
                    e_menu = self.menus[menu]
                    separator = macro_options.get('menu_separator', 'False')
                    separator = eval(separator)
                    if separator:
                        self.add_menuseparator(e_menu, pos)
                        pos += 1
                    # menu_text = ' '.join(name.split('_'))
                    # menu_text = macro_options.get('menu_text', menu_text)
                    menu_text = e_macro.find('menu_text').find('locale_1033').text
                    self.add_menuitem(e_menu, macro_guid, menu_text, pos)
                    pos += 1

    def add_menuitem(self, root, macro_id, menu_text, pos=None):
        guid = uuid.uuid4()
        s_menuitem = TPL_MENUITEM.format(guid, menu_text, macro_id)
        e_menuitem = ET.fromstring(s_menuitem)
        if pos is None:
            root.append(e_menuitem)
        else:
            root.insert(pos, e_menuitem)
        return e_menuitem

    def add_menuseparator(self, root, pos=None):
        guid = uuid.uuid4()
        s_separator = TPL_MENUSEPARATOR.format(guid)
        e_separator = ET.fromstring(s_separator)
        if pos is None:
            root.append(e_separator)
        else:
            root.insert(pos, e_separator)
        return e_separator

    # --------------------------------------------------------------------------
    # add toolbars
    # --------------------------------------------------------------------------

    def add_toolbars(self, toolbars):
        for toolbar in toolbars:
            self.add_toolbar(toolbar)

    def add_toolbar(self, toolbar):
        options = self.default_toolbar_options.copy()
        options.update(toolbar)
        root = self.root_toolbars
        name = toolbar['name']
        guid = uuid.uuid4()
        text = name
        s_tb = TPL_TOOLBAR.format(guid, text, options)
        e_tb = ET.fromstring(s_tb)
        root.append(e_tb)
        self.toolbars[name] = e_tb
        return e_tb

    def add_toolbaritems(self, members):
        # pos = 1
        for name, obj in members:
            if name not in self.macros:
                continue
            e_macro = self.macros[name]
            macro_guid = e_macro.attrib['guid']
            macro_options = self.get_parsed_object_comments(obj)
            if 'toolbar' in macro_options:
                toolbar = macro_options['toolbar']
                if toolbar in self.toolbars:
                    e_toolbar = self.toolbars[toolbar]
                    separator = macro_options.get('toolbar_separator', 'False')
                    separator = eval(separator)
                    if separator:
                        self.add_toolbarseparator(e_toolbar)
                        # pos += 1
                    # button_text = macro_options.get('button_text', name)
                    button_text = e_macro.find('button_text').find('locale_1033').text
                    self.add_toolbaritem(e_toolbar, macro_guid, button_text)
                    # pos += 1

    def add_toolbaritem(self, root, macro_id, button_text, pos=None):
        guid = uuid.uuid4()
        s_toolbaritem = TPL_TOOLBARITEM.format(guid, button_text, macro_id)
        e_toolbaritem = ET.fromstring(s_toolbaritem)
        if pos is None:
            root.append(e_toolbaritem)
        else:
            root.insert(pos, e_toolbaritem)
        return e_toolbaritem

    def add_toolbarseparator(self, root, pos=None):
        guid = uuid.uuid4()
        s_separator = TPL_TOOLBARSEPARATOR.format(guid)
        e_separator = ET.fromstring(s_separator)
        if pos is None:
            root.append(e_separator)
        else:
            root.insert(pos, e_separator)
        return e_separator

    # --------------------------------------------------------------------------
    # add toolbargroups
    # --------------------------------------------------------------------------

    def add_toolbargroups(self, toolbargroups):
        for tbg in toolbargroups:
            self.add_toolbargroup(tbg)

    def add_toolbargroup(self, toolbargroup):
        options = self.default_toolbargroup_options.copy()
        options.update(toolbargroup)
        root  = self.root_toolbargroups
        name  = toolbargroup['name']
        guid  = uuid.uuid4()
        text  = name
        s_tbg = TPL_TOOLBARGROUP.format(guid, text, options)
        e_tbg = ET.fromstring(s_tbg)
        root.append(e_tbg)
        self.toolbargroups[name] = e_tbg
        if 'toolbars' in toolbargroup:
            for tb in toolbargroup['toolbars']:
                self.add_toolbargroupitem(e_tbg, tb)
        return e_tbg

    def add_toolbargroupitem(self, root, toolbar_name, pos=None):
        if toolbar_name not in self.toolbars:
            return
        e_tb   = self.toolbars[toolbar_name]
        tb_id  = e_tb.attrib['guid']
        text   = toolbar_name
        guid   = uuid.uuid4()
        s_tbgi = TPL_TOOLBARGROUPITEM.format(guid, text, tb_id)
        e_tbgi = ET.fromstring(s_tbgi)
        if pos is None:
            root.append(e_tbgi)
        else:
            root.insert(pos, e_tbgi)
        return e_tbgi


# ==============================================================================
# Debugging
# ==============================================================================


if __name__ == '__main__':

    class Controller(object):

        def __init__(self):
            pass

        # tooltip           => init MeshTools
        # help_text         => init MeshTools
        # menu              => MeshTools
        # toolbar           => MeshTools
        # script            => -_RunPythonScript ResetEngine (import sys)
        def init(self):
            pass

    menus = [
        {'name': 'MeshTools', 'menus': []}
    ]

    toolbargroups = [
        {'name': 'MeshTools', 'toolbars': ['MeshTools']}
    ]

    toolbars = [
        {'name': 'MeshTools', },
    ]

    rui = Rui('./data/test.rui')

    rui.add_menus(menus)
    rui.add_toolbars(toolbars)
    rui.add_toolbargroups(toolbargroups)

    methods = rui.get_public_class_methods(Controller)

    rui.add_macros(methods, 'meshtools')
    rui.add_menuitems(methods)
    rui.add_toolbaritems(methods)

    rui.write()
