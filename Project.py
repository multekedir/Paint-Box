class Project:
    """A simple example class"""

    def __init__(self, name):
         self.tag_list = []
         self.name = name

    def add_tag(self, tags):
        for i in tags:
             self.tag_list.append(i)

    def remove_tag(self, tag):
        index = self.tag_list.index(tag)
        del self.tag_list[index]

    def set_name(self, name):
        self.name = name
        
