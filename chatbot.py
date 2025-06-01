import os
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import logging
import re
from config import (
    OPENAI_API_KEY,
    MODEL_CONFIG,
    DOC_CONFIG,
    VECTOR_STORE_CONFIG,
    LOG_CONFIG,
    LANGUAGE_CONFIG
)
from evaluation import ChatbotEvaluator

# Set up logging
logging.basicConfig(
    filename=LOG_CONFIG['filename'],
    level=getattr(logging, LOG_CONFIG['level']),
    format=LOG_CONFIG['format']
)

# Load environment variables
load_dotenv()

class VisaBridgeBot:
    def __init__(self):
        # Check for OpenAI API key
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
            
        # Initialize language model
        self.llm = ChatOpenAI(
            temperature=MODEL_CONFIG['temperature'],
            model_name=MODEL_CONFIG['model_name'],
            openai_api_key=OPENAI_API_KEY
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize evaluator
        self.evaluator = ChatbotEvaluator()
        
        try:
            self.docs = self._load_documents()
            self.vector_store = self._create_vector_store()
            self.qa_chain = self._create_qa_chain()
        except Exception as e:
            logging.error(f"Error initializing chatbot: {str(e)}")
            raise

    def _detect_primary_language(self, text: str) -> str:
        """
        Determine if the query is primarily in English or Urdu.
        Returns 'en' for English or 'ur' for Urdu.
        """
        # Clean the text - remove any examples or quotes that might confuse detection
        # This regex pattern tries to identify and remove text between quotes or examples
        cleaned_text = re.sub(r'["\'](.*?)["\']', '', text)
        
        # Count characters in Urdu Unicode range
        urdu_char_count = sum(1 for c in cleaned_text if '\u0600' <= c <= '\u06FF')
        
        # If more than 15% of characters are in Urdu range, consider it an Urdu query
        if urdu_char_count > len(cleaned_text) * 0.15:
            return 'ur'
        return 'en'

    def _load_documents(self) -> List:
        """Load and process documents from the data directory."""
        documents = []
        data_dir = DOC_CONFIG['data_directory']
        
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Data directory '{data_dir}' not found")
            
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                try:
                    loader = TextLoader(os.path.join(data_dir, filename))
                    documents.extend(loader.load())
                except Exception as e:
                    logging.error(f"Error loading document {filename}: {str(e)}")
                    continue

        if not documents:
            raise ValueError("No documents found in the data directory")

        text_splitter = CharacterTextSplitter(
            chunk_size=DOC_CONFIG['chunk_size'],
            chunk_overlap=DOC_CONFIG['chunk_overlap']
        )
        return text_splitter.split_documents(documents)    

    def _create_vector_store(self):
        """Create a FAISS vector store from the documents."""
        try:
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            return FAISS.from_documents(self.docs, embeddings)
        except Exception as e:
            logging.error(f"Error creating vector store: {str(e)}")
            raise

    def _create_qa_chain(self):
        """Create a conversational retrieval chain."""
        try:
            # Define a prompt template that includes multilingual capability
            template = """You are VisaBridge AI Assistant, a helpful chatbot that provides information about visa and immigration processes for over 20 countries.
            
            You can understand and respond to queries in multiple languages including English and Urdu (اردو).
            
            IMPORTANT RULES FOR LANGUAGE DETECTION:
            1. Carefully analyze the user's query to determine its primary language
            2. If the query is primarily in English (Latin script), respond in English only
            3. Only respond in Urdu if the query itself is primarily written in Urdu script
            4. Ignore any examples or quotes of other languages within the query when determining response language
            5. If a query contains both languages, respond in the language that makes up the majority of the query
            
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            {context}
            
            Question: {question}
            Answer:"""
            
            qa_prompt = PromptTemplate(
                template=template,
                input_variables=["context", "question"]
            )
            
            return ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": VECTOR_STORE_CONFIG['similarity_search_k']}
                ),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": qa_prompt},
                verbose=True
            )
        except Exception as e:
            logging.error(f"Error creating QA chain: {str(e)}")
            raise

    def chat(self, query: str) -> str:
        """Process a user query and return a response."""
        start_time = time.time()
        error = None
        
        try:
            logging.info(f"User query: {query}")
            
            # Detect the primary language of the query
            language = self._detect_primary_language(query)
            logging.info(f"Detected language: {language}")
            
            # Simply pass the question to the QA chain
            response = self.qa_chain({"question": query})
            
            answer = response['answer']
            logging.info(f"Bot response: {answer}")
        except Exception as e:
            error = str(e)
            logging.error(f"Error processing query: {error}")
            answer = f"I encountered an error: {error}"
        
        response_time = time.time() - start_time
        self.evaluator.record_interaction(query, answer, response_time, error)
        
        return answer

    def start_conversation(self):
        """Start a new conversation session."""
        self.evaluator.start_conversation()

    def end_conversation(self):
        """End the current conversation session."""
        self.evaluator.end_conversation()
        return self.evaluator.generate_summary()

    def clear_conversation(self):
        """Clear the conversation history and start a new session."""
        # Clear the memory
        self.memory.clear()
        # Start a new conversation
        self.evaluator.start_conversation()
        logging.info("Conversation cleared and new session started")

if __name__ == "__main__":
    print("Initializing VisaBridge Chatbot...")
    try:
        bot = VisaBridgeBot()
        print("Chatbot ready! Type 'quit' to exit.")
        
        bot.start_conversation()
        
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in ['quit', 'exit']:
                summary = bot.end_conversation()
                print("\nConversation Summary:")
                print(f"Total queries: {summary['total_queries']}")
                print(f"Average response time: {summary['average_response_time']} seconds")
                print(f"Error rate: {summary['error_rate']}%")
                break
            response = bot.chat(query)
            print(f"\nBot: {response}")
            
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        print(f"Error: {str(e)}")