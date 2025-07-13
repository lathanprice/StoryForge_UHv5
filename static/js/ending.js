document.addEventListener('DOMContentLoaded', () => {
    // Get the story content and split it into pages
    const storyContainer = document.querySelector('.ending-story');
    const storyContent = storyContainer.textContent.trim();
    
    if (!storyContent) {
        console.error('No story content found');
        return;
    }

    // Split the content into pages
    const pages = parseStoryPages(storyContent);
    console.log('Parsed pages:', pages); // Debug log
    
    if (pages.length === 0) {
        console.error('No pages found in content');
        storyContainer.innerHTML = '<p>Story could not be loaded.</p>';
        return;
    }
    
    // Clear the original content
    storyContainer.textContent = '';
    
    // Create page elements with animations
    pages.forEach((pageContent, index) => {
        if (!pageContent.trim()) return; // Skip empty pages
        
        const pageElement = createPageElement(pageContent, index + 1);
        storyContainer.appendChild(pageElement);
        
        // Trigger animation after a delay based on page number
        setTimeout(() => {
            pageElement.classList.add('visible');
        }, index * 300);
    });
    
    // Add restart button functionality with confirmation
    const restartButton = document.querySelector('.restart-link');
    restartButton.addEventListener('click', (e) => {
        e.preventDefault();
        
        const confirmed = confirm('Are you sure you want to start a new tale?');
        if (confirmed) {
            document.body.classList.add('fade-out');
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        }
    });
});

function parseStoryPages(content) {
    const pages = [];
    const pageRegex = /Page\s+(\d+):\s*([\s\S]*?)(?=(?:Page\s+\d+:|$))/gi;
    let match;
    
    while ((match = pageRegex.exec(content)) !== null) {
        const [_, pageNum, pageContent] = match;
        if (pageContent.trim()) {
            pages.push(pageContent.trim());
        }
    }
    
    if (pages.length === 0 && content.trim()) {
        // Fallback: If no page markers found but content exists,
        // split by double newlines
        pages.push(...content.split('\n\n').filter(p => p.trim()));
    }
    
    console.log('Parsed content:', content); // Debug log
    console.log('Found pages:', pages); // Debug log
    
    return pages;
}

function createPageElement(content, pageNumber) {
    const pageDiv = document.createElement('div');
    pageDiv.className = 'story-page';
    
    const pageTitle = document.createElement('h2');
    pageTitle.className = 'page-title';
    pageTitle.textContent = `Page ${pageNumber}`;
    
    const pageContent = document.createElement('div');
    pageContent.className = 'page-content';
    pageContent.textContent = content;
    
    pageDiv.appendChild(pageTitle);
    pageDiv.appendChild(pageContent);
    
    return pageDiv;
}
