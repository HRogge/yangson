"""Type aliases (for type hints)."""

from typing import Any, Dict, List, Optional, Tuple, Union

RevisionDate = Optional[str]
Uri = str
YangIdentifier = str
NodeName = Tuple[YangIdentifier, YangIdentifier] # (namespace, name)
SchemaAddress = List[NodeName]
ModuleId = Tuple[YangIdentifier, Optional[RevisionDate]]
Range = List[List[Any]]
QName = Tuple[YangIdentifier, YangIdentifier]
PrefixMap = Dict[YangIdentifier, ModuleId]
