from langchain_openai import AzureChatOpenAI
from dotenv import find_dotenv, load_dotenv
import os
import logging

#print("✅ dotenv loaded")
from langchain.chains.llm import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())

# Configure logging to ensure logs show in Azure App Service
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Log endpoint details
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
version = os.getenv("AZURE_OPENAI_API_VERSION")
model = "text-embedding-ada-002"

logging.info(f"Using Azure OpenAI endpoint: {endpoint}")
logging.info(f"Deployment name: {deployment}, API version: {version}, Model: {model}")



def draft_email(user_input, name="Dave"):
    chat = AzureChatOpenAI(
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        model_name="gpt-4o-mini",
        temperature=1
    )

    template = """
    You are a helpful assistant that drafts an email reply based on a new email.

    Your goal is to help the user quickly create a perfect email reply.

    Keep your reply short and to the point and mimic the style of the email so you reply in a similar manner to match the tone.

    Start your reply by saying: "Hi {name}, here's a draft for your reply:". And then proceed with the reply on a new line.

    Make sure to sign off with {signature}.
    """

    signature = f"Kind regards, \n{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Here's the email to reply to and consider any other comments from the user for reply as well: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    logging.info(f"Expected input variables: {chat_prompt.input_variables}")

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run({"user_input": user_input, "signature": signature, "name": name})

    return response
