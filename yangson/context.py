from typing import Dict, MutableSet
from .constants import YangsonException
from .statement import Statement
from .typealiases import *

"""Context for schema generation."""

class Context:
    """This class provides context for schema generation.

    The information is installed in class varables, which means that
    different schemas cannot be generated in parallel.
    """

    modules = {} # type: Dict[ModuleId, Statement]
    """Dictionary of parsed modules comprising the data model."""

    prefix_map = {} # type: Dict[ModuleId, Dict[YangIdentifier, ModuleId]]
    """Per-module prefix assignments."""

    ns_map = {} # type: Dict[YangIdentifier, YangIdentifier]
    """Map of module and submodule names to namespaces."""

    features = set() # type: MutableSet[QName]

    @classmethod
    def resolve_qname(cls, mid: ModuleId,
                      qname: QName) -> Tuple[ModuleId, YangIdentifier]:
        """Resolve prefix-based QName.

        :param mid: identifier of the context module
        :param qname: qualified name in prefix form
        """
        p, s, loc = qname.partition(":")
        try:
            return (cls.prefix_map[mid][p], loc) if s else (mid, p)
        except KeyError:
            raise BadQName(qname) from None

    @classmethod
    def translate_qname(cls, mid: ModuleId, qname: QName) -> NodeName:
        """Translate prefix-based QName to an absolute name.

        :param mid: identifier of the context module
        :param qname: qualified name in prefix form
        """
        nid, loc = cls.resolve_qname(mid, qname)
        return (loc, nid[0])

    @classmethod
    def sid2address(cls, mid: ModuleId, sid: str) -> SchemaAddress:
        """Construct schema address from a schema node identifier.

        :param mid: identifier of the context module
        :param sid: schema node identifier (absolute or relative)
        """
        nlist = sid.split("/")
        return [ cls.translate_qname(mid, qn)
                 for qn in (nlist[1:] if sid[0] == "/" else nlist) ]

    @classmethod
    def path2address(cls, path: str) -> SchemaAddress:
        """Translate path to schema address.

        :param path: schema or data path
        """
        nlist = path.split("/")
        prevns = None
        res = []
        for n in (nlist[1:] if path[0] == "/" else nlist):
            p, s, loc = n.partition(":")
            if s:
                if p == prevns: raise BadPath(path)
                res.append((loc, p))
                prevns = p
            elif prevns:
                res.append((p, prevns))
            else:
                raise BadPath(path)
        return res

    @classmethod
    def get_definition(cls, stmt: Statement, mid: ModuleId) -> Statement:
        """Return the statement defining a grouping or derived type.

        :param stmt: "uses" or "type" statement
        :param mid: YANG module context
        """
        kw = "grouping" if stmt.keyword == "uses" else "typedef"
        did, loc = cls.resolve_qname(mid, stmt.argument)
        dstmt = (stmt.get_definition(loc, kw) if did == mid else
                 cls.modules[did].find1(kw, loc, required=True))
        return (dstmt, did)

class BadPath(YangsonException):
    """Exception to be raised for invalid schema or data path."""

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return self.path

class BadQName(YangsonException):
    """Exception to be raised for QName."""

    def __init__(self, qname: str) -> None:
        self.qname = qname

    def __str__(self) -> str:
        return self.qname
