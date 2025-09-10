"""
Offline demo version of OrgChar Streamlit application.
This version works without external API calls or model downloads.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append('src')

from orgchar.config import Config
from orgchar.document_processor import DocumentProcessor

# Page configuration
st.set_page_config(
    page_title="OrgChar - Organizational Behavior Chatbot (Demo)",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_demo():
    """Initialize demo data."""
    if 'documents_processed' not in st.session_state:
        config = Config()
        config.ensure_directories()
        
        # Process documents
        processor = DocumentProcessor()
        docs = processor.process_directory(config.KNOWLEDGE_BASE_PATH)
        
        st.session_state.documents_processed = docs
        st.session_state.document_stats = {
            'total_chunks': len(docs),
            'sources': list(set(doc.metadata['filename'] for doc in docs)),
            'total_sources': len(set(doc.metadata['filename'] for doc in docs))
        }
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def simulate_search(query: str, documents: list, k: int = 3):
    """Simulate similarity search using keyword matching."""
    keywords = query.lower().split()
    
    results = []
    for doc in documents:
        content_lower = doc.page_content.lower()
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            results.append((doc, score))
    
    # Sort by relevance score and return top k
    results.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in results[:k]]

def simulate_answer(question: str, context_docs: list) -> str:
    """Simulate answer generation based on context."""
    if not context_docs:
        return "I don't have enough information in my knowledge base to answer that question. Please try rephrasing or ask about organizational behavior topics."
    
    # Extract key information from context
    sources = [doc.metadata['filename'] for doc in context_docs]
    
    # Simple response based on question keywords
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['leadership', 'leader', 'leaders']):
        return f"""Based on the organizational behavior knowledge base, here are key insights about leadership:

**Leadership Styles:**
- Transformational Leadership: Focuses on inspiring and motivating followers through vision and personal charisma
- Transactional Leadership: Based on exchange relationships and contingent rewards
- Situational Leadership: Adapts style based on follower readiness and situation
- Authentic Leadership: Emphasizes genuine relationships and moral perspective
- Servant Leadership: Prioritizes serving others and empowering team members

**Key Leadership Principles:**
- Effective leaders adapt their style to the situation and followers' needs
- Building trust and psychological safety is crucial for team performance
- Leaders should focus on developing others and creating shared vision

*This information is compiled from the knowledge base sources: {', '.join(set(sources))}*"""
    
    elif any(word in question_lower for word in ['team', 'teams', 'group', 'collaboration']):
        return f"""Based on the organizational behavior knowledge base, here's what we know about team dynamics:

**Team Development Stages (Tuckman's Model):**
1. **Forming**: Team members get to know each other, roles unclear
2. **Storming**: Conflicts arise as personalities emerge and positions are established
3. **Norming**: Team resolves differences and establishes ground rules
4. **Performing**: Team operates at peak efficiency
5. **Adjourning**: Team disbands after achieving objectives

**Factors Affecting Team Performance:**
- Team size (optimal: 5-7 members)
- Diversity in skills and perspectives
- Clear communication patterns
- Defined roles and responsibilities
- Psychological safety

**Building High-Performance Teams:**
- Create shared vision and goals
- Establish effective communication
- Encourage continuous improvement
- Build trust and respect among members

*This information is compiled from the knowledge base sources: {', '.join(set(sources))}*"""
    
    elif any(word in question_lower for word in ['culture', 'organizational', 'behavior']):
        return f"""Based on the organizational behavior knowledge base:

**What is Organizational Behavior?**
Organizational behavior (OB) is the study of how people interact within groups and organizations. It draws from psychology, sociology, anthropology, and management.

**Key Areas of Study:**

**Individual Level:**
- Personality and individual differences
- Perception and attribution
- Motivation and engagement
- Learning and development

**Group Level:**
- Team dynamics and collaboration
- Communication patterns
- Leadership processes
- Conflict and negotiation

**Organizational Level:**
- Organizational culture and values
- Structure and coordination
- Change management
- Human resource practices

**Core Principles:**
- People are complex and influenced by multiple factors
- Context and situation matter significantly
- Individual differences affect behavior
- Humans are inherently social beings

*This information is compiled from the knowledge base sources: {', '.join(set(sources))}*"""
    
    else:
        # General response using first context document
        preview = context_docs[0].page_content[:300]
        return f"""Based on the information in my knowledge base, here's what I found:

{preview}...

For more specific information about organizational behavior topics like leadership, team dynamics, or organizational culture, please ask a more targeted question.

*Source: {context_docs[0].metadata['filename']}*"""

def render_sidebar():
    """Render the sidebar."""
    st.sidebar.title("🏢 OrgChar Demo")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📚 Knowledge Base Status")
    
    if 'document_stats' in st.session_state:
        stats = st.session_state.document_stats
        st.sidebar.success(f"✅ {stats['total_chunks']} chunks from {stats['total_sources']} documents")
        
        with st.sidebar.expander("📂 Available Sources"):
            for source in stats['sources']:
                st.sidebar.write(f"• {source}")
    else:
        st.sidebar.warning("⚠️ Knowledge base not loaded")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Demo Information")
    st.sidebar.info("""
    **This is a demo version** showing the OrgChar interface and basic functionality.
    
    **Limitations:**
    - Uses keyword-based search simulation
    - Pre-programmed responses for common topics
    - No actual AI model integration
    
    **Full Version Features:**
    - Vector similarity search
    - OpenAI GPT integration
    - Real-time document processing
    - Discord bot integration
    """)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def render_main_content():
    """Render the main chat interface."""
    st.title("🏢 OrgChar - Organizational Behavior Assistant")
    st.markdown("**Demo Version** - Ask me about leadership, team dynamics, or organizational culture!")
    
    st.warning("⚠️ This is a demonstration version with simulated responses. The full system requires API keys and internet access for AI model integration.")
    
    # Display chat history
    for question, answer in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(question)
        
        with st.chat_message("assistant"):
            st.write(answer)
    
    # Chat input
    question = st.chat_input("Ask about organizational behavior...")
    
    if question:
        process_question(question)

def process_question(question: str):
    """Process user question and generate demo response."""
    # Add user question to chat
    with st.chat_message("user"):
        st.write(question)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            # Simulate search
            context_docs = simulate_search(question, st.session_state.documents_processed, k=3)
            
            # Generate answer
            answer = simulate_answer(question, context_docs)
        
        st.write(answer)
        
        # Show sources
        if context_docs:
            with st.expander("📚 Knowledge Sources Used"):
                sources = set(doc.metadata['filename'] for doc in context_docs)
                for source in sources:
                    st.write(f"• {source}")
    
    # Add to chat history
    st.session_state.chat_history.append((question, answer))
    st.rerun()

def render_footer():
    """Render footer information."""
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "OrgChar Demo - Organizational Behavior RAG Chatbot | "
        "Built with Streamlit & LangChain | "
        "<a href='https://github.com/im45145v/OrgChar' target='_blank'>GitHub Repository</a>"
        "</div>",
        unsafe_allow_html=True
    )

def main():
    """Main function to run the demo app."""
    try:
        # Initialize demo data
        initialize_demo()
        
        # Render components
        render_sidebar()
        render_main_content()
        render_footer()
        
    except Exception as e:
        st.error(f"Demo application error: {e}")
        st.info("Please check that the knowledge_base directory exists and contains sample documents.")

if __name__ == "__main__":
    main()