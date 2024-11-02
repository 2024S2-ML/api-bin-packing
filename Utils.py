import json

from models import GartmentTable


class Utils:

    @staticmethod
    def mount_table_return(table: GartmentTable):
        obj = {
            "width": table.width, "height": table.height,
            "rects": table.bin_guillotine
        }

        return json.dumps(obj)