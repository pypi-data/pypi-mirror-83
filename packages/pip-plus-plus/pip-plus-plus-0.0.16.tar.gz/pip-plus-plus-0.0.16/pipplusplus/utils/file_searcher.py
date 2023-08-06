import os


class PathlibFileSearcher(object):
    @classmethod
    def find_file(cls, head, file_name, should_contain=None):
        found = PathlibFileSearcher.check_path()
        if not found:
            for file in head.glob(f"**/{file_name}"):
                if "Python" not in str(file):
                    found += [str(file)]
        return found

    @classmethod
    def filter(cls, found, should_contain=None):
        if should_contain is None:
            return found
        new_found = []
        for s_con in should_contain:
            for child in found:
                if s_con in str(child):
                    new_found += [child]
        return new_found

    @classmethod
    def check_path(cls):
        path_ev = os.environ['PATH'].split(";")
        for val in path_ev:
            if "Python" in val and "Scripts" in val:
                return [val]
        return []



