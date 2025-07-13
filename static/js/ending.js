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

    // Create the book container and pages
    const bookContainer = document.querySelector('.book-container');
    const leftPage = document.querySelector('.left-page .page-content');
    const rightPage = document.querySelector('.right-page .page-content');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    
    let currentPage = 0; // Start from the first page

    // Function to render pages
    function renderPages() {
        // Set the left and right pages
        leftPage.textContent = pages[currentPage];

        if (currentPage + 1 < pages.length) {
            rightPage.textContent = pages[currentPage + 1];
        } else {
            rightPage.textContent = ''; // Right page will be empty for odd-numbered pages
        }

        // Hide the previous button on the first page
        if (currentPage === 0) {
            prevButton.classList.add('hidden');
        } else {
            prevButton.classList.remove('hidden');
        }

        // Hide the next button on the last page
        if (currentPage === pages.length - 1) {
            nextButton.classList.add('hidden');
        } else {
            nextButton.classList.remove('hidden');
        }

        // Apply the flip effect to the book container
        bookContainer.style.transform = `rotateY(${currentPage * -180}deg)`;
    }

    // Button event listeners
    prevButton.addEventListener('click', () => {
        if (currentPage > 0) {
            currentPage--;
            renderPages();
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentPage < pages.length - 1) {
            currentPage++;
            renderPages();
        }
    });

    // Initial render
    renderPages();
});

// Function to parse story pages
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
