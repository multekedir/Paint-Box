import Project

pro = Project.Project("test")

assert pro.get_name() == "test", "Should be test"

pro.set_name("new")

assert pro.get_name() == "new", "Should be new"

pro.add_tag("gold")
pro.add_tag("tag1")
pro.add_tag("tag2")

assert pro.get_tags() == ['gold', 'tag1', 'tag2'], "Should be ['gold', 'tag1', 'tag2']"

pro.remove_tag("tag1")

assert pro.get_tags() == ['gold', 'tag2'], "Should be ['gold', 'tag2']"

pro.add_process("you")
pro.add_process("poiob")

#assert pro.get_processes == ['you', 'poiob'], "Should be ['you', 'poiob']"

print(pro.get_processes())

for i in pro.get_processes():
    print(i.get_name())

if __name__ == "__main__":
    print("Everything passed")
