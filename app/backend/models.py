from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Article:
    id: str
    title: str
    summary: str
    link: str
    published: str
    source: str
    tags: List[str] = field(default_factory=list)
    saved: bool = False
    
@dataclass
class ArticleList:
    articles: List[Article]
