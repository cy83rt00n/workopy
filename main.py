import os
import pathlib
import sys
import cli
import yaml
import pprint

worcopy_root_dir = None
assets_root_dir = None
projects_root_dir = None

class Worko:
    root_dir = None
    assets_dir = None
    projects_dir = None

    def __init__(self, root_dir = None) -> None:
        path = pathlib.Path()

        self.root_dir = root_dir

        if self.root_dir is None:
            self.root_dir = path.joinpath(path.home(), 'workspace-2/')

        self.assets_dir = self.root_dir.joinpath('assets/')
        self.projects_dir = self.root_dir.joinpath('projects/')
        self.check_hier()

    def check_hier(self):
        path = pathlib.Path(self.root_dir)

        if not self.root_dir.exists():
            self.root_dir.mkdir()

        if not self.assets_dir.exists():
            self.assets_dir.mkdir()

        if not self.projects_dir.exists():
            self.projects_dir.mkdir()

    def create_project_dir(self, project_name):
            
        if not self.projects_dir.joinpath(project_name).exists():
            self.projects_dir.joinpath(project_name).mkdir(mode=0o755,parents=True,exist_ok=True)
        

    def create_project_copy_dir(self, project_name):
        print('scanning worko projects dir...')

        copy_dir_name = self.make_project_copy_dir_name(project_name)
        copy_dir= self.projects_dir.joinpath(project_name, copy_dir_name)
        print(f'New copy {copy_dir} will be created...')
        copy_dir.mkdir(mode=0o755,parents=True)

    def count_project_copies(self, project_name):
        copies_count = 0

        for copy_path in self.projects_dir.joinpath(project_name).glob('*'):
                copies_count += 1 if copy_path.is_dir() else 0
        
        print(f'{copies_count} copies found for project {project_name}')
        
        return copies_count


    def make_project_copy_dir_name(self, project_name):
        
        return self.projects_dir.joinpath(project_name).stem + f'-{self.count_project_copies(project_name)+1}'


    def make_copy_by_pattern(self,pattern_name):
        def wrapper(*args, **kwargs):
            handler = WorkoCopyNamePatterns().__getattribute__(pattern_name)
            handler(*args, **kwargs)
        return wrapper


    def scan_projects(self, start_path = None, as_list = False, with_copies=True):
        max_nested_level = 3  if with_copies else 2
        start_path = self.projects_dir if start_path is None else self.projects_dir.joinpath(start_path)

        projects_list = []

        for sub_path in start_path.rglob('*'):
            current_nested_level = len(sub_path.relative_to(start_path).parts)
            if current_nested_level < max_nested_level:
                continue

            if sub_path.is_dir() and  current_nested_level == max_nested_level:
                if max_nested_level == 3:
                    namespace, project, copy = sub_path.relative_to(start_path).parts
                    print(f'namespace: {namespace}, project: {project}, copy: {copy}')
                else:
                    namespace, project = sub_path.relative_to(start_path).parts
                    print(f'namespace: {namespace}, project: {project}')
                if as_list:
                    projects_list.append(sub_path.relative_to(start_path))

        if as_list:
            return projects_list


    def scan_copies(self, project_name):
        for copy_path in self.projects_dir.joinpath(project_name).glob('*'):
            if copy_path.is_dir():
                namespace, project, copy = copy_path.relative_to(self.projects_dir).parts
                print(f'namespace: {namespace}, project: {project}, copy: {copy}')


    def welcome(self):
        project = cli.prompt("Select project to scan")
        project = project.replace('\\', os.path.sep)

        if project == 'all':
            self.scan_projects()
            return True

        if project == 'select':
            self.selector()
            return True

        if project == 'copy':
            project_path = self.select_project()
            self.create_project_copy_dir(project_path)
            return True

        if project == 'project':
            project_name = cli.prompt("New project name")
            project_name = project_name.replace('\\', os.path.sep)
            if len(pathlib.Path(project_name).parts) != 2:
                print(f"Wrong project name ({project_name}). Project name is 'namespace\\project_name'")
                return False
            self.create_project_dir(project_name)
            return True

        if len(pathlib.Path(project).parts) != 2:
            print("Wrong project name. Project name is 'namespace\\project_name'")
            return False

        self.scan_copies(project)
        return True


    def select_project(self):
        selection = cli.select(self.scan_projects(as_list=True, with_copies=False))
        return selection


    def selector(self):
        selection = cli.select(self.scan_projects(as_list=True))
        self.scan_copies(selection)


class WorkoCopyNamePatterns():
    """
        WorkoCopyNamePatterns - provides copy name generation functions
    """


    def port_based_copy_pattern(self, project_name):    
        """
            pattern_name: port_based
        """
        print(f"Port based copy pattern for {project_name}")


    def autoincrement_copy_pattern(self, project_name):
        """
            pattern_name: autoincrement
        """
        print(f"Port based copy pattern for {project_name}")


def eval_config_value(value):
    ev_value = eval(value)

    if isinstance(ev_value,range):
        ev_value = list(ev_value)

    return ev_value


def main():

    worko = Worko()

    # worko.welcome()

    # pattern_name = 'port_based_copy_pattern'
    # worko.make_copy_by_pattern(pattern_name)("company\\the-project")    

    y = yaml.safe_load(pathlib.Path("./port_based.yaml").open())

    copyname_parts = dict()
    
    for part_name,rule in y['copy_name_parts'].items():
        if isinstance(rule,(dict)):
            copyname_parts[part_name] = eval_config_value(rule['eval'])
        if isinstance(rule,(str)):
            copyname_parts[part_name] = rule

    pprint.pprint(copyname_parts)

    methods = [method for method in WorkoCopyNamePatterns.__dict__ if callable(WorkoCopyNamePatterns().__getattribute__(method))]
    pprint.pprint(methods)

main()