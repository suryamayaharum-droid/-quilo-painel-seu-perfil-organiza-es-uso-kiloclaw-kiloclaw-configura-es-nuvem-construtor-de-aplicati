"""
HoloOS LangChain Adapter
=========================
Adapter para integração com LangChain.
Permite usar ferramentas e memória do HoloOS no LangChain.
"""

from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

try:
    from langchain_core.tools import BaseTool
    from langchain_core.callbacks import CallbackManagerForToolRun
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("LangChain not installed. Install with: pip install langchain-core")


class HoloOSTool:
    """Wrapper para ferramentas do HoloOS no LangChain."""
    
    def __init__(self, name: str = "holoos_tool", description: str = "Ferramenta do HoloOS", holoos_tool: Any = None):
        self.name = name
        self.description = description
        self.holoos_tool = holoos_tool
    
    def run(self, tool_input: str) -> str:
        """Executa a ferramenta do HoloOS."""
        if not self.holoos_tool:
            return "Error: No HoloOS tool configured"
        
        try:
            result = self.holoos_tool.execute(tool_input)
            return str(result)
        except Exception as e:
            return f"Error executing tool: {e}"


class LangChainAdapter:
    """
    Adapter para integrar HoloOS com LangChain.
    
    Converte ferramentas, memória e agentes do HoloOS
    para formatos compatíveis com LangChain.
    """
    
    def __init__(self, holoos_system: Any = None):
        """
        Inicializa o adapter.
        
        Args:
            holoos_system: Instância do sistema HoloOS ou módulos específicos
        """
        self.holoos_system = holoos_system
        self._tools_cache: List[Any] = []
        
    def to_langchain_tools(
        self,
        tool_executor: Any = None
    ) -> List[Any]:
        """
        Converte ferramentas do HoloOS para LangChain.
        
        Args:
            tool_executor: ToolExecutor do HoloOS
            
        Returns:
            Lista de ferramentas LangChain
        """
        if not LANGCHAIN_AVAILABLE:
            logger.error("LangChain not available")
            return []
        
        tools = []
        
        # Se não passou executor, tenta pegar do sistema
        if tool_executor is None and self.holoos_system:
            try:
                from holoos import get_tool_executor
                tool_executor = get_tool_executor()
            except Exception:
                pass
        
        if tool_executor:
            # Pega ferramentas registradas
            registered_tools = tool_executor.registry.list_tools()
            
            for tool_info in registered_tools:
                tool_name = tool_info.get("name", "unknown")
                tool_desc = tool_info.get("description", "")
                
                # Cria wrapper LangChain
                lc_tool = HoloOSTool(
                    name=tool_name,
                    description=tool_desc,
                    holoos_tool=tool_executor
                )
                tools.append(lc_tool)
        
        self._tools_cache = tools
        return tools
    
    def create_agent_executor(
        self,
        llm: Any,
        tools: Optional[List[Any]] = None
    ) -> Any:
        """
        Cria um Agent Executor do LangChain com ferramentas do HoloOS.
        
        Args:
            llm: Modelo de linguagem do LangChain
            tools: Lista de ferramentas (usa cache se None)
            
        Returns:
            Agent Executor configurado
        """
        if not LANGCHAIN_AVAILABLE:
            logger.error("LangChain not available")
            return None
        
        try:
            from langchain.agents import initialize_agent, AgentType
            
            tools_to_use = tools or self._tools_cache
            
            if not tools_to_use:
                logger.warning("No tools available for agent")
                return None
            
            agent = initialize_agent(
                tools=tools_to_use,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )
            
            return agent
            
        except Exception as e:
            logger.error(f"Error creating agent executor: {e}")
            return None
    
    def sync_memory(
        self,
        langchain_memory: Any,
        holoos_memory: Any = None
    ) -> None:
        """
        Sincroniza memória entre LangChain e HoloOS.
        
        Args:
            langchain_memory: Instância de memória do LangChain
            holoos_memory: Instância de memória do HoloOS
        """
        if holoos_memory is None and self.holoos_system:
            try:
                from holoos import get_memory
                holoos_memory = get_memory()
            except Exception:
                pass
        
        if not holoos_memory:
            logger.warning("No HoloOS memory available for sync")
            return
        
        # Implementação de sincronização bidirecional
        # (depende das APIs específicas de cada sistema)
        logger.info("Memory sync not fully implemented yet")
    
    def create_retriever(self, vector_store: Any = None) -> Any:
        """
        Cria um retriever do LangChain baseado no RAG do HoloOS.
        
        Args:
            vector_store: Vector store do LangChain (opcional)
            
        Returns:
            Retriever configurado
        """
        if not LANGCHAIN_AVAILABLE:
            return None
        
        try:
            from langchain_core.retrievers import BaseRetriever
            
            class HoloOSRetriever(BaseRetriever):
                def _get_relevant_documents(self, query: str) -> List[Any]:
                    # Usa o motor RAG do HoloOS
                    try:
                        from holoos.rag import get_rag_engine
                        rag = get_rag_engine()
                        results = rag.retrieve(query, top_k=5)
                        return [doc.content for doc in results]
                    except Exception as e:
                        logger.error(f"RAG retrieval error: {e}")
                        return []
            
            return HoloOSRetriever()
            
        except Exception as e:
            logger.error(f"Error creating retriever: {e}")
            return None


def get_langchain_adapter(holoos_system: Any = None) -> LangChainAdapter:
    """Factory function para criar adapter LangChain."""
    return LangChainAdapter(holoos_system)


__all__ = [
    "LangChainAdapter",
    "HoloOSTool",
    "get_langchain_adapter"
]
