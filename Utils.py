import json

from models import GartmentTable


class Utils:

    @staticmethod
    def mount_table_return(table: GartmentTable):
        obj = {
            "width": table.width, "height": table.height,
            "maxRects": table.bin_maxrects,
            "skyline": table.bin_skyline,
            "guillotine": table.bin_guillotine
        }

        return json.dumps(obj)