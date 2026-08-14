"""
Prometheus Archive Engine - Master Orchestrator Router
Coordination engine for multi-agent workflows
"""
import os
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import internetarchive as ia
from uuid import uuid4

from ...core.db import get_db
from ...core.auth import get_current_user
from ...models.database import User, SearchHistory, ArchivedContent
from ...agents.orchestrator import MasterOrchestratorAgent
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import re

router = APIRouter()

# Instantiate single static orchestrator
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "simulated_key")
agent = MasterOrchestratorAgent(
    ia_client=ia,
    anthropic_api_key=ANTHROPIC_API_KEY,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

class OrchestrateRequest(BaseModel):
    user_request: str

class RebuildRequest(BaseModel):
    url_or_identifier: str
    goal: str
    brand_name: str = "RJ Business Solutions"
    custom_author: str = "Rick Jefferson"


def extract_ia_identifier(url_or_id: str) -> str:
    """Extracts raw Internet Archive identifier from full URLs or raw input"""
    # Match details or download paths
    match = re.search(r"archive\.org/(?:details|download|metadata|stream)/([^/]+)", url_or_id)
    if match:
        return match.group(1)
    return url_or_id.strip().split('/')[-1]


def generate_premium_fallback_rebuild(identifier: str, title: str, creator: str, description: str, goal: str, brand_name: str, author: str) -> str:
    """Generates an outstanding, publication-grade white-labeled Markdown fallback doc"""
    clean_desc = description.replace("<br />", "\n").replace("<p>", "").replace("</p>", "\n") if description else "No primary description provided."
    clean_desc = clean_desc[:400] + "..." if len(clean_desc) > 400 else clean_desc

    if "Blog" in goal:
        return f"""# {title}: Strategic Modernization Review
> **Published by:** {author} | **Enterprise Systems Architect**
> **Corporate Identity:** {brand_name} Research Division
> **Original Source:** Internet Archive Archive-ID: `{identifier}`

## 🌐 Meta Configuration & SEO Schema
- **Target Primary Keywords:** `{title.lower().replace(" ", ", ")}, marketing strategy, enterprise scale`
- **Target Secondary Keywords:** `rj business solutions, white label content, asset monetization`
- **Canonical URL:** `https://archive.org/details/{identifier}`
- **Meta Description:** An in-depth executive analysis on modernizing '{title}' for modern business operations. Written by {author} for {brand_name}.

---

## 🚀 Executive Introduction
In an era dominated by rapid digital transformation, historic intellectual properties and foundational concepts are often left underutilized. At **{brand_name}**, led by **{author}**, we specialize in transforming legacy archives into active profit-generating assets. 

This review provides a comprehensive architectural breakdown of **"{title}"** (originally produced by *{creator}*), translating its timeless core tenets into actionable modern frameworks.

---

## 💡 Core Insights & Translation Matrix

### 1. Legacy Analysis
The original document, *"{title}"*, offers a fascinating historical perspective:
> "{clean_desc}"

While historically significant, these principles require an active translation layer to meet modern 2026 enterprise benchmarks. 

### 2. High-Yield Application Framework
To successfully deploy these ideas at scale, we recommend implementing a three-phase integration pipeline:
- **Phase I: Asset Ingestion & Parsing:** Extract the underlying concepts and eliminate obsolete formatting anomalies.
- **Phase II: Rebranding & Voice Synthesis:** Elevate the terminology to align with your corporate branding standards.
- **Phase III: Omnichannel Deployment:** Distribute the compiled assets via high-authority SEO portals.

---

## 🎯 Strategic Takeaways for 2026
1. **Leverage Historical Moats:** Audiences crave authentic, authoritative information. Legacy assets carry inherent brand trust.
2. **Automate the Transformation:** Utilize multi-agent orchestrators to handle parsing, rebranding, and distribution seamlessly.
3. **Monetize with White-Label Delivery:** Package the final outputs into premium newsletters, summaries, or structured courses.

---

## 📬 Connect with RJ Business Solutions
Are you ready to turn your legacy archives into automated growth systems? Let the engineers at **{brand_name}** build your custom scaling solution.

- **Founder & Director:** {author}
- **Corporate Web Portal:** [rjbusinesssolutions.org](https://rjbusinesssolutions.org)
- **Support & Inquiries:** [support@rjbusinesssolutions.org](mailto:support@rjbusinesssolutions.org)
"""

    elif "Newsletter" in goal:
        return f"""# 📧 THE RJ MONETIZATION BRIEF: Rebuilding "{title}"
> **From the Desk of:** {author} | {brand_name}
> **To:** RJ Business Partners & Venture Operators

Hello Business Partners,

This week, we are looking directly at a highly valuable asset retrieved from the Internet Archive database: **"{title}"** (Creator: *{creator}*).

Many operators view the archive as a quiet digital library. But at **{brand_name}**, we see a massive, untapped goldmine of white-label monetization potential. 

Here is how we are rebuilding this asset today:

---

## 📝 The Brief: Modernizing "{title}"
The original work focuses heavily on foundational ideas:
*"{clean_desc}"*

To make this highly engaging for today's busy executives, we've compiled the three core action steps you can deploy this afternoon:

### 1. Re-Anchor the Value Proposition
Shift the narrative from theoretical historical context to high-yield current applications. Your readers do not just want to read history—they want to know how it improves their bottom line today.

### 2. Establish Brand Authority
By delivering this modernized insight under your custom byline, you position yourself as the ultimate bridge between classic wisdom and modern execution.

### 3. Deploy Structured Follow-Ups
Do not let the conversation end with one brief. Build a multi-part email sequence or a specialized summary series that guides your readers step-by-step.

---

## 🛠️ RJ Business Automation Spotlight
Our automated **Prometheus Engine** makes it easier than ever to ingest, rebrand, and distribute these assets with zero manual friction. Let our multi-agent systems handle the heavy lifting while you focus on scaling your operations.

To your automated success,

**{author}**  
Founder, {brand_name}  
[rjbusinesssolutions.org](https://rjbusinesssolutions.org)
"""

    else: # Executive Summary or other
        return f"""# 📋 EXECUTIVE SUMMARY: Rebranding "{title}"
> **Lead Architect:** {author}
> **Prepared for:** {brand_name} Stakeholders
> **Original Document Ref:** `archive.org/details/{identifier}`

## 🔍 Document Profile
- **Title:** {title}
- **Original Creator:** {creator}
- **Asset Type:** Internet Archive Legacy Publication
- **White-Label Custodian:** {brand_name}

---

## 📊 Summary of Modernized Principles
At **{brand_name}**, we conducted an automated deep-dive audit of the historic publication **"{title}"**. Below is the strategic summary of our findings and the modernized white-label translation compiled under the direction of **{author}**.

### 1. Tactical Objective
To strip away dated historical context and extract the high-value business principles, formatting them into an immediately digestible executive blueprint.

### 2. Core Operational Pillars
- **Authoritative Anchor:** Grounding your marketing materials in classic, high-trust documentation.
- **Brand Elevation:** Seamlessly blending legacy insights with the modern corporate voice of {brand_name}.
- **Value Optimization:** Enhancing readability with clean, modular formatting and premium styling cues.

---

## 💡 Recommended Implementation Roadmap
1. **Deploy Digital Cabinets:** Save all rebranded assets into your custom Base44 Cloud dashboard.
2. **Publish Authority Content:** Distribute this executive summary to clients, partners, and leads to drive high-conversion acquisitions.
3. **Narrate with Voice Scribes:** Utilize advanced text-to-speech tools to deliver audio-enabled summaries for on-the-go professionals.

*Compiled and authorized by {author} for {brand_name}.*
"""


@router.post("/execute")
async def execute_orchestration_workflow(
    payload: OrchestrateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Parses natural language instructions and coordinates sub-agents to achieve goal"""
    try:
        result = await agent.execute(payload.user_request)

        # Log query history
        history_id = str(uuid4())
        results_count = len(result.get("results", {}))
        results_summary = f"Task: {result.get('task_type')}. Errors: {len(result.get('errors', []))}"
        
        history = SearchHistory(
            id=history_id,
            query=payload.user_request[:200],
            search_type="orchestrator",
            results_count=results_count,
            results_summary=results_summary,
            created_by_id=current_user.id
        )
        db.add(history)
        await db.commit()

        # Real-time sync to Base44
        try:
            from ...core.base44_sync import sync_to_base44
            await sync_to_base44("SearchHistory", {
                "id": history_id,
                "query": payload.user_request[:200],
                "search_type": "orchestrator",
                "results_count": results_count,
                "results_summary": results_summary,
                "created_by_id": current_user.id
            })
        except Exception as sync_exc:
            from ...core.base44_sync import logger as sync_logger
            sync_logger.error(f"Failed to sync orchestrator history to Base44: {sync_exc}")

        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to coordinate master orchestrator: {str(exc)}"
        ) from exc


@router.post("/rebuild")
async def rebuild_archive_content(
    payload: RebuildRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Parses raw Internet Archive detail URLs, compiles rebranded documents, and syncs to Base44 Cloud"""
    try:
        identifier = extract_ia_identifier(payload.url_or_identifier)
        if not identifier:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract a valid Internet Archive identifier from the provided URL"
            )

        # Fetch metadata from Internet Archive
        try:
            item = await asyncio.to_thread(ia.get_item, identifier)
            metadata = item.item_metadata if item else {}
        except Exception as ia_err:
            metadata = {
                "title": identifier.title().replace("_", " ").replace("-", " "),
                "creator": "Unknown Archive Author",
                "description": "Internet Archive detail entry metadata fetch timed out. Initializing smart local fallback content."
            }

        title = metadata.get("title", identifier.title().replace("_", " ").replace("-", " "))
        creator = metadata.get("creator", "Unknown Archive Author")
        if isinstance(creator, list) and len(creator) > 0:
            creator = creator[0]
        description = metadata.get("description", "No description provided.")

        # AI-powered high-quality document synthesis
        markdown_content = ""
        if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "simulated_key":
            try:
                prompt = f"""You are a master content rebuilder and corporate copywriter at {payload.brand_name}.
Your founder and director is {payload.custom_author}, and you must write an extremely polished piece of media under their byline.

Based on the following Internet Archive item:
- Identifier: {identifier}
- Title: {title}
- Creator: {creator}
- Description: {description}

REBUILD GOAL: {payload.goal}

Generate a premium, complete, publication-ready article/blog post/newsletter in valid Markdown.
Include:
1. An eye-catching SEO title.
2. A list of optimized meta tags (title, description, keywords).
3. A compelling executive introduction.
4. Rich body sections with detailed insights, analysis, and takeaways.
5. All references to old systems or obsolete facts modernized to 2026 standards.
6. A call to action at the end referencing {payload.brand_name} and {payload.custom_author}.

Provide ONLY the final markdown content. Do not include any preambles, introductory commentary, or chat conversational filler.
"""
                response = await agent.claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                markdown_content = response.content[0].text
            except Exception as claude_exc:
                logger.error(f"Claude API compilation failed, using premium local fallback: {claude_exc}")
        
        if not markdown_content:
            markdown_content = generate_premium_fallback_rebuild(
                identifier, title, creator, description, payload.goal, payload.brand_name, payload.custom_author
            )

        # Write to Local Database
        content_id = f"rebuilt-{identifier}-{payload.goal.lower().replace(' ', '-')[:20]}"
        new_archive = ArchivedContent(
            id=content_id,
            url=f"https://archive.org/details/{identifier}",
            title=f"{title} ({payload.goal})",
            description=f"AI-rebuilt {payload.goal} based on {title}",
            content_type="document",
            snapshot_url=f"https://archive.org/details/{identifier}",
            thumbnail_url=None,
            extracted_text=markdown_content,
            metadata_json=metadata,
            status="archived",
            archive_source="ai_agent",
            created_by_id=current_user.id
        )
        db.add(new_archive)
        await db.commit()

        # Synchronize to Base44 Cloud BaaS database
        sync_status = "Successfully synchronized with Base44 Cloud"
        try:
            from ...core.base44_sync import sync_to_base44
            sync_data = {
                "id": content_id,
                "url": f"https://archive.org/details/{identifier}",
                "title": f"{title} ({payload.goal})",
                "description": f"AI-rebuilt {payload.goal} based on {title}",
                "content_type": "document",
                "snapshot_url": f"https://archive.org/details/{identifier}",
                "extracted_text": markdown_content,
                "metadata_json": metadata,
                "status": "archived",
                "archive_source": "ai_agent",
                "created_by_id": current_user.id
            }
            await sync_to_base44("ArchivedContent", sync_data)
        except Exception as sync_err:
            logger.error(f"Failed to synchronize rebuilt document to Base44: {sync_err}")
            sync_status = f"Local archive saved. Base44 sync omitted: {str(sync_err)}"

        return {
            "id": content_id,
            "identifier": identifier,
            "title": title,
            "creator": creator,
            "goal": payload.goal,
            "markdown_content": markdown_content,
            "sync_status": sync_status,
            "metadata": metadata
        }
    except Exception as exc:
        logger.error(f"Failed to execute rebuild workflow: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rebuild engine failure: {str(exc)}"
        )

