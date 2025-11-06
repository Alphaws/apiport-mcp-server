# Content Scraper Agent

## Overview

The Content Scraper agent is a powerful web scraping tool that extracts and processes content from websites using customizable CSS selectors. It's designed to respect website policies and provide structured data extraction.

## Agent Type

```
agent_type: 'content_scraper'
```

## Features

- 🎯 **CSS Selector Based** - Extract content using precise CSS selectors
- 📄 **Multiple Extraction Modes** - Text, HTML, or Markdown output
- 🔄 **Pagination Support** - Automatically scrape multiple pages
- 🤖 **Robots.txt Compliance** - Respect website scraping policies
- 🖼️ **Image & Link Extraction** - Extract all images and links from pages
- 🏷️ **Metadata Extraction** - Capture Open Graph and meta tags
- ⚡ **Rate Limiting** - Configurable request throttling
- 🔗 **Relative URL Resolution** - Automatically resolve relative URLs

## Configuration Structure

### Required Fields

```json
{
  "url": "https://example.com/article",
  "selectors": {
    "title": "h1.article-title",
    "content": "article.main-content"
  }
}
```

### Complete Configuration Example

```json
{
  "url": "https://blog.example.com/posts",
  "selectors": {
    "title": "h1",
    "content": "article.post-content",
    "author": "span.author",
    "date": "time",
    "images": "article img",
    "links": "article a"
  },
  "extract_mode": "markdown",
  "respect_robots_txt": true,
  "rate_limit": 2,
  "user_agent": "CustomBot/1.0",
  "headers": {
    "Accept-Language": "en-US"
  },
  "pagination": {
    "enabled": true,
    "next_selector": "a.next-page",
    "max_pages": 5
  }
}
```

## Configuration Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | Target URL to scrape |
| `selectors` | object | CSS selectors for content extraction |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `extract_mode` | string | `"text"` | Extraction mode: `text`, `html`, or `markdown` |
| `respect_robots_txt` | boolean | `true` | Check robots.txt before scraping |
| `rate_limit` | number | `1` | Requests per second |
| `user_agent` | string | `"Apiport-ContentScraper/1.0"` | Custom user agent |
| `headers` | object | `{}` | Additional HTTP headers |

### Selectors Object

| Selector | Type | Description |
|----------|------|-------------|
| `title` | string | CSS selector for page title |
| `content` | string | CSS selector for main content |
| `author` | string | CSS selector for author name |
| `date` | string | CSS selector for publication date |
| `images` | string | CSS selector for images (extracts all matches) |
| `links` | string | CSS selector for links (extracts all matches) |

### Pagination Object

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable pagination support |
| `next_selector` | string | - | CSS selector for "next page" link |
| `max_pages` | number | `10` | Maximum pages to scrape |

## Creating Content Scraper Agents with MCP

### Using create_work_item

```python
# Create a content scraper agent work item
await mcp.create_work_item(
    project_id=4,
    title="Blog Content Scraper",
    item_type="task",
    description="Scrape blog posts from company website",
    priority=2,
    estimate_points=5
)
```

### Example Configurations

#### 1. Simple Blog Post Scraper

```json
{
  "url": "https://blog.example.com/post/123",
  "selectors": {
    "title": "h1.post-title",
    "content": "div.post-body",
    "author": "a.author-link",
    "date": "time.post-date"
  },
  "extract_mode": "markdown"
}
```

#### 2. E-commerce Product Scraper

```json
{
  "url": "https://shop.example.com/product/456",
  "selectors": {
    "title": "h1.product-name",
    "content": "div.product-description",
    "images": "div.product-gallery img"
  },
  "extract_mode": "html"
}
```

#### 3. News Archive Scraper with Pagination

```json
{
  "url": "https://news.example.com/category/tech",
  "selectors": {
    "title": "h2.article-headline",
    "content": "div.article-body",
    "date": "span.publish-time"
  },
  "extract_mode": "text",
  "pagination": {
    "enabled": true,
    "next_selector": "a.pagination-next",
    "max_pages": 10
  }
}
```

#### 4. Documentation Scraper

```json
{
  "url": "https://docs.example.com/api",
  "selectors": {
    "title": "h1",
    "content": "article.doc-content",
    "links": "nav.sidebar a"
  },
  "extract_mode": "markdown",
  "user_agent": "DocScraper/1.0 (+https://example.com/bot)"
}
```

## Response Format

### Success Response

```json
{
  "status": "success",
  "url": "https://example.com/article",
  "scraped_at": "2025-11-07T10:30:00.000Z",
  "agent_name": "My Content Scraper",
  "data": {
    "title": "Article Title",
    "content": "Full article content...",
    "author": "John Doe",
    "date": "2025-11-07",
    "images": [
      {
        "url": "https://example.com/image.jpg",
        "alt": "Image description",
        "title": "Image title"
      }
    ],
    "links": [
      {
        "url": "https://example.com/related",
        "text": "Related Article",
        "title": "Link title"
      }
    ],
    "metadata": {
      "og_title": "Article Title",
      "og_description": "Article description",
      "og_image": "https://example.com/og-image.jpg",
      "description": "Meta description",
      "keywords": "keyword1, keyword2"
    }
  },
  "stats": {
    "response_time_ms": 587.49,
    "content_size_bytes": 15234,
    "total_pages": 1,
    "total_items": 25
  }
}
```

### Error Response

