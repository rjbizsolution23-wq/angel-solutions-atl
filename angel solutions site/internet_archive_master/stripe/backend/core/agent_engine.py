"""
AI Agent Engine powered by LangChain and Gemini Pro.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from core.config import get_settings
from services.supabase_service import get_supabase_service

# Import all tools
from tools.payments_tools import (
    create_payment_intent_tool,
    create_refund_tool,
    create_checkout_session_tool,
    create_payment_link_tool
)
from tools.products_tools import (
    create_product_tool,
    create_price_tool,
    list_products_tool,
    create_coupon_tool
)
from tools.customers_tools import (
    create_customer_tool,
    list_customers_tool,
    create_subscription_tool,
    cancel_subscription_tool,
    list_subscriptions_tool
)
from tools.connect_tools import (
    create_connect_account_tool,
    create_account_onboarding_link_tool,
    create_transfer_tool
)
from tools.reporting_tools import (
    get_balance_tool,
    list_recent_transactions_tool
)

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


# Agent prompt template
AGENT_PROMPT = """You are a Stripe Supreme Agent, an expert AI assistant for managing Stripe operations.

You have access to comprehensive Stripe tools for:
- **Payments**: Create payment intents, refunds, checkout sessions, payment links
- **Products & Pricing**: Create products, prices, coupons
- **Customers & Subscriptions**: Manage customers and subscriptions
- **Connect**: Set up marketplace accounts, transfers, onboarding
- **Reporting**: Check balances and transactions

**Your capabilities:**
1. Understand natural language requests about Stripe operations
2. Break down complex workflows into steps
3. Execute Stripe API calls using the appropriate tools
4. Provide clear, helpful responses with all relevant details
5. Handle errors gracefully and suggest alternatives

**Guidelines:**
- Always confirm sensitive operations (refunds, cancellations, transfers)
- Provide IDs and URLs in responses for easy reference
- Explain what you're doing in simple terms
- If a request is ambiguous, ask clarifying questions
- For multi-step workflows, explain each step

**Current Mode**: {stripe_mode}

TOOLS:
------
You have access to the following tools:

{tools}

To use a tool, use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""


class StripeAgent:
    """AI Agent for Stripe operations."""
    
    def __init__(self, conversation_id: Optional[str] = None):
        """Initialize the agent."""
        settings = get_settings()
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.google_ai_api_key,
            temperature=0.1,
            convert_system_message_to_human=True
        )
        
        # Collect all tools
        self.tools = [
            # Payments
            create_payment_intent_tool,
            create_refund_tool,
            create_checkout_session_tool,
            create_payment_link_tool,
            # Products
            create_product_tool,
            create_price_tool,
            list_products_tool,
            create_coupon_tool,
            # Customers
            create_customer_tool,
            list_customers_tool,
            create_subscription_tool,
            cancel_subscription_tool,
            list_subscriptions_tool,
            # Connect
            create_connect_account_tool,
            create_account_onboarding_link_tool,
            create_transfer_tool,
            # Reporting
            get_balance_tool,
            list_recent_transactions_tool,
        ]
        
        # Create prompt
        self.prompt = PromptTemplate(
            template=AGENT_PROMPT,
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools]),
                "stripe_mode": settings.stripe_mode.upper()
            }
        )
        
        # Create memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=False
        )
        
        # Create agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        self.conversation_id = conversation_id
        logger.info(f"Stripe Agent initialized with {len(self.tools)} tools")
    
    async def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user message and return agent response.
        
        Args:
            user_message: The user's input message
        
        Returns:
            Dict with response and metadata
        """
        try:
            # Store user message if we have a conversation
            if self.conversation_id:
                supabase = get_supabase_service()
                supabase.add_message(
                    conversation_id=self.conversation_id,
                    role="user",
                    content=user_message
                )
            
            # Execute agent
            result = self.agent_executor.invoke({"input": user_message})
            
            response = result.get("output", "I encountered an error processing your request.")
            
            # Store agent response
            if self.conversation_id:
                supabase.add_message(
                    conversation_id=self.conversation_id,
                    role="assistant",
                    content=response
                )
            
            return {
                "success": True,
                "response": response,
                "conversation_id": self.conversation_id
            }
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_response = f"I encountered an error: {str(e)}"
            
            return {
                "success": False,
                "response": error_response,
                "error": str(e),
                "conversation_id": self.conversation_id
            }


def create_agent(conversation_id: Optional[str] = None) -> StripeAgent:
    """Factory function to create a new agent instance."""
    return StripeAgent(conversation_id=conversation_id)
