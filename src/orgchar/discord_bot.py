"""
Discord bot integration for OrgChar RAG chatbot.
"""

import discord
from discord.ext import commands
import logging
import asyncio
from typing import Optional
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from orgchar.config import Config
from orgchar.rag_system import RAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrgCharBot(commands.Bot):
    """Discord bot for OrgChar RAG system."""
    
    def __init__(self, config: Config = None):
        """
        Initialize the Discord bot.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config()
        
        # Bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Initialize bot
        super().__init__(
            command_prefix='!org ',
            intents=intents,
            description='Organizational Behavior RAG Chatbot'
        )
        
        # Initialize RAG system
        self.rag_system = RAGSystem(self.config)
        self.rag_loaded = False
    
    async def setup_hook(self):
        """Setup hook called when bot is starting up."""
        logger.info("Setting up OrgChar Discord bot...")
        
        # Load knowledge base
        success = self.rag_system.load_knowledge_base()
        if success:
            self.rag_loaded = True
            logger.info("Knowledge base loaded successfully")
        else:
            logger.warning("Failed to load knowledge base")
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f'{self.user} is now online!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Set status
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="organizational behavior questions | !org help"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        """Handle incoming messages."""
        # Ignore bot messages
        if message.author == self.user:
            return
        
        # Process commands first
        await self.process_commands(message)
        
        # Handle direct mentions
        if self.user.mentioned_in(message) and not message.mention_everyone:
            await self._handle_mention(message)
    
    async def _handle_mention(self, message):
        """Handle when bot is mentioned."""
        # Remove mention from message
        content = message.content.replace(f'<@{self.user.id}>', '').strip()
        
        if not content:
            await message.reply(
                "Hi! I'm OrgChar, your organizational behavior assistant. "
                "Ask me questions about leadership, workplace dynamics, management, and more!\n"
                "Use `!org help` to see available commands."
            )
            return
        
        # Process as question
        await self._answer_question(message, content)
    
    async def _answer_question(self, message, question: str):
        """Answer a question using the RAG system."""
        if not self.rag_loaded:
            await message.reply(
                "❌ Knowledge base not available. Please contact an administrator."
            )
            return
        
        # Show typing indicator
        async with message.channel.typing():
            try:
                # Get answer from RAG system
                response = self.rag_system.answer_question(question)
                
                # Prepare response
                answer = response['answer']
                sources = response['sources']
                
                # Create embed for better formatting
                embed = discord.Embed(
                    title="🏢 Organizational Behavior Answer",
                    description=answer[:4000],  # Discord embed description limit
                    color=0x3498db
                )
                
                # Add question as field
                embed.add_field(
                    name="❓ Question",
                    value=question[:1000],  # Limit length
                    inline=False
                )
                
                # Add sources if available
                if sources:
                    source_text = "\n".join([
                        f"• {source['filename']} ({source['type']})"
                        for source in sources[:5]  # Limit to 5 sources
                    ])
                    embed.add_field(
                        name="📚 Sources",
                        value=source_text[:1000],  # Limit length
                        inline=False
                    )
                
                # Add footer
                embed.set_footer(text="OrgChar • Organizational Behavior Assistant")
                
                await message.reply(embed=embed)
                
            except Exception as e:
                logger.error(f"Error answering question: {e}")
                await message.reply(f"❌ Error processing your question: {str(e)}")

# Bot commands
@commands.command(name='ask', aliases=['question', 'q'])
async def ask_question(ctx, *, question: str):
    """
    Ask a question about organizational behavior.
    
    Usage: !org ask <your question>
    """
    bot = ctx.bot
    await bot._answer_question(ctx.message, question)

@commands.command(name='stats', aliases=['status', 'info'])
async def knowledge_base_stats(ctx):
    """
    Get knowledge base statistics.
    
    Usage: !org stats
    """
    bot = ctx.bot
    
    if not bot.rag_loaded:
        await ctx.reply("❌ Knowledge base not available.")
        return
    
    try:
        stats = bot.rag_system.get_knowledge_base_stats()
        
        embed = discord.Embed(
            title="📊 Knowledge Base Statistics",
            color=0x2ecc71
        )
        
        embed.add_field(
            name="Status",
            value="✅ Online" if stats['status'] == 'initialized' else "❌ Offline",
            inline=True
        )
        
        embed.add_field(
            name="Documents",
            value=stats.get('document_count', 0),
            inline=True
        )
        
        embed.add_field(
            name="Embedding Model",
            value=stats.get('embedding_model', 'Unknown'),
            inline=True
        )
        
        await ctx.reply(embed=embed)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await ctx.reply(f"❌ Error getting statistics: {str(e)}")

@commands.command(name='refresh', aliases=['update', 'reload'])
@commands.has_permissions(administrator=True)
async def refresh_knowledge_base(ctx):
    """
    Refresh the knowledge base (Admin only).
    
    Usage: !org refresh
    """
    bot = ctx.bot
    
    async with ctx.typing():
        try:
            success = bot.rag_system.update_knowledge_base()
            
            if success:
                bot.rag_loaded = True
                await ctx.reply("✅ Knowledge base refreshed successfully!")
            else:
                await ctx.reply("❌ Failed to refresh knowledge base.")
                
        except Exception as e:
            logger.error(f"Error refreshing knowledge base: {e}")
            await ctx.reply(f"❌ Error refreshing knowledge base: {str(e)}")

@commands.command(name='help', aliases=['commands', 'usage'])
async def bot_help(ctx):
    """
    Show help information.
    
    Usage: !org help
    """
    embed = discord.Embed(
        title="🏢 OrgChar Bot Help",
        description="I'm your organizational behavior assistant! Here's how to use me:",
        color=0x9b59b6
    )
    
    embed.add_field(
        name="🗨️ Direct Questions",
        value="Mention me with your question:\n`@OrgChar What is transformational leadership?`",
        inline=False
    )
    
    embed.add_field(
        name="📝 Commands",
        value=(
            "`!org ask <question>` - Ask a specific question\n"
            "`!org stats` - View knowledge base statistics\n"
            "`!org help` - Show this help message\n"
            "`!org refresh` - Refresh knowledge base (Admin only)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💡 Example Topics",
        value=(
            "• Leadership styles and theories\n"
            "• Team dynamics and collaboration\n"
            "• Organizational culture and change\n"
            "• Employee motivation and engagement\n"
            "• Workplace communication"
        ),
        inline=False
    )
    
    embed.set_footer(text="OrgChar • Organizational Behavior Assistant")
    
    await ctx.reply(embed=embed)

# Add commands to bot
async def setup_commands(bot):
    """Setup bot commands."""
    bot.add_command(ask_question)
    bot.add_command(knowledge_base_stats)
    bot.add_command(refresh_knowledge_base)
    bot.add_command(bot_help)

def run_discord_bot(config: Config = None):
    """
    Run the Discord bot.
    
    Args:
        config: Configuration object
    """
    config = config or Config()
    
    if not config.DISCORD_BOT_TOKEN:
        logger.error("Discord bot token not configured")
        return
    
    # Create bot instance
    bot = OrgCharBot(config)
    
    # Setup commands
    asyncio.run(setup_commands(bot))
    
    # Run bot
    try:
        logger.info("Starting Discord bot...")
        bot.run(config.DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"Failed to run Discord bot: {e}")

if __name__ == "__main__":
    run_discord_bot()