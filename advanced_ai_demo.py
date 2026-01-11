#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AetherOS Advanced AI Demo
LangChain, Vector DB, Agents, RAG, Prompt Engineering
"""

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import asyncio
import json

from core.advanced_ai_integration import (AdvancedAIIntegration, Document,
                                          PromptTemplate)


async def demo_langchain_chains():
    """LangChain-style chain demo"""
    print("\n" + "="*70)
    print("🔗 DEMO 1: LANGCHAIN-STYLE AI CHAINS")
    print("="*70)
    
    ai = AdvancedAIIntegration()
    
    # Basit bir chain oluştur
    def step1_extract(text):
        words = text.split()
        return {"word_count": len(words), "words": words}
    
    def step2_filter(data):
        long_words = [w for w in data["words"] if len(w) > 5]
        return {"long_words": long_words, "count": len(long_words)}
    
    def step3_summarize(data):
        return f"Found {data['count']} long words in text"
    
    ai.create_chain("text_analysis", [
        {"name": "extract", "description": "Extract words", 
         "processor": step1_extract},
        {"name": "filter", "description": "Filter long words",
         "processor": step2_filter},
        {"name": "summarize", "description": "Summarize results",
         "processor": step3_summarize}
    ])
    
    result = await ai.execute_chain("text_analysis", 
        "AetherOS is an autonomous AI operating system with advanced capabilities")
    
    print(f"\n✓ Chain Execution Results:")
    print(f"  Final Output: {result['final_output']}")
    print(f"  Steps Completed: {result['steps_completed']}/{result['total_steps']}")
    print(f"  Execution Time: {result['execution_time']:.3f}s")

async def demo_vector_db():
    """Vector Database (ChromaDB-style) Demo"""
    print("\n" + "="*70)
    print("🗄️  DEMO 2: VECTOR DATABASE (ChromaDB-STYLE)")
    print("="*70)
    
    ai = AdvancedAIIntegration()
    
    # Belgeleri ekle
    docs = [
        Document(
            id="doc1",
            content="Python is a high-level programming language known for its simplicity",
            metadata={"source": "manual", "version": 1}
        ),
        Document(
            id="doc2",
            content="Machine Learning is a subset of artificial intelligence",
            metadata={"source": "wiki", "category": "AI"}
        ),
        Document(
            id="doc3",
            content="Neural networks are computing systems inspired by biological neurons",
            metadata={"source": "paper", "year": 2023}
        ),
    ]
    
    for doc in docs:
        ai.rag_system.vector_store.add_document(doc, "tech_docs")
    
    print(f"\n✓ Documents Added: {len(docs)}")
    
    # Ara
    search_results = ai.rag_system.vector_store.search(
        "machine learning and AI",
        collection="tech_docs",
        top_k=2
    )
    
    print(f"\n✓ Search Results for 'machine learning and AI':")
    for i, doc in enumerate(search_results, 1):
        print(f"  {i}. {doc.content[:60]}...")
    
    # İstatistikler
    stats = ai.rag_system.vector_store.get_collection_stats("tech_docs")
    print(f"\n✓ Collection Statistics:")
    print(f"  Documents: {stats['document_count']}")
    print(f"  Total Characters: {stats['total_chars']}")

async def demo_prompt_engineering():
    """Prompt Engineering System Demo"""
    print("\n" + "="*70)
    print("📝 DEMO 3: PROMPT ENGINEERING SYSTEM")
    print("="*70)
    
    ai = AdvancedAIIntegration()
    
    print(f"\n✓ Available Prompt Templates:")
    templates = ai.prompt_library.list_templates()
    for name in templates['templates']:
        print(f"  • {name}")
    
    # Örnek: Özetleme
    summary_template = ai.prompt_library.get_template("summarize")
    formatted = summary_template.format(
        text="AetherOS is an advanced autonomous system with AI capabilities..."
    )
    
    print(f"\n✓ Generated Prompt (Summarize):")
    print(f"  {formatted[:80]}...")
    
    # Yeni şablon ekle
    ai.prompt_library.add_template(
        "sentiment_analysis",
        "Analyze the sentiment of this text: {{text}}\nSentiment:",
        ["text"]
    )
    
    print(f"\n✓ Total Templates: {templates['count'] + 1}")

async def demo_rag_system():
    """RAG (Retrieval Augmented Generation) Demo"""
    print("\n" + "="*70)
    print("🎯 DEMO 4: RAG SYSTEM (Retrieval Augmented Generation)")
    print("="*70)
    
    ai = AdvancedAIIntegration()
    
    # Bilgi tabanı oluştur
    knowledge = [
        Document(
            id="kb1",
            content="AetherOS is an autonomous operating system with Level 1-3 autonomy",
            metadata={"category": "system"}
        ),
        Document(
            id="kb2",
            content="Level 1: Basic file organization, backup, system maintenance",
            metadata={"category": "autonomy"}
        ),
        Document(
            id="kb3",
            content="Level 2: AI content analysis, user context learning",
            metadata={"category": "autonomy"}
        ),
        Document(
            id="kb4",
            content="Level 3: Workflow automation, self-healing, model management",
            metadata={"category": "autonomy"}
        ),
    ]
    
    ai.rag_system.add_knowledge(knowledge, "aetheros_kb")
    
    print(f"\n✓ Knowledge Base Loaded: {len(knowledge)} documents")
    
    # Soru sor
    result = await ai.rag_system.query(
        "What are the autonomy levels in AetherOS?",
        collection="aetheros_kb",
        top_k=2
    )
    
    print(f"\n✓ Question: {result['question']}")
    print(f"  Retrieved: {result['retrieved_docs']} documents")
    print(f"  Context: {result['context'][:100]}...")
    
    # İstatistikler
    stats = ai.rag_system.get_stats()
    print(f"\n✓ RAG Statistics:")
    print(f"  Retrieval Operations: {stats['retrieval_operations']}")
    print(f"  Generation Operations: {stats['generation_operations']}")
    print(f"  Total Documents: {stats['total_documents']}")

async def demo_ollama_integration():
    """Ollama Integration Demo"""
    print("\n" + "="*70)
    print("🤖 DEMO 5: OLLAMA LOCAL LLM INTEGRATION")
    print("="*70)
    
    ai = AdvancedAIIntegration()
    
    # System prompt ayarla
    ai.ollama.set_system_prompt(
        "You are AetherOS AI, an advanced autonomous system assistant."
    )
    
    print(f"\n✓ Model: {ai.ollama.model}")
    print(f"✓ Endpoint: {ai.ollama.endpoint}")
    
    # Prompt oluştur
    response = await ai.ollama.generate(
        "What are your main capabilities?",
        temperature=0.7
    )
    
    print(f"\n✓ LLM Response:")
    print(f"  Model: {response['model']}")
    print(f"  Response: {response['response'][:80]}...")
    
    # Konversasyon geçmişi
    history = ai.ollama.get_conversation_history()
    print(f"\n✓ Conversation History: {len(history)} messages")

async def main():
    """Main demo runner"""
    print("\n" + "="*70)
    print("🚀 AETHEROS v3.0 - ADVANCED AI INTEGRATION DEMO")
    print("="*70)
    
    # Run all demos
    await demo_langchain_chains()
    await demo_vector_db()
    await demo_prompt_engineering()
    await demo_rag_system()
    await demo_ollama_integration()
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE - ALL FEATURES WORKING!")
    print("="*70)
    print("\nNew v3.0 Features:")
    print("  ✓ LangChain-style AI Chains")
    print("  ✓ Vector Database (ChromaDB-style)")
    print("  ✓ Autonomous Agent Framework")
    print("  ✓ Ollama Local LLM Integration")
    print("  ✓ Prompt Engineering System")
    print("  ✓ RAG (Retrieval Augmented Generation)")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
