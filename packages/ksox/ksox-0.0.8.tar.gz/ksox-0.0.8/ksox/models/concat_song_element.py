# ------------------------------------------------------- class: ConcatSongElement ------------------------------------------------------- #

from jsoncodable import JSONCodable
class ConcatSongElement(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        path: str,
        start: float,
        end: float
    ):
        self.path = path
        self.name = path.split('/')[-1]
        self.name_no_ext = self.name.split('.')[0]
        self.start = start
        self.end = end
        self.duration = end - start


# ---------------------------------------------------------------------------------------------------------------------------------------- #