#from typing import Protocol
#from typing import Protocol, Optional, Union
from typing import Protocol, Union, Any, Dict, Optional
#from mcp.types import (
#    ElicitRequestParams as MCPElicitRequestParams,
#    ElicitResult,
#    ErrorData,
#)
from mcp.types import ElicitResult, ErrorData

# 创建全新的ElicitRequestParams类，完全不依赖MCPElicitRequestParams
class ElicitRequestParams:
    """重新实现的请求参数类，避免继承导致的types.UnionType错误"""
    
    def __init__(self, **kwargs):
        # 设置默认值
        self.server_name: Optional[str] = kwargs.get("server_name", None)
        
        # 存储所有原始数据
        self._raw_data = kwargs.copy()
        
        # 动态设置其他属性（避免类型注解冲突）
        for key, value in kwargs.items():
            if key != 'server_name':
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        attrs = []
        for key in dir(self):
            if not key.startswith('_'):
                try:
                    value = getattr(self, key)
                    if not callable(value):
                        attrs.append(f"{key}={value!r}")
                except:
                    pass
        return f"ElicitRequestParams({', '.join(attrs)})"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {"server_name": self.server_name}
        result.update(self._raw_data)
        return result


#class ElicitRequestParams(MCPElicitRequestParams):
    #server_name: str | None = None
#    server_name: Optional[str] = None
#    """Name of the MCP server making the elicitation request"""


class ElicitationCallback(Protocol):
    """Protocol for callbacks that handle elicitations."""

    #async def __call__(self, request: ElicitRequestParams) -> ElicitResult | ErrorData:
    async def __call__(self, request: ElicitRequestParams) -> Union[ElicitResult, ErrorData]:
        """Handle a elicitation request.

        Args:
            request (ElicitRequestParams): The elictation request to handle

        Returns:
            ElicitResult | ErrorData: The elicitation response to return back to the MCP server
        """
        ...
