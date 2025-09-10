"""
Streamlit web interface for the OrgChar RAG chatbot.
"""

import streamlit as st
import logging
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from orgchar.config import Config
from orgchar.rag_system import RAGSystem
from orgchar.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=Config.STREAMLIT_PAGE_TITLE,
    page_icon=Config.STREAMLIT_PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        """Initialize the Streamlit app."""
        self.config = Config()
        self.config.ensure_directories()
        
        # Initialize RAG system
        if 'rag_system' not in st.session_state:
            st.session_state.rag_system = RAGSystem(self.config)
            st.session_state.rag_system.load_knowledge_base()
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
    
    def render_sidebar(self):
        """Render the sidebar with knowledge base management."""
        st.sidebar.title("🏢 OrgChar Settings")
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("📚 Knowledge Base")
        
        # Display knowledge base stats
        stats = st.session_state.rag_system.get_knowledge_base_stats()
        
        if stats['status'] == 'initialized':
            st.sidebar.success(f"✅ {stats['document_count']} documents indexed")
        else:
            st.sidebar.warning("⚠️ Knowledge base not initialized")
        
        # Knowledge base management buttons
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🔄 Refresh KB", help="Refresh knowledge base from documents"):
                self._refresh_knowledge_base()
        
        with col2:
            if st.button("📊 View Stats", help="View detailed statistics"):
                self._show_kb_stats()
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("📁 Document Upload")
        
        # File uploader
        uploaded_files = st.sidebar.file_uploader(
            "Upload documents",
            type=['pdf', 'txt', 'md'],
            accept_multiple_files=True,
            help="Upload PDF, TXT, or MD files to add to knowledge base"
        )
        
        if uploaded_files:
            if st.sidebar.button("💾 Process & Add Documents"):
                self._process_uploaded_files(uploaded_files)
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚙️ Settings")
        
        # Chat settings
        retrieve_k = st.sidebar.slider(
            "Context Documents",
            min_value=1,
            max_value=10,
            value=4,
            help="Number of documents to retrieve for context"
        )
        st.session_state.retrieve_k = retrieve_k
        
        # Clear chat history
        if st.sidebar.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    def _refresh_knowledge_base(self):
        """Refresh the knowledge base from documents."""
        with st.spinner("Refreshing knowledge base..."):
            st.sidebar.text("Refreshing knowledge base...")
            success = st.session_state.rag_system.update_knowledge_base()
            if success:
                st.sidebar.success("Knowledge base refreshed!")
            else:
                st.sidebar.error("Failed to refresh knowledge base")
        st.rerun()
    
    def _show_kb_stats(self):
        """Show knowledge base statistics."""
        stats = st.session_state.rag_system.get_knowledge_base_stats()
        st.sidebar.json(stats)
    
    def _process_uploaded_files(self, uploaded_files):
        """Process and add uploaded files to knowledge base."""
        try:
            processor = DocumentProcessor(
                chunk_size=self.config.CHUNK_SIZE,
                chunk_overlap=self.config.CHUNK_OVERLAP
            )
            
            all_documents = []
            
            with st.spinner(f"Processing {len(uploaded_files)} files..."):
                st.sidebar.text(f"Processing {len(uploaded_files)} files...")
                for uploaded_file in uploaded_files:
                    # Save uploaded file temporarily
                    temp_path = Path("/tmp") / uploaded_file.name
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Process based on file type
                    try:
                        if uploaded_file.type == "application/pdf":
                            content = processor.load_pdf(temp_path)
                        else:
                            content = processor.load_text_file(temp_path)
                        
                        # Create document
                        from langchain.schema import Document
                        doc = Document(
                            page_content=content,
                            metadata={
                                'source': uploaded_file.name,
                                'filename': uploaded_file.name,
                                'type': uploaded_file.name.split('.')[-1].upper()
                            }
                        )
                        
                        # Chunk document
                        chunks = processor.chunk_documents([doc])
                        all_documents.extend(chunks)
                        
                        # Clean up temp file
                        temp_path.unlink()
                        
                    except Exception as e:
                        st.sidebar.error(f"Error processing {uploaded_file.name}: {e}")
            
            # Add to knowledge base
            if all_documents:
                success = st.session_state.rag_system.add_documents_to_knowledge_base(all_documents)
                if success:
                    st.sidebar.success(f"Added {len(all_documents)} document chunks to knowledge base!")
                else:
                    st.sidebar.error("Failed to add documents to knowledge base")
            
        except Exception as e:
            st.sidebar.error(f"Error processing files: {e}")
    
    def render_main_content(self):
        """Render the main chat interface."""
        st.title("🏢 OrgChar - Organizational Behavior Assistant")
        st.markdown("Ask me anything about organizational behavior, leadership, workplace dynamics, and management!")
        
        # Display chat history
        chat_container = st.container()
        
        with chat_container:
            for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
                # Question
                with st.chat_message("user"):
                    st.write(question)
                
                # Answer
                with st.chat_message("assistant"):
                    st.write(answer)
                    
                    # Show sources if available
                    if sources:
                        with st.expander("📚 Sources"):
                            for source in sources:
                                st.write(f"• **{source['filename']}** ({source['type']})")
        
        # Chat input
        question = st.chat_input("Ask a question about organizational behavior...")
        
        if question:
            self._process_question(question)
    
    def _process_question(self, question: str):
        """Process user question and generate response."""
        # Add user question to chat
        with st.chat_message("user"):
            st.write(question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                retrieve_k = getattr(st.session_state, 'retrieve_k', 4)
                response = st.session_state.rag_system.answer_question(
                    question, 
                    retrieve_k=retrieve_k
                )
            
            # Display answer
            st.write(response['answer'])
            
            # Display sources
            if response['sources']:
                with st.expander("📚 Sources"):
                    for source in response['sources']:
                        st.write(f"• **{source['filename']}** ({source['type']})")
            
            # Add to chat history
            st.session_state.chat_history.append((
                question,
                response['answer'],
                response['sources']
            ))
        
        st.rerun()
    
    def render_footer(self):
        """Render footer information."""
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray;'>"
            "OrgChar - Organizational Behavior RAG Chatbot | "
            "Built with Streamlit & LangChain"
            "</div>",
            unsafe_allow_html=True
        )
    
    def run(self):
        """Run the Streamlit application."""
        try:
            # Render components
            self.render_sidebar()
            self.render_main_content()
            self.render_footer()
            
        except Exception as e:
            st.error(f"Application error: {e}")
            logger.error(f"Streamlit app error: {e}")

def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()