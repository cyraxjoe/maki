class Controller(object):
    __views__ = ()


    def __init__(self):
        self.__branches__ = {}
        self.__init_branches()

    def __setattr__(self, name, value):
        # if is a controller, merge the subtree.
        if isinstance(value, Controller):
            for mime, branch in value.__branches__.items():
                if mime not in self.__branches__:
                    self.__create_branch(mime) # bridge branch.
                setattr(self.__branches__[mime], name, branch)
        super(Controller, self).__setattr__(name, value)


    def __init_branches(self):        
        for ViewClass in self.__views__:
            self.__create_branch(ViewClass.__mime__,
                                 (self, ),  # connect the controller.
                                 ViewClass)
        # create the routes of the subcontrollers already binded to the class
        # We are using again the "isinstance" because the value could
        # be a method and this will make it a function.
        for name, value in vars(self.__class__).items():
            if not name.startswith('_') and \
                   isinstance(value, Controller):
                setattr(self, name, value)


    def __create_branch(self, mime, initargs=(), *parents):
        if mime in self.__branches__:
            raise Exception('Branch "%s" already exists' % mime)
        else:
            clsname = ''.join([self.__class__.__name__,
                               mime.split('/')[-1].upper(),
                               'Branch'])
            Branch = type(clsname, parents, {})
            self.__branches__[mime] = Branch(*initargs)
