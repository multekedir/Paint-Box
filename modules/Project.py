class Process:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.img_url = ""

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

    def __init__(self, name, num):
        self.tag_list = []
        self.name = name
        self.process_list = []
        self.id = num
        self.description = ""

    def get_id(self):
        return self.id

    def add_tag(self, tags):
        if isinstance(tags, list):
            for i in tags:
                self.tag_list.append(i)
        else:
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

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def add_process(self, name):
        pro = Process(name)
        self.process_list.append(pro)

    def get_processes(self):
        return self.process_list