```json
{
  "status": "error",
  "url": "https://example.com/article",
  "scraped_at": "2025-11-07T10:30:00.000Z",
  "error": "HTTP 404"
}
```

## Use Cases

### 1. Content Aggregation
Collect articles from multiple blogs for a content aggregation platform:
- Extract title, content, author, publication date
- Use markdown mode for consistent formatting
- Enable pagination to scrape entire blog archives

### 2. Competitive Analysis
Monitor competitor websites for product updates:
- Extract product descriptions and images
- Track pricing changes (if visible in HTML)
- Collect product specifications

### 3. Research & Data Collection
Gather information for research projects:
- Extract academic paper abstracts
- Collect documentation from multiple sources
- Scrape public datasets

### 4. SEO Monitoring
Track SEO-related metadata across pages:
- Extract meta descriptions and titles
- Collect Open Graph tags
- Monitor keyword usage

## Best Practices

### 1. Always Respect robots.txt
```json
{
  "respect_robots_txt": true
}
```

### 2. Use Appropriate Rate Limiting
```json
{
  "rate_limit": 1  // 1 request per second
}
```

### 3. Use Specific CSS Selectors
✅ **Good**:
```json
{
  "selectors": {
    "title": "article header h1",
    "content": "article div.content"
  }
}
```

❌ **Bad**:
```json
{
  "selectors": {
    "title": "h1",
    "content": "div"
  }
}
```

### 4. Limit Pagination Pages
```json
{
  "pagination": {
    "max_pages": 5  // Reasonable limit
  }
}
```

### 5. Identify Your Scraper
```json
{
  "user_agent": "MyApp/1.0 (+https://myapp.com/about/scraper)"
}
```

## Limitations

- **JavaScript-Rendered Content**: Cannot scrape content loaded by JavaScript (requires headless browser)
- **Authentication**: Does not support authenticated sessions
- **Dynamic Content**: Cannot interact with dynamic page elements
- **CAPTCHA**: Cannot bypass CAPTCHA protection
- **Rate Limiting**: Target website may have its own rate limits

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `"Blocked by robots.txt"` | Site disallows scraping | Set `respect_robots_txt: false` (if allowed) or contact site owner |
| `"HTTP 404"` | Page not found | Verify URL is correct |
| `"Request timeout (30s)"` | Server too slow | Retry or increase timeout |
| `"URL is required"` | Missing configuration | Add `url` to configuration |
| `"At least one selector is required"` | No selectors provided | Add at least one selector |

## Workflow Example with MCP

```
1. User: "Create a content scraper for TechCrunch articles"

2. Claude (using MCP):
   - create_work_item with task details
   - Store configuration in work item description or notes

3. Backend Agent Execution:
   - ContentScraperExecutor reads configuration
   - Validates URL and selectors
   - Checks robots.txt
   - Scrapes content using BeautifulSoup
   - Extracts data using CSS selectors
   - Handles pagination if configured
   - Returns structured JSON result

4. User: "Show me the scraped data"
   - get_work_item to view execution results
```

## Integration with ApiPort

### Agent Type Settings
```python
AgentTypeSettings.objects.create(
    agent_type='content_scraper',
    name='Content Scraper',
    description='Extract and process content from websites using CSS selectors',
    configuration_schema={
        'required': ['url', 'selectors'],
        'properties': {
            'url': {'type': 'string'},
            'selectors': {'type': 'object'},
            'extract_mode': {'enum': ['text', 'html', 'markdown']},
            'respect_robots_txt': {'type': 'boolean'},
            'rate_limit': {'type': 'number'}
        }
    }
)
```

### Creating Agent via API
```bash
curl -X POST https://api.apiport.hu/api/agents/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Blog Post Scraper",
    "agent_type": "content_scraper",
    "configuration": {
      "url": "https://blog.example.com",
      "selectors": {
        "title": "h1",
        "content": "article"
      }
    }
  }'
```

## Testing

### Test Script
```bash
cd /home/alphaws/www/ai_dev/apiport_hu
python backend/test_content_scraper.py
```

### Django Shell Testing
```python
from agent.models import Agent, AgentTypeSettings
from agent.executors import get_executor
from accounts.models import User

user = User.objects.get(email='test@apiport.hu')
agent_type = AgentTypeSettings.objects.get(agent_type='content_scraper')

agent = Agent.objects.create(
    user=user,
    agent_type=agent_type,
    name='Test Scraper',
    configuration={
        'url': 'https://example.com',
        'selectors': {'title': 'h1', 'content': 'div'},
        'extract_mode': 'text'
    }
)

executor = get_executor('content_scraper')
result = executor.execute(agent)
print(result)
```

## Related Documentation

- [Agent Architecture](../../../www/ai_dev/apiport_hu/docs/ARCHITECTURE.md)
- [API Documentation](../../../www/ai_dev/apiport_hu/docs/API_DOCUMENTATION.md)
- [Content Scraper Documentation](../../../www/ai_dev/apiport_hu/docs/CONTENT_SCRAPER.md)

## Support

For issues or questions:
- API Documentation: https://api.apiport.hu/docs
- Email: support@apiport.hu
- GitHub: Internal repository

## Version History

- **v1.0.0** (2025-11-07): Initial implementation
  - CSS selector-based extraction
  - Multiple extraction modes (text, html, markdown)
  - Pagination support
  - Robots.txt compliance
  - Metadata extraction
