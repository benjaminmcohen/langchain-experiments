from dotenv import find_dotenv, load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits.load_tools import load_tools, get_all_tool_names
from langchain.chains import ConversationChain
import os

# Load environment variables
load_dotenv(find_dotenv())

# Create AzureChatOpenAI instance using environment config
llm = AzureChatOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],  # ✅ "gpt-4o-mini"
    api_version=os.environ["OPENAI_API_VERSION"]
)

# --------------------------------------------------------------
# Direct LLM usage
# --------------------------------------------------------------
print(llm.invoke("Write a poem about Python, AI, and sunlight."))

# --------------------------------------------------------------
# Prompt Template + Chain
# --------------------------------------------------------------
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?"
)
chain = LLMChain(llm=llm, prompt=prompt)
print(chain.invoke({"product": "AI Chatbots for Dental Offices"}))

# --------------------------------------------------------------
# Another Chain
# --------------------------------------------------------------
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write an email subject for this topic {topic}?"
)
chain = LLMChain(llm=llm, prompt=prompt)
print(chain.invoke({"topic": "AI Session"}))

# --------------------------------------------------------------
# Tools + Agents
# --------------------------------------------------------------
tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

result = agent.run("In what year was Python released and who is the original creator? Multiply the year by 3")
print(result)

result = agent.run("In what year was Tesla released and who is the original creator? Multiply the year by 3")
print(result)

result = agent.run("In what year was Tesla born and who is the original creator? Multiply the year by 3")
print(result)

# --------------------------------------------------------------
# Conversation with memory
# --------------------------------------------------------------
conversation = ConversationChain(llm=llm, verbose=True)
print(conversation.predict(input="Hi there!"))
print(conversation.predict(input="I'm doing well! Just having a conversation with an AI."))
