"""
Master Orchestrator Agent - Natural Language Interface for All Operations
Uses LangGraph for multi-agent workflow coordination
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from enum import Enum

import anthropic
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

from .book_rebrander import BookRebranderAgent
from .game_emulator import GameEmulatorAgent

logger = logging.getLogger(__name__)


class TaskType(str, Enum):
    BOOK_SEARCH = "book_search"
    BOOK_REBRAND = "book_rebrand"
    GAME_SEARCH = "game_search"
    GAME_BUNDLE = "game_bundle"
    CREATE_COURSE = "create_course"
    MONETIZE = "monetize"
    UNKNOWN = "unknown"


@dataclass
class AgentState:
    """State object passed between nodes in LangGraph"""
    user_request: str
    task_type: TaskType
    parameters: Dict[str, Any]
    results: Dict[str, Any]
    errors: List[str]
    messages: List[Any]
    next_action: Optional[str] = None


class MasterOrchestratorAgent:
    """
    Natural language interface for all Internet Archive operations
    
    Capabilities:
    - Understand complex multi-step requests
    - Decompose into specialized agent tasks
    - Coordinate execution across agents
    - Provide real-time progress updates
    - Handle errors gracefully
    
    Example requests:
    - "Find 10 programming books from the 1990s and update them"
    - "Create a NES game collection with 50 games and emulators"
    - "Turn these 5 books into a course and set up payments"
    """
    
    def __init__(
        self,
        ia_client,
        anthropic_api_key: str,
        openai_api_key: Optional[str] = None
    ):
        self.ia = ia_client
        self.claude = anthropic.AsyncAnthropic(api_key=anthropic_api_key)
        
        # Initialize specialized agents
        self.book_agent = BookRebranderAgent(
            ia_client=ia_client,
            anthropic_api_key=anthropic_api_key,
            openai_api_key=openai_api_key
        )
        
        self.game_agent = GameEmulatorAgent(ia_client=ia_client)
        
        # Build LangGraph workflow
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Define nodes
        workflow.add_node("understand", self._understand_request)
        workflow.add_node("plan", self._create_plan)
        workflow.add_node("execute_book", self._execute_book_task)
        workflow.add_node("execute_game", self._execute_game_task)
        workflow.add_node("execute_course", self._execute_course_task)
        workflow.add_node("execute_monetize", self._execute_monetize_task)
        workflow.add_node("finalize", self._finalize_results)
        
        # Set entry point
        workflow.set_entry_point("understand")
        
        # Define edges
        workflow.add_edge("understand", "plan")
        
        # Conditional routing from plan
        workflow.add_conditional_edges(
            "plan",
            self._route_task,
            {
                "book": "execute_book",
                "game": "execute_game",
                "course": "execute_course",
                "monetize": "execute_monetize",
                "finalize": "finalize"
            }
        )
        
        # All execution nodes go to finalize
        workflow.add_edge("execute_book", "finalize")
        workflow.add_edge("execute_game", "finalize")
        workflow.add_edge("execute_course", "finalize")
        workflow.add_edge("execute_monetize", "finalize")
        
        # Finalize goes to END
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    async def _understand_request(self, state: AgentState) -> AgentState:
        """Understand the user's request using AI"""
        logger.info(f"Understanding request: {state.user_request}")
        
        prompt = f"""Analyze this user request for Internet Archive operations:

USER REQUEST:
{state.user_request}

Identify:
1. Primary task type: book_search, book_rebrand, game_search, game_bundle, create_course, monetize
2. Key parameters (search queries, filters, quantities, etc.)
3. Multiple steps if complex request

OUTPUT (JSON):
{{
    "task_type": "book_rebrand",
    "parameters": {{
        "search_query": "programming",
        "year_range": [1990, 1999],
        "max_results": 10,
        "enhancement": "update code examples to modern syntax",
        "rebrand": {{"brand_name": "CodeMaster Academy"}}
    }},
    "multi_step": false,
    "estimated_complexity": "medium"
}}
"""
        
        response = await self.claude.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse AI response
        try:
            understanding = json.loads(response.content[0].text)
            state.task_type = TaskType(understanding.get('task_type', 'unknown'))
            state.parameters = understanding.get('parameters', {})
            state.messages.append(AIMessage(content=f"Understood: {understanding.get('task_type')}"))
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse understanding: {e}")
            state.task_type = TaskType.UNKNOWN
            state.errors.append(f"Could not understand request: {e}")
        
        return state
    
    async def _create_plan(self, state: AgentState) -> AgentState:
        """Create execution plan"""
        logger.info(f"Creating plan for task: {state.task_type}")
        
        if state.task_type == TaskType.BOOK_REBRAND:
            state.next_action = "book"
            state.messages.append(AIMessage(content="Plan: Search books → Download → Enhance → Rebrand → Export"))
        
        elif state.task_type == TaskType.GAME_BUNDLE:
            state.next_action = "game"
            state.messages.append(AIMessage(content="Plan: Search games → Download ROMs → Create bundle → Package"))
        
        elif state.task_type == TaskType.CREATE_COURSE:
            state.next_action = "course"
            state.messages.append(AIMessage(content="Plan: Analyze materials → Generate outline → Create lessons → Export"))
        
        elif state.task_type == TaskType.MONETIZE:
            state.next_action = "monetize"
            state.messages.append(AIMessage(content="Plan: Create product → Set pricing → Setup Stripe → Generate checkout"))
        
        else:
            state.next_action = "finalize"
            state.errors.append("Unknown task type")
        
        return state
    
    def _route_task(self, state: AgentState) -> str:
        """Route to appropriate execution node"""
        return state.next_action or "finalize"
    
    async def _execute_book_task(self, state: AgentState) -> AgentState:
        """Execute book-related tasks"""
        logger.info("Executing book task")
        
        try:
            params = state.parameters
            
            # Search books
            books = await self.book_agent.search_books(
                query=params.get('search_query', ''),
                year_range=tuple(params.get('year_range', [])) if params.get('year_range') else None,
                max_results=params.get('max_results', 10)
            )
            
            state.results['books_found'] = len(books)
            state.messages.append(AIMessage(content=f"Found {len(books)} books"))
            
            # Download and process if requested
            if params.get('download', True) and books:
                processed_books = []
                
                for book_meta in books[:params.get('max_results', 5)]:
                    # Download
                    book = await self.book_agent.download_book(book_meta['identifier'])
                    
                    # Enhance if requested
                    if params.get('enhancement'):
                        enhanced = await self.book_agent.enhance_content(
                            book,
                            params['enhancement']
                        )
                        
                        # Rebrand if requested
                        if params.get('rebrand'):
                            branded = await self.book_agent.rebrand(enhanced, params['rebrand'])
                            processed_books.append({
                                'identifier': book.identifier,
                                'title': branded.new_title,
                                'status': 'rebranded'
                            })
                        else:
                            processed_books.append({
                                'identifier': book.identifier,
                                'title': enhanced.original.title,
                                'status': 'enhanced'
                            })
                    else:
                        processed_books.append({
                            'identifier': book.identifier,
                            'title': book.title,
                            'status': 'downloaded'
                        })
                    
                    state.messages.append(AIMessage(content=f"Processed: {book.title}"))
                
                state.results['processed_books'] = processed_books
        
        except Exception as e:
            logger.error(f"Book task failed: {e}")
            state.errors.append(f"Book processing error: {e}")
        
        state.next_action = "finalize"
        return state
    
    async def _execute_game_task(self, state: AgentState) -> AgentState:
        """Execute game-related tasks"""
        logger.info("Executing game task")
        
        try:
            params = state.parameters
            
            # Search games
            games = await self.game_agent.search_games(
                platform=params.get('platform', 'nes'),
                genre=params.get('genre'),
                year_range=tuple(params.get('year_range', [])) if params.get('year_range') else None,
                max_results=params.get('max_results', 20)
            )
            
            state.results['games_found'] = len(games)
            state.messages.append(AIMessage(content=f"Found {len(games)} games"))
            
            # Download and bundle if requested
            if params.get('create_bundle', True) and games:
                game_packages = []
                
                for game_meta in games[:params.get('max_results', 10)]:
                    game_pkg = await self.game_agent.download_game(game_meta['identifier'])
                    game_packages.append(game_pkg)
                    state.messages.append(AIMessage(content=f"Downloaded: {game_pkg.title}"))
                
                # Create bundle
                if game_packages:
                    bundle = await self.game_agent.create_bundle(
                        game_packages,
                        theme=params.get('bundle_name', 'Game Collection'),
                        output_path=params.get('output_path', '/tmp/game_bundle.zip')
                    )
                    
                    state.results['bundle'] = {
                        'name': bundle.name,
                        'games_count': len(bundle.games),
                        'platform': bundle.platform
                    }
                    state.messages.append(AIMessage(content=f"Created bundle: {bundle.name}"))
        
        except Exception as e:
            logger.error(f"Game task failed: {e}")
            state.errors.append(f"Game processing error: {e}")
        
        state.next_action = "finalize"
        return state
    
    async def _execute_course_task(self, state: AgentState) -> AgentState:
        """Execute course creation tasks"""
        logger.info("Executing course task")
        
        # TODO: Implement course generator
        state.messages.append(AIMessage(content="Course generation not yet implemented"))
        state.next_action = "finalize"
        return state
    
    async def _execute_monetize_task(self, state: AgentState) -> AgentState:
        """Execute monetization tasks"""
        logger.info("Executing monetization task")
        
        # TODO: Implement monetization
        state.messages.append(AIMessage(content="Monetization not yet implemented"))
        state.next_action = "finalize"
        return state
    
    async def _finalize_results(self, state: AgentState) -> AgentState:
        """Finalize and summarize results"""
        logger.info("Finalizing results")
        
        summary = f"""
Task completed: {state.task_type.value}

Results:
{json.dumps(state.results, indent=2)}

Errors: {len(state.errors)}
"""
        
        if state.errors:
            summary += f"\nErrors:\n" + "\n".join(f"- {e}" for e in state.errors)
        
        state.messages.append(AIMessage(content=summary))
        return state
    
    async def execute(self, user_request: str) -> Dict[str, Any]:
        """
        Execute a user request through the workflow
        
        Args:
            user_request: Natural language request
            
        Returns:
            Dictionary with results and messages
        """
        logger.info(f"Executing request: {user_request}")
        
        # Initialize state
        initial_state = AgentState(
            user_request=user_request,
            task_type=TaskType.UNKNOWN,
            parameters={},
            results={},
            errors=[],
            messages=[HumanMessage(content=user_request)]
        )
        
        # Run workflow
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            'task_type': final_state.task_type.value,
            'results': final_state.results,
            'errors': final_state.errors,
            'messages': [m.content for m in final_state.messages]
        }


# Example usage
if __name__ == "__main__":
    import internetarchive as ia
    
    async def main():
        orchestrator = MasterOrchestratorAgent(
            ia_client=ia,
            anthropic_api_key="your-key-here"
        )
        
        # Example: Book rebranding
        result = await orchestrator.execute(
            "Find 5 programming books from the 1990s, update them with modern "
            "Python examples, and rebrand with 'CodeMaster Academy' branding"
        )
        
        print("=" * 60)
        print("ORCHESTRATOR RESULT")
        print("=" * 60)
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
