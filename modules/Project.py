class Process:
    def __init__ (self, name):
        self.name  = name

    def set_name(self, name):
        self.name = name

    def set_description(self, des):
        self.description = des
    
    def set_img(self, url):
        self.img_url = url
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description

    def get_img(self):
        return self.img_url


class Project:
    """A simple example class"""

    def __init__(self, name, id):
         self.tag_list = []
         self.name = name
         self.process_list = []
         self.id = id
    
    def get_id(self):
        return self.id

    def add_tag(self, tags):
        self.tag_list.append(tags)

    def remove_tag(self, tag):
        index = self.tag_list.index(tag)
        del self.tag_list[index]
    
    def get_tags(self):
        return self.tag_list

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_process(self, name):
        pro = Process(name)
        self.process_list.append(pro)

    def get_processes(self):
        return self.process_list



    

    
        
