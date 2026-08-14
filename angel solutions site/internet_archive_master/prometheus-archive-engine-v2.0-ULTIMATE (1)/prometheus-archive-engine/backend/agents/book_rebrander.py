"""
Book Rebrander Agent - AI-Powered Book Enhancement System
Transforms Internet Archive books into premium enhanced versions
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional, List, Dict
import fitz  # PyMuPDF
from ebooklib import epub, ITEM_DOCUMENT
import pytesseract
from PIL import Image
from io import BytesIO
from dataclasses import dataclass
import anthropic
import openai

logger = logging.getLogger(__name__)


@dataclass
class Book:
    """Represents a book from Internet Archive"""
    identifier: str
    title: str
    author: str
    year: Optional[int]
    content: str
    format: str  # pdf, epub, txt
    metadata: Dict


@dataclass
class EnhancedBook:
    """Represents an AI-enhanced book"""
    original: Book
    enhanced_content: str
    enhancement_summary: str
    chapters: List[Dict]
    word_count: int


@dataclass
class BrandedBook:
    """Represents a fully rebranded book"""
    enhanced: EnhancedBook
    new_title: str
    new_author: str
    brand_name: str
    cover_image: Optional[bytes]
    styled_content: str


class BookRebranderAgent:
    """
    Autonomous agent for discovering, enhancing, and rebranding books
    
    Capabilities:
    - Search Internet Archive for books
    - Download and parse multiple formats (PDF, EPUB, TXT)
    - AI-powered content enhancement
    - Rebranding and formatting
    - Multi-format export
    """
    
    def __init__(
        self,
        ia_client,
        anthropic_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        default_ai: str = "claude"  # claude or gpt4
    ):
        self.ia = ia_client
        self.default_ai = default_ai
        
        # Initialize AI clients
        if anthropic_api_key:
            self.claude = anthropic.AsyncAnthropic(api_key=anthropic_api_key)
        else:
            self.claude = None
            
        if openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None
    
    async def search_books(
        self,
        query: str,
        subject: Optional[str] = None,
        year_range: Optional[tuple] = None,
        max_results: int = 20
    ) -> List[Dict]:
        """
        Search Internet Archive for books
        
        Args:
            query: Search keywords
            subject: Subject filter
            year_range: (min_year, max_year) tuple
            max_results: Maximum number of results
            
        Returns:
            List of book metadata dictionaries
        """
        logger.info(f"Searching books: query='{query}', subject={subject}")
        
        # Build search query
        search_parts = [f"title:({query}) OR creator:({query}) OR subject:({query})"]
        search_parts.append("mediatype:texts")
        
        if subject:
            search_parts.append(f"subject:({subject})")
        
        if year_range:
            search_parts.append(f"year:[{year_range[0]} TO {year_range[1]}]")
        
        search_query = " AND ".join(search_parts)
        
        # Execute search
        results = await asyncio.to_thread(
            self.ia.search_items,
            search_query,
            fields=['identifier', 'title', 'creator', 'year', 'subject', 'description'],
            max_results=max_results
        )
        
        books = []
        for result in results:
            books.append({
                'identifier': result.get('identifier'),
                'title': result.get('title', 'Unknown'),
                'author': result.get('creator', ['Unknown'])[0] if result.get('creator') else 'Unknown',
                'year': result.get('year'),
                'subjects': result.get('subject', []),
                'description': result.get('description', '')
            })
        
        logger.info(f"Found {len(books)} books")
        return books
    
    async def download_book(self, identifier: str) -> Book:
        """
        Download and parse book from Internet Archive
        
        Args:
            identifier: Internet Archive item identifier
            
        Returns:
            Book object with extracted content
        """
        logger.info(f"Downloading book: {identifier}")
        
        # Get item metadata
        item = await asyncio.to_thread(self.ia.get_item, identifier)
        metadata = item.metadata
        
        # Determine best file format
        files = item.files
        pdf_file = next((f for f in files if f['name'].endswith('.pdf')), None)
        epub_file = next((f for f in files if f['name'].endswith('.epub')), None)
        txt_file = next((f for f in files if f['name'].endswith('_djvu.txt')), None)
        
        content = ""
        book_format = ""
        
        if txt_file:
            # Prefer text format (already extracted)
            logger.info(f"Using TXT format: {txt_file['name']}")
            file_path = await asyncio.to_thread(item.download, files=[txt_file['name']], destdir='/tmp')
            with open(f"/tmp/{identifier}/{txt_file['name']}", 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            book_format = "txt"
            
        elif pdf_file:
            # PDF format
            logger.info(f"Using PDF format: {pdf_file['name']}")
            file_path = await asyncio.to_thread(item.download, files=[pdf_file['name']], destdir='/tmp')
            content = await self._extract_pdf_text(f"/tmp/{identifier}/{pdf_file['name']}")
            book_format = "pdf"
            
        elif epub_file:
            # EPUB format
            logger.info(f"Using EPUB format: {epub_file['name']}")
            file_path = await asyncio.to_thread(item.download, files=[epub_file['name']], destdir='/tmp')
            content = await self._extract_epub_text(f"/tmp/{identifier}/{epub_file['name']}")
            book_format = "epub"
        else:
            raise ValueError(f"No compatible book format found for {identifier}")
        
        book = Book(
            identifier=identifier,
            title=metadata.get('title', 'Unknown'),
            author=metadata.get('creator', ['Unknown'])[0] if metadata.get('creator') else 'Unknown',
            year=metadata.get('year'),
            content=content,
            format=book_format,
            metadata=metadata
        )
        
        logger.info(f"Downloaded book: {book.title} ({len(content)} characters)")
        return book
    
    async def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        doc = await asyncio.to_thread(fitz.open, pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return text
    
    async def _extract_epub_text(self, epub_path: str) -> str:
        """Extract text from EPUB file"""
        book = await asyncio.to_thread(epub.read_epub, epub_path)
        text = ""
        
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                # Simple HTML stripping (can be improved)
                content = item.get_body_content().decode('utf-8', errors='ignore')
                # Remove HTML tags (basic)
                import re
                content = re.sub(r'<[^>]+>', '', content)
                text += content + "\n\n"
        
        return text
    
    async def enhance_content(
        self,
        book: Book,
        instructions: str,
        chunk_size: int = 8000
    ) -> EnhancedBook:
        """
        AI-powered content enhancement
        
        Args:
            book: Original book
            instructions: Enhancement instructions
            chunk_size: Characters per chunk for processing
            
        Returns:
            EnhancedBook with enhanced content
        """
        logger.info(f"Enhancing book: {book.title}")
        logger.info(f"Instructions: {instructions}")
        
        # Split content into chunks
        chunks = self._chunk_text(book.content, chunk_size)
        logger.info(f"Processing {len(chunks)} chunks")
        
        enhanced_chunks = []
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Enhancing chunk {i+1}/{len(chunks)}")
            
            enhanced = await self._enhance_chunk(
                chunk,
                instructions,
                chunk_index=i,
                total_chunks=len(chunks),
                book_context=f"{book.title} by {book.author}"
            )
            
            enhanced_chunks.append(enhanced)
        
        # Combine enhanced chunks
        enhanced_content = "\n\n".join(enhanced_chunks)
        
        # Generate summary
        summary = await self._generate_enhancement_summary(
            original_length=len(book.content),
            enhanced_length=len(enhanced_content),
            instructions=instructions
        )
        
        enhanced_book = EnhancedBook(
            original=book,
            enhanced_content=enhanced_content,
            enhancement_summary=summary,
            chapters=[],  # TODO: Extract chapters
            word_count=len(enhanced_content.split())
        )
        
        logger.info(f"Enhancement complete: {enhanced_book.word_count} words")
        return enhanced_book
    
    def _chunk_text(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks of approximately chunk_size characters"""
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = para
            else:
                current_chunk += "\n\n" + para
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    async def _enhance_chunk(
        self,
        chunk: str,
        instructions: str,
        chunk_index: int,
        total_chunks: int,
        book_context: str
    ) -> str:
        """Enhance a single content chunk using AI"""
        
        prompt = f"""You are a professional book editor and content enhancer working on: {book_context}

ENHANCEMENT INSTRUCTIONS:
{instructions}

CONTENT CHUNK ({chunk_index + 1} of {total_chunks}):
{chunk[:6000]}  # Limit to prevent token overflow

TASK: Enhance this content following these steps:
1. Analyze the current content structure and quality
2. Identify areas that need updating or improvement based on the instructions
3. Apply enhancements while maintaining the author's voice
4. Ensure factual accuracy for any new information
5. Maintain consistency with the rest of the book

OUTPUT: Only the enhanced version of the content. No explanations, no meta-commentary.
"""
        
        if self.default_ai == "claude" and self.claude:
            response = await self.claude.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=8000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        elif self.default_ai == "gpt4" and self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        
        else:
            raise ValueError("No AI client configured")
    
    async def _generate_enhancement_summary(
        self,
        original_length: int,
        enhanced_length: int,
        instructions: str
    ) -> str:
        """Generate a summary of the enhancements made"""
        
        prompt = f"""Summarize the enhancements made to a book:

INSTRUCTIONS GIVEN:
{instructions}

STATISTICS:
- Original length: {original_length:,} characters
- Enhanced length: {enhanced_length:,} characters
- Change: {((enhanced_length - original_length) / original_length * 100):.1f}%

Provide a brief summary (2-3 sentences) of what enhancements were likely applied.
"""
        
        if self.default_ai == "claude" and self.claude:
            response = await self.claude.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        else:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return response.choices[0].message.content
    
    async def rebrand(
        self,
        enhanced: EnhancedBook,
        brand_config: Dict
    ) -> BrandedBook:
        """
        Apply branding to enhanced book
        
        Args:
            enhanced: Enhanced book
            brand_config: {
                'new_title': str,
                'new_author': str,
                'brand_name': str,
                'cover_prompt': str (for AI cover generation),
                'styling': dict (font, colors, etc.)
            }
        """
        logger.info(f"Rebranding book: {brand_config.get('new_title')}")
        
        branded = BrandedBook(
            enhanced=enhanced,
            new_title=brand_config.get('new_title', enhanced.original.title),
            new_author=brand_config.get('new_author', enhanced.original.author),
            brand_name=brand_config.get('brand_name', ''),
            cover_image=None,  # TODO: Generate cover
            styled_content=enhanced.enhanced_content  # TODO: Apply styling
        )
        
        return branded
    
    async def export_pdf(self, branded: BrandedBook, output_path: str):
        """Export branded book as PDF"""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title page
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#000000',
            spaceAfter=30,
            alignment=1  # Center
        )
        
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(branded.new_title, title_style))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(f"by {branded.new_author}", styles['Normal']))
        
        if branded.brand_name:
            story.append(Spacer(1, 1 * inch))
            story.append(Paragraph(branded.brand_name, styles['Normal']))
        
        story.append(PageBreak())
        
        # Content
        paragraphs = branded.styled_content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para, styles['Normal']))
                story.append(Spacer(1, 0.2 * inch))
        
        await asyncio.to_thread(doc.build, story)
        logger.info(f"Exported PDF: {output_path}")
    
    async def export_epub(self, branded: BrandedBook, output_path: str):
        """Export branded book as EPUB"""
        book = epub.EpubBook()
        
        # Metadata
        book.set_identifier(f"rebranded-{branded.enhanced.original.identifier}")
        book.set_title(branded.new_title)
        book.set_language('en')
        book.add_author(branded.new_author)
        
        # Create chapter
        chapter = epub.EpubHtml(
            title='Content',
            file_name='content.xhtml',
            lang='en'
        )
        
        # Format content as HTML
        html_content = "<h1>" + branded.new_title + "</h1>"
        html_content += "<p><strong>by " + branded.new_author + "</strong></p>"
        
        for para in branded.styled_content.split('\n\n'):
            if para.strip():
                html_content += f"<p>{para}</p>"
        
        chapter.content = html_content
        book.add_item(chapter)
        
        # Table of contents
        book.toc = (epub.Link('content.xhtml', 'Content', 'content'),)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Spine
        book.spine = ['nav', chapter]
        
        await asyncio.to_thread(epub.write_epub, output_path, book)
        logger.info(f"Exported EPUB: {output_path}")


# Example usage
if __name__ == "__main__":
    import internetarchive as ia
    
    async def main():
        # Initialize agent
        agent = BookRebranderAgent(
            ia_client=ia,
            anthropic_api_key="your-key-here"
        )
        
        # Search for books
        books = await agent.search_books(
            query="programming",
            year_range=(1990, 1999),
            max_results=5
        )
        
        # Download first book
        if books:
            book = await agent.download_book(books[0]['identifier'])
            
            # Enhance
            enhanced = await agent.enhance_content(
                book,
                "Update all code examples to use modern Python 3.12 syntax and best practices"
            )
            
            # Rebrand
            branded = await agent.rebrand(
                enhanced,
                {
                    'new_title': f"{book.title} - 2026 Edition",
                    'new_author': book.author,
                    'brand_name': "CodeMaster Academy"
                }
            )
            
            # Export
            await agent.export_pdf(branded, "/tmp/rebranded_book.pdf")
            print("Book rebranding complete!")
    
    asyncio.run(main())
