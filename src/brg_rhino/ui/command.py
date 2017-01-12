""""""

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'

import rhinoscriptsyntax as rs

class Command(object):
	pass


class CommandLoop(object):
	""""""

	def __init__(self):
		self.options = None
		self.default = None
		self.option = None
		self.message = None

	def is_option(self):
		if not self.option:
			return False
		if self.option not in self.options:
			return False

	def get_option(self):
		self.option = rs.GetString(self.message, self.default, self.options)

	def handle_option(self):
		self.handlers[self.option]()

	def loop(self):
		while True:
			self.get_option()
			if not self.is_option():
				return
			self.handle_option()



#rhino style command line menu
def command_line_menu(interface):
    if rs.GetDocumentData(interface["ID"],interface["ID"]): 
        interface["default"] = rs.GetDocumentData(interface["ID"],interface["ID"])
    new_options = []
    sub_menus = {}
    for option in interface["options"]:
        if isinstance(option, basestring):
            new_options.append(option)
        else:
            new_options.append(option["show"])
            sub_menus[option["show"]] = option
    result = rs.GetString(interface["message"],interface["default"],new_options)
    interface["default"] = result
    rs.SetDocumentData(interface["ID"],interface["ID"],result)
    if result in sub_menus: result = command_line_menu(sub_menus[result])
    return result
    


if __name__ == "__main__":

    #template for command line menu
	interface_3 =   {"options":["sub_sub_option_1","sub_sub_option_2"],
	                "message":"Select C",
	                "default":"sub_sub_option_1",
	                "show":"sub_sub_menu",
	                "ID":"interface_3"}
	
	interface_2 =   {"options":["sub_option_1",interface_3],
	                "message":"Select B",
	                "default":"sub_option_1",
	                "show":"sub_menu",
	                "ID":"interface_2"}
	
	interface_1 =   {"options":["option_1","option_2",interface_2],
	                "message":"Select A",
	                "default":"option_1",
	                "show":None,
	                "ID":"interface_1"}
	
	print command_line_menu(interface_1)
