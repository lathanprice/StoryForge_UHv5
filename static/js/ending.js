document.addEventListener('DOMContentLoaded', function () {
    // Get story data from the hidden element
    const storyDataElem = document.getElementById('ending-story-data');
    let storyText = '';
    if (storyDataElem) {
        storyText = storyDataElem.textContent || storyDataElem.innerText || '';
        if (storyText.startsWith('"') && storyText.endsWith('"')) {
            storyText = storyText.slice(1, -1);
        }
        storyText = storyText.replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\'/g, "'");
        // Decode Unicode escapes (e.g., \u0027)
        storyText = storyText.replace(/\\u([\dA-Fa-f]{4})/g, function(match, grp) {
            return String.fromCharCode(parseInt(grp, 16));
        });
        storyText = storyText.trim();
    }
    if (!storyText) {
        storyText = 'Once upon a time, in a world of magic and mystery, a story was born...';
    }

    // Paginate: split paragraphs into sentences, build pages by sentence up to a char limit
    let paragraphs = storyText.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
    let pages = [];
    const charsPerPage = 550;
    for (let para of paragraphs) {
        // Split paragraph into sentences (simple split on period, exclamation, or question mark)
        let sentences = para.match(/[^.!?]+[.!?]+["']?|[^.!?]+$/g) || [para];
        let current = '';
        for (let sentence of sentences) {
            if ((current + ' ' + sentence).trim().length > charsPerPage && current.length > 0) {
                pages.push(current.trim());
                current = sentence;
            } else {
                current += (current ? ' ' : '') + sentence;
            }
        }
        if (current.length > 0) pages.push(current.trim());
    }
    // Ensure even number of pages for proper spread
    if (pages.length % 2 !== 0) {
        pages.push('');
    }
    // Group pages into spreads (2 pages per spread)
    let spreads = [];
    for (let i = 0; i < pages.length; i += 2) {
        spreads.push([pages[i], pages[i + 1]]);
    }

    let currentSpread = 0;

    function renderPage(text, isFirstPage) {
        if (!text || text.length === 0) return '';
        // Only the very first letter of the whole story gets the special style, and only if this is the first non-empty page
        if (isFirstPage && currentSpread === 0) {
            return `<p class="book-paragraph first-dropcap-paragraph"><span class="first-letter">${text.charAt(0)}</span>${text.slice(1)}</p>`;
        }
        return `<p class="book-paragraph">${text}</p>`;
    }

    // Get DOM elements
    const leftPage = document.getElementById('left-page');
    const rightPage = document.getElementById('right-page');
    const leftContent = leftPage.querySelector('.page-content');
    const rightContent = rightPage.querySelector('.page-content');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    function renderSpread() {
        leftContent.innerHTML = renderPage(spreads[currentSpread][0], currentSpread === 0);
        rightContent.innerHTML = renderPage(spreads[currentSpread][1], false);
        // Show navigation if more than one spread
        if (spreads.length > 1) {
            prevBtn.style.display = currentSpread > 0 ? 'inline-block' : 'inline-block';
            nextBtn.style.display = currentSpread < spreads.length - 1 ? 'inline-block' : 'inline-block';
        } else {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
        }
    }

    prevBtn.addEventListener('click', function () {
        if (currentSpread > 0) {
            currentSpread--;
            renderSpread();
        }
    });
    nextBtn.addEventListener('click', function () {
        if (currentSpread < spreads.length - 1) {
            currentSpread++;
            renderSpread();
        }
    });

    renderSpread();
    // Fade in the book container
    const bookContainer = document.querySelector('.book-container');
    if (bookContainer) {
        setTimeout(() => {
            bookContainer.style.opacity = '1';
            bookContainer.style.transform = 'translateY(0)';
        }, 100);
    }
});
