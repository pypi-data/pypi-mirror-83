from rich.table import Table
from rich.console import Console

class Debugger: 

    def __init__(self, obj: any,) -> dict:
        self.obj = obj
        self.methods(noDunder=True)

    def methods(self, output:bool = True, noDunder:bool = False) -> dict:
        """ returns a dict of method name and doc string.
        :arg: output: output tabe
        :arg: noDunder: removes all dunder methods
        """
        
        tbl = Table(show_lines=True)
        tbl.add_column('name')
        tbl.add_column('doc string')
        tbl.add_column('profile')

        return_obj = {}

        for method in dir(self.obj):
            doc_string = getattr(self.obj, method).__doc__
            profile = str(getattr(self.obj, method))

            if noDunder:
                if method[:2] == '__':
                    continue

            tbl.add_row(method, doc_string, profile)
            return_obj[method] = doc_string

        if output:
            Console().print(tbl)
        return return_obj

